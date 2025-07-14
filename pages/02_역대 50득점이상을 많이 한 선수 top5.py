import streamlit as st
import plotly.graph_objects as go

# 하드코딩된 데이터: 역대 50득점 이상 경기 수 Top 5
fifty_point_games = {
    "Wilt Chamberlain": 118,
    "Michael Jordan": 31,
    "Kobe Bryant": 25,
    "James Harden": 23,
    "Elgin Baylor": 17
}

# Streamlit 설정
st.set_page_config(page_title="NBA 50득점 경기 TOP 5", page_icon="🔥")
st.title("🔥 역대 NBA 50득점 이상 경기 수 TOP 5")
st.write("역사상 50득점 이상 경기를 가장 많이 기록한 선수들을 확인해보세요!")

# 데이터 분리
players = list(fifty_point_games.keys())
counts = list(fifty_point_games.values())

# Plotly 그래프 생성
fig = go.Figure(
    data=[
        go.Bar(
            x=counts,
            y=players,
            orientation='h',
            text=counts,
            textposition='outside',
            marker_color='crimson'
        )
    ]
)

# 그래프 설정
fig.update_layout(
    title="🏀 NBA 역대 50득점 경기 수 (Top 5)",
    xaxis_title="50득점 이상 경기 수",
    yaxis_title="선수",
    yaxis=dict(autorange="reversed"),
    template="plotly_white",
    height=500
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 텍스트로도 출력
st.subheader("📋 상세 목록")
for player, count in fifty_point_games.items():
    st.write(f"🔹 {player}: {count}회")
