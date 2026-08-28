"""
pages/직업학과_탐색기.py
F-001 직업/학과 탐색기 UI

지금은 실제 API 대신 더미 데이터로 화면 흐름을 완성합니다.
실제 API로 바꾸려면 아래 "DUMMY DATA" 구간만 career_api.py의
search_job / get_job_detail / search_major / get_major_detail 호출로
교체하면 됩니다. (함수 시그니처는 이미 맞춰뒀습니다)
"""

import streamlit as st

# from utils.career_api import search_job, get_job_detail, search_major, get_major_detail

st.set_page_config(page_title="직업/학과 탐색기", page_icon="🧭", layout="wide")


# ---------------------------------------------------------------------------
# DUMMY DATA (실제 연동 전 UI 확인용 — 나중에 삭제하고 API 호출로 교체)
# ---------------------------------------------------------------------------
DUMMY_JOBS = [
    {
        "job_cd": 1,
        "job_nm": "소프트웨어개발자",
        "top_nm": "연구직 및 공학 기술직",
        "wage": "3,800만원",
        "work": "컴퓨터 프로그램을 설계하고 개발하며, 시스템의 오류를 점검하고 수정합니다.",
        "future": "IT 산업 성장에 따라 수요가 꾸준히 증가할 것으로 전망됩니다.",
        "related_majors": [101, 102],
    },
    {
        "job_cd": 2,
        "job_nm": "데이터분석가",
        "top_nm": "연구직 및 공학 기술직",
        "wage": "4,200만원",
        "work": "대량의 데이터를 수집·가공하여 의미 있는 정보를 도출하고 의사결정을 지원합니다.",
        "future": "데이터 기반 의사결정 확산으로 수요가 증가하고 있습니다.",
        "related_majors": [101, 103],
    },
    {
        "job_cd": 3,
        "job_nm": "게임기획자",
        "top_nm": "문화 예술 디자인 방송직",
        "wage": "3,500만원",
        "work": "게임의 전체적인 컨셉과 규칙, 스토리를 기획하고 개발 과정을 총괄합니다.",
        "future": "게임 산업 규모 확대와 함께 수요가 유지될 것으로 보입니다.",
        "related_majors": [102, 104],
    },
]

DUMMY_MAJORS = [
    {
        "major_seq": 101,
        "major_nm": "컴퓨터공학과",
        "l_class": "공학계열",
        "summary": "컴퓨터 시스템과 소프트웨어의 이론 및 실제 개발 기술을 배우는 학과입니다.",
        "employment_rate": "78%",
        "universities": ["A대학교", "B대학교", "C대학교"],
        "related_jobs": [1, 2],
    },
    {
        "major_seq": 102,
        "major_nm": "소프트웨어학과",
        "l_class": "공학계열",
        "summary": "소프트웨어 설계, 개발, 테스트 전 과정을 실습 중심으로 학습합니다.",
        "employment_rate": "81%",
        "universities": ["A대학교", "D대학교"],
        "related_jobs": [1, 3],
    },
    {
        "major_seq": 103,
        "major_nm": "통계학과",
        "l_class": "자연계열",
        "summary": "데이터 분석의 기초가 되는 통계 이론과 통계적 사고력을 기릅니다.",
        "employment_rate": "70%",
        "universities": ["B대학교", "E대학교"],
        "related_jobs": [2],
    },
    {
        "major_seq": 104,
        "major_nm": "게임학과",
        "l_class": "예체능계열",
        "summary": "게임 기획, 그래픽, 프로그래밍 등 게임 개발 전반을 다룹니다.",
        "employment_rate": "65%",
        "universities": ["C대학교", "F대학교"],
        "related_jobs": [3],
    },
]


def find_job(job_cd):
    return next((j for j in DUMMY_JOBS if j["job_cd"] == job_cd), None)


def find_major(major_seq):
    return next((m for m in DUMMY_MAJORS if m["major_seq"] == major_seq), None)


def search_jobs_dummy(keyword):
    if not keyword:
        return DUMMY_JOBS
    return [j for j in DUMMY_JOBS if keyword in j["job_nm"]]


def search_majors_dummy(keyword):
    if not keyword:
        return DUMMY_MAJORS
    return [m for m in DUMMY_MAJORS if keyword in m["major_nm"]]


# ---------------------------------------------------------------------------
# 화면 상태 관리
# ---------------------------------------------------------------------------
if "detail_type" not in st.session_state:
    st.session_state.detail_type = None  # "job" or "major" or None
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


