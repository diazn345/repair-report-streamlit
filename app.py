import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# QR 관련 라이브러리
import cv2
from pyzbar.pyzbar import decode
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import urllib.parse

# 🔐 구글 API 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("cobalt-ship-460502-m7-a815d208aae2.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1kkqtHsSK-QNfvtL4d3IYhcCsV0ut0y1jDm-u-lsMOZc").sheet1

# 🚀 Streamlit UI
st.title("🔧 수리 보고서 제출")
st.write("📸 QR코드를 스캔하면 장비 ID가 자동 입력됩니다.")

# 🔍 QR 코드 인식 처리 클래스
class QRProcessor(VideoProcessorBase):
    def __init__(self):
        self.result = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objs = decode(img)
        for obj in decoded_objs:
            self.result = obj.data.decode("utf-8")
            break
        return frame

# 📸 웹캠 실행
ctx = webrtc_streamer(
    key="qr",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=QRProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# 📥 QR 코드 결과 처리 및 장비 ID 추출
equipment_id = ""
if ctx.video_processor and ctx.video_processor.result:
    qr_data = ctx.video_processor.result.strip()
    parsed_url = urllib.parse.urlparse(qr_data)

    if parsed_url.query:
        query_dict = urllib.parse.parse_qs(parsed_url.query)
        equipment_id = query_dict.get("qr", [""])[0]
    else:
        equipment_id = parsed_url.path.strip("/").split("/")[-1]

    st.success(f"✅ 인식된 장비 ID: {equipment_id}")

# 📝 사용자 입력 폼
name = st.text_input("이름")
equipment = st.text_input("장비 ID", value=equipment_id)
issue = st.text_area("고장 내용")
submitted = st.button("제출")

if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [name, equipment, issue, timestamp]
    sheet.append_row(new_row)
    st.success(f"✅ 감사합니다, {name}님. 보고서가 Google Sheets에 저장되었습니다!")
