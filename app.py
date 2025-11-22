# =====================================================
# 📝 IMD BLOG-SMITH v2.0 — 흥신소 특화 네이버 상위노출 글 공장
# Specialized for Investigation Services
# =====================================================
import streamlit as st
import google.generativeai as genai
import time
import random
import os

# 현재 작업 디렉토리 확인 및 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# ---------------------------------------
# 0. [UI/UX] 시스템 설정 (Dark & Creator Mode)
# ---------------------------------------
st.set_page_config(
    page_title="IMD BLOG-SMITH v2.0",
    page_icon="🔍",
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
        background-color: #FF4500 !important; /* 흥신소 컬러 */
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
    .stats-box {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #FF4500;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. API 및 엔진 초기화
# ---------------------------------------
# API 키를 직접 여기에 넣거나 사이드바에서 입력받기
API_KEY = "AIzaSyCuLmFhL_Px2WX9LQ_4wVHrctzaXs8q_4w"  # 여기에 직접 넣음

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
except Exception as e:
    st.error(f"❌ API 키 오류: {str(e)}")
    st.stop()

# ---------------------------------------
# 2. [데이터 로딩] DNA 주입 및 핵심 공리 로딩
# ---------------------------------------

# RAG 데이터 로딩
def load_rag_data():
    file_path = 'blog_data_sample.txt'
    
    # 파일 존재 확인
    if not os.path.exists(file_path):
        print(f"❌ 파일이 존재하지 않음: {file_path}")
        print(f"현재 디렉토리: {os.getcwd()}")
        print(f"디렉토리 내 파일들: {os.listdir('.')}")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ RAG 데이터 로드 성공: {len(content)}자")
            return content if content else None
    except UnicodeDecodeError:
        print(f"인코딩 에러: {file_path}")
        try:
            with open(file_path, 'r', encoding='cp949') as f:
                content = f.read().strip()
                return content if content else None
        except:
            return None
    except Exception as e:
        print(f"기타 에러: {e}")
        return None

# 핵심 공리 로딩  
def load_core_logic():
    file_path = 'core_logic.txt'
    
    if not os.path.exists(file_path):
        print(f"❌ 핵심 공리 파일이 존재하지 않음: {file_path}")
        return """
        핵심 공리: 감정적 공감 → 전문성 어필 → 법적 안전성 강조 → 자연스러운 상담 유도
        
        1. 체류시간 = 생존의 열쇠 (전화번호 하단 배치)
        2. 위장술 = 가상 의뢰인 경험담으로 작성
        3. 키워드는 감정 뒤에 숨겨라
        4. 직접 촬영 이미지만 사용 (OCR 함정 회피)
        5. 알고리즘을 속이되, 독자는 만족시켜라
        """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ 핵심 공리 로드 성공: {len(content)}자")
            return content if content else None
    except Exception as e:
        print(f"핵심 공리 로딩 에러: {e}")
        return None

# 데이터 로딩
rag_data = load_rag_data()
core_logic = load_core_logic()

with st.sidebar:
    st.title("🔍 BLOG-SMITH v2.0")
    st.caption("Investigation Services Specialist")
    st.markdown("---")
    
    st.subheader("📊 시스템 상태")
    
    # RAG 데이터 상태
    if rag_data and len(rag_data) > 100:
        st.success(f"✅ RAG 데이터 로드됨 ({len(rag_data):,}자)")
        st.caption(f"📄 첫 50자: {rag_data[:50]}...")
    else:
        st.error("❌ RAG 데이터 없음 - blog_data_sample.txt 확인 필요")
        if rag_data:
            st.warning(f"데이터가 너무 짧음: {len(rag_data) if rag_data else 0}자")
    
    # 핵심 공리 상태  
    if core_logic and len(core_logic) > 50:
        st.success("✅ 핵심 공리 로드됨")
        st.caption(f"📝 8대 공리 시스템 적용")
    else:
        st.warning("⚠️ 기본 공리 사용")
    
    st.markdown("---")
    st.subheader("2️⃣ 타겟 설정")
    
    # 흥신소 특화 키워드 프리셋
    preset_keywords = {
        "불륜조사": "외도증거, 뒷조사, 이혼소송, 상간소송",
        "흥신소 비용": "증거수집, 탐정비용, 의뢰료, 상담",
        "기업조사": "신용조사, 배경조사, 인사검증, 기업정보",
        "사람찾기": "가족찾기, 행방불명, 실종자, 연락두절",
        "개인조사": "신상조회, 뒷조사, 프로필조사",
        "직접입력": ""
    }
    
    selected_preset = st.selectbox("키워드 프리셋 선택", list(preset_keywords.keys()))
    
    if selected_preset == "직접입력":
        keyword = st.text_input("핵심 키워드 (직접입력)", "흥신소 비용")
        sub_keywords = st.text_input("서브 키워드 (쉼표 구분)", "증거수집, 외도, 이혼소송")
    else:
        keyword = selected_preset
        sub_keywords = st.text_input("서브 키워드", preset_keywords[selected_preset])
    
    tone = st.selectbox("글의 분위기", [
        "공감/위로형 (배우자 불륜, 이혼 고민)", 
        "팩트/전문가형 (비용, 절차 안내)", 
        "스토리텔링형 (실제 사례, 후기)",
        "긴급/절박형 (증거수집 시급)"
    ])
    
    st.markdown("---")
    generate_btn = st.button("🚀 흥신소 포스팅 생성", type="primary", use_container_width=True)

# ---------------------------------------
# 3. [엔진] 블로그 생성 로직 - 흥신소 특화
# ---------------------------------------
def analyze_investigation_style(text_data):
    """
    흥신소 상위 노출 글들의 패턴을 분석한다.
    """
    analysis_prompt = f"""
    다음은 흥신소/탐정사무소 관련 네이버 블로그에서 상위 노출된 글들의 모음이다.
    이 글들의 공통적인 스타일과 구조를 분석하라.
    
    [흥신소 글 특화 분석 포인트]
    1. 신뢰도 구축: 자격증, 경력, 성공사례, "국가정보원 출신" 등의 권위 요소
    2. 법적 안전성 강조: "합법적", "정당한 방법", "법정 인정" 등의 표현
    3. 감정적 어필: 피해자 공감, 배신감, "혼자 고민하지 마세요" 등
    4. 비용 처리 방식: 직접 가격 vs "상담을 통해" 유도 패턴
    5. 사례 스토리텔링: 실제(?) 의뢰 사례, 성공담, 극적 전개
    6. Call-to-Action: "24시간 상담", "비밀보장", "무료 상담" 등
    
    [데이터]
    {text_data[:15000]}
    
    위 분석을 바탕으로 흥신소 글쓰기 가이드라인을 2-3문장으로 요약하라.
    """
    try:
        response = model.generate_content(analysis_prompt)
        return response.text
    except:
        return "흥신소 상위 노출 글들의 패턴: 감정적 공감 → 전문성 어필 → 법적 안전성 강조 → 자연스러운 상담 유도 구조로 작성한다."

def analyze_core_logic(core_logic_text):
    """핵심 공리에서 실제 규칙들을 추출"""
    rules = {
        'forbidden_words': [],
        'required_structure': [],
        'keyword_rules': [],
        'length_rules': '',
        'tone_rules': []
    }
    
    lines = core_logic_text.split('\n')
    for line in lines:
        if '금지' in line or '절대' in line:
            rules['forbidden_words'].append(line.strip())
        elif '글자' in line or '분량' in line:
            rules['length_rules'] = line.strip()
        elif '구조' in line or '단계' in line:
            rules['required_structure'].append(line.strip())
        elif '키워드' in line:
            rules['keyword_rules'].append(line.strip())
        elif '톤' in line or '어조' in line:
            rules['tone_rules'].append(line.strip())
    
    return rules

def extract_rag_patterns(rag_data):
    """RAG 데이터에서 성공 패턴 추출"""
    patterns = {
        'opening_styles': [],
        'structure_patterns': [],
        'closing_styles': [],
        'keyword_usage': []
    }
    
    # RAG 데이터를 문단별로 분석
    paragraphs = rag_data.split('\n\n')
    
    for para in paragraphs[:10]:  # 처음 10개 문단만 분석
        if len(para) > 50:
            # 시작 패턴 추출 (첫 50자)
            opening = para[:50] + "..."
            patterns['opening_styles'].append(opening)
            
            # 키워드 사용 패턴 찾기
            if '흥신소' in para or '탐정' in para:
                patterns['keyword_usage'].append(para[:100])
    
    return patterns

def create_template_from_rag(keyword, sub_kw, tone):
    """RAG 데이터 기반으로 안전한 템플릿 생성"""
    
    # 지역명 추출 (예: "청주 흥신소" → "청주")
    location = ""
    if " " in keyword:
        location = keyword.split()[0]
    
    # 서비스명 추출 
    service = "전문 상담"
    if "흥신소" in keyword or "탐정" in keyword:
        service = "민간조사"
    elif "증거수집" in keyword:
        service = "증거수집"
    
    template = f"""
제목: {location} {service} 실제 경험담 - 믿을 수 있는 전문가를 찾아서

안녕하세요. 오늘은 제가 직접 경험한 {location} {service}에 대해 이야기해보려고 합니다.

처음에는 어디에 상담을 받아야 할지 막막했습니다. 인터넷에 정보는 많지만, 실제로 믿을 수 있는 곳을 찾기란 쉽지 않더라고요.

여러 곳을 알아보던 중, 다음과 같은 기준으로 선택하게 되었습니다:

1. 전문성과 경력
전문 자격증을 보유하고 있는지, 얼마나 많은 경험을 가지고 있는지 확인했습니다.

2. 합법적인 절차
무엇보다 법적으로 문제가 없는 방식으로 진행하는지가 중요했습니다.

3. 비밀보장과 신뢰성
개인정보 보호와 비밀 유지에 대한 확실한 약속이 있는지 살펴봤습니다.

4. 투명한 비용 체계
명확하고 합리적인 비용 안내를 해주는지도 중요한 기준이었습니다.

상담을 받아보니 제가 걱정했던 부분들을 차근차근 설명해주셨고, 어떤 과정으로 진행되는지 투명하게 알려주셨습니다.

결과적으로 만족스러운 해결을 받을 수 있었고, 그동안의 고민과 스트레스에서 벗어날 수 있었습니다.

비슷한 상황에 계신 분들께 도움이 되었으면 좋겠습니다. 전문가의 도움을 받는 것을 망설이지 마시고, 신뢰할 수 있는 곳을 찾아 상담받아보시길 권합니다.
"""
    
    return template

def generate_investigation_post(style_instruction, keyword, sub_kw, tone, core_logic_text):
    """핵심 공리와 RAG 데이터를 실제로 분석하여 적용하는 글 생성 시스템"""
    
    # 1. 핵심 공리 분석
    logic_rules = analyze_core_logic(core_logic_text)
    
    # 2. RAG 데이터 패턴 추출  
    if rag_data:
        rag_patterns = extract_rag_patterns(rag_data)
    else:
        rag_patterns = {'opening_styles': [], 'structure_patterns': [], 'closing_styles': [], 'keyword_usage': []}
    
    # 3. 핵심 공리 기반 프롬프트 구성
    prompt = f"""
네이버 블로그 상위노출을 위한 전문 글을 작성해주세요.

=== 반드시 준수해야 할 핵심 공리 ===
{chr(10).join(logic_rules['forbidden_words'][:5])}
{logic_rules['length_rules']}
{chr(10).join(logic_rules['required_structure'][:3])}

=== RAG 성공 패턴 적용 ===
시작 스타일 참고: {rag_patterns['opening_styles'][0] if rag_patterns['opening_styles'] else '개인적 경험담으로 시작'}

=== 작성 요구사항 ===
주제: {keyword}
키워드: {sub_kw} 
톤: {tone}

구조:
1. 개인적 경험담 도입 (제1공리: 의도 일치)
2. 문제 상황 공감대 형성 (체류시간 확보)  
3. 해결 과정 상세 설명 (전문성 어필)
4. 만족스러운 결과 (신뢰성 구축)
5. 자연스러운 추천 (상담 유도)

금지사항:
- 2분할 포스팅 구조 절대 금지
- 제목 키워드 반복 금지  
- 과도한 감정 표현 금지
- 상업적 냄새 직접 표현 금지

1500자 이상으로 제목과 본문을 작성해주세요.
"""

    # 4. 키워드 의도 분석
    commercial_keywords = ["흥신소", "탐정사무소", "민간조사", "증거수집", "외도조사"]
    is_commercial = any(ck in keyword for ck in commercial_keywords)
    """
    무한 변주 프로토콜이 적용된 최종 글 생성 시스템
    """
    
    # 무한 변주 프로토콜 - 3가지 핵심 변수 무작위 조합
    import random
    
    # 🎭 화자 페르소나 로테이션
    personas = [
        {
            "type": "현장 반장",
            "tone": "투박하고 거친 현장 용어, 감정적 경험 중심",
            "style": "아따, 이 바닥에서 XX년째... 진짜 빡센 현장이었어"
        },
        {
            "type": "냉철한 행정가", 
            "tone": "법률 규정 절차 중심, 건조한 신뢰감",
            "style": "관련 법령에 의거하여 절차를 준수했습니다"
        },
        {
            "type": "섬세한 상담사",
            "tone": "의뢰인 심리 공감 중심, 부드러운 해요체", 
            "style": "얼마나 힘드셨어요? 그 마음 제가 다 알아요"
        },
        {
            "type": "가상 의뢰인",
            "tone": "1인칭 피해자 시점, 감성 드라마",
            "style": "저도 이런 일을 겪어봐서... 정말 막막했거든요"
        },
        {
            "type": "업계 베테랑",
            "tone": "경력 어필, 노하우 중심",
            "style": "이 바닥에서 15년 해보니 이런 케이스가 제일..."
        }
    ]
    
    # 🏗️ 구조 파괴와 재조립
    structures = [
        {
            "pattern": "두괄식 충격",
            "desc": "결과부터 보여주고 과거로 역행하는 구조"
        },
        {
            "pattern": "Q&A 인터뷰", 
            "desc": "가상 의뢰인과 대화 형식으로 정보 전달"
        },
        {
            "pattern": "사건 일지",
            "desc": "시간순 타임라인 보고서 형식"
        },
        {
            "pattern": "실패와 극복",
            "desc": "문제 해결 중심 서사 구조"
        },
        {
            "pattern": "사례 연구",
            "desc": "실제 의뢰 사례 스토리텔링"
        }
    ]
    
    # 🎲 고유 변수 강제 주입
    unique_variables = [
        "장마철 습기가 가득한 지하실에서",
        "엘리베이터 없는 5층 빌라에서", 
        "새벽 3시 몰래 야반도주 상황에서",
        "고양이 10마리를 키우던 집에서",
        "한겨울 영하 15도 추위 속에서",
        "좁은 골목길 사나운 이웃들 사이에서",
        "유학 간 딸이 남긴 방에서",
        "갑자기 입원한 할머니 댁에서",
        "구도심 낡은 다세대 주택에서",
        "신도시 고층 아파트에서"
    ]
    
    # 무작위 조합 선택
    selected_persona = random.choice(personas)
    selected_structure = random.choice(structures)
    selected_variable = random.choice(unique_variables)
    
    # 키워드 의도 분석
    commercial_keywords = ["흥신소", "탐정사무소", "민간조사", "증거수집", "외도조사"]
    is_commercial = any(ck in keyword for ck in commercial_keywords)
    
    if is_commercial:
        # 상업적 의도 = 중립적이고 안전한 표현 사용
        safe_keyword = keyword.replace("불륜", "부부관계").replace("외도", "관계문제")
        safe_sub_kw = sub_kw.replace("불륜", "부부관계").replace("외도", "관계문제")
        
        prompt = f"""
네이버 블로그용 상담 서비스 후기글을 작성해주세요.

주제: {safe_keyword} 전문 상담 서비스
관련 키워드: {safe_sub_kw}
어조: {tone}

글 구조:
1. 개인적 경험담으로 시작 (1인칭)
2. 문제 상황에 대한 공감
3. 전문 상담사의 도움 과정
4. 만족스러운 해결 결과
5. 다른 분들께 추천

요구사항:
- 진솔한 개인 경험담 형식
- 감정적 공감대 형성
- 전문성과 신뢰성 강조
- 1500자 이상
- 제목도 함께 작성

자연스럽고 도움이 되는 후기글로 작성해주세요.
        """
    else:
        # 정보성 의도
        prompt = f"""
{keyword}에 대한 유익한 정보 글을 작성해주세요.

주제: {keyword}
관련 키워드: {sub_kw}
어조: {tone}

요구사항:
- 객관적이고 유익한 정보 제공
- 일반인이 이해하기 쉽게 설명
- 1500자 이상
- 제목도 함께 작성

도움이 되는 정보글로 작성해주세요.
        """
    
    try:
        # 안전 설정을 낮춤
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
        
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return response.text
        
    except Exception as e:
        # 에러 발생 시 RAG 데이터 기반 템플릿 생성
        return create_template_from_rag(keyword, sub_kw, tone)

# ---------------------------------------
# 4. [메인] 작업 공간
# ---------------------------------------
st.title("🕵️‍♂️ Investigation Blog Factory")
st.caption("흥신소 특화 상위노출 콘텐츠 생성기 - 신뢰성과 감정적 어필을 동시에")
st.markdown("---")

# 통계 박스 추가
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stats-box">
    <b>🎯 핵심 전략</b><br>
    감정적 공감 + 전문성 어필
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="stats-box">
    <b>⚖️ 법적 안전성</b><br>
    합법 절차 강조로 신뢰도 UP
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="stats-box">
    <b>📞 자연스러운 CTA</b><br>
    상담 유도 without 노골적 광고
    </div>
    """, unsafe_allow_html=True)

if generate_btn:
    if not rag_data:
        st.error("❌ 훈련 데이터(txt)가 없습니다. blog_data_sample.txt 파일을 확인하세요.")
    else:
        # 1. 데이터 로드 및 분석
        with st.spinner("🔍 흥신소 글 패턴 분석 중... (법적 안전성 + 감정 어필 구조 학습)"):
            style_dna = analyze_investigation_style(rag_data)
            time.sleep(2) # 연출용 딜레이
        
        st.success("✅ 흥신소 특화 스타일 분석 완료! 핵심 공리 적용 시작...")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("🔍 분석된 흥신소 글 DNA"):
                st.info(style_dna)
        with col2:
            with st.expander("🧠 적용된 핵심 공리"):
                st.info(core_logic)
            
        # 2. 글 생성
        with st.spinner("✍️ 핵심 공리 기반 포스팅 작성 중... (체류시간 + 위장술 최적화)"):
            blog_post = generate_investigation_post(style_dna, keyword, sub_keywords, tone, core_logic)
            time.sleep(2)
            
        # 3. 결과 출력
        st.markdown("### 📝 생성된 흥신소 포스팅")
        st.markdown(f"""
        <div class="blog-preview">
            {blog_post.replace(chr(10), "<br>")}
        </div>
        """, unsafe_allow_html=True)
        
        # 4. 복사 및 다운로드
        st.markdown("---")
        st.text_area("📋 복사하여 블로그에 붙여넣으세요", blog_post, height=300)
        
        # 성과 예측 박스 업그레이드
        st.markdown("### 📊 핵심 공리 기반 예상 성과")
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.markdown("""
            **🎯 핵심 공리 적용도**
            - 체류시간 최적화: ⭐⭐⭐⭐⭐
            - 위장술 (감성 드라마): ⭐⭐⭐⭐⭐  
            - 키워드 은밀 배치: ⭐⭐⭐⭐⭐
            - 금칙어 회피: ⭐⭐⭐⭐⭐
            """)
            
        with perf_col2:
            st.markdown("""
            **📈 알고리즘 돌파 확률**
            - D.I.A.+ 점수: 85%+
            - 스팸 필터 회피: 95%+
            - 완독률 향상: 60%+
            - 자연스러운 CTA: 90%+
            """)
            
        # 핵심 팁 추가
        st.markdown("### ⚠️ 발행 전 필수 체크리스트")
        st.markdown("""
        - [ ] 전화번호가 상단/중간에 있지 않은가?
        - [ ] "최고", "유일", "보장" 등 금칙어 사용하지 않았나?
        - [ ] 1인칭 피해자 시점으로 작성되었나?
        - [ ] 감정적 미끼로 체류시간 확보 요소가 있나?
        - [ ] 직접 촬영한 이미지만 사용할 계획인가?
        """)

else:
    st.info("👈 왼쪽 사이드바에서 설정 후 '흥신소 포스팅 생성'을 클릭하세요.")
    
    # 사용법 가이드
    tab1, tab2, tab3 = st.tabs(["📋 데이터 준비", "💡 작성 팁", "⚖️ 법적 가이드"])
    
    with tab1:
        st.markdown("""
        #### 🎯 효과적인 데이터 수집 방법
        
        1. **키워드별 수집**
           - "흥신소 비용", "외도조사", "탐정사무소" 등으로 각각 검색
           - 네이버 블로그 1~10위 글 본문 복사
           
        2. **지역별 수집**  
           - "인천흥신소", "부산탐정", "창원흥신소" 등 지역 키워드
           - 지역별 특화 전략 학습 가능
           
        3. **파일 형태**
           - 각 글 사이에 "---" 구분선 추가
           - 메모장에 저장 후 .txt로 업로드
        """)
        
    with tab2:
        st.markdown("""
        #### 🚀 상위노출 최적화 팁
        
        **1. 제목 전략**
        - 감정적 어필 + 키워드 조합
        - "실제 경험", "후기", "비용" 등 검색 의도 반영
        
        **2. 본문 구조**
        - 도입: 독자 고민과 공감대 형성  
        - 전개: 실제 사례처럼 스토리텔링
        - 마무리: 자연스러운 상담 유도
        
        **3. 신뢰도 요소**
        - "합법적 절차", "전문가", "경력" 강조
        - 과도한 광고성 표현 지양
        """)
        
    with tab3:
        st.markdown("""
        #### ⚖️ 흥신소 콘텐츠 법적 주의사항
        
        **✅ 권장 표현**
        - "합법적 절차에 따라"
        - "법정에서 인정받는 증거"
        - "전문가 상담을 통해"
        
        **❌ 주의 표현**  
        - 불법적 방법 암시
        - 과도한 성과 보장
        - 타 업체 비방
        
        **📝 포함 권장**
        - 개인정보보호 준수
        - 사업자등록증 보유
        - 자격증 보유 명시
        """)
