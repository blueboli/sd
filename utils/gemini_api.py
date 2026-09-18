"""
utils/gemini_api.py
F-003 세특 탐구 주제 추천 도우미 - Gemini 2.5 Flash API 연동

담당: 유지현
- API 키 발급: Google AI Studio (무료 티어)
- API 키는 st.secrets["GEMINI_API_KEY"] 로 불러오세요.
"""
import json

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

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    model = genai.GenerativeModel("gemini-2.5-flash")

    
    prompt = f"""
당신은 대한민국 고등학교 교사이자 세특 탐구 주제 추천 전문가입니다.

학생의 정보를 바탕으로 교과 세특에 활용할 수 있는
탐구 주제 3개를 추천해주세요.

[학생 정보]
- 학년: {grade}
- 희망 진로: {career}
- 관심 분야: {interest}
- 탐구 유형: {topic_type}

[작성 조건]
- 학생의 학년 수준에 적절해야 합니다.
- 희망 진로와 관심 분야를 자연스럽게 반영해주세요.
- 단순한 정보 조사보다는 분석, 비교, 실험, 탐구 등이 가능해야 합니다.
- 교과 지식을 심화하거나 다른 분야와 융합할 수 있어야 합니다.
- 서로 차별화되는 3개의 주제를 제안해주세요.

[출력 형식]
반드시 아래 JSON 형식으로만 답변해주세요.
JSON 이외의 설명이나 Markdown은 출력하지 마세요.

{{
    "topics": [
        {{
            "title": "탐구 주제명",
            "direction": "탐구 방향",
            "extension": "심화 탐구 아이디어"
        }},
        {{
            "title": "탐구 주제명",
            "direction": "탐구 방향",
            "extension": "심화 탐구 아이디어"
        }},
        {{
            "title": "탐구 주제명",
            "direction": "탐구 방향",
            "extension": "심화 탐구 아이디어"
        }}
    ]
}}
"""

    try:
        response = model.generate_content(prompt)

    except Exception as e:
        raise RuntimeError(f"Gemini API 호출 중 오류가 발생했습니다: {e}")


    try:
        result = json.loads(response.text)
        topics = result["topics"]

        return topics

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise RuntimeError(
            f"Gemini 응답을 JSON으로 파싱하지 못했습니다: {e}"
        )

    
    # TODO:
    # 1) genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 2) 프롬프트 구성 (grade, career, interest, topic_type 반영)
    # 3) model.generate_content(prompt) 호출
    # 4) 응답을 JSON으로 파싱해서 위 형식으로 반환
    raise NotImplementedError("gemini_api.generate_topics 구현 필요")
