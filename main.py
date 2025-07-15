import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# 1. 데이터 불러오기
# -----------------------------
st.set_page_config(page_title="기온 이상치 데이터 분석", layout="wide")
st.title("🌍 기온 이상치 데이터 분석 (zonann_temps)")

@st.cache_data
def load_data():
    df = pd.read_csv("zonann_temps.csv")
    return df

df = load_data()

st.subheader("📌 데이터 미리보기")
st.dataframe(df.head())

# -----------------------------
# 2. 기본 통계 및 결측치 점검
# -----------------------------
st.subheader("📊 기본 통계 요약")
st.write(df.describe())

st.subheader("❗ 결측치 점검")
missing = df.isnull().sum()
st.write(missing[missing > 0] if missing.sum() > 0 else "✅ 결측치 없음")

# -----------------------------
# 3. 연도별 전 지구 평균 기온 변화 (글로벌 트렌드)
# -----------------------------
st.subheader("🌡️ 연도별 전 지구 평균 기온 이상치 (Glob)")
fig_glob = px.line(df, x="Year", y="Glob",
                   title="연도별 전 지구 기온 이상치 변화",
                   labels={"Year": "연도", "Glob": "기온 이상치(°C)"},
                   markers=True)
st.plotly_chart(fig_glob, use_container_width=True)

# -----------------------------
# 4. 북반구 vs 남반구 비교
# -----------------------------
st.subheader("🌎 북반구 vs 남반구 기온 이상치 비교")
fig_hemi = go.Figure()
fig_hemi.add_trace(go.Scatter(x=df["Year"], y=df["NHem"], mode="lines", name="북반구 (NHem)", line=dict(color="red")))
fig_hemi.add_trace(go.Scatter(x=df["Year"], y=df["SHem"], mode="lines", name="남반구 (SHem)", line=dict(color="blue")))
fig_hemi.update_layout(title="북반구 vs 남반구 기온 이상치 변화", xaxis_title="연도", yaxis_title="기온 이상치(°C)")
st.plotly_chart(fig_hemi, use_container_width=True)

# -----------------------------
# 5. 위도대별 기온 변화 트렌드 선택
# -----------------------------
st.subheader("🗺️ 위도대별 기온 이상치 트렌드")
lat_columns = [col for col in df.columns if col != "Year"]
selected_lats = st.multiselect("위도대를 선택하세요 (여러 개 가능)", lat_columns, default=["64N-90N", "24S-24N", "90S-64S"])

if selected_lats:
    fig_lat = px.line(df, x="Year", y=selected_lats,
                      title="선택한 위도대별 기온 이상치 변화",
                      labels={"value": "기온 이상치(°C)", "variable": "위도대"},
                      markers=True)
    st.plotly_chart(fig_lat, use_container_width=True)

# -----------------------------
# 6. 온난화 속도 분석 (최근 50년 기울기)
# -----------------------------
st.subheader("🔥 최근 50년 온난화 속도 분석")

recent_df = df[df["Year"] >= df["Year"].max() - 50]  # 최근 50년
trend = recent_df[["Year", "Glob"]].copy()
slope = (trend["Glob"].iloc[-1] - trend["Glob"].iloc[0]) / (trend["Year"].iloc[-1] - trend["Year"].iloc[0])
st.write(f"**최근 50년간 전 지구 기온 상승 속도: {slope:.3f} °C/년 → 약 {slope*10:.2f} °C/10년**")

fig_trend = px.scatter(trend, x="Year", y="Glob", trendline="ols",
                       title="최근 50년 전 지구 온난화 추세 (회귀선 포함)",
                       labels={"Glob": "기온 이상치(°C)"})
st.plotly_chart(fig_trend, use_container_width=True)

st.info("✅ 이 앱은 CSV 데이터를 자동으로 분석하며, 필터와 시각화를 제공합니다.")
