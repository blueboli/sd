"""
utils/career_api.py
F-001 직업/학과 탐색기 - 커리어넷 오픈API 연동
- 직업백과: https://www.career.go.kr/cnet/front/openapi/jobs.json / job.json (JSON)
- 학과정보: https://www.career.go.kr/cnet/openapi/getOpenApi (XML)
"""
from urllib.parse import quote
import xml.etree.ElementTree as ET

import streamlit as st 
import requests
import re

# TODO: 여기에 발급받은 인증키를 그대로 넣으세요 (비공개 레포)
CAREERNET_API_KEY = st.secrets["CAREERNET_API_KEY"]  # <-- 여기 채우기

JOB_LIST_URL = "https://www.career.go.kr/cnet/front/openapi/jobs.json"
JOB_DETAIL_URL = "https://www.career.go.kr/cnet/front/openapi/job.json"
MAJOR_URL = "https://www.career.go.kr/cnet/openapi/getOpenApi"

def remove_html_tags(text):
    """문자열에 포함된 HTML 태그 제거"""
    if not text:
        return "정보 없음"

    return re.sub(r"<[^>]*>", "", str(text)).strip()
    
def search_job(keyword: str) -> list[dict]:
    """직업백과 목록 검색 -> [{job_cd, job_nm, top_nm, wage, work, ...}, ...]"""
    res = requests.get(
        JOB_LIST_URL,
        params={"apiKey": CAREERNET_API_KEY, "searchJobNm": keyword},
        timeout=5,
    )
    res.raise_for_status()
    return res.json().get("jobs", [])


def get_job_detail(job_cd) -> dict:
    """직업백과 상세 -> {baseInfo, workList, forecastList, departList, ...}"""
    res = requests.get(
        JOB_DETAIL_URL,
        params={"apiKey": CAREERNET_API_KEY, "seq": job_cd},
        timeout=5,
    )
    res.raise_for_status()
    return res.json()


def search_major(keyword: str, gubun: str = "univ_list") -> list[dict]:
    """학과정보 목록 검색 -> [{majorSeq, lClass, mClass, facilName}, ...]"""
    params = {
        "apiKey": CAREERNET_API_KEY,
        "svcType": "api",
        "svcCode": "MAJOR",
        "gubun": gubun,          # UTF-8 그대로, 수동 EUC-KR 인코딩 제거
        "contentType": "xml",
        "searchTitle": keyword,  # UTF-8 그대로
    }
    res = requests.get(MAJOR_URL, params=params, timeout=5)

    res.raise_for_status()

    root = ET.fromstring(res.content)
    if root.tag != "dataSearch":
        # <result><content><code>...</code></content></result> 형태면
        # 인증/서비스 승인 문제일 가능성이 큼
        print("API ERROR:", res.text)
        return []

    return [
        {
            "majorSeq": c.findtext("majorSeq"),
            "lClass": c.findtext("lClass"),
            "mClass": c.findtext("mClass"),
            "facilName": c.findtext("facilName"),
        }
        for c in root.findall("content")
    ]


def get_major_detail(major_seq, gubun: str = "univ_list") -> dict:
    """학과정보 상세 -> {major, summary, employment, salary, job, universities, ...}"""
    query = "&".join([
        f"apiKey={CAREERNET_API_KEY}",
        "svcType=api",
        "svcCode=MAJOR_VIEW",
        f"gubun={quote(gubun, encoding='euc-kr')}",
        "contentType=xml",
        f"majorSeq={major_seq}",
    ])
    res = requests.get(f"{MAJOR_URL}?{query}", timeout=5)
    res.raise_for_status()
    root = ET.fromstring(res.content)
    content = root.find("content")
    if content is None:
        return {}
    universities = [
        {
            "area": u.findtext("area"),
            "schoolName": u.findtext("schoolName"),
            "campus_nm": u.findtext("campus_nm"),
        }
        for u in content.findall("university/content")
    ]
    return {
        "major": content.findtext("major"),
        "summary": content.findtext("summary"),
        "employment": remove_html_tags(content.findtext("employment")),
        "salary": content.findtext("salary"),
        "job": content.findtext("job"),
        "interest": content.findtext("interest"),
        "property": content.findtext("property"),
        "universities": universities,
    }
