import streamlit as st
import plotly.graph_objects as go

# 역대 NBA 3점슛 성공 수 Top 10 (2024년 기준 예시 하드코딩)
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

# Streamlit 페이지 설정
st.set_page_config(page_title="NBA 역대 3점슛 TOP 10", page_icon="🏀")
st.title("🏀 NBA 역대 3점슛 성공 수 TOP 10")
st.write("역사상 가장 많은 3점슛을 성공시킨 선수들을 그래프로 확인해보세요!")

# 데이터 정렬
players = list(three_point_all_time.keys())
counts = list(three_point_all_time.values())

# Plotly 그래프 생성
fig = go.Figure(
    data=[
        go.Bar(
            x=counts,
            y=players,
            orientation='h',
            text=counts,
            textposition='outside',
            marker_color='darkorange'
        )
    ]
)

# 그래프 설정
fig.update_layout(
    title="🏀 역대 NBA 3점슛 성공 수 (Top 10)",
    xaxis_title="3점슛 성공 수",
    yaxis_title="선수",
    yaxis=dict(autorange="reversed"),  # 가장 많은 선수가 위에
    height=600,
    template="plotly_white"
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 표 형태로도 출력
st.subheader("📋 상세 목록")
for player, count in three_point_all_time.items():
    st.write(f"🔹 {player}: {count}개")
