import streamlit as st
from datetime import datetime
import textwrap

st.set_page_config(page_title="MBTI 주말 여행 추천", page_icon="🌤️", layout="wide")

MBTI_LIST = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ",
]

RECOMMENDATIONS = {
    "ISTJ": {
        "title": "계획적인 역사 탐방",
        "summary": "사전조사된 역사 유적지 루트 + 미니 체크리스트가 있는 하루 코스",
        "details": [
            "장소: 근교의 사적지 또는 박물관",
            "추천 활동: 가이드 투어, 오디오 가이드 청취, 기념품 샵 방문",
            "이동수단: 기차 + 도보",
            "예상 예산: 보통",
            "함께 하면 좋은 사람: 같은 관심사 친구 1~2명"
        ],
        "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=60"
    },
    "ISFJ": {
        "title": "편안한 온천 & 지역 맛집 투어",
        "summary": "느릿느릿 회복형 주말 — 온천에서 쉬고 현지 식당에서 식사",
        "details": ["장소: 온천 마을 또는 휴양지","추천 활동: 스파, 카페 탐방, 지역 음식 맛보기","이동수단: 자동차 혹은 렌터카","예상 예산: 중간","함께하면 좋은 사람: 가족 또는 친한 친구"],
        "image": "https://images.unsplash.com/photo-1502920917128-1aa500764b5f?auto=format&fit=crop&w=1200&q=60"
    },
    "INFJ": {
        "title": "자연 속 리트릿",
        "summary": "한적한 숲이나 호숫가에서 책과 사색을 즐기는 힐링 주말",
        "details": ["장소: 호숫가 통나무집/글램핑","추천 활동: 독서, 저널 쓰기, 사진 촬영","이동수단: 자동차","예상 예산: 보통","함께하면 좋은 사람: 혼자 혹은 가까운 친구"],
        "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=60"
    },
    "INTJ": {
        "title": "디테일 있는 도시 연구여행",
        "summary": "건축/전시/카페까지 루트를 정해두고 효율적으로 움직이는 주말",
        "details": ["장소: 근교 대도시의 건축/미술 전시","추천 활동: 전시 관람, 건축 포인트 촬영","이동수단: 기차/지하철","예상 예산: 보통~높음","함께하면 좋은 사람: 계획 잘 세우는 사람"],
        "image": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1200&q=60"
    },
    "ISTP": {
        "title": "액티브한 아웃도어 원데이",
        "summary": "서바이벌 감성의 등산/카약/클라이밍 같은 체험형 액티비티",
        "details": ["장소: 근교 산/강","추천 활동: 등산, 카약, 자전거","이동수단: 자동차","예상 예산: 중간","함께하면 좋은 사람: 모험을 즐기는 친구"],
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=60"
    },
    "ISFP": {
        "title": "감성 가득한 사진 산책",
        "summary": "골목골목, 카페, 벽화 앞에서 여유롭게 사진을 찍는 주말",
        "details": ["장소: 예쁜 골목/감성 카페 거리","추천 활동: 사진 촬영, 카페 호핑, 소품샵 방문","이동수단: 대중교통/도보","예상 예산: 낮음~보통","함께하면 좋은 사람: 감성 공유 가능한 친구"],
        "image": "https://images.unsplash.com/photo-1470770903676-69b98201ea1c?auto=format&fit=crop&w=1200&q=60"
    },
    "INFP": {
        "title": "문학-예술 주말",
        "summary": "작은 책방과 독립서점, 갤러리를 돌아다니는 감성 투어",
        "details": ["장소: 예술가의 거리/작은 서점 밀집 지역","추천 활동: 독립서점 방문, 작은 전시 관람, 일기쓰기","이동수단: 대중교통","예상 예산: 낮음","함께하면 좋은 사람: 혼자 혹은 깊은 대화를 나눌 친구"],
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1200&q=60"
    },
    "INTP": {
        "title": "테크-카페 해킹 데이",
        "summary": "좋은 와이파이와 전원, 조용한 카페에서 프로젝트에 몰입하는 1박2일",
        "details": ["장소: 디지털 노마드 친화 카페/코워킹 스페이스","추천 활동: 개인 프로젝트, 작은 워크숍 참여","이동수단: 기차/버스","예상 예산: 낮음~중간","함께하면 좋은 사람: 기억하기 좋은 소수의 친구"],
        "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=60"
    },
    "ESTP": {
        "title": "도심 액션 & 나이트라이프",
        "summary": "하루는 액티브 액티비티, 밤은 클럽/바에서 에너지 발산",
        "details": ["장소: 도심 액티비티 존 + 핫플","추천 활동: 레이싱 체험, 실내서핑, 밤문화 즐기기","이동수단: 택시/대중교통","예상 예산: 중간~높음","함께하면 좋은 사람: 에너지 좋은 친구들"],
        "image": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?auto=format&fit=crop&w=1200&q=60"
    },
    "ESFP": {
        "title": "페스티벌 & 공연 주말",
        "summary": "라이브 음악이나 지역 행사에 뛰어들어 흥겹게 노는 주말",
        "details": ["장소: 페스티벌/라이브하우스","추천 활동: 공연 관람, 길거리 음식 탐방","이동수단: 대중교통/택시","예상 예산: 보통","함께하면 좋은 사람: 큰 무리의 친구들"],
        "image": "https://images.unsplash.com/photo-1508973371-8a5a7f5b4d42?auto=format&fit=crop&w=1200&q=60"
    },
    "ENFP": {
        "title": "즉흥 로드트립",
        "summary": "지도 없이 떠나는 드라이브와 중간중간 만나는 장소들로 채우는 모험",
        "details": ["장소: 국도 드라이브 코스, 작은 마을","추천 활동: 로컬카페, 수공예 마켓, 즉흥 액티비티","이동수단: 자동차","예상 예산: 중간","함께하면 좋은 사람: 즉흥 즐기는 친구"],
        "image": "https://images.unsplash.com/photo-1504215680853-026ed2a45def?auto=format&fit=crop&w=1200&q=60"
    },
    "ENTP": {
        "title": "아이디어 충전 브레인스토밍 데이",
        "summary": "다양한 장소(카페/전시/공원)를 돌아다니며 아이디어를 잇는 활동",
        "details": ["장소: 핫스팟 카페 + 미니 전시","추천 활동: 즉석 토론, 팝업 이벤트 참여","이동수단: 대중교통","예상 예산: 낮음~중간","함께하면 좋은 사람: 호기심 많은 친구"],
        "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=60"
    },
    "ESTJ": {
        "title": "일사불란한 일정관광",
        "summary": "시간표를 짜서 핵심 명소를 빠르게 돌며 효율적으로 즐기는 주말",
        "details": ["장소: 인기 관광지 루트","추천 활동: 가이드 투어, 예약식당 방문","이동수단: 투어버스/렌터카","예상 예산: 보통~높음","함께하면 좋은 사람: 계획된 활동을 좋아하는 그룹"],
        "image": "https://images.unsplash.com/photo-1505765057842-7902f5b3b955?auto=format&fit=crop&w=1200&q=60"
    },
    "ESFJ": {
        "title": "사교형 지역 체험",
        "summary": "지역 행사, 시장, 워크숍에서 사람들과 어울리며 즐기는 주말",
        "details": ["장소: 전통시장/지역 축제","추천 활동: 쿠킹 클래스, 마켓 탐방","이동수단: 대중교통","예상 예산: 낮음~보통","함께하면 좋은 사람: 큰 친구 그룹/가족"],
        "image": "https://images.unsplash.com/photo-1512058564366-c9e3df0a7d2b?auto=format&fit=crop&w=1200&q=60"
    },
    "ENFJ": {
        "title": "감성 가득한 플래너",
        "summary": "모임을 기획해 사람들을 모아 즐거운 주말을 만드는 일정",
        "details": ["장소: 예쁜 카페 + 공원 피크닉","추천 활동: 소규모 파티, 사진 촬영","이동수단: 자동차/대중교통","예상 예산: 중간","함께하면 좋은 사람: 다양한 친구들"],
        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1200&q=60"
    },
    "ENTJ": {
        "title": "목표지향형 액티브 플랜",
        "summary": "짧은 시간에 많은 것을 이루는 효율적 주말 — 마라톤, 박람회, 네트워킹",
        "details": ["장소: 이벤트/컨퍼런스, 스포츠 행사","추천 활동: 대회 참여, 네트워킹","이동수단: 자동차/기차","예상 예산: 중간~높음","함께하면 좋은 사람: 목표 지향 친구"],
        "image": "https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d?auto=format&fit=crop&w=1200&q=60"
    }
}


