import streamlit as st
from utils.gemini_api import generate_topics


st.set_page_config(
    page_title="세특 탐구주제 추천",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI 기반 세특(세부능력특기사항) 탐구주제 추천")
st.markdown(
    "학생의 학년과 관심 분야를 바탕으로 **Gemini 2.5 Flash**가 "
    "맞춤형 탐구 주제와 심화 방향을 제안합니다."
)
st.markdown("---")

# 입력 폼
with st.form("recommendation_form"):
    col1, col2 = st.columns(2)

    with col1:
        # 학년 (필수)
        grade = st.selectbox(
            "학년 선택 (필수) *",
            ["", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"],
            help="학생의 현재 학년을 선택해주세요."
        )

        # 희망 진로 (선택)
        career = st.text_input(
            "희망 진로 (선택)",
            placeholder="예: 인공지능 엔지니어, 바이오 제약 연구원 등"
        )

    with col2:
        # 관심 분야 (필수)
        interest = st.text_input(
            "관심 분야 / 교과 단원 (필수) *",
            placeholder="예: 확률과 통계 - 빅데이터 분석, 생명과학 - 유전자 가위 등"
        )

        # 선호 탐구 유형 (선택)
        inquiry_type = st.selectbox(
            "선호 탐구 유형 (선택)",
            [
                "상관없음",
                "심층 문헌 연구형",
                "데이터 분석 및 실험형",
                "사회적 이슈 융합형",
                "프로그램 구현 및 공학적 설계형"
            ]
        )

    submitted = st.form_submit_button(
        "🚀 맞춤형 세특 주제 추천받기",
        use_container_width=True
    )

# 제출 결과 처
if submitted:

    # 필수값 검증
    if not grade or not interest.strip():
        st.markdown(
            '<p style="color: red; font-weight: bold; font-size: 16px;">'
            '⚠️ [필수 입력 누락] 학년과 관심 분야는 필수 입력 항목입니다. '
            '모두 입력 후 다시 시도해 주세요.'
            '</p>',
            unsafe_allow_html=True
        )

    else:
        # Gemini API 호출 중 로딩 표시
        with st.spinner(
            "✨ Gemini 2.5 Flash가 생기부를 빛내줄 반짝이는 아이디어를 "
            "구상 중입니다... 잠시만 기다려주세요!"
        ):
            try:
                # Gemini API 호출
                topics = generate_topics(
                    grade,
                    career,
                    interest,
                    inquiry_type
                )
                
                # 성공 메시지
                st.success("🎉 세특 탐구 주제 추천이 완료되었습니다!")
                
                st.markdown("---")

                # 추천 결과
                st.subheader("💡 추천 탐구 주제 리스트")

                # 추천 결과 카드 출력
                for i, topic in enumerate(topics, start=1):

                    with st.container(border=True):
                        st.markdown(
                            f"### {i}. {topic['title']}"
                        )

                        st.markdown(
                            f"**🔎 탐구 방향**  \n"
                            f"{topic['direction']}"
                        )

                        st.markdown(
                            f"**🚀 심화 탐구 아이디어**  \n"
                            f"{topic['extension']}"
                        )
                        
                # 복사용 전체 텍스트 생성  
                copy_text = ""

                for i, topic in enumerate(topics, start=1):
                    copy_text += (
                        f"{i}. {topic['title']}\n"
                        f"탐구 방향: {topic['direction']}\n"
                        f"심화 탐구 아이디어: {topic['extension']}\n\n"
                    )
                    
                # 복사 영역
                st.subheader("📋 추천 결과 복사")

                st.code(
                    copy_text,
                    language=None
                )
                
            # 오류 처리
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
