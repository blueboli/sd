"""
utils/common_ui.py
전 화면 공통으로 쓰는 헤더/푸터/스타일 함수

담당: 조준원
필요해지면 여기에 공통 CSS, 배지, 카드 스타일 등을 추가하세요.
현재는 Home.py에서 직접 렌더링하고 있어, 반복되는 부분이 생기면
이 파일로 분리하면 됩니다.
"""

import streamlit as st


def render_footer():
    """모든 페이지 하단에 공통으로 넣을 데이터 출처 표기"""
    st.caption(
        "데이터 출처: [커리어넷](https://www.career.go.kr) · "
        "[대학알리미](https://www.academyinfo.go.kr)  |  "
        "활용 AI: Gemini 2.5 Flash"
    )
