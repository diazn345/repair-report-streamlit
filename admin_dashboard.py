import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt

# 🔑 구글 시트 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
client = gspread.authorize(creds)

# 📄 시트 열기
sheet = client.open("repair_reports").sheet1
data = sheet.get_all_records()

# 📊 데이터프레임 변환
df = pd.DataFrame(data)

# 📅 '제출 시간' → datetime 변환 및 'timestamp' 컬럼 생성
df["timestamp"] = pd.to_datetime(df["제출 시간"], errors="coerce")

# 🧭 사이드바 필터
st.sidebar.header("📅 날짜 필터")
start_date = st.sidebar.date_input("시작일", value=df["timestamp"].min().date())
end_date = st.sidebar.date_input("종료일", value=df["timestamp"].max().date())

# 📦 날짜 필터링
filtered_df = df[
    (df["timestamp"].dt.date >= start_date) &
    (df["timestamp"].dt.date <= end_date)
]

# 🧮 대시보드 본문
st.title("🔧 관리자 대시보드")
st.write("필터링된 보고 수:", len(filtered_df))

# 📊 날짜별 보고 수 시각화
st.subheader("📊 날짜별 보고 수")
report_counts = filtered_df["timestamp"].dt.date.value_counts().sort_index()
st.bar_chart(report_counts)

# 🔩 장비별 고장 빈도
st.subheader("🔩 장비별 고장 빈도")
if "장비ID" in filtered_df.columns:
    equip_counts = filtered_df["장비ID"].value_counts()
    st.bar_chart(equip_counts)
else:
    st.warning("⚠️ '장비ID' 컬럼이 존재하지 않습니다. 정확한 컬럼명을 확인하세요.")

# 📥 다운로드 버튼
st.subheader("⬇️ 필터링된 데이터 다운로드")
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="CSV 파일 다운로드",
    data=csv,
    file_name="filtered_repair_reports.csv",
    mime="text/csv"
)

# 📝 데이터 테이블 보기
st.subheader("📋 데이터 테이블")
st.dataframe(filtered_df)
