import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# 1. 페이지 설정 및 데이터 불러오기
# -----------------------------
st.set_page_config(page_title="기온 이상치 발표 슬라이드", layout="wide")
st.title("🌍 지구 온난화: 기온 이상치 발표 자료")

@st.cache_data
def load_data():
    return pd.read_csv("zonann_temps.csv")

df = load_data()

# -----------------------------
# 2. 슬라이드 선택 (1~7)
# -----------------------------
slide = st.slider("슬라이드를 선택하세요", 1, 7, 1)
st.markdown(f"### ▶️ 현재 슬라이드: **{slide}/7**")

# -----------------------------
# 3. 슬라이드별 내용
# -----------------------------

# ✅ 1. 데이터 개요
if slide == 1:
    st.header("✅ 데이터 개요")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("데이터 기간", f"{df['Year'].min()} ~ {df['Year'].max()}")
    with col2:
        st.metric("총 관측 연도", f"{len(df)}년")
    st.caption("출처: NASA GISS Surface Temperature Analysis (GISTEMP)")
    st.success("이 데이터는 전 지구 기온 이상치 변화를 보여줍니다.")

# ✅ 2. 전 지구 평균 기온 이상치 변화
elif slide == 2:
    st.header("🌡️ 전 지구 평균 기온 이상치 변화")
    st.markdown("**지구 기온은 최근 100년 동안 꾸준히 상승하는 추세를 보입니다.**")
    fig_glob = px.line(df, x="Year", y="Glob",
                       title="연도별 전 지구 기온 이상치 변화",
                       labels={"Year": "연도", "Glob": "기온 이상치(°C)"},
                       markers=True)
    st.plotly_chart(fig_glob, use_container_width=True)

# ✅ 3. 북반구 vs 남반구 비교
elif slide == 3:
    st.header("🌎 북반구 vs 남반구 온난화 속도 비교")
    st.markdown("**북반구가 남반구보다 더 빠른 온난화 경향을 보입니다.**")
    fig_hemi = go.Figure()
    fig_hemi.add_trace(go.Scatter(x=df["Year"], y=df["NHem"], mode="lines",
                                  name="북반구 (NHem)", line=dict(color="red")))
    fig_hemi.add_trace(go.Scatter(x=df["Year"], y=df["SHem"], mode="lines",
                                  name="남반구 (SHem)", line=dict(color="blue")))
    fig_hemi.update_layout(title="북반구 vs 남반구 기온 이상치 변화",
                           xaxis_title="연도", yaxis_title="기온 이상치(°C)")
    st.plotly_chart(fig_hemi, use_container_width=True)

# ✅ 4. 위도대별 기온 이상치
elif slide == 4:
    st.header("🗺️ 위도대별 기온 이상치")
    st.markdown("**고위도 지역(북극·남극)에서 온난화가 특히 빠르게 진행됩니다.**")
    lat_columns = [col for col in df.columns if col != "Year"]
    selected_lats = st.multiselect("위도대를 선택하세요 (여러 개 가능)",
                                   lat_columns, default=["64N-90N", "24S-24N", "90S-64S"])
    if selected_lats:
        fig_lat = px.line(df, x="Year", y=selected_lats,
                          title="선택한 위도대별 기온 이상치 변화",
                          labels={"value": "기온 이상치(°C)", "variable": "위도대"},
                          markers=True)
        st.plotly_chart(fig_lat, use_container_width=True)

# ✅ 5. 최근 50년 온난화 속도
elif slide == 5:
    st.header("🔥 최근 50년 온난화 속도")
    recent_df = df[df["Year"] >= df["Year"].max() - 50]
    trend = recent_df[["Year", "Glob"]]
    slope = (trend["Glob"].iloc[-1] - trend["Glob"].iloc[0]) / \
            (trend["Year"].iloc[-1] - trend["Year"].iloc[0])
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("최근 50년 온난화 속도", f"{slope*10:.2f} °C / 10년", delta=f"{slope:.3f} °C / 년")
    with col2:
        st.markdown("**최근 50년간 기온이 지속적으로 상승하며, "
                    "인류 활동이 온난화 가속의 주요 요인으로 지목됩니다.**")
    fig_trend = px.scatter(trend, x="Year", y="Glob", trendline="ols",
                           title="최근 50년 전 지구 온난화 추세 (회귀선 포함)",
                           labels={"Glob": "기온 이상치(°C)"})
    st.plotly_chart(fig_trend, use_container_width=True)

# ✅ 6. (위치 변경됨) 미래 기온 이상치 예측
elif slide == 6:
    st.header("📈 미래 기온 이상치 예측 (IPCC AR6 기반)")
    st.markdown("""
    **출처**: [IPCC AR6, WGI, Summary for Policymakers (2021)](https://www.ipcc.ch/report/ar6/wg1/)  
    기준: 1850~1900년 평균 대비 전 지구 평균 지표 온도(GSAT) 상승치
    """)
    
    future_data = {
        "시나리오": ["SSP1-1.9", "SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5"],
        "단기(2021-2040)": [1.5, 1.5, 1.5, 1.5, 1.6],
        "중기(2041-2060)": [1.6, 1.7, 2.0, 2.1, 2.4],
        "장기(2081-2100)": [1.4, 1.8, 2.7, 3.6, 4.4]
    }
    df_future = pd.DataFrame(future_data)
    df_melt = df_future.melt(id_vars="시나리오", 
                             var_name="기간", 
                             value_name="기온 이상치(°C)")

    fig_future = px.bar(
        df_melt, x="시나리오", y="기온 이상치(°C)", color="기간",
        barmode="group",
        title="IPCC AR6 시나리오별 미래 기온 이상치 예측",
        labels={"시나리오": "배출 시나리오", "기온 이상치(°C)": "기온 이상치 (°C)"}
    )
    st.plotly_chart(fig_future, use_container_width=True)

    st.warning("""
    🔹 **배출량 억제(SSP1)** → 1.4~1.8°C 수준에서 안정화 가능  
    🔹 **중간 배출(SSP2-4.5)** → 21세기 말 2.7°C 상승 예상  
    🔹 **고배출(SSP5-8.5)** → 최대 4.4°C 이상 상승 전망 → 극단적 기상현상, 해수면 상승 위험 가중
    """)

# ✅ 7. (위치 변경됨) 결론 및 시사점
elif slide == 7:
    st.header("🚨 결론 및 시사점")
    st.error("✅ 지구는 뚜렷한 온난화 추세에 있습니다.\n"
             "✅ 북반구·극지방에서 온난화 속도가 특히 빠릅니다.\n"
             "✅ 최근 50년간 온난화 속도가 더욱 가팔라졌습니다.")
    st.success("🌱 **지속 가능한 미래를 위해 온실가스 감축과 기후 대응이 시급합니다.**")
