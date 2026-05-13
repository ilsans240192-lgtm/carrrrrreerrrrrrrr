import streamlit as st
import requests
import pandas as pd

# --- 설정 ---
st.set_page_config(page_title="누구나 진로 탐색", layout="wide")

# --- 확장된 샘플 데이터 (API 키가 없을 때 보여줄 데이터) ---
SAMPLE_JOBS = [
    {"jobNm": "데이터 사이언티스트", "jobDefinition": "데이터를 수집, 분석하여 유의미한 정보를 추출하는 전문가입니다.", "work": "통계 모델링, 머신러닝 알고리즘 개발", "possibility": "수학적 사고력, 프로그래밍 기술"},
    {"jobNm": "화이트해커", "jobDefinition": "정보보안 전문가로서 시스템의 취약점을 찾아 방어 전략을 세웁니다.", "work": "보안 점검, 해킹 방어 시스템 구축", "possibility": "윤리 의식, 창의적 문제해결 능력"},
    {"jobNm": "로봇 공학자", "jobDefinition": "로봇의 설계, 제조 및 응용 분야를 연구하는 전문가입니다.", "work": "로봇 제어 시스템 설계, 하드웨어 제작", "possibility": "논리적 사고, 기계공학 지식"},
    {"jobNm": "인공지능 전문가", "jobDefinition": "컴퓨터가 인간의 지능적인 행동을 수행할 수 있도록 알고리즘을 연구합니다.", "work": "딥러닝 모델 설계, 자연어 처리 시스템 개발", "possibility": "알고리즘 이해도, 창의력"},
    {"jobNm": "웹툰 작가", "jobDefinition": "인터넷 플랫폼을 통해 연재되는 만화를 창작합니다.", "work": "스토리 구상, 캐릭터 디자인, 작화 및 채색", "possibility": "스토리텔링 능력, 드로잉 기술"},
    {"jobNm": "게임 개발자", "jobDefinition": "비디오 게임의 기획, 프로그래밍, 그래픽 등을 담당하여 게임을 완성합니다.", "work": "게임 엔진 프로그래밍, 게임 밸런스 기획", "possibility": "협동심, 논리력"},
    {"jobNm": "환경 공학자", "jobDefinition": "오염된 환경을 정화하고 환경 보호를 위한 기술을 연구합니다.", "work": "대기 및 수질 오염 측정, 정화 장치 설계", "possibility": "생물학 및 화학 지식, 책임감"},
    {"jobNm": "드론 조종사", "jobDefinition": "무인 항공기를 조종하여 촬영, 방제, 수송 등의 업무를 수행합니다.", "work": "드론 기체 점검 및 비행 제어, 촬영 데이터 분석", "possibility": "공간 지각력, 위기 대처 능력"},
    {"jobNm": "디지털 포렌식 전문가", "jobDefinition": "범죄 수사에서 디지털 기기에 남은 증거를 수집하고 분석합니다.", "work": "삭제된 파일 복구, 사이버 범죄 증거 분석", "possibility": "법적 지식, 컴퓨터 시스템 이해"},
    {"jobNm": "스마트팜 구축가", "jobDefinition": "정보통신기술(ICT)을 농업에 접목하여 지능형 농장을 설계하고 운영합니다.", "work": "농장 자동화 시스템 설치, 재배 환경 데이터 분석", "possibility": "IT 융합 능력, 농업에 대한 관심"},
    {"jobNm": "3D 프린팅 전문가", "jobDefinition": "3D 프린터를 활용하여 모델을 설계하고 제품을 출력합니다.", "work": "3D 모델링 설계, 출력물 후처리 및 장비 유지보수", "possibility": "공간 구성 능력, 예술적 감각"}
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
        res = requests.get(url, params=params, timeout=3)
        data = res.json().get("dataSearch", {}).get("content", [])
        if data:
            return data
    except:
        pass
    
    # API 호출 실패 시 키워드가 포함된 샘플 데이터 반환
    if menu_type == "직업":
        return [item for item in SAMPLE_JOBS if keyword in item['jobNm']]
    else:
        return [item for item in SAMPLE_MAJORS if keyword in item['majorName']]

# --- UI 레이아웃 ---
st.title("🎓 학생 진로 탐색 대시보드 (오프라인 모드)")
st.info("💡 커리어넷 API 키 없이도 주요 직업과 학과 정보를 탐색할 수 있는 버전입니다.")

tab1, tab2 = st.tabs(["💼 직업 탐색", "📚 학과 탐색"])

with tab1:
    st.subheader("관심 있는 직업을 검색해 보세요")
    search_job = st.text_input("직업명 입력 (예: 인공지능, 웹툰, 드론)", key="job_input")
    
    if search_job:
        results = get_data("직업", search_job)
        if results:
            st.success(f"'{search_job}' 관련 {len(results)}개의 결과가 있습니다.")
            for item in results:
                with st.expander(f"🔍 {item.get('jobNm')}"):
                    st.write(f"**🌟 직업 정의**\n{item.get('jobDefinition', '내용 없음')}")
                    st.write(f"**🛠 하는 일**\n{item.get('work', '내용 없음')}")
                    if item.get('possibility'):
                        st.info(f"💡 필요 역량: {item.get('possibility')}")
        else:
            st.warning("검색 결과가 없습니다. 샘플에 등록된 직업(컴퓨터, 인공지능, 환경 등)을 입력해 보세요.")
    else:
        st.write("---")
        st.write("📊 **탐색 가능한 추천 직업:**")
        cols = st.columns(3)
        for i, job in enumerate(SAMPLE_JOBS[:9]):
            cols[i % 3].button(job['jobNm'], disabled=True)

with tab2:
    st.subheader("진학하고 싶은 학과를 찾아보세요")
    search_major = st.text_input("학과명 입력 (예: 컴퓨터, 심리, 경영)", key="major_input")
    
    if search_major:
        results = get_data("학과", search_major)
        if results:
            for item in results:
                with st.container():
                    st.markdown(f"### 📖 {item.get('majorName')}")
                    st.write(f"**학과 개요:** {item.get('summary')}")
                    st.write(f"**졸업 후 진로:** {item.get('job')}")
                    st.divider()
        else:
            st.warning("샘플 데이터에 없는 학과입니다. (컴퓨터, 심리, 미디어 등 입력 가능)")
    else:
        st.write("💡 학과 검색창에 키워드를 입력하면 정보가 나타납니다.")

# --- 하단 안내 ---
st.sidebar.title("도움말")
st.sidebar.write("이 앱은 커리어넷 API 키가 없어도 작동하도록 설계되었습니다.")
st.sidebar.write("**추천 키워드:**")
st.sidebar.code("데이터, 인공지능, 환경, 드론, 게임, 경영, 심리")

st.divider()
st.caption("© 2024 진로 탐색 프로젝트 - 공공데이터 활용 교육용 도구")
