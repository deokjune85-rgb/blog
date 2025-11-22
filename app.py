# =====================================================
# 📝 IMD BLOG-SMITH v1.0 — 네이버 상위노출 글 공장
# Authorized by: The Architect
# =====================================================
import streamlit as st
import google.generativeai as genai
import time
import random

# ---------------------------------------
# 0. [UI/UX] 시스템 설정 (Dark & Creator Mode)
# ---------------------------------------
st.set_page_config(
    page_title="IMD BLOG-SMITH",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    header, footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp {
        background-color: #1E1E1E; /* 크리에이터 다크 모드 */
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
        background-color: #00C73C !important; /* 네이버 그린 */
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
    .blog-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. API 및 엔진 초기화
# ---------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("models/gemini-2.5-flash") # 최신 모델 사용
except:
    st.error("❌ API 키 오류. secrets.toml을 확인하라.")
    st.stop()

# ---------------------------------------
# 2. [사이드바] 데이터 주입 및 설정
# ---------------------------------------
with st.sidebar:
    st.title("📝 BLOG-SMITH")
    st.caption("Naver Viral Logic Cloner")
    st.markdown("---")
    
    st.subheader("1️⃣ DNA 주입 (RAG Data)")
    uploaded_file = st.file_uploader("상위노출 글 모음 (.txt)", type=["txt"])
    
    st.markdown("---")
    st.subheader("2️⃣ 타겟 설정")
    keyword = st.text_input("핵심 키워드", "흥신소 비용")
    sub_keywords = st.text_input("서브 키워드 (쉼표 구분)", "증거수집, 외도, 이혼소송")
    tone = st.selectbox("글의 분위기", ["공감/위로형 (이혼/가사)", "팩트/전문가형 (기업조사)", "충격/폭로형 (썰 풀기)"])
    
    st.markdown("---")
    generate_btn = st.button("🚀 블로그 포스팅 생성", type="primary", use_container_width=True)

# ---------------------------------------
# 3. [엔진] 블로그 생성 로직 (The Smith)
# ---------------------------------------
def analyze_style(text_data):
    """
    업로드된 텍스트에서 '상위 노출 패턴'을 분석한다.
    """
    analysis_prompt = f"""
    다음은 네이버 블로그에서 상위 노출된 글들의 모음이다.
    이 글들의 '공통적인 스타일'과 '구조'를 분석하라.
    
    [분석 포인트]
    1. 도입부(Hook): 어떻게 독자의 주의를 끄는가? (예: 질문 던지기, 충격적 통계)
    2. 본문 구조: 문제 제기 -> 공감 -> 해결책 제시 순서인가?
    3. 말투: 친근한가? 전문적인가? 문장 끝맺음(~해요, ~입니다)은 어떤가?
    4. 홍보 방식: 노골적인가? 정보성으로 위장하는가?
    
    [데이터]
    {text_data[:10000]}
    
    분석 결과를 바탕으로 '글쓰기 지침(Instruction)'을 한 문단으로 요약해라.
    """
    try:
        response = model.generate_content(analysis_prompt)
        return response.text
    except:
        return "상위 노출 글들의 패턴을 분석하여, 독자의 체류 시간을 늘리고 공감을 이끌어내는 구조로 작성하라."

def generate_post(style_instruction, keyword, sub_kw, tone):
    """
    분석된 스타일(DNA)을 기반으로 새로운 글을 창조한다.
    """
    prompt = f"""
    너는 대한민국 최고의 '네이버 블로그 마케터'다.
    아래 [스타일 지침]을 완벽하게 모방하여, 지정된 [주제]로 블로그 포스팅을 작성하라.
    
    [스타일 지침]
    {style_instruction}
    
    [작성 조건]
    1. **주제:** {keyword}
    2. **포함해야 할 단어:** {sub_kw}
    3. **분위기:** {tone}
    4. **형식:** - 제목은 클릭을 유도하는 '자극적인' 것으로 3개 제안할 것.
       - 본문은 가독성을 위해 소제목을 나누고, 이모지(😊, 😢, ✅)를 적절히 사용할 것.
       - 문단 사이에는 [이미지 삽입 위치: 우울한 여성이 창밖을 보는 사진] 처럼 이미지 가이드를 넣을 것.
       - 절대 'AI가 쓴 티'를 내지 말 것. 마치 '옆집 언니'나 '친한 형'이 조언하듯이 자연스럽게.
       - **중요:** 글의 마지막에는 자연스럽게 상담이나 문의로 유도하는 'Call to Action'을 넣을 것.
       - 서론에서 독자의 고통(Pain Point)을 건드려 공감대를 형성할 것.
    
    [출력 시작]
    """
    response = model.generate_content(prompt)
    return response.text

# ---------------------------------------
# 4. [메인] 작업 공간
# ---------------------------------------
st.title("🛡️ Viral Content Factory")
st.caption("상위 노출의 DNA를 복제하여 승리하는 글을 생산합니다.")
st.markdown("---")

if generate_btn:
    if not uploaded_file:
        st.error("❌ 훈련 데이터(txt)가 없습니다. 상위 노출 글을 긁어오십시오.")
    else:
        # 1. 데이터 로드 및 분석
        with st.spinner("🧬 상위 노출 글 DNA 추출 및 분석 중..."):
            raw_text = uploaded_file.read().decode("utf-8")
            style_dna = analyze_style(raw_text)
            time.sleep(1) # 연출용 딜레이
        
        st.success("✅ 스타일 분석 완료! DNA 복제 시작...")
        with st.expander("🔍 분석된 스타일 DNA 보기"):
            st.info(style_dna)
            
        # 2. 글 생성
        with st.spinner("✍️ 원고 작성 중... (네이버 로직 최적화)"):
            blog_post = generate_post(style_dna, keyword, sub_keywords, tone)
            time.sleep(1)
            
        # 3. 결과 출력 (블로그 미리보기 스타일)
        st.markdown("### 🖨️ 생성된 원고")
        st.markdown(f"""
        <div class="blog-preview">
            {blog_post.replace(chr(10), "<br>")}
        </div>
        """, unsafe_allow_html=True)
        
        # 4. 복사 버튼 (텍스트 에리어로 제공)
        st.markdown("---")
        st.text_area("복사하여 블로그에 붙여넣으세요 (Ctrl+C)", blog_post, height=300)

else:
    st.info("👈 왼쪽 사이드바에 '데이터 파일'을 넣고 '생성'을 누르십시오.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📋 데이터 준비 가이드")
        st.markdown("""
        1. 네이버에 '흥신소', '증거수집' 검색.
        2. 1~5위 블로그 글을 복사.
        3. 메모장에 순서대로 붙여넣고 저장(.txt).
        4. 업로드.
        """)
    with c2:
        st.markdown("#### 💡 팁 (Tip)")
        st.markdown("""
        * **상위 노출의 핵심**은 '체류 시간'입니다.
        * AI가 생성한 글 중간중간에 **본인의 진짜 경험담** 한 줄을 섞으면 무적입니다.
        """)
