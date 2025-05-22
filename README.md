
# 🔧 Repair Report Streamlit App

이 프로젝트는 QR 코드 스캔 기능을 포함한 **수리 보고서 제출 및 관리자 대시보드 시스템**입니다.  
Google Sheets와 연동되어 데이터를 저장하고, 관리자 페이지에서는 통계를 확인할 수 있습니다.

---

## 📸 주요 기능

- **QR 코드 스캔**으로 장비 ID 자동 입력
- **작성자 / 고장 내용 / 사용 부품** 선택 가능 (Google Sheets에서 동적 불러오기)
- **Google Sheets 저장 연동**
- **관리자 대시보드**: 보고서 통계, 필터, 정렬, 시각화 등 제공

---

## 🚀 실행 방법

### 1. 설치

```bash
git clone https://github.com/diazn345/repair-report-streamlit.git
cd repair-report-streamlit
pip install -r requirements.txt
```

### 2. 실행

```bash
streamlit run app.py
```

관리자 페이지는 아래 명령어로 실행:

```bash
streamlit run admin_dashboard.py
```

---

## 🗂️ 프로젝트 구조

```
repair-report-streamlit/
├── app.py                # 메인 수리 보고 앱
├── admin_dashboard.py    # 관리자 대시보드
├── requirements.txt      # 필요한 패키지 목록
├── .gitignore
└── README.md             # 프로젝트 설명 파일
```

---

## 🔑 주의 사항

- Google Sheets 연동을 위해 `credentials.json` 파일이 필요합니다.  
  이 파일은 **보안상의 이유로 GitHub에 업로드되지 않습니다.**
- `.gitignore`에 민감한 정보(.json, .DS_Store 등)가 추가되어 있습니다.

---

## 📦 배포

이 앱은 [Streamlit Community Cloud](https://streamlit.io/cloud)를 통해 웹으로 배포할 수 있습니다.

---

## 🙋‍♂️ 만든 사람

- **GitHub**: [@diazn345](https://github.com/diazn345)
