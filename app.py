# =====================================================
# 📝 IMD BLOG-SMITH v3.0 — 흥신소 특화 네이버 상위노출 공장 (Direct Key Ver.)
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
    page_title="IMD BLOG-SMITH v3.0",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
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
# 1. API 및 엔진 초기화 (★하드코딩 수정★)
# ---------------------------------------
try:
    # [수정됨] secrets.toml 찾지 말고 그냥 여기에 키를 박아버린다.
    # 네놈이 아까 말한 키다. 만약 바뀌었으면 여기만 수정해라.
    API_KEY = "AIzaSyCuLmFhL_Px2WX9LQ_4wVHrctzaXs8q_4w"
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

except Exception as e:
    st.error(f"❌ 엔진 초기화 실패: {str(e)}")
    st.stop()

# ---------------------------------------
# 2. [데이터 로딩] RAG 데이터 및 핵심 공리 로딩
# ---------------------------------------

def load_text_file(file_path):
    """텍스트 파일을 안전하게 로드"""
    if not os.path.exists(file_path):
        # 파일이 없어도 에러 내지 않고 빈 문자열 반환 (유연성 확보)
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else None
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp949') as f:
                content = f.read().strip()
                return content if content else None
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
core_logic = load_text_file('core_logic.txt')
rag_chunks = load_and_chunk_rag_data()

# ---------------------------------------
# 3. [엔진] 무한 변주 프로토콜 (Chaos Engine v3.0)
# ---------------------------------------

def generate_investigation_post_v3(keyword, sub_kw, tone, core_logic_text, rag_chunks):
    
    # === 1. 무한 변주 프로토콜 ===
    personas = [
        {"type": "현장 팀장 (15년 경력)", "style": "투박하지만 신뢰감 있는 현장 용어 사용. 경험 중심."},
        {"type": "냉철한 법률 전문가", "style": "법적 절차와 증거 효력 중심. 건조하고 객관적인 톤."},
        {"type": "섬세한 상담 실장", "style": "의뢰인의 심리적 고통에 깊이 공감. 부드러운 해요체."},
        {"type": "가상 의뢰인 (피해자 후기)", "style": "1인칭 시점, 감정에 호소하는 스토리텔링."},
        {"type": "데이터 분석가 탐정", "style": "통계와 데이터 기반의 신뢰성 강조."},
    ]
    
    structures = [
        {"pattern": "두괄식 충격 요법", "desc": "충격적인 결론 먼저 제시 후 역순 설명."},
        {"pattern": "Q&A 인터뷰 형식", "desc": "가상의 문답 형식."},
        {"pattern": "사건 일지 보고서", "desc": "시간순 타임라인 전개."},
        {"pattern": "실패 사례 극복", "desc": "잘못된 대처 경고 후 해결책 제시."},
    ]
    
    unique_variables = [
        "새벽 3시 긴급 전화", "차량 블랙박스의 낯선 목소리", "주말의 이유 없는 외출",
        "카드 명세서의 낯선 지역", "갑자기 바뀐 휴대폰 비번", "동창회 후 달라진 태도"
    ]
    
    selected_persona = random.choice(personas)
    selected_structure = random.choice(structures)
    selected_variable = random.choice(unique_variables)

    # === 2. RAG Few-Shot 예제 선택 ===
    if rag_chunks:
        selected_examples = random.sample(rag_chunks, min(len(rag_chunks), 2))
        rag_injection = ""
        for i, example in enumerate(selected_examples):
            trimmed = example[:1000]
            rag_injection += f"[참고 예시 {i+1}]\n{trimmed}\n---\n"
    else:
        rag_injection = "(데이터 없음 - 기본 창작 모드)"

    # === 3. 프롬프트 ===
    prompt = f"""
당신은 네이버 블로그 상위 노출 전문가이자 흥신소 베테랑입니다.
아래 지침에 따라 블로그 포스팅을 작성하십시오.

[상황 변수]
- 화자: {selected_persona['type']} ({selected_persona['style']})
- 구조: {selected_structure['pattern']}
- 소재: {selected_variable}

[핵심 공리 (반드시 준수)]
{core_logic_text if core_logic_text else "기본 원칙: 공감 형성 -> 위기 고조 -> 전문가적 해결 제시 -> 은밀한 홍보"}

[참고 스타일 (RAG)]
{rag_injection}

[작성 미션]
- 키워드: {keyword}
- 서브키워드: {sub_kw}
- 톤: {tone}
- 분량: 공백 포함 2000자 이상 권장
- 주의: 연락처는 맨 마지막에만 배치.

[출력 시작]
"""

    try:
        response = model.generate_content(prompt)
        return response.text, selected_persona['type'], selected_structure['pattern'], selected_variable
    except Exception as e:
        return f"❌ 생성 실패: {e}", "Error", "Error", "Error"

# ---------------------------------------
# 4. [UI 구성] 사이드바
# ---------------------------------------
with st.sidebar:
    st.title("🔍 BLOG-SMITH v3.0")
    st.caption("Chaos Engine Activated")
    st.markdown("---")
    
    # 데이터 상태 확인
    st.subheader("📊 데이터 상태")
    if rag_chunks:
        st.success(f"✅ RAG 데이터: {len(rag_chunks)}개")
    else:
        st.warning("⚠️ RAG 데이터 없음 (blog_data_sample.txt)")
        
    if core_logic:
        st.success("✅ 핵심 공리 로드됨")
    else:
        st.warning("⚠️ 핵심 공리 없음 (core_logic.txt)")
    
    st.markdown("---")
    
    # 입력 폼
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
    
    tone = st.selectbox("글 분위기", ["공감/위로형", "팩트/전문가형", "충격/폭로형", "긴급/절박형"])
    
    st.markdown("---")
    generate_btn = st.button("🚀 포스팅 생성", type="primary", use_container_width=True)

# ---------------------------------------
# 5. [메인] 작업 공간
# ---------------------------------------
st.title("🕵️‍♂️ Investigation Blog Factory")
st.caption("무한 변주 프로토콜(Chaos Engine) 가동 중")
st.markdown("---")

if generate_btn:
    with st.spinner("🎲 알고리즘 교란 및 원고 생성 중..."):
        blog_post, p_type, s_type, v_type = generate_investigation_post_v3(
            keyword, sub_keywords, tone, core_logic, rag_chunks
        )
        time.sleep(1)
        
    st.success("✅ 생성 완료")
    
    # 변주 정보 표시
    c1, c2, c3 = st.columns(3)
    c1.info(f"🎭 **{p_type}**")
    c2.info(f"🏗️ **{s_type}**")
    c3.info(f"🎲 **{v_type}**")
    
    st.markdown("### 📝 결과물")
    st.markdown(f"""<div class="blog-preview">{blog_post.replace(chr(10), "<br>")}</div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.text_area("📋 복사하기 (Ctrl+C)", blog_post, height=300)

else:
    st.info("👈 왼쪽에서 옵션을 선택하고 **'포스팅 생성'**을 누르세요.")
    st.markdown("##### 💡 사용 팁")
    st.markdown("- `blog_data_sample.txt`에 상위노출 글을 긁어 넣으면 스타일이 복제됩니다.")
    st.markdown("- `core_logic.txt`에 나만의 필수 문구를 넣으세요.")
