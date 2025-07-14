import streamlit as st

# MBTI에 따른 추천 직업 목록
mbti_jobs = {
    "INTJ": ["전략 컨설턴트", "데이터 과학자", "정책 분석가"],
    "INTP": ["연구 과학자", "소프트웨어 엔지니어", "이론 물리학자"],
    "ENTJ": ["경영 컨설턴트", "CEO", "프로젝트 매니저"],
    "ENTP": ["스타트업 창업가", "마케팅 기획자", "기술 혁신가"],
    "INFJ": ["상담사", "작가", "사회 운동가"],
    "INFP": ["예술가", "심리상담사", "소설가"],
    "ENFJ": ["교육자", "HR 매니저", "공공 리더"],
    "ENFP": ["콘텐츠 크리에이터", "기획자", "광고 전문가"],
    "ISTJ": ["회계사", "관리자", "공무원"],
    "ISFJ": ["간호사", "초등 교사", "행정 직원"],
    "ESTJ": ["군 장교", "경영 관리자", "현장 감독"],
    "ESFJ": ["간호 관리자", "상담 교사", "행정 간부"],
    "ISTP": ["기계 엔지니어", "파일럿", "응급 구조사"],
    "ISFP": ["디자이너", "셰프", "플로리스트"],
    "ESTP": ["영업 전문가", "기업 트레이너", "운동 코치"],
    "ESFP": ["MC/방송인", "이벤트 플래너", "배우"]
}

# 웹앱 UI
st.set_page_config(page_title="MBTI 직업 추천기", page_icon="🧠")
st.title("🧠 MBTI 직업 추천기")
st.write("MBTI 성격유형을 선택하면, 어울리는 직업 3가지를 추천해드립니다.")

# 사용자 입력: MBTI 선택
selected_mbti = st.selectbox("당신의 MBTI는 무엇인가요?", sorted(mbti_jobs.keys()))

# 결과 출력
if selected_mbti:
    st.subheader(f"✅ {selected_mbti} 유형에게 어울리는 직업")
    for i, job in enumerate(mbti_jobs[selected_mbti], start=1):
        st.write(f"{i}. {job}")
