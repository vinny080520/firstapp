import streamlit as st

# 역대 NBA 3점슛 성공 수 Top 10 (하드코딩된 정적 데이터)
three_point_all_time = {
    "Stephen Curry": 3617,
    "Ray Allen": 2973,
    "James Harden": 2945,
    "Reggie Miller": 2560,
    "Kyle Korver": 2450,
    "Klay Thompson": 2390,
    "Damian Lillard": 2337,
    "Vince Carter": 2290,
    "Jason Terry": 2282,
    "Jamal Crawford": 2221
}

# Streamlit 앱 설정
st.set_page_config(page_title="NBA 역대 3점슛 TOP 10", page_icon="🏀")
st.title("🏀 NBA 역대 3점슛 성공 수 TOP 10")
st.write("NBA 역사상 가장 많은 3점슛을 성공시킨 선수들을 확인해보세요!")

# 데이터 출력
st.subheader("📈 선수별 누적 3점슛 성공 수")
st.write("**선수명** | **3점슛 성공 수**")
st.write("---")
for player, count in three_point_all_time.items():
    st.write(f"{player} | {count}")
