import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- 설정 ---
st.set_page_config(page_title="누구나 진로 탐색", layout="wide")

# --- 샘플 데이터 (API 키가 없을 때 보여줄 데이터) ---
SAMPLE_JOBS = [
    {"jobNm": "데이터 사이언티스트", "jobDefinition": "데이터를 수집, 분석하여 유의미한 정보를 추출하는 전문가입니다.", "work": "통계 모델링, 머신러닝 알고리즘 개발", "possibility": "수학적 사고력, 프로그래밍 기술", "salary": 6500, "satisfaction": 85},
    {"jobNm": "화이트해커", "jobDefinition": "정보보안 전문가로서 시스템의 취약점을 찾아 방어 전략을 세웁니다.", "work": "보안 점검, 해킹 방어 시스템 구축", "possibility": "윤리 의식, 창의적 문제해결 능력", "salary": 6000, "satisfaction": 90},
    {"jobNm": "로봇 공학자", "jobDefinition": "로봇의 설계, 제조 및 응용 분야를 연구하는 전문가입니다.", "work": "로봇 제어 시스템 설계, 하드웨어 제작", "possibility": "논리적 사고, 기계공학 지식", "salary": 5800, "satisfaction": 82},
    {"jobNm": "인공지능 전문가", "jobDefinition": "컴퓨터가 인간의 지능적인 행동을 수행할 수 있도록 알고리즘을 연구합니다.", "work": "딥러닝 모델 설계, 자연어 처리 시스템 개발", "possibility": "알고리즘 이해도, 창의력", "salary": 7000, "satisfaction": 88},
    {"jobNm": "웹툰 작가", "jobDefinition": "인터넷 플랫폼을 통해 연재되는 만화를 창작합니다.", "work": "스토리 구상, 캐릭터 디자인, 작화 및 채색", "possibility": "스토리텔링 능력, 드로잉 기술", "salary": 4500, "satisfaction": 95},
    {"jobNm": "게임 개발자", "jobDefinition": "비디오 게임의 기획, 프로그래밍, 그래픽 등을 담당하여 게임을 완성합니다.", "work": "게임 엔진 프로그래밍, 게임 밸런스 기획", "possibility": "협동심, 논리력", "salary": 5500, "satisfaction": 80},
    {"jobNm": "환경 공학자", "jobDefinition": "오염된 환경을 정화하고 환경 보호를 위한 기술을 연구합니다.", "work": "대기 및 수질 오염 측정, 정화 장치 설계", "possibility": "생물학 및 화학 지식, 책임감", "salary": 4800, "satisfaction": 78},
    {"jobNm": "드론 조종사", "jobDefinition": "무인 항공기를 조종하여 촬영, 방제, 수송 등의 업무를 수행합니다.", "work": "드론 기체 점검 및 비행 제어, 촬영 데이터 분석", "possibility": "공간 지각력, 위기 대처 능력", "salary": 4200, "satisfaction": 84},
    {"jobNm": "디지털 포렌식 전문가", "jobDefinition": "범죄 수사에서 디지털 기기에 남은 증거를 수집하고 분석합니다.", "work": "삭제된 파일 복구, 사이버 범죄 증거 분석", "possibility": "법적 지식, 컴퓨터 시스템 이해", "salary": 5200, "satisfaction": 83},
    {"jobNm": "스마트팜 구축가", "jobDefinition": "정보통신기술(ICT)을 농업에 접목하여 지능형 농장을 설계하고 운영합니다.", "work": "농장 자동화 시스템 설치, 재배 환경 데이터 분석", "possibility": "IT 융합 능력, 농업에 대한 관심", "salary": 4600, "satisfaction": 86},
    {"jobNm": "3D 프린팅 전문가", "jobDefinition": "3D 프린터를 활용하여 모델을 설계하고 제품을 출력합니다.", "work": "3D 모델링 설계, 출력물 후처리 및 장비 유지보수", "possibility": "공간 구성 능력, 예술적 감각", "salary": 4300, "satisfaction": 79}
]

SAMPLE_MAJORS = [
    {"majorName": "컴퓨터공학과", "summary": "정보기술 사회의 핵심인 컴퓨터 시스템과 소프트웨어를 연구합니다.", "job": "소프트웨어 개발자, 시스템 엔지니어, 보안 전문가"},
    {"majorName": "심리학과", "summary": "인간의 마음과 행동을 과학적으로 연구하는 학문입니다.", "job": "상담 심리사, 마케팅 전문가, 임상 심리사"},
    {"majorName": "미디어커뮤니케이션학과", "summary": "신문, 방송, 광고 등 미디어 콘텐츠 기획과 제작을 공부합니다.", "job": "PD, 기자, 광고 기획자, 유튜버"},
    {"majorName": "생명공학과", "summary": "생물학적 원리를 공학적으로 응용하여 인류 건강과 환경을 연구합니다.", "job": "제약 연구원, 바이오 공학자, 식품 공학자"},
    {"majorName": "경영학과", "summary": "기업 경영에 필요한 마케팅, 회계, 인사 관리 등을 배웁니다.", "job": "경영 컨설턴트, 마케터, 공인회계사"}
]

