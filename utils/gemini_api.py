"""
utils/gemini_api.py
F-003 세특 탐구 주제 추천 도우미 - Gemini 2.5 Flash API 연동

담당: 유지현
- API 키 발급: Google AI Studio (무료 티어)
- API 키는 st.secrets["GEMINI_API_KEY"] 로 불러오세요.
"""

import streamlit as st
import google.generativeai as genai


def generate_topics(grade: str, career: str, interest: str, topic_type: str) -> list[dict]:
    """
    입력값을 바탕으로 세특 탐구 주제 3개를 추천.

    Returns:
        [
            {"title": "탐구 주제명", "direction": "탐구 방향", "extension": "심화 탐구 아이디어"},
            ... (3개)
        ]
    """
    # TODO:
    # 1) genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 2) 프롬프트 구성 (grade, career, interest, topic_type 반영)
    # 3) model.generate_content(prompt) 호출
    # 4) 응답을 JSON으로 파싱해서 위 형식으로 반환
    raise NotImplementedError("gemini_api.generate_topics 구현 필요")
