import streamlit as st
import requests
import pandas as pd

# --- 설정 및 초기화 ---
st.set_page_config(page_title="진로/직업 탐색 대시보드", layout="wide")

# 커리어넷 API 정보 (공공데이터포털/커리어넷 제공)
# 실제 사용 시 본인의 API 키를 입력하세요.
# 키 발급처: https://www.career.go.kr/cnet/front/openapi/openApiMain.do
API_KEY = st.sidebar.text_input("커리어넷 API 키를 입력하세요", type="password")
BASE_URL = "https://www.career.go.kr/cnet/openapi/getOpenApi"

def fetch_career_data(svc_type, svc_grp, search_word=""):
    """
    커리어넷 API를 호출하여 데이터를 가져오는 함수
    """
    if not API_KEY:
        st.warning("사이드바에 커리어넷 API 키를 입력해야 데이터 조회가 가능합니다.")
        return []

    params = {
        "apiKey": API_KEY,
        "svcType": svc_type,
        "svcGrp": svc_grp,
        "contentType": "json",
        "searchJobNm": search_word if svc_type == "job" else "",
        "searchNm": search_word if svc_type == "major" else ""
    }
    
    try:
        # timeout을 설정하여 무한 대기를 방지하고 에러를 포착합니다.
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status() # 4xx, 5xx 에러 발생 시 예외 발생
        
        data = response.json()
        content = data.get("dataSearch", {}).get("content", [])
        
        if not content:
            return []
        return content
        
    except requests.exceptions.Timeout:
        st.error("서버 응답 시간이 초과되었습니다. 다시 시도해 주세요.")
        return []
    except requests.exceptions.ConnectionError:
        st.error("네트워크 연결 오류가 발생했습니다. 인터넷 연결을 확인하거나 잠시 후 시도해 주세요.")
        return []
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return []

# --- 사이드바 메뉴 ---
st.sidebar.title("🔍 진로 데이터 탐색기")
menu = st.sidebar.radio("원하는 정보를 선택하세요", ["직업 정보 탐색", "학과 정보 탐색", "진로 상담 사례"])

# --- 메인 화면 ---
st.title("🎓 미래를 설계하는 진로 대시보드")
st.markdown("커리어넷 공공데이터 API를 활용하여 실시간 정보를 제공합니다.")

if not API_KEY:
    st.info("💡 시작하기: 사이드바에서 커리어넷 오픈 API 키를 입력해 주세요. 키가 없다면 커리어넷 홈페이지에서 무료로 발급받을 수 있습니다.")

if menu == "직업 정보 탐색":
    st.header("💼 직업 정보 검색")
    search_q = st.text_input("궁금한 직업명을 입력하세요 (예: 데이터 사이언티스트, 요리사)")
    
    if st.button("검색"):
        with st.spinner('데이터를 불러오는 중...'):
            jobs = fetch_career_data("job", "jobDicList", search_q)
            if jobs:
                for job in jobs:
                    with st.expander(f"📌 {job.get('jobNm')}"):
                        st.write(f"**직업 정의:** {job.get('jobDefinition', '정보 없음')}")
                        st.write(f"**주요 업무:** {job.get('work', '정보 없음')}")
                        st.info(f"📍 관련 역량: {job.get('possibility', '정보 없음')}")
            elif API_KEY:
                st.warning("검색 결과가 없습니다. 다른 키워드로 검색해 보세요.")

elif menu == "학과 정보 탐색":
    st.header("📚 대학 학과 정보")
    search_q = st.text_input("궁금한 학과명을 입력하세요 (예: 컴퓨터공학, 심리학)")
    
    if st.button("검색"):
        with st.spinner('데이터를 불러오는 중...'):
            majors = fetch_career_data("major", "majorDicList", search_q)
            if majors:
                for major in majors:
                    with st.container():
                        st.subheader(f"📖 {major.get('facilName', major.get('majorName'))}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**학과 개요**")
                            st.caption(major.get('summary', '정보 없음'))
                        with col2:
                            st.write("**졸업 후 진로**")
                            st.success(major.get('job', '정보 없음'))
                        st.divider()
            elif API_KEY:
                st.warning("검색 결과가 없습니다. 다른 키워드로 검색해 보세요.")

elif menu == "진로 상담 사례":
    st.header("💬 진로 고민 해결소")
    st.info("다른 학생들의 진로 상담 사례를 통해 팁을 얻어보세요.")
    st.write("상담 데이터 API 서비스 연동 준비 중입니다.")
    
# --- 푸터 ---
st.sidebar.markdown("---")
st.sidebar.caption("Data Source: CareerNet Open API")
st.sidebar.caption("Environment: Streamlit")
