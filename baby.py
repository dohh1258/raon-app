import streamlit as st
import datetime
import os
import pandas as pd
from PIL import Image

st.set_page_config(page_title="라온이 마중", page_icon="🧸", layout="centered")

st.title("🧸 라온이 마중: 우리 가족의 여정")
st.subheader("라온이 엄마, 아빠가 된 걸 축하해요! 💕")

today = datetime.date.today()
due_date = datetime.date(2026, 12, 25)
d_day = (due_date - today).days
st.info(f"✨ **라온이** 만나는 날까지 **D-{d_day}일** 남았어요! (예정일: {due_date.strftime('%Y년 %m월 %d일')})")
st.markdown("---")

current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
DB_FILE = os.path.join(current_dir, "raon_diary.csv")
CHECKLIST_FILE = os.path.join(current_dir, "raon_checklist.csv")
NAME_FILE = os.path.join(current_dir, "raon_names.csv")
GALLERY_DIR = os.path.join(current_dir, "raon_gallery")

if not os.path.exists(GALLERY_DIR):
    os.makedirs(GALLERY_DIR)

tab1, tab2, tab3, tab4 = st.tabs(["📝 일기", "🎒 체크리스트", "📛 이름 투표", "📸 갤러리"])

# ==================== 탭 1: 마중 일기 ====================
with tab1:
    with st.form("raon_form", clear_on_submit=True):
        st.header("🤰 오늘 엄마 컨디션")
        condition = st.select_slider("컨디션", options=["매우 힘듦 😭", "지침 😮‍💨", "보통 😐", "좋음 😊", "최상! 🌟"], value="보통 😐")
        mom_note = st.text_area("엄마의 상태나 먹고 싶은 음식")
        st.header("🧔 아빠의 한 줄 다짐")
        dad_note = st.text_area("엄마에게 보내는 메시지")
        if st.form_submit_button("저장하기"):
            if mom_note.strip() or dad_note.strip():
                new_df = pd.DataFrame([{"날짜": today.strftime("%Y-%m-%d"), "엄마 컨디션": condition, "엄마의 한 줄": mom_note, "아빠의 응원": dad_note}])
                final_df = pd.concat([pd.read_csv(DB_FILE), new_df], ignore_index=True) if os.path.exists(DB_FILE) else new_df
                final_df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
                st.success("✅ 저장 완료!")
                st.rerun()
            else:
                st.warning("⚠️ 내용을 입력해주세요.")

    st.markdown("---")
    if os.path.exists(DB_FILE):
        display_df = pd.read_csv(DB_FILE)
        for idx, row in display_df.iloc[::-1].iterrows():
            with st.expander(f"📅 {row['날짜']}의 기록"):
                st.write(f"**🤰 엄마 컨디션:** {row['엄마 컨디션']}")
                st.write(f"**💬 엄마:** {row['엄마의 한 줄'] if pd.notna(row['엄마의 한 줄']) else '없음'}")
                st.write(f"**💬 아빠:** {row['아빠의 응원'] if pd.notna(row['아빠의 응원']) else '없음'}")

# ==================== 탭 2: 체크리스트 ====================
with tab2:
    st.header("🎒 출산 가방 체크리스트")
    default_items = [{"물품": "배냇저고리", "완료": False}, {"물품": "아기 물티슈", "완료": False}, {"물품": "수유 패드", "완료": False}]
    check_df = pd.read_csv(CHECKLIST_FILE) if os.path.exists(CHECKLIST_FILE) else pd.DataFrame(default_items)
    
    with st.form("add_item_form", clear_on_submit=True):
        new_item = st.text_input("➕ 준비물 추가")
        if st.form_submit_button("추가") and new_item.strip():
            if new_item not in check_df["물품"].values:
                check_df = pd.concat([check_df, pd.DataFrame([{"물품": new_item, "완료": False}])], ignore_index=True)
                check_df.to_csv(CHECKLIST_FILE, index=False, encoding="utf-8-sig")
                st.rerun()

    st.markdown("---")
    updated_status = []
    for idx, row in check_df.iterrows():
        is_checked = st.checkbox(row["물품"], value=row["완료"], key=f"item_{idx}")
        updated_status.append(is_checked)
    if updated_status != list(check_df["완료"]):
        check_df["완료"] = updated_status
        check_df.to_csv(CHECKLIST_FILE, index=False, encoding="utf-8-sig")
        st.rerun()

# ==================== 탭 3: 이름 투표 ====================
with tab3:
    st.header("📛 라온이 이름 투표")
    name_df = pd.read_csv(NAME_FILE) if os.path.exists(NAME_FILE) else pd.DataFrame([{"이름": "김라온", "득표수": 0}])

    with st.form("add_name_form", clear_on_submit=True):
        new_name = st.text_input("✍️ 이름 후보 입력")
        if st.form_submit_button("후보 등록") and new_name.strip():
            if new_name not in name_df["이름"].values:
                name_df = pd.concat([name_df, pd.DataFrame([{"이름": new_name, "득표수": 0}])], ignore_index=True)
                name_df.to_csv(NAME_FILE, index=False, encoding="utf-8-sig")
                st.rerun()

    st.markdown("---")
    name_df = name_df.sort_values(by="득표수", ascending=False).reset_index(drop=True)
    for idx, row in name_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1: st.markdown(f"### 🏷️ **{row['이름']}**")
        with col2: st.markdown(f"❤️ **{row['득표수']}표**")
        with col3:
            if st.button("투표", key=f"vote_{idx}"):
                name_df.at[idx, "득표수"] += 1
                name_df.to_csv(NAME_FILE, index=False, encoding="utf-8-sig")
                st.rerun()

# ==================== 탭 4: 갤러리 ====================
with tab4:
    st.header("📸 라온이 갤러리")
    uploaded_file = st.file_uploader("사진 선택 (jpg, jpeg, png)", type=["jpg", "jpeg", "png"], key="gallery_uploader")

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            image.save(os.path.join(GALLERY_DIR, f"IMG_{timestamp}.png"))
            st.success("📸 사진 등록 완료!")
            st.rerun()
        except Exception as e:
            st.error(f"오류: {e}")

    st.markdown("---")
    if os.path.exists(GALLERY_DIR):
        photo_files = [f for f in os.listdir(GALLERY_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
        photo_files.sort(reverse=True)
        if photo_files:
            for i in range(0, len(photo_files), 2):
                cols = st.columns(2)
                with cols[0]:
                    st.image(os.path.join(GALLERY_DIR, photo_files[i]), use_container_width=True)
                    try: st.caption(f"📅 {photo_files[i].split('_')[1][:8]}")
                    except: st.caption("📅 업로드 완료")
                if i + 1 < len(photo_files):
                    with cols[1]:
                        st.image(os.path.join(GALLERY_DIR, photo_files[i+1]), use_container_width=True)
                        try: st.caption(f"📅 {photo_files[i+1].split('_')[1][:8]}")
                        except: st.caption("📅 업로드 완료")
        else:
            st.info("등록된 사진이 없습니다. 📸")