# --- 함수: 데이터 가져오기 ---
def get_data(menu_type, keyword=""):
    url = "https://www.career.go.kr/cnet/openapi/getOpenApi"
    params = {
        "apiKey": "guest_mode_no_key",
        "svcType": "job" if menu_type == "직업" else "major",
        "svcGrp": "jobDicList" if menu_type == "직업" else "majorDicList",
        "contentType": "json",
        "searchJobNm": keyword,
        "searchNm": keyword
    }

    try:
        res = requests.get(url, params=params, timeout=2)
        data = res.json().get("dataSearch", {}).get("content", [])
        if data:
            return data
    except:
        pass
    
    if menu_type == "직업":
        return [item for item in SAMPLE_JOBS if keyword in item['jobNm']]
    else:
        return [item for item in SAMPLE_MAJORS if keyword in item['majorName']]

# --- 메인 화면 UI ---
st.title("🎓 청소년 진로 설계 도우미")
st.markdown("API 키 없이도 다양한 직업과 학과 정보를 탐색하고 통계를 확인할 수 있습니다.")

menu = st.sidebar.selectbox("메뉴 선택", ["직업/학과 탐색", "진로 통계 리포트"])

if menu == "직업/학과 탐색":
    tab1, tab2 = st.tabs(["💼 직업 탐색", "📚 학과 탐색"])

    with tab1:
        st.subheader("관심 있는 직업을 검색해 보세요")
        search_job = st.text_input("직업명 입력 (예: 인공지능, 웹툰, 드론)", key="job_input")
        
        if search_job:
            results = get_data("직업", search_job)
            if results:
                for item in results:
                    with st.expander(f"🔍 {item.get('jobNm')}"):
                        st.write(f"**🌟 직업 정의:** {item.get('jobDefinition')}")
                        st.write(f"**🛠 하는 일:** {item.get('work')}")
                        st.info(f"💡 필요 역량: {item.get('possibility')}")
            else:
                st.warning("결과가 없습니다. '추천 키워드'를 참고하세요.")
        else:
            st.write("---")
            st.caption("아래 추천 키워드를 입력해 보세요: 인공지능, 데이터, 웹툰, 환경, 드론 등")

    with tab2:
        st.subheader("진학하고 싶은 학과를 찾아보세요")
        search_major = st.text_input("학과명 입력 (예: 컴퓨터, 심리, 경영)", key="major_input")
        if search_major:
            results = get_data("학과", search_major)
            for item in results:
                st.markdown(f"### 📖 {item.get('majorName')}")
                st.write(f"**학과 개요:** {item.get('summary')}")
                st.success(f"**졸업 후 진로:** {item.get('job')}")
                st.divider()

elif menu == "진로 통계 리포트":
    st.subheader("📊 한눈에 보는 직업 트렌드")
    st.markdown("연봉 수준과 직업 만족도의 관계를 분석한 그래프입니다. (샘플 데이터 기반)")

    # 데이터프레임 생성
    df = pd.DataFrame(SAMPLE_JOBS)
    
    # 버블 차트 생성
    fig = px.scatter(
        df, 
        x="salary", 
        y="satisfaction", 
        size="salary", 
        color="jobNm",
        hover_name="jobNm",
        text="jobNm",
        labels={
            "salary": "평균 연봉 수준 (만원)",
            "satisfaction": "직업 만족도 (%)",
            "jobNm": "직업명"
        },
        title="직업별 연봉 vs 만족도 분포"
    )
    
    fig.update_traces(textposition='top center')
    fig.update_layout(height=600, showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **💡 그래프 해석 가이드:**
    - **오른쪽 상단:** 연봉도 높고 만족도도 높은 직업군입니다. (예: 인공지능 전문가, 데이터 사이언티스트)
    - **왼쪽 상단:** 연봉은 상대적으로 낮을 수 있으나 자아실현이나 재미가 큰 직업군입니다. (예: 웹툰 작가)
    - **원의 크기:** 연봉의 크기를 의미합니다.
    """)

# --- 하단 정보 ---
st.sidebar.divider()
st.sidebar.caption("데이터 출처: 커리어넷 오픈 API 및 교육 통계 샘플")
st.sidebar.write("본 서비스는 교육용으로 제작되었습니다.")
