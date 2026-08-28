# 진로진학도우미

풍동고 학생을 위한 2028 대입 전형 비교·분석 웹 대시보드 (알파엔지니어스 동아리)

## 폴더 구조
```
project-root/
├── Home.py                        # 홈 화면 (조준원)
├── index.html                     # 랜딩페이지 (정적 배포용, GitHub Pages)
├── pages/
│   ├── 1_직업학과_탐색기.py         # F-001 (윤준호)
│   ├── 2_대입정보_비교.py           # F-002 (임찬서) — 개발 중
│   └── 3_세특_추천.py               # F-003 (유지현) — 개발 중
├── utils/
│   ├── career_api.py              # 커리어넷 API — 개발 중
│   ├── admission_data.py          # 대입정보 데이터 처리 — 개발 중
│   ├── gemini_api.py              # Gemini API — 개발 중
│   └── common_ui.py               # 공통 UI 요소
├── data/
│   └── admission_2028.csv         # 대학알리미 정제 데이터 (담당자 업로드 예정)
├── .streamlit/
│   ├── config.toml                # 테마 설정
│   └── secrets.toml.example       # API 키 예시 (실제 키는 secrets.toml, gitignore 처리)
├── requirements.txt
└── .gitignore
```

## 실행 방법
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # 발급받은 API 키 입력
streamlit run Home.py
```

## 배포
- **Streamlit 앱**: Streamlit Community Cloud (share.streamlit.io) — GitHub 레포 연결 후 자동 배포
  - ⚠️ GitHub Pages는 정적 파일만 지원해서 Streamlit 앱 자체는 배포할 수 없습니다.
- **랜딩페이지(`index.html`)**: GitHub Pages로 별도 배포 가능 (저장소 Settings → Pages)

## 담당
| 이름 | 담당 기능 | GitHub |
|---|---|---|
| 조준원 | 총괄 / Home.py | @blueboli |
| 윤준호 | F-001 직업/학과 탐색기 | @c7wsy4s |
| 임찬서 | F-002 대입정보 비교 대시보드 | @foreverchan4280-ai |
| 유지현 | F-003 세특 탐구 주제 추천 도우미 | @25-037-hash |

## 진행 상태
- [x] Home.py 기본 화면
- [x] index.html 랜딩페이지
- [x] F-001 직업/학과 탐색기 UI (더미 데이터, API 연동 전)
- [ ] F-001 커리어넷 API 실제 연동 (`utils/career_api.py`)
- [ ] F-002 대입정보 비교 대시보드
- [ ] F-003 세특 탐구 주제 추천 도우미
