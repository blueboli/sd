"""
pages/1_직업학과_탐색기.py
F-001 직업/학과 탐색기 UI (커리어넷 실 API 연동)

기획서 반영:
- 직업/학과 탭 분리
- 키워드 입력 후 검색
- 검색 결과 목록 및 상세보기
- 상세 화면에서 직업 ↔ 관련 학과 연결 탐색
"""

import streamlit as st

from utils.career_api import (
    search_job,
    get_job_detail,
    search_major,
    get_major_detail,
)

st.set_page_config(
    page_title="직업/학과 탐색기",
    page_icon="🧭",
    layout="wide",
)

# 홈 화면 검색창에서 넘어온 키워드 프리필
if "jm_prefill_keyword" in st.session_state:
    keyword = st.session_state.pop("jm_prefill_keyword")
    st.session_state["job_keyword"] = keyword
    st.session_state["major_keyword"] = keyword

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
    """직업 상세 화면의 관련 학과를 눌렀을 때 해당 학과 상세 화면으로 이동."""
    try:
        results = search_major(name.strip())
        if results:
            major_seq = results[0].get("majorSeq")
            if major_seq:
                show_major_detail(major_seq)
            else:
                st.warning("해당 학과의 상세 정보 식별자를 찾지 못했습니다.")
        else:
            st.warning("관련 학과 정보를 찾을 수 없습니다.")
    except Exception as exc:
        st.error(f"학과 검색 중 오류가 발생했습니다: {exc}")


def go_to_job_by_name(name):
    """학과 상세 화면의 관련 직업을 눌렀을 때 해당 직업 상세 화면으로 이동."""
    try:
        results = search_job(name.strip())
        if results:
            job_cd = results[0].get("job_cd")
            if job_cd:
                show_job_detail(job_cd)
            else:
                st.warning("해당 직업의 상세 정보 식별자를 찾지 못했습니다.")
        else:
            st.warning("관련 직업 정보를 찾을 수 없습니다.")
    except Exception as exc:
        st.error(f"직업 검색 중 오류가 발생했습니다: {exc}")


def render_job_search():
    """직업 검색: 학과 검색과 동일한 입력-검색-결과-상세보기 흐름."""
    with st.form("job_search_form"):
        keyword = st.text_input(
            "직업 키워드를 입력하세요",
            key="job_keyword",
            placeholder="예: 반도체 엔지니어",
        )
        submitted = st.form_submit_button("직업 검색", use_container_width=True)

    if not submitted:
        st.caption("직업명을 입력하고 검색 버튼을 눌러주세요.")
        return

    keyword = keyword.strip()
    if not keyword:
        st.warning("검색할 직업 키워드를 입력해 주세요.")
        return

    try:
        with st.spinner("직업 정보를 검색하고 있습니다..."):
            jobs = search_job(keyword)
    except Exception as exc:
        st.error(f"커리어넷 직업 API 호출에 실패했습니다: {exc}")
        return

    if not jobs:
        st.info("검색 결과가 없습니다. 다른 직업명이나 키워드로 검색해보세요.")
        return

    st.success(f"'{keyword}' 검색 결과 {len(jobs)}건")
    for index, job in enumerate(jobs):
        job_name = job.get("job_nm") or "직업명 정보 없음"
        job_category = job.get("top_nm") or "분류 정보 없음"
        wage = job.get("wage") or "정보 없음"
        job_cd = job.get("job_cd")

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{job_name}**")
                st.caption(f"{job_category} · 평균 연봉 {wage}")
            with col2:
                if st.button(
                    "상세보기",
                    key=f"job_search_{job_cd or index}",
                    use_container_width=True,
                    disabled=not bool(job_cd),
                ):
                    show_job_detail(job_cd)
                    st.rerun()


