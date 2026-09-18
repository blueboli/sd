"""
pages/1_직업학과_탐색기.py
F-001 직업/학과 탐색기 UI (커리어넷 실 API 연동)
"""

import streamlit as st

from utils.career_api import search_job, get_job_detail, search_major, get_major_detail

st.set_page_config(page_title="직업/학과 탐색기", page_icon="🧭", layout="wide")

# 홈 화면 검색창에서 넘어온 키워드 프리필
if "jm_prefill_keyword" in st.session_state:
    _kw = st.session_state.pop("jm_prefill_keyword")
    st.session_state["job_keyword"] = _kw
    st.session_state["major_keyword"] = _kw

# 화면 상태 관리
if "detail_type" not in st.session_state:
    st.session_state.detail_type = None
if "detail_id" not in st.session_state:
    st.session_state.detail_id = None


def show_job_detail(job_cd):
    st.session_state.detail_type = "job"
    st.session_state.detail_id = job_cd


def show_major_detail(major_seq):
    st.session_state.detail_type = "major"
    st.session_state.detail_id = major_seq


def back_to_search():
    st.session_state.detail_type = None
    st.session_state.detail_id = None


def go_to_major_by_name(name):
    results = search_major(name.strip())
    if results:
        show_major_detail(results[0]["majorSeq"])
    st.rerun()


def go_to_job_by_name(name):
    results = search_job(name.strip())
    if results:
        show_job_detail(results[0]["job_cd"])
    st.rerun()


st.title("🧭 직업/학과 탐색기")
st.caption("궁금한 직업이나 학과를 검색하고, 서로 어떻게 연결되는지 살펴보세요.")

# ---------------------------------------------------------------------------
# 상세 화면
# ---------------------------------------------------------------------------
if st.session_state.detail_type == "job":
    if st.button("← 검색으로 돌아가기"):
        back_to_search()
        st.rerun()

    try:
        detail = get_job_detail(st.session_state.detail_id)
    except Exception:
        st.error("직업 정보를 불러오지 못했습니다.")
        detail = None

    if detail:
        base = detail.get("baseInfo", {})
        st.header(base.get("job_nm", ""))
        st.badge(base.get("aptit_name", ""))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("하는 일")
            for w in detail.get("workList", []):
                st.write(w.get("work", ""))
        with col2:
            wage = base.get("wage")
            st.subheader("평균 연봉")
            st.write(f"{wage}만원" if wage else "정보 없음")
            st.subheader("미래 전망")
            for f in detail.get("forecastList", []):
                st.write(f.get("forecast", ""))

        st.divider()
        st.subheader("🔗 관련 학과")
        departs = detail.get("departList", [])
        if not departs:
            st.info("연결된 학과 정보가 없습니다.")
        else:
            cols = st.columns(min(len(departs), 4))
            for col, d in zip(cols, departs):
                with col:
                    with st.container(border=True):
                        st.markdown(f"**{d.get('depart_name', '')}**")
                        if st.button("자세히 보기", key=f"major_{d.get('depart_id')}"):
                            go_to_major_by_name(d.get("depart_name", ""))

elif st.session_state.detail_type == "major":
    if st.button("← 검색으로 돌아가기"):
        back_to_search()
        st.rerun()

    try:
        major = get_major_detail(st.session_state.detail_id)
    except Exception:
        st.error("학과 정보를 불러오지 못했습니다.")
        major = None

    if major:
        st.header(major.get("major", ""))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("학과 소개")
            st.write(major.get("summary", ""))
            st.subheader("개설 대학")
            for u in major.get("universities", [])[:10]:
                st.write(f"- {u.get('schoolName', '')} ({u.get('area', '')})")
        with col2:
            st.subheader("취업률")
            st.write(major.get("employment", "정보 없음"))
            st.subheader("졸업 후 임금")
            st.write(major.get("salary", "정보 없음"))

        st.divider()
        st.subheader("🔗 관련 직업")
        job_names = [j.strip() for j in (major.get("job") or "").split(",") if j.strip()]
        if not job_names:
            st.info("연결된 직업 정보가 없습니다.")
        else:
            cols = st.columns(min(len(job_names), 4))
            for col, name in zip(cols, job_names[:8]):
                with col:
                    with st.container(border=True):
                        st.markdown(f"**{name}**")
                        if st.button("자세히 보기", key=f"job_{name}"):
                            go_to_job_by_name(name)

# ---------------------------------------------------------------------------
# 검색 화면
# ---------------------------------------------------------------------------
else:
    tab_job, tab_major = st.tabs(["💼 직업", "🎓 학과"])

    with tab_job:
        keyword = st.text_input("직업 키워드를 입력하세요", key="job_keyword", placeholder="예: 개발자")
        try:
            jobs = search_job(keyword) if keyword else []
        except Exception:
            st.error("커리어넷 API 호출에 실패했습니다.")
            jobs = []

        if not jobs:
            st.info("검색어를 입력하거나 다른 키워드로 검색해보세요.")
        else:
            for job in jobs:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(
                            f"**{job.get('job_nm', '')}**  \n"
                            f":gray[{job.get('top_nm', '')}] · 연봉 {job.get('wage', '정보 없음')}"
                        )
                    with c2:
                        if st.button("상세보기", key=f"job_search_{job.get('job_cd')}"):
                            show_job_detail(job.get("job_cd"))
                            st.rerun()

    with tab_major:
        keyword = st.text_input("학과 키워드를 입력하세요", key="major_keyword", placeholder="예: 컴퓨터")
        try:
            majors = search_major(keyword) if keyword else []
        except Exception:
            st.error("커리어넷 API 호출에 실패했습니다.")
              
            majors = []

        if not majors:
            st.info("검색어를 입력하거나 다른 키워드로 검색해보세요.")
        else:
            for major in majors:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"**{major.get('mClass', '')}**  \n:gray[{major.get('lClass', '')}]")
                    with c2:
                        if st.button("상세보기", key=f"major_search_{major.get('majorSeq')}"):
                            show_major_detail(major.get("majorSeq"))
                            st.rerun()

st.divider()
st.subheader('🔧 디버그: search_major 테스트')
test_keyword = st.text_input('테스트 검색어', '컴퓨터공학')
if st.button('테스트 실행'): 
    result = search_major(test_keyword) 
    st.write('결과 개수:', len(result)) 
    st.write(result)
