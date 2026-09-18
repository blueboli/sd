import streamlit as st

st.set_page_config(page_title="진로진학 플랫폼", page_icon="🧭", layout="wide")

# 상단바 (페이지 이동 버튼)
nav1, nav2, nav3, nav4 = st.columns(4)
with nav1:
    st.page_link("Home.py", label="🏠 홈", use_container_width=True)
with nav2:
    st.page_link("pages/1_직업학과_탐색기.py", label="🔍 직업·학과 탐색", use_container_width=True)
with nav3:
    st.page_link("pages/2_대입정보_비교.py", label="🏫 대입정보 비교", use_container_width=True)
with nav4:
    st.page_link("pages/3_세특_추천.py", label="✏️ 세특 추천", use_container_width=True)

st.divider()

st.title("🧭 진로진학 플랫폼")
st.caption("직업·학과 정보부터 대입 비교, AI 세특 추천까지 — 진로 결정에 필요한 모든 것을 한 곳에서.")

# 빠른 검색 (입력 후 탐색기 페이지로 이동 + 검색어 자동 반영)
st.subheader("빠른 검색")
search_col, btn_col = st.columns([5, 1])
with search_col:
    home_keyword = st.text_input(
        "직업 또는 학과 키워드를 입력하세요",
        key="home_keyword",
        placeholder="예: 소프트웨어 개발자, 컴퓨터공학과...",
        label_visibility="collapsed",
    )
with btn_col:
    go_search = st.button("검색", use_container_width=True)

if go_search:
    if home_keyword.strip():
        st.session_state["jm_prefill_keyword"] = home_keyword.strip()
        st.switch_page("pages/1_직업학과_탐색기.py")
    else:
        st.warning("검색어를 입력해주세요.")

st.divider()

st.subheader("핵심 기능")
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown("### 🔍 직업·학과 탐색기")
        st.write("커리어넷 공공 API 기반으로 직업 상세 정보와 관련 학과를 탐색하고 서로 연결해 확인할 수 있어요.")
        st.caption("커리어넷 API · 직업 정보 · 학과 정보 · 연관 탐색")
with col2:
    with st.container(border=True):
        st.markdown("### 🏫 대입정보 비교 대시보드")
        st.write("대학알리미 공시데이터를 바탕으로 원하는 대학들을 나란히 비교하고 전형별 반영비율을 시각화해요.")
        st.caption("대학알리미 · 전형 비교 · 수능최저 여부 · 차트 시각화")
with col3:
    with st.container(border=True):
        st.markdown("### ✏️ 세특 탐구 주제 추천")
        st.write("희망 진로·관심 분야·학년을 입력하면 AI가 세특에 쓸 수 있는 탐구 주제와 방향을 추천해드려요.")
        st.caption("Gemini AI · 맞춤 추천 · 탐구 방향 · 심화 아이디어")

st.divider()

st.subheader("사용 방법")
s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("**STEP 01**")
    st.write("관심 있는 직업명이나 학과명을 입력해 기본 정보를 확인하세요.")
with s2:
    st.markdown("**STEP 02**")
    st.write("가고 싶은 대학들을 선택해 전형별 반영비율을 한눈에 비교하세요.")
with s3:
    st.markdown("**STEP 03**")
    st.write("과목과 진로를 입력하면 AI가 맞춤 세특 탐구 주제를 제안해드려요.")

st.divider()

st.caption(
    "데이터 출처: [커리어넷](https://www.career.go.kr) · "
    "[대학알리미](https://www.academyinfo.go.kr)  |  "
    "활용 AI: Gemini 2.5 Flash"
)
