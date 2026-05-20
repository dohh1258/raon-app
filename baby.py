import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="라온이 마중", page_icon="🧸", layout="centered")

# CSS 디자인
st.markdown("""
    <style>
    .diary-card { background-color: #1e2130; padding: 20px; border-radius: 15px; border-left: 5px solid #FF4B4B; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기 (diary 탭 지정)
def get_data():
    return conn.read(worksheet="diary", ttl="0s")

# 데이터 저장하기
def save_diary(date, title, content):
    existing_data = get_data()
    new_data = pd.DataFrame([{"날짜": date, "제목": title, "내용": content}])
    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
    conn.update(worksheet="diary", data=updated_df)
    st.cache_data.clear()

st.title("🧸 라온이 마중")
st.info("✨ 라온이를 만나는 날까지 D-203일 남았어요!")

# 폼 입력
with st.form("diary_form", clear_on_submit=True):
    title = st.text_input("제목")
    content = st.text_area("내용")
    submitted = st.form_submit_button("저장")
    
    if submitted:
        if title and content:
            date_str = datetime.now().strftime("%m/%d")
            save_diary(date_str, title, content)
            st.success("저장 완료!")
            st.rerun()
        else:
            st.error("제목과 내용을 다 적어줘!")

st.divider()

# 일기 목록 보여주기
df = get_data()
if not df.empty:
    for i, row in df.iloc[::-1].iterrows():
        st.markdown(f"""
        <div class='diary-card'>
            <h4>{row['제목']} <small>({row['날짜']})</small></h4>
            <p>{row['내용']}</p>
        </div>
        """, unsafe_allow_html=True)
