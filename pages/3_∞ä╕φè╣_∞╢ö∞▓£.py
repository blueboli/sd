"""
pages/3_세특_추천.py
F-003 세특 탐구 주제 추천 도우미 UI

담당: 유지현
※ 이 파일은 아직 자리만 잡아둔 placeholder입니다.
   utils/gemini_api.py 연동 전까지는 더미 응답으로 화면 흐름만 완성해두세요.

TODO:
- [ ] 입력 폼: 학년(필수) / 희망 진로 / 관심 분야(필수) / 선호 탐구 유형
- [ ] 필수값 미입력 시 빨간색 안내 문구
- [ ] "추천받기" 버튼 -> st.spinner -> 결과 출력
- [ ] utils/gemini_api.py 연동 (주제 3개 + 탐구방향 + 심화아이디어)
- [ ] 추천 결과 카드 + 복사 버튼
- [ ] API 오류/타임아웃 예외 처리
"""

import streamlit as st

st.set_page_config(page_title="세특 탐구 주제 추천", page_icon="✏️", layout="wide")

st.title("✏️ 세특 탐구 주제 추천 도우미")
st.caption("학년, 희망 진로, 관심 분야를 입력하면 AI가 맞춤 탐구 주제를 추천해드려요.")

st.info("🚧 이 기능은 아직 개발 중입니다. (담당: 유지현)")
