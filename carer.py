import streamlit as st
import requests
import pandas as pd

# --- 설정 ---
st.set_page_config(page_title="누구나 진로 탐색", layout="wide")

# --- 샘플 데이터 (API 키가 없을 때 보여줄 데이터) ---
SAMPLE_JOBS = [
    {"jobNm": "데이터 사이언티스트", "jobDefinition": "데이터를 수집, 분석하여 유의미한 정보를 추출하는 전문가입니다.", "work": "통계 모델링, 머신러닝 알고리즘 개발", "possibility": "수학적 사고력, 프로그래밍 기술"},
    {"jobNm": "화이트해커", "jobDefinition": "정보보안 전문가로서 시스템의 취약점을 찾아 방어 전략을 세웁니다.", "work": "보안 점검, 해킹 방어 시스템 구축", "possibility": "윤리 의식, 창의적 문제해결 능력"},
    {"jobNm": "로봇 공학자", "jobDefinition": "로봇의 설계, 제조 및 응용 분야를 연구하는 전문가입니다.", "work": "로봇 제어 시스템 설계, 하드웨어 제작", "possibility": "논리적 사고, 기계공학 지식"}
]

# --- 함수: 데이터 가져오기 ---
def get_data(menu_type, keyword=""):
    # 여기서는 테스트용 공용 키 혹은 빈 키를 사용 (일부 API는 키가 없어도 제한적 호출 허용)
    # 실제 운영 시에는 본인의 키를 넣거나 아래 샘플 로직을 유지하세요.
    url = "https://www.career.go.kr/cnet/openapi/getOpenApi"
    params = {
        "apiKey": "guest_mode_no_key", # 임의의 값
        "svcType": "job" if menu_type == "직업" else "major",
        "svcGrp": "jobDicList" if menu_type == "직업" else "majorDicList",
        "contentType": "json",
        "searchJobNm": keyword,
        "searchNm": keyword
    }

    try:
        # 키 없이 호출 시 에러가 날 경우를 대비해 try-except 구성
        res = requests.get(url, params=params, timeout=5)
        data = res.json().get("dataSearch", {}).get("content", [])
        if data:
            return data
    except:
        pass
    
    # API 호출 실패 시 키워드가 포함된 샘플 데이터 반환
    return [item for item in SAMPLE_JOBS if keyword in item['jobNm']] if menu_type == "직업" else []

# --- UI 레이아웃 ---
st.title("🚀 API 키 없이 시작하는 진로 탐색기")
st.info("현재 '게스트 모드'로 작동 중입니다. 일부 검색 결과는 샘플 데이터로 대체될 수 있습니다.")

tab1, tab2 = st.tabs(["💼 직업 탐색", "📚 학과 탐색"])

with tab1:
    search_job = st.text_input("직업명을 입력하세요 (예: 데이터, 로봇)", key="job_input")
    if search_job:
        results = get_data("직업", search_job)
        if results:
            for item in results:
                with st.expander(f"🔍 {item.get('jobNm')}"):
                    st.write(f"**어떤 일을 하나요?**\n{item.get('work', '내용 없음')}")
                    st.write(f"**정의:** {item.get('jobDefinition', '내용 없음')}")
        else:
            st.warning("샘플 데이터에 없는 직업입니다. '데이터'나 '로봇'을 입력해 보세요.")

with tab2:
    st.write("학과 정보는 API 키가 등록된 후 실시간으로 조회가 가능합니다.")
    st.button("실시간 API 키 등록하기 (준비 중)")

# --- 하단 안내 ---
st.divider()
st.caption("공공데이터를 활용한 교육용 프로토타입입니다.")