def render_major_search():
    """학과 검색: 직업 검색과 같은 입력-검색-결과-상세보기 흐름."""
    with st.form("major_search_form"):
        keyword = st.text_input(
            "학과 키워드를 입력하세요",
            key="major_keyword",
            placeholder="예: 반도체, 컴퓨터, 생명공학",
        )
        submitted = st.form_submit_button("학과 검색", use_container_width=True)

    if not submitted:
        st.caption("학과명을 입력하고 검색 버튼을 눌러주세요.")
        return

    keyword = keyword.strip()
    if not keyword:
        st.warning("검색할 학과 키워드를 입력해 주세요.")
        return

    try:
        with st.spinner("학과 정보를 검색하고 있습니다..."):
            majors = search_major(keyword)
    except Exception as exc:
        st.error(f"커리어넷 학과 API 호출에 실패했습니다: {exc}")
        return

    if not majors:
        st.info("검색 결과가 없습니다. 다른 학과명이나 키워드로 검색해보세요.")
        return

    st.success(f"'{keyword}' 검색 결과 {len(majors)}건")
    for index, major in enumerate(majors):
        # 커리어넷 학과 검색 결과의 학과명/계열명/상세조회 키를 사용
        major_name = major.get("mClass") or major.get("major") or "학과명 정보 없음"
        major_category = major.get("lClass") or "계열 정보 없음"
        major_seq = major.get("majorSeq")

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{major_name}**")
                st.caption(major_category)
            with col2:
                if st.button(
                    "상세보기",
                    key=f"major_search_{major_seq or index}",
                    use_container_width=True,
                    disabled=not bool(major_seq),
                ):
                    show_major_detail(major_seq)
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
        with st.spinner("직업 상세 정보를 불러오고 있습니다..."):
            detail = get_job_detail(st.session_state.detail_id)
    except Exception as exc:
        st.error(f"직업 정보를 불러오지 못했습니다: {exc}")
        detail = None

    if detail:
        base = detail.get("baseInfo") or {}
        st.header(base.get("job_nm") or "직업 정보")
        aptitude = base.get("aptit_name")
        if aptitude:
            st.badge(aptitude)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("하는 일")
            work_list = detail.get("workList") or []
            if work_list:
                for item in work_list:
                    if item.get("work"):
                        st.write(item["work"])
            else:
                st.write("등록된 정보가 없습니다.")

        with col2:
            wage = base.get("wage")
            st.subheader("평균 연봉")
            st.write(f"{wage}만원" if wage else "정보 없음")

            st.subheader("미래 전망")
            forecast_list = detail.get("forecastList") or []
            if forecast_list:
                for item in forecast_list:
                    if item.get("forecast"):
                        st.write(item["forecast"])
            else:
                st.write("등록된 정보가 없습니다.")

        st.divider()
        st.subheader("🔗 관련 학과")
        departments = detail.get("departList") or []
        if not departments:
            st.info("연결된 학과 정보가 없습니다.")
        else:
            cols = st.columns(min(len(departments), 4))
            for index, department in enumerate(departments):
                department_name = department.get("depart_name") or "학과명 정보 없음"
                with cols[index % len(cols)]:
                    with st.container(border=True):
                        st.markdown(f"**{department_name}**")
                        if st.button(
                            "자세히 보기",
                            key=f"related_major_{department.get('depart_id') or index}",
                            use_container_width=True,
                        ):
                            go_to_major_by_name(department_name)
                            if st.session_state.detail_type == "major":
                                st.rerun()

elif st.session_state.detail_type == "major":
    if st.button("← 검색으로 돌아가기"):
        back_to_search()
        st.rerun()

    try:
        with st.spinner("학과 상세 정보를 불러오고 있습니다..."):
            major_detail = get_major_detail(st.session_state.detail_id)
    except Exception as exc:
        st.error(f"학과 정보를 불러오지 못했습니다: {exc}")
        major_detail = None

    if major_detail:
        st.header(major_detail.get("major") or "학과 정보")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("학과 소개")
            st.write(major_detail.get("summary") or "등록된 학과 소개가 없습니다.")

            st.subheader("개설 대학")
            universities = major_detail.get("universities") or []
            if universities:
                for university in universities[:10]:
                    school = university.get("schoolName") or "대학명 정보 없음"
                    area = university.get("area") or "지역 정보 없음"
                    st.write(f"- {school} ({area})")
            else:
                st.write("개설 대학 정보가 없습니다.")

        with col2:
            st.subheader("취업률")
            st.write(major_detail.get("employment") or "정보 없음")

            st.subheader("졸업 후 임금")
            st.write(major_detail.get("salary") or "정보 없음")

        st.divider()
        st.subheader("🔗 관련 직업")
        job_names = [
            name.strip()
            for name in (major_detail.get("job") or "").split(",")
            if name.strip()
        ]

        if not job_names:
            st.info("연결된 직업 정보가 없습니다.")
        else:
            cols = st.columns(min(len(job_names), 4))
            for index, name in enumerate(job_names[:8]):
                with cols[index % len(cols)]:
                    with st.container(border=True):
                        st.markdown(f"**{name}**")
                        if st.button(
                            "자세히 보기",
                            key=f"related_job_{index}_{name}",
                            use_container_width=True,
                        ):
                            go_to_job_by_name(name)
                            if st.session_state.detail_type == "job":
                                st.rerun()

# ---------------------------------------------------------------------------
# 검색 화면
# ---------------------------------------------------------------------------
else:
    tab_job, tab_major = st.tabs(["💼 직업", "🎓 학과"])

    with tab_job:
        render_job_search()

    with tab_major:
        render_major_search()
