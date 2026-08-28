"""
utils/career_api.py
F-001 직업/학과 탐색기 - 커리어넷 OpenAPI 연동

담당: 윤준호
※ 아래 4개 함수의 시그니처는 pages/1_직업학과_탐색기.py 에서
   이미 그대로 호출하도록 맞춰뒀습니다. 내부 구현만 채우면 됩니다.

- API 신청: https://www.career.go.kr (Open API)
- API 키는 st.secrets["CAREERNET_API_KEY"] 로 불러오세요.
"""

import requests
import streamlit as st

BASE_URL = "https://www.career.go.kr/cnet/openapi/getOpenApi.json"


def search_job(keyword: str) -> dict:
    """
    직업명 키워드로 검색.
    Returns: {"jobs": [ {job_cd, job_nm, top_nm, wage, ...}, ... ]}
    """
    # TODO: requests.get(BASE_URL, params={...}) 로 실제 호출 구현
    raise NotImplementedError("career_api.search_job 구현 필요")


def get_job_detail(job_cd) -> dict:
    """
    직업 상세 정보 조회.
    Returns: {job_cd, job_nm, work, wage, future, related_majors: [...]}
    """
    # TODO
    raise NotImplementedError("career_api.get_job_detail 구현 필요")


def search_major(keyword: str) -> dict:
    """
    학과명 키워드로 검색.
    Returns: {"majors": [ {major_seq, major_nm, l_class, ...}, ... ]}
    """
    # TODO
    raise NotImplementedError("career_api.search_major 구현 필요")


def get_major_detail(major_seq) -> dict:
    """
    학과 상세 정보 조회.
    Returns: {major_seq, major_nm, summary, employment_rate, universities: [...], related_jobs: [...]}
    """
    # TODO
    raise NotImplementedError("career_api.get_major_detail 구현 필요")
