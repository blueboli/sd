"""
utils/admission_data.py
F-002 대입정보 비교 대시보드 - 대학알리미 데이터 로딩/가공

담당: 임찬서
data/admission_2028.csv 를 pandas로 불러와 비교 화면에서 쓸 수 있는
형태로 가공하는 함수들을 여기에 작성하세요.

예상 CSV 컬럼:
대학명 / 전형구분(학생부교과·학생부종합·논술·정시) /
교과반영률 / 서류반영률 / 면접반영률 / 논술반영률 / 수능반영률 / 수능최저여부
"""

import pandas as pd

DATA_PATH = "data/admission_2028.csv"


def load_admission_data() -> pd.DataFrame:
    """CSV 원본 로딩"""
    # TODO: pd.read_csv(DATA_PATH) 로 구현
    raise NotImplementedError("admission_data.load_admission_data 구현 필요")


def get_university_list() -> list[str]:
    """대학 선택 드롭다운용 전체 대학 목록 반환"""
    # TODO
    raise NotImplementedError("admission_data.get_university_list 구현 필요")


def filter_by_universities(universities: list[str], admission_type: str) -> pd.DataFrame:
    """선택한 대학(최대 5개) + 전형구분으로 필터링된 데이터 반환"""
    # TODO
    raise NotImplementedError("admission_data.filter_by_universities 구현 필요")
