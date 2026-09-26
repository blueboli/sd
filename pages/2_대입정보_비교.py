"""F-002 대입정보 비교 대시보드

외부 Excel 원본을 자동으로 읽어 대학을 최대 5개까지 고르고,
같은 전형구분의 교과·서류·면접·논술·수능·실기 반영비율과
수능최저 여부를 비교한다.

기본 원본 경로: data/admission_2028.xlsx
다른 로컬 경로나 URL은 ADMISSION_EXCEL_SOURCE 환경변수로 지정한다.
"""

import os
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="대입정보 비교",
    page_icon="⚖️",
    layout="wide",
)


WEIGHTS = ["교과", "서류", "면접", "논술", "수능", "실기"]

WEIGHT_COLORS = {
    "교과": "#2563eb",
    "서류": "#10b981",
    "면접": "#f97316",
    "논술": "#8b5cf6",
    "수능": "#ef4444",
    "실기": "#14b8a6",
}

CAT_ORDER = [
    "학생부교과",
    "학생부종합",
    "논술",
    "정시",
    "실기",
]


# Excel 원본에서 사용하는 다양한 컬럼명을 표준 컬럼명으로 변환한다.
COLUMN_ALIASES = {
    "대학명": [
        "대학명",
        "대학",
        "대학교",
        "학교명",
    ],
    "전형구분": [
        "전형구분",
        "전형 유형",
        "전형유형",
        "모집전형",
    ],
    "전형명": [
        "전형명",
        "전형 이름",
        "전형명칭",
    ],
    "선발방식": [
        "선발방식",
        "선발 방식",
    ],
    "주요반영요소": [
        "주요반영요소",
        "주요 반영 요소",
        "반영요소",
        "반영 요소",
    ],
    "교과": [
        "교과반영률",
        "교과 반영률",
        "교과",
    ],
    "서류": [
        "서류반영률",
        "서류 반영률",
        "서류",
    ],
    "면접": [
        "면접반영률",
        "면접 반영률",
        "면접",
    ],
    "논술": [
        "논술반영률",
        "논술 반영률",
        "논술",
    ],
    "수능": [
        "수능반영률",
        "수능 반영률",
        "수능",
    ],
    "실기": [
        "실기반영률",
        "실기 반영률",
        "실기",
    ],
    "수능최저": [
        "수능최저여부",
        "수능최저",
        "수능 최저 여부",
        "수능최저학력기준",
    ],
}


REQUIRED_COLUMNS = [
    "대학명",
    "전형구분",
    "교과",
    "서류",
    "면접",
    "논술",
    "수능",
    "수능최저",
]


def normalize_header(value: object) -> str:
    """헤더의 공백과 줄바꿈을 제거해 비교한다."""
    return "".join(
        str(value)
        .replace("\n", " ")
        .split()
    )


def find_column(
    columns: list[object],
    aliases: list[str],
) -> object | None:
    """여러 후보명 중 실제 Excel 컬럼명을 찾는다."""
    normalized_columns = {
        normalize_header(column): column
        for column in columns
    }

    for alias in aliases:
        normalized_alias = normalize_header(alias)

        if normalized_alias in normalized_columns:
            return normalized_columns[normalized_alias]

    return None


