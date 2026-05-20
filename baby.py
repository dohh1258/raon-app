import streamlit as st
import datetime
import calendar

st.set_page_config(page_title="라온이 마중", page_icon="🧸", layout="centered")

# --- CSS 추가: 이름 투표 글씨 강제 검정색 설정 ---
st.markdown("""
    <style>
    .postit-text {
        color: #000000 !important;
        font-weight: 800 !important;
        text-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 세션 데이터 초기화 ---
if "diaries" not in st.session_state: st.session_state.diaries = []
if "conditions" not in st.session_state: st.session_state.conditions = []
if "hospitals" not in st.session_state: st.session_state.hospitals = []
if "posts" not in st.session_state: st.session_state.posts = []
if "tasks" not in st.session_state: st.session_state.tasks = []
if "gallery" not in st.session_state: st.session_state.gallery = []
if "selected_day" not in st.session_state: st.session_state.selected_day = datetime.datetime.now().day

# --- 상단 요약 정보 ---
st.title("🧸 라온이 마중: 우리 가족의 여정")
target_date = datetime.date(2026, 12, 9)
d_day = (target_date - datetime.date.today()).days
c1, c2 = st.columns(2)
with c1: st.metric("✨ 라온이 만나는 날", f"D-{d_day}일")
with c2: st.metric("🤰 현재 임신 주차", "11주 0일차")
st.info("💡 지금 라온이는 방울토마토 🍅 크기에요!")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 일기", "🤰 컨디션", "🏥 병원 검진", "🎒 체크리스트", "📛 이름 투표", "📸 갤러리"])

# 1. 일기장 탭
with tab1:
    st.subheader("📝 일기장")
    t = st.text_input("제목", key="d_t")
    c = st.text_area("내용", key="d_c")
    if st.button("저장", key="d_s"): 
        today_str = datetime.date.today().strftime("%m/%d")
        st.session_state.diaries.append({"t": t, "c": c, "date": today_str})
        st.rerun()
    st.write("---")
    for i, item in enumerate(st.session_state.diaries):
        st.info(f"### 📖 {item['t']} ({item['date']})\n\n{item['c']}")
        if st.button("🗑️ 삭제", key=f"del_d_{i}"): 
            st.session_state.diaries.pop(i); st.rerun()

# 2. 컨디션 탭
with tab2:
    st.subheader("🤰 컨디션 기록")
    stat = st.radio("상태", ["보통 😐", "힘듦 😭", "최상 🌟"], key="c_r")
    msg = st.text_input("메시지", key="c_m")
    if st.button("저장", key="c_s"): 
        today_str = datetime.date.today().strftime("%m/%d")
        st.session_state.conditions.append({"stat": stat, "msg": msg, "date": today_str})
        st.rerun()
    st.write("---")
    for i, item in enumerate(st.session_state.conditions):
        st.warning(f"📅 {item['date']} | {item['stat']} | {item['msg']}")
        if st.button("🗑️ 삭제", key=f"del_c_{i}"): 
            st.session_state.conditions.pop(i); st.rerun()

# 3. 병원 검진 탭
with tab3:
    st.subheader("🏥 병원 검진")
    m = st.selectbox("월 선택", range(1, 13), index=datetime.datetime.now().month - 1)
    cal = calendar.Calendar(firstweekday=6)
    month_cal = cal.monthdayscalendar(2026, m)
    cols = st.columns(7)
    for i, d in enumerate(["일", "월", "화", "수", "목", "금", "토"]): cols[i].markdown(f"**{d}**")
    for week in month_cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day != 0:
                has_event = any(h['d'] == day for h in st.session_state.hospitals)
                label = f"{day} 🏥" if has_event else str(day)
                if cols[i].button(label, key=f"d_{day}"): 
                    st.session_state.selected_day = day; st.rerun()
    st.write(f"📍 선택된 날짜: **{st.session_state.selected_day}일**")
    memo = st.text_input("메모", key="h_m")
    if st.button("추가", key="h_add"): 
        st.session_state.hospitals.append({"d": st.session_state.selected_day, "m": memo}); st.rerun()
    st.write("---")
    for i, h in enumerate(st.session_state.hospitals):
        st.write(f"📅 **{h['d']}일**: {h['m']}")
        if st.button("🗑️ 삭제", key=f"del_h_{i}"): 
            st.session_state.hospitals.pop(i); st.rerun()

# 4. 체크리스트 탭
with tab4:
    st.subheader("🎒 체크리스트")
    new_task = st.text_input("준비물 입력", key="new_task")
    if st.button("추가", key="add_task"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False}); st.rerun()
    st.write("---")
    for i, item in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.8, 0.2])
        with col1: item['done'] = st.checkbox(item['task'], value=item['done'], key=f"chk_{i}")
        with col2:
            if st.button("🗑️", key=f"del_task_{i}"): st.session_state.tasks.pop(i); st.rerun()

# 5. 이름 투표 탭 (CSS 클래스 적용)
with tab5:
    st.subheader("📛 이름 후보")
    n = st.text_input("이름", key="p_n"); m = st.text_input("뜻", key="p_m")
    if st.button("등록", key="p_s"): 
        st.session_state.posts.append({"n": n, "m": m})
        st.rerun()
    st.write("---")
    postit_colors = ["#FFF9C4", "#FFCCBC", "#C8E6C9", "#BBDEFB", "#E1BEE7", "#F8BBD0"]
    for i in range(0, len(st.session_state.posts), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(st.session_state.posts):
                p = st.session_state.posts[idx]
                with cols[j]:
                    st.markdown(f"""
                        <div class="postit-text" style="background-color: {postit_colors[idx%6]}; padding: 15px; border-radius: 2px; box-shadow: 2px 2px 5px rgba(0,0,0,0.15); min-height: 120px; text-align: center; transform: rotate({-1 if idx%2==0 else 1}deg);">
                            <h4 class="postit-text" style="margin:0; font-weight: bold; font-size: 20px;">{p["n"]}</h4>
                            <p class="postit-text" style="margin-top:10px; font-size: 14px; font-weight: bold;">{p["m"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_p_{idx}"): st.session_state.posts.pop(idx); st.rerun()

# 6. 갤러리 탭
with tab6:
    st.subheader("📸 라온이 앨범")
    uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "png", "jpeg"], key="gallery_up")
    if uploaded_file and st.button("앨범에 저장"):
        st.session_state.gallery.append(uploaded_file); st.rerun()
    st.write("---")
    if st.session_state.gallery:
        for i in range(0, len(st.session_state.gallery), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx < len(st.session_state.gallery):
                    with cols[j]:
                        st.markdown('<div style="background-color: white; padding: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 5px;">', unsafe_allow_html=True)
                        st.image(st.session_state.gallery[idx], use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if st.button("🗑️ 삭제", key=f"del_img_{idx}"):
                            st.session_state.gallery.pop(idx); st.rerun()
