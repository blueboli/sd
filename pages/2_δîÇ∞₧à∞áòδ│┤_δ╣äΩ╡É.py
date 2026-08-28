"""
pages/2_대입정보_비교.py
F-002 대입정보 비교 대시보드 UI

담당: 임찬서
※ 이 파일은 아직 자리만 잡아둔 placeholder입니다.
   1_직업학과_탐색기.py 처럼 DUMMY DATA로 화면 흐름부터 완성한 뒤,
   utils/admission_data.py 연동으로 교체해주세요.

TODO:
- [ ] data/admission_2028.csv 로딩 (utils/admission_data.py)
- [ ] 대학 다중 선택 (최대 5개 제한) - st.multiselect
- [ ] 전형 구분 선택 - st.radio / st.selectbox
- [ ] plotly 그룹 막대 차트로 반영비율 비교
- [ ] 비교표 + 수능최저 여부 배지
- [ ] 예외 처리(대학 미선택 / 6개 이상 선택)
"""

import streamlit as st

st.set_page_config(page_title="대입정보 비교", page_icon="🏫", layout="wide")

st.title("🏫 대입정보 비교 대시보드")
st.caption("비교할 대학과 전형 구분을 선택하면 반영비율을 한눈에 비교할 수 있어요.")

st.info("🚧 이 기능은 아직 개발 중입니다. (담당: 임찬서)")