def get_recommendation(mbti: str):
    return RECOMMENDATIONS.get(mbti, None)

# --- UI ---
st.title("🌤️ MBTI별 맞춤 주말 여행 추천")
st.write("MBTI 유형을 선택하면 그 유형에 딱 맞는 주말 여행 스타일과 실용적인 팁, 이미지까지 보여줍니다.\nStreamlit Cloud에서 바로 실행 가능합니다.")

col1, col2 = st.columns([1, 2])
with col1:
    mbti = st.selectbox("당신의 MBTI를 선택하세요:", MBTI_LIST, index=0)
    agree = st.checkbox("간단한 추천 메모 포함해서 받기", value=True)
    if st.button("추천 받기"):
        rec = get_recommendation(mbti)
        if rec:
            st.success(f"{mbti}에게 추천: {rec['title']}")
        else:
            st.error("추천을 불러오는 데 실패했습니다.")

with col2:
    st.markdown("---")
    st.subheader("오늘의 추천 미리보기")
    rec_preview = get_recommendation(MBTI_LIST[0])
    if rec_preview:
        st.image(rec_preview['image'], use_column_width=True, caption=rec_preview['title'])

st.markdown("---")

# 결과 영역
if 'mbti' in locals():
    rec = get_recommendation(mbti)
    if rec:
        left, right = st.columns([2,3])
        with left:
            st.image(rec['image'], width=420)
            st.markdown(f"### {rec['title']}")
            st.write(rec['summary'])
            if agree:
                st.info("추천 세부사항")
                for d in rec['details']:
                    st.write(f"- {d}")

        with right:
            st.markdown("#### 주말 플랜 일정 예시")
            sample_itinerary = textwrap.dedent(f"""
            {datetime.now().strftime('%Y-%m-%d')} - {mbti} 맞춤 주말 플랜

            09:00 출발
            11:00 현지 도착 & 아침/카페
            13:00 핵심 활동 시작
            16:00 여유 시간 (사진/휴식)
            18:00 지역 맛집 저녁
            20:00 귀가
            """)
            st.code(sample_itinerary)

            st.markdown("#### 짐 체크리스트")
            checklist = ["신분증/교통카드","충전기/보조배터리","간편한 간식","편한 신발"]
            for c in checklist:
                st.write(f"- {c}")

            # 다운로드
            download_text = f"{rec['title']}\n\n{rec['summary']}\n\n" + "\n".join(rec['details'])
            st.download_button("일정 텍스트로 다운로드", download_text, file_name=f"{mbti}_weekend_plan.txt")

            st.markdown("---")
            st.markdown("**더 개인화된 일정 만들기**: 메모를 입력해 주세요")
            user_note = st.text_area("메모 (예: 이동수단, 동행자, 예산)")
            if st.button("개인화 일정 생성"):
                personalized = sample_itinerary + "\n추가 메모:\n" + (user_note or "없음")
                st.success("개인화 일정이 만들어졌습니다 — 아래에서 다운로드하세요")
                st.download_button("개인화 일정 다운로드", personalized, file_name=f"{mbti}_personalized_itinerary.txt")

st.markdown("---")
st.caption("이미지 출처: Unsplash (예시 이미지) — 배포/상업적 사용 시 라이선스를 확인하세요.")

st.sidebar.header("사용 팁")
st.sidebar.write("• Streamlit Cloud에 이 파일(app.py)을 업로드하고 배포하세요.\n• 이미지 URL을 바꾸면 다른 분위기의 이미지를 넣을 수 있습니다.\n• 추천 내용은 샘플이므로, 지역 특성에 맞게 수정해주세요.")

# 끝