# ---------------------------------------------------------------------------
# 헤더
# ---------------------------------------------------------------------------
st.title("🧭 직업/학과 탐색기")
st.caption("궁금한 직업이나 학과를 검색하고, 서로 어떻게 연결되는지 살펴보세요.")

# ---------------------------------------------------------------------------
# 상세 화면 (직업 or 학과가 선택된 경우)
# ---------------------------------------------------------------------------
if st.session_state.detail_type == "job":
    job = find_job(st.session_state.detail_id)

    if st.button("← 검색으로 돌아가기"):
        back_to_search()
        st.rerun()

    if job is None:
        st.error("해당 직업 정보를 찾을 수 없습니다.")
    else:
        st.header(job["job_nm"])
        st.badge(job["top_nm"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("하는 일")
            st.write(job["work"])
        with col2:
            st.subheader("평균 임금")
            st.write(job["wage"])
            st.subheader("미래 전망")
            st.write(job["future"])

        st.divider()
        st.subheader("🔗 관련 학과")
        related = [find_major(m) for m in job["related_majors"]]
        related = [m for m in related if m]
        if not related:
            st.info("연결된 학과 정보가 없습니다.")
        else:
            cols = st.columns(len(related))
            for col, major in zip(cols, related):
                with col:
                    with st.container(border=True):
                        st.markdown(f"**{major['major_nm']}**")
                        st.caption(major["l_class"])
                        if st.button("자세히 보기", key=f"major_{major['major_seq']}"):
                            show_major_detail(major["major_seq"])
                            st.rerun()

elif st.session_state.detail_type == "major":
    major = find_major(st.session_state.detail_id)

    if st.button("← 검색으로 돌아가기"):
        back_to_search()
        st.rerun()

    if major is None:
        st.error("해당 학과 정보를 찾을 수 없습니다.")
    else:
        st.header(major["major_nm"])
        st.badge(major["l_class"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("학과 소개")
            st.write(major["summary"])
            st.subheader("개설 대학")
            st.write(", ".join(major["universities"]))
        with col2:
            st.subheader("취업률")
            st.write(major["employment_rate"])

        st.divider()
        st.subheader("🔗 관련 직업")
        related = [find_job(j) for j in major["related_jobs"]]
        related = [j for j in related if j]
        if not related:
            st.info("연결된 직업 정보가 없습니다.")
        else:
            cols = st.columns(len(related))
            for col, job in zip(cols, related):
                with col:
                    with st.container(border=True):
                        st.markdown(f"**{job['job_nm']}**")
                        st.caption(job["top_nm"])
                        if st.button("자세히 보기", key=f"job_{job['job_cd']}"):
                            show_job_detail(job["job_cd"])
                            st.rerun()

# ---------------------------------------------------------------------------
# 검색 화면 (기본 화면)
# ---------------------------------------------------------------------------
else:
    tab_job, tab_major = st.tabs(["💼 직업", "🎓 학과"])

    with tab_job:
        keyword = st.text_input("직업 키워드를 입력하세요", key="job_keyword", placeholder="예: 개발자")

        # 실제 연동 시:
        # try:
        #     result = search_job(keyword)
        #     jobs = result["jobs"]
        # except Exception:
        #     jobs = []
        jobs = search_jobs_dummy(keyword)

        if not jobs:
            st.info("검색 결과가 없습니다. 다른 키워드로 검색해보세요.")
        else:
            for job in jobs:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"**{job['job_nm']}**  \n:gray[{job['top_nm']}] · 평균임금 {job['wage']}")
                    with c2:
                        if st.button("상세보기", key=f"job_search_{job['job_cd']}"):
                            show_job_detail(job["job_cd"])
                            st.rerun()

    with tab_major:
        keyword = st.text_input("학과 키워드를 입력하세요", key="major_keyword", placeholder="예: 컴퓨터")

        # 실제 연동 시:
        # try:
        #     majors = search_major(keyword)
        # except Exception:
        #     majors = []
        majors = search_majors_dummy(keyword)

        if not majors:
            st.info("검색 결과가 없습니다. 다른 키워드로 검색해보세요.")
        else:
            for major in majors:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"**{major['major_nm']}**  \n:gray[{major['l_class']}] · 취업률 {major['employment_rate']}")
                    with c2:
                        if st.button("상세보기", key=f"major_search_{major['major_seq']}"):
                            show_major_detail(major["major_seq"])
                            st.rerun()
