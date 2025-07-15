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
# 3. (1~6 슬라이드 기존 내용 생략)
# -----------------------------
# 기존 슬라이드 1~6 코드는 그대로 유지

# -----------------------------
# 4. ✅ 슬라이드 7: IPCC AR6 기반 미래 예측
# -----------------------------
if slide == 7:
    st.header("📈 미래 기온 이상치 예측 (IPCC AR6 기반)")
    st.markdown("""
    **출처**: [IPCC AR6, WGI, Summary for Policymakers (2021)](https://www.ipcc.ch/report/ar6/wg1/)  
    기준: 1850~1900년 평균 대비 전 지구 평균 지표 온도(GSAT) 상승치
    """)
    
    # --- IPCC AR6 예측 데이터프레임 생성 ---
    future_data = {
        "시나리오": ["SSP1-1.9", "SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5"],
        "단기(2021-2040)": [1.5, 1.5, 1.5, 1.5, 1.6],
        "중기(2041-2060)": [1.6, 1.7, 2.0, 2.1, 2.4],
        "장기(2081-2100)": [1.4, 1.8, 2.7, 3.6, 4.4]
    }
    df_future = pd.DataFrame(future_data)

    # --- 시각화를 위해 melt 변환 ---
    df_melt = df_future.melt(id_vars="시나리오", 
                             var_name="기간", 
                             value_name="기온 이상치(°C)")

    # --- Plotly Bar Chart ---
    fig_future = px.bar(
        df_melt, x="시나리오", y="기온 이상치(°C)", color="기간",
        barmode="group",
        title="IPCC AR6 시나리오별 미래 기온 이상치 예측",
        labels={"시나리오": "배출 시나리오", "기온 이상치(°C)": "기온 이상치 (°C)"}
    )
    st.plotly_chart(fig_future, use_container_width=True)

    # --- 요약 메시지 ---
    st.warning("""
    🔹 **배출량 억제(SSP1)** → 1.4~1.8°C 수준에서 안정화 가능  
    🔹 **중간 배출(SSP2-4.5)** → 21세기 말 2.7°C 상승 예상  
    🔹 **고배출(SSP5-8.5)** → 최대 4.4°C 이상 상승 전망 → 극단적 기상현상, 해수면 상승 위험 가중
    """)