def to_percentage(series: pd.Series) -> pd.Series:
    """퍼센트 기호가 포함된 값을 숫자로 변환한다."""
    values = (
        series.astype("string")
        .str.strip()
        .str.replace("%", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace(
            {
                "": pd.NA,
                "-": pd.NA,
                "–": pd.NA,
                "없음": pd.NA,
            }
        )
    )

    return pd.to_numeric(
        values,
        errors="coerce",
    ).fillna(0.0)


def normalize_minimum(value: object) -> str:
    """수능최저 여부를 있음/없음으로 통일한다."""
    text = str(value).strip().lower()

    if text in {
        "있음",
        "있다",
        "적용",
        "예",
        "yes",
        "y",
        "o",
        "1",
        "true",
    }:
        return "있음"

    if text in {
        "없음",
        "없다",
        "미적용",
        "아니오",
        "no",
        "n",
        "x",
        "0",
        "false",
        "nan",
        "<na>",
    }:
        return "없음"

    return str(value).strip()


def normalize_data(raw: pd.DataFrame) -> pd.DataFrame:
    """외부 Excel 원본을 화면에서 사용하는 표준 데이터로 변환한다."""
    frame = raw.copy()

    frame.columns = [
        str(column).strip()
        for column in frame.columns
    ]

    frame = frame.dropna(
        how="all"
    ).reset_index(drop=True)

    rename_map = {}
    missing_columns = []

    for standard_name, aliases in COLUMN_ALIASES.items():
        source_column = find_column(
            list(frame.columns),
            aliases,
        )

        if source_column is None:
            if standard_name in REQUIRED_COLUMNS:
                missing_columns.append(standard_name)
        else:
            rename_map[source_column] = standard_name

    if missing_columns:
        raise ValueError(
            "필수 컬럼이 없습니다: "
            + ", ".join(missing_columns)
            + "\n"
            + "Excel 첫 번째 행에 컬럼명을 넣어 주세요."
        )

    frame = frame.rename(
        columns=rename_map
    )

    # 선택 컬럼이 없는 경우에도 화면이 작동하도록 빈 컬럼을 만든다.
    for optional_column in [
        "전형명",
        "선발방식",
        "주요반영요소",
    ]:
        if optional_column not in frame:
            frame[optional_column] = ""

    if "실기" not in frame:
        frame["실기"] = 0.0

    required_data = [
        "대학명",
        "전형구분",
        "수능최저",
    ]

    if frame[required_data].isna().any().any():
        raise ValueError(
            "대학명·전형구분·수능최저여부가 "
            "비어 있는 행이 있습니다."
        )

    frame["대학명"] = (
        frame["대학명"]
        .astype(str)
        .str.strip()
    )

    frame["전형구분"] = (
        frame["전형구분"]
        .astype(str)
        .str.strip()
    )

    frame["수능최저"] = (
        frame["수능최저"]
        .map(normalize_minimum)
    )

    for weight in WEIGHTS:
        frame[weight] = to_percentage(
            frame[weight]
        )

    # 전형명이 없는 경우 임시 전형명을 만든다.
    empty_name = (
        frame["전형명"].isna()
        | frame["전형명"]
        .astype(str)
        .str.strip()
        .isin({"", "nan", "<NA>"})
    )

    frame.loc[empty_name, "전형명"] = [
        f"{category} 전형 {index + 1}"
        for index, category in zip(
            frame.index[empty_name],
            frame.loc[
                empty_name,
                "전형구분",
            ],
        )
    ]

    return frame


@st.cache_data(show_spinner=False)
def read_excel_sheet(
    file_bytes: bytes,
    sheet_name: str,
) -> pd.DataFrame:
    """Excel 바이트 데이터를 읽는다."""
    return pd.read_excel(
        BytesIO(file_bytes),
        sheet_name=sheet_name,
    )


@st.cache_data(show_spinner=False)
def read_external_source(source: str) -> bytes:
    """로컬 파일 또는 HTTP(S) URL에서 Excel 원본을 읽는다."""
    if source.startswith(
        ("http://", "https://")
    ):
        with urlopen(
            source,
            timeout=30,
        ) as response:
            return response.read()

    return Path(
        source
    ).expanduser().read_bytes()


def get_external_source() -> str:
    """외부 Excel 기본 경로 또는 환경변수 경로를 반환한다."""
    default_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "admission_2028.xlsx"
    )

    return os.getenv(
        "ADMISSION_EXCEL_SOURCE",
        str(default_path),
    ).strip()


def make_long_weights(
    frame: pd.DataFrame,
) -> pd.DataFrame:
    """반영요소를 차트용 세로형 데이터로 변환한다."""
    long_frame = frame.assign(
        항목=(
            frame["대학명"]
            + " · "
            + frame["전형명"].astype(str)
        )
    ).melt(
        id_vars=["항목"],
        value_vars=WEIGHTS,
        var_name="반영요소",
        value_name="비율",
    )

    return long_frame[
        long_frame["비율"] > 0
    ]


st.title("⚖️ 대입정보 비교")

st.caption(
    "외부 Excel 원본을 자동으로 불러와 "
    "대학 최대 5개와 전형구분별 반영비율을 비교합니다."
)


source = get_external_source()

try:
    file_bytes = read_external_source(source)

    workbook = pd.ExcelFile(
        BytesIO(file_bytes)
    )

    sheet_name = workbook.sheet_names[0]

    if len(workbook.sheet_names) > 1:
        sheet_name = st.selectbox(
            "불러올 시트",
            workbook.sheet_names,
        )

    raw_data = read_excel_sheet(
        file_bytes,
        sheet_name,
    )

    df = normalize_data(raw_data)

