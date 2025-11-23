# =====================================================
# 📝 IMD BLOG-SMITH v3.2 — 흥신소 특화 네이버 상위노출 공장 (Chaos Engine 극대화)
# =====================================================
import streamlit as st
import google.generativeai as genai
import time
import random
import os
import re

# ---------------------------------------
# 0. [UI/UX] 시스템 설정 (Dark & Creator Mode)
# ---------------------------------------
st.set_page_config(
    page_title="IMD BLOG-SMITH v3.2",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링 (기존 유지)
custom_css = """
<style>
    header, footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp {
        background-color: #1E1E1E;
        color: #E0E0E0;
        font-family: 'Noto Sans KR', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #252526;
        border-right: 1px solid #333;
    }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #333;
        color: white;
        border: 1px solid #555;
    }
    button[kind="primary"] {
        background-color: #FF4500 !important;
        color: white !important;
        font-weight: bold;
        border: none;
    }
    .blog-preview {
        background-color: white;
        color: black;
        padding: 30px;
        border-radius: 10px;
        font-family: 'Nanum Gothic', sans-serif;
        line-height: 1.8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. API 및 엔진 초기화 (★보안 강화 및 모델 수정★)
# ---------------------------------------
try:
    # [★수정됨★] API 키는 Streamlit Secrets 사용 (보안 강화)
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    if not API_KEY:
         raise ValueError("GOOGLE_API_KEY not found in Streamlit Secrets.")
    
    genai.configure(api_key=API_KEY)
    # [★수정됨★] 모델명 오류 수정: 'gemini-2.0-flash' -> 'gemini-1.5-flash-latest'
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

except Exception as e:
    st.error(f"❌ 엔진 초기화 실패: {str(e)}. Streamlit Secrets에 GOOGLE_API_KEY를 설정하세요.")
    st.stop()

# ---------------------------------------
# 2. [데이터 로딩] RAG 데이터 및 핵심 공리 로딩
# ---------------------------------------

def load_text_file(file_path):
    """텍스트 파일을 안전하게 로드"""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip() or None
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp949') as f:
                return f.read().strip() or None
        except:
            return None
    except Exception:
        return None

def load_and_chunk_rag_data(file_path='blog_data_sample.txt'):
    """RAG 데이터를 로드하고 포스팅 단위로 분할한다."""
    raw_data = load_text_file(file_path)
    if not raw_data:
        return []
    # 구분자(하이픈 3개 이상)를 기준으로 분할
    chunks = re.split(r'\n\s*---+\s*\n', raw_data)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip() and len(chunk.strip()) > 50]
    return chunks

# 데이터 로딩 실행
core_logic_raw = load_text_file('core_logic.txt')
rag_chunks = load_and_chunk_rag_data()

# ---------------------------------------
# 3. [엔진] 무한 변주 프로토콜 (Chaos Engine v3.2)
# ---------------------------------------

# [★핵심 수정 v3.2★] 핵심 공리 증류 (인지 과부하 방지)
# 방대한 core_logic.txt를 그대로 사용하지 않고, LLM 실행에 필수적인 핵심 규칙만 요약하여 사용.
DISTILLED_LOGIC = """
[네이버 SEO 핵심 공리 (LLM 실행 버전)]
1. [의도 일치 (제1공리)]: 사용자의 검색 의도에 완벽히 부합하는 해결책을 제시하라. 1포스트 1의도 원칙.
2. [위장술/페르소나 (핵심)]: 지정된 '화자 페르소나'를 완벽하게 연기하라. 업체 홍보 톤 절대 금지. 1인칭 경험담/전문가 조언 스타일 선호.
3. [체류 시간 확보]: 도입부에서 강력한 감정적 공감이나 충격적 사실로 후킹. 최소 2000자 이상 깊이 있게 작성.
4. [키워드/맥락 (제2공리)]: 키워드 반복 금지. 제목/본문에 핵심 키워드 3-5회만 자연스럽게 사용.
5. [구조 준수]: 지정된 '글 구조 패턴'을 엄격히 따라야 한다. 2분할 포스팅 절대 금지 (제3공리).
6. [유사 문서 회피 (무한 변주)]: 지정된 '고유 상황 변수'와 '감정선'을 핵심 소재로 활용하여 독창성을 확보하라.
7. [금칙어/YMYL 회피]: "최고", "100% 보장", 불법 암시 단어(도청, 위치추적) 절대 금지. "합법적 절차", "전문가 조력" 강조.
8. [CTA 위치]: 연락처나 상담 유도는 글의 '최하단'에만 은밀하게 배치.
"""

def generate_investigation_post_v3_2(keyword, sub_kw, tone, rag_chunks, temperature, top_p):
    
    # === 1. 무한 변주 프로토콜 (Chaos Engine 강화) ===
    personas = [
        {"type": "현장 팀장 (15년 경력)", "style": "투박하지만 신뢰감 있는 현장 용어 사용. 경험 중심. '이 바닥에서 15년 구르다 보니 별의별 케이스를 다 봅니다.'"},
        {"type": "냉철한 법률 전문가", "style": "법적 절차와 증거 효력 중심. 건조하고 객관적인 톤. '저희는 합법적인 테두리 안에서만 움직입니다.'"},
        {"type": "섬세한 상담 실장", "style": "의뢰인의 심리적 고통에 깊이 공감. 부드러운 해요체. '얼마나 힘드셨어요? 그 막막한 마음 압니다.'"},
        {"type": "가상 의뢰인 (피해자 후기)", "style": "1인칭 시점, 감정에 호소하는 스토리텔링. 후기 형식. '저도 이런 일을 겪게 될 줄은 몰랐습니다.'"},
    ]
    
    structures = [
        {"pattern": "두괄식 충격 요법", "desc": "가장 충격적인 결론을 먼저 제시하고, 과정을 역순으로 설명."},
        {"pattern": "Q&A 인터뷰 형식", "desc": "가상의 의뢰인과 전문가가 묻고 답하는 대화체로 구성."},
        {"pattern": "사건 일지 보고서", "desc": "시간순 타임라인(Day 1, Day 2...)에 따라 사건 해결 과정을 보고."},
        {"pattern": "실패 사례 분석 및 극복", "desc": "잘못된 대처의 위험성을 경고하고, 전문가의 필요성을 강조."},
    ]

    # [★신설 v3.2★] 감정선 설계 (Emotional Arc)
    emotional_arcs = [
        {"arc": "절망에서 희망으로", "desc": "초반에는 극도의 절망과 불안을 묘사하고, 후반부로 갈수록 해결을 통한 희망과 안정 강조."},
        {"arc": "의심에서 확신으로", "desc": "초반에는 의심과 불확실성을 묘사하고, 증거 확보를 통해 확신과 결단으로 이어지는 과정."},
        {"arc": "분노에서 냉철함으로", "desc": "초반에는 배신감과 분노를 표현하고, 전문가의 조언을 통해 냉철한 대응으로 전환."},
    ]
    
    unique_variables = [
        "새벽 3시 긴급하게 걸려온 전화 한 통", "아이의 학원 시간표를 보며 느낀 위화감", "남편의 차량 블랙박스에서 발견된 낯선 목소리",
        "주말마다 반복되는 이유 없는 야근", "카드 명세서에 찍힌 낯선 지역의 숙박업소"
    ]
    
    # 무작위 조합 선택
    selected_persona = random.choice(personas)
    selected_structure = random.choice(structures)
    selected_variable = random.choice(unique_variables)
    selected_arc = random.choice(emotional_arcs)

    # === 2. RAG Few-Shot 예제 선택 ===
    num_examples = 2 # 예제 수 최적화
    if rag_chunks:
        selected_examples = random.sample(rag_chunks, min(len(rag_chunks), num_examples))
        rag_injection = ""
        for i, example in enumerate(selected_examples):
            trimmed_example = example[:1200] # 길이 제한
            rag_injection += f"--- [성공 사례 스타일 예시 {i+1}] ---\n{trimmed_example}\n"
    else:
        rag_injection = "(성공 사례 데이터 없음)."

    # === 3. 프롬프트 엔지니어링 (The Blueprint v3.2) ===
    # [★핵심★] 무한 변주 프로토콜을 최우선 지침으로 배치하고, 증류된 공리 사용. (덮어쓰기 오류 해결)
    
    prompt = f"""
당신은 네이버 블로그 SEO 전문가이자 흥신소 업계 베테랑 작가입니다. 목표는 상위 노출되면서도 유사문서에 걸리지 않는 고유한 콘텐츠를 생성하는 것입니다. 아래 3가지 원칙을 통합하여 작성하십시오.

=== [제 1원칙: 무한 변주 프로토콜 (Chaos Engine) - ★최우선 적용★] ===
(매우 중요! 이번 글은 반드시 다음 조합으로 작성해야 합니다. 이 조합이 글의 전체 뼈대를 결정합니다.)
* **화자 페르소나:** {selected_persona['type']} (스타일: "{selected_persona['style']}")
* **글 구조 패턴:** {selected_structure['pattern']} (가이드: {selected_structure['desc']})
* **감정선(Emotional Arc):** {selected_arc['arc']} (가이드: {selected_arc['desc']})
* **고유 상황 변수:** "{selected_variable}" (이 상황을 글에 자연스럽게 녹여낼 것)

=== [제 2원칙: 증류된 핵심 공리 (Distilled Rules)] ===
(다음은 블로그 작성의 필수 SEO 규칙입니다. 철저히 준수하세요.)
{DISTILLED_LOGIC}

=== [제 3원칙: RAG 스타일 모방 (Stylistic Few-Shot)] ===
(다음 예시들의 문체, 톤앤매너, 정보 전달 방식을 학습하고 모방하세요. 단, 내용은 절대 복사하지 말고 스타일 학습용으로만 사용하세요.)
<RAG_EXAMPLES>
{rag_injection}
</RAG_EXAMPLES>

=== [작성 미션] ===
* 핵심 키워드: {keyword}
* 서브 키워드: {sub_kw}
* 기본 톤 (참고용): {tone}

=== [실행] ===
위의 3가지 원칙(무한 변주, 핵심 공리, 스타일 모방)을 모두 적용하여, {keyword}에 대한 완전히 새롭고 독창적인 블로그 포스팅(제목 포함)을 작성하십시오. 제 1원칙(무한 변주)을 최우선으로 적용하여 다양성을 확보하고, 분량(2000자 이상)을 반드시 준수하세요.
"""

    # === 4. 생성 실행 ===
    try:
        # [★신설 v3.2★] 생성 설정 (Temperature, Top P 적용)
        generation_config = genai.GenerationConfig(
            temperature=temperature, # 사용자가 설정한 Temperature 값 적용
            top_p=top_p,             # 사용자가 설정한 Top P 값 적용
        )

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]
        
        response = model.generate_content(prompt, generation_config=generation_config, safety_settings=safety_settings)
        return response.text, selected_persona['type'], selected_structure['pattern'], selected_variable, selected_arc['arc']
        
    except Exception as e:
        return f"❌ 생성 실패: {e}\n\n(프롬프트 길이: {len(prompt)}자)", "Error", "Error", "Error", "Error"

# ---------------------------------------
# 4. [UI 구성] 사이드바
# ---------------------------------------
with st.sidebar:
    st.title("🔍 BLOG-SMITH v3.2")
    st.caption("Chaos Engine Maximized")
    st.markdown("---")
    
    # 데이터 상태 확인
    st.subheader("📊 시스템 상태")
    if rag_chunks:
        st.success(f"✅ RAG 데이터: {len(rag_chunks)}개")
    else:
        st.warning("⚠️ RAG 데이터 없음 (blog_data_sample.txt)")
        
    if core_logic_raw:
        st.success("✅ 핵심 공리 (증류됨) 로드됨")
    else:
        st.warning("⚠️ 핵심 공리 없음 (core_logic.txt)")
    
    st.markdown("---")
    
    # 입력 폼 (기존 유지)
    st.subheader("🎯 타겟 설정")
    preset_keywords = {
        "불륜조사": "외도증거, 뒷조사, 이혼소송",
        "흥신소 비용": "탐정비용, 의뢰료, 증거수집",
        "기업조사": "신용조사, 횡령, 산업스파이",
        "사람찾기": "가족찾기, 실종, 연락두절",
        "직접입력": ""
    }
    selected_preset = st.selectbox("키워드 선택", list(preset_keywords.keys()))
    
    if selected_preset == "직접입력":
        keyword = st.text_input("메인 키워드", "흥신소")
        sub_keywords = st.text_input("서브 키워드", "증거, 상담")
    else:
        keyword = selected_preset
        sub_keywords = st.text_input("서브 키워드", preset_keywords[selected_preset])
    
    tone = st.selectbox("글 분위기 (참고용)", ["공감/위로형", "팩트/전문가형", "충격/폭로형", "긴급/절박형"])
    
    # [★신설 v3.2★] 창의성 제어 장치
    st.markdown("---")
    st.subheader("🔥 창의성 제어 (Chaos Control)")
    temperature = st.slider("Temperature (창의성)", min_value=0.6, max_value=1.0, value=0.85, step=0.05, help="높을수록(0.9 이상) 창의적이지만 규칙 준수도가 낮아질 수 있습니다.")
    top_p = st.slider("Top P (어휘 다양성)", min_value=0.8, max_value=1.0, value=0.95, step=0.01, help="높을수록 다양한 어휘와 문장 구조를 사용합니다.")

    st.markdown("---")
    generate_btn = st.button("🚀 포스팅 생성 (Chaos Engine)", type="primary", use_container_width=True)

# ---------------------------------------
# 5. [메인] 작업 공간
# ---------------------------------------
st.title("🕵️‍♂️ Investigation Blog Factory v3.2")
st.caption("인지 과부하 해결 및 무한 변주 프로토콜 극대화")
st.markdown("---")

if generate_btn:
    # [★수정됨★] temperature와 top_p를 함수에 전달
    with st.spinner(f"🎲 Chaos Engine 가동 중... (Temp: {temperature:.2f}, TopP: {top_p:.2f})"):
        blog_post, p_type, s_type, v_type, a_type = generate_investigation_post_v3_2(
            keyword, sub_keywords, tone, rag_chunks, temperature, top_p
        )
        time.sleep(1)
        
    st.success("✅ 생성 완료")
    
    # 변주 정보 표시 (감정선 추가)
    st.subheader("🔄 적용된 무한 변주 프로토콜")
    c1, c2, c3, c4 = st.columns(4)
    c1.info(f"🎭 화자: **{p_type}**")
    c2.info(f"🏗️ 구조: **{s_type}**")
    c3.info(f"📈 감정선: **{a_type}**")
    c4.info(f"🎲 변수: **{v_type[:15]}...**")
    
    st.markdown("### 📝 결과물 미리보기")
    st.markdown(f"""<div class="blog-preview">{blog_post.replace(chr(10), "<br>")}</div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.text_area("📋 복사하기 (Ctrl+C)", blog_post, height=300)

else:
    st.info("👈 왼쪽에서 옵션을 선택하고 '포스팅 생성'을 누르세요.")
    st.markdown("""
    ### 💡 v3.2 핵심 개선 사항: 창의성 폭발
    1. **핵심 공리 증류:** 방대한 규칙(`core_logic.txt`)을 핵심만 요약하여 AI의 인지 부하를 제거했습니다.
    2. **창의성 제어(Temp/Top P):** 사이드바에서 창의성 레벨을 조절하여 글의 다양성을 직접 제어할 수 있습니다.
    3. **카오스 엔진 극대화:** 랜덤 변수(페르소나, 구조, 감정선, 상황)가 최우선으로 작동하도록 프롬프트를 재설계했습니다.
    """)