except ValueError as exc:
    st.error(str(exc))
    st.stop()

except FileNotFoundError:
    st.error(
        "외부 Excel 원본을 찾을 수 없습니다."
    )

    st.info(
        "기본 경로 "
        "`data/admission_2028.xlsx`에 파일을 두거나 "
        "`ADMISSION_EXCEL_SOURCE`를 지정해 주세요."
    )

    st.stop()

except Exception as exc:
    st.error(
        f"Excel 파일을 읽을 수 없습니다: {exc}"
    )
    st.stop()


if df.empty:
    st.warning(
        "외부 Excel 원본에 데이터 행이 없습니다."
    )
    st.stop()


universities = (
    df["대학명"]
    .drop_duplicates()
    .tolist()
)

file_categories = (
    df["전형구분"]
    .drop_duplicates()
    .tolist()
)

categories = [
    category
    for category in CAT_ORDER
    if category in file_categories
]

categories += [
    category
    for category in file_categories
    if category not in categories
]


st.success(
    "외부 Excel 원본에서 "
    f"{len(df)}개 전형, "
    f"{len(universities)}개 대학을 불러왔습니다."
)


with st.expander(
    "불러온 데이터 확인",
    expanded=False,
):
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )


st.divider()


col1, col2 = st.columns(
    [1.4, 1]
)


with col1:
    selected_universities = st.multiselect(
        "대학 선택 (최대 5개)",
        universities,
        default=universities[
            : min(3, len(universities))
        ],
    )


with col2:
    selected_category = st.selectbox(
        "전형구분",
        categories,
    )


if len(selected_universities) > 5:
    st.warning(
        "대학은 최대 5개까지만 비교할 수 있습니다. "
        "처음 선택한 5개만 사용합니다."
    )

    selected_universities = (
        selected_universities[:5]
    )


if not selected_universities:
    st.info(
        "비교할 대학을 1개 이상 선택해 주세요."
    )
    st.stop()


comparison = df[
    df["대학명"].isin(
        selected_universities
    )
    & (
        df["전형구분"]
        == selected_category
    )
].reset_index(drop=True)


if comparison.empty:
    st.warning(
        f"선택한 대학 중 "
        f"'{selected_category}' 전형이 있는 곳이 없습니다. "
        "다른 전형구분을 선택해 보세요."
    )
    st.stop()


st.subheader(
    f"{selected_category} 반영요소 비교"
)


long_data = make_long_weights(
    comparison
)


if long_data.empty:
    st.info(
        "선택한 전형에 반영비율 데이터가 없습니다."
    )

else:
    fig = px.bar(
        long_data,
        x="항목",
        y="비율",
        color="반영요소",
        barmode="group",
        color_discrete_map=WEIGHT_COLORS,
        category_orders={
            "반영요소": WEIGHTS,
        },
        text="비율",
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        hovertemplate=(
            "%{x}<br>"
            "%{fullData.name}: %{y}%"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        template="plotly_white",
        height=440,
        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title="반영요소",
        ),
    )

    fig.update_yaxes(
        title="반영 비율 (%)",
        range=[0, 110],
    )

    fig.update_xaxes(title="")

    st.plotly_chart(
        fig,
        width="stretch",
    )


st.divider()
st.subheader("비교 표")


present_weights = [
    weight
    for weight in WEIGHTS
    if comparison[weight].sum() > 0
]


display_columns = [
    "대학명",
    "전형명",
    "선발방식",
    *present_weights,
    "수능최저",
    "주요반영요소",
]


display_df = comparison[
    display_columns
].rename(
    columns={
        "대학명": "대학",
    }
)


def format_percent(value: object) -> str:
    if pd.isna(value) or float(value) <= 0:
        return "–"

    return f"{float(value):g}%"


def color_minimum(value: object) -> str:
    if value == "있음":
        return (
            "background-color:#ffedd5;"
            "color:#9a3412;"
            "font-weight:700"
        )

    if value == "없음":
        return (
            "background-color:#dcfce7;"
            "color:#166534;"
            "font-weight:700"
        )

    return ""


styled = display_df.style.format(
    format_percent,
    subset=[
        weight
        for weight in present_weights
        if weight in display_df.columns
    ],
).map(
    color_minimum,
    subset=["수능최저"],
)


st.dataframe(
    styled,
    width="stretch",
    hide_index=True,
)
