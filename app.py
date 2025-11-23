# =====================================================
# 📝 IMD BLOG-SMITH v3.0 — 흥신소 특화 네이버 상위노출 공장 (Chaos Engine 탑재)
# =====================================================
import streamlit as st
import google.generativeai as genai
import time
import random
import os
import re # 정규표현식 추가

# ---------------------------------------
# 0. [UI/UX] 시스템 설정 (Dark & Creator Mode)
# ---------------------------------------
st.set_page_config(
    page_title="IMD BLOG-SMITH v3.0",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링 (사용자 코드 유지 및 정리)
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
# 1. API 및 엔진 초기화 (★보안 강화★)
# ---------------------------------------
try:
    # API 키를 Streamlit Secrets에서 로드 (보안 강화)
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    if not API_KEY:
         raise ValueError("GOOGLE_API_KEY not found in Streamlit Secrets.")
         
    genai.configure(api_key=API_KEY)
    # 성능과 컨텍스트 길이를 고려하여 1.5 Flash 사용
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
except Exception as e:
    st.error(f"❌ 엔진 초기화 실패: {str(e)}. Streamlit Secrets에 GOOGLE_API_KEY를 설정하세요.")
    # 임시 폴백 (개발용): 만약 Secrets 설정이 어렵다면 아래 주석을 해제하고 키를 직접 입력
    # API_KEY = "YOUR_API_KEY_HERE"
    # genai.configure(api_key=API_KEY)
    # model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    st.stop()

# ---------------------------------------
# 2. [데이터 로딩] RAG 데이터 및 핵심 공리 로딩
# ---------------------------------------

def load_text_file(file_path):
    """텍스트 파일을 안전하게 로드 (UTF-8 우선, CP949 폴백)"""
    if not os.path.exists(file_path):
        print(f"❌ 파일 없음: {file_path}")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✅ 파일 로드 성공 ({file_path}): {len(content)}자")
            return content if content else None
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp949') as f:
                content = f.read().strip()
                return content if content else None
        except:
            return None
    except Exception as e:
        print(f"❌ 파일 로드 실패 ({file_path}): {e}")
        return None

def load_and_chunk_rag_data(file_path='blog_data_sample.txt'):
    """RAG 데이터를 로드하고 포스팅 단위로 분할한다."""
    raw_data = load_text_file(file_path)
    if not raw_data:
        return []
    # 구분자(하이픈 3개 이상이 있는 라인)를 기준으로 포스팅 분할 (정규식 사용)
    chunks = re.split(r'\n\s*---+\s*\n', raw_data)
    # 유효한 청크만 필터링 (길이 100자 이상)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip() and len(chunk.strip()) > 100]
    print(f"✅ RAG 데이터 청킹 완료: {len(chunks)}개 포스팅")
    return chunks

# 데이터 로딩 실행
core_logic = load_text_file('core_logic.txt')
rag_chunks = load_and_chunk_rag_data() # RAG 데이터를 청크 단위로 로드

# ---------------------------------------
# 3. [엔진] 무한 변주 프로토콜 (Chaos Engine v3.0)
# ---------------------------------------

def generate_investigation_post_v3(keyword, sub_kw, tone, core_logic_text, rag_chunks):
    """
    [v3.0 핵심] RAG 예제 주입(Few-Shot) + 무한 변주 프로토콜(Randomization)을 결합한 최종 생성기.
    """
    
    # === 1. 무한 변주 프로토콜 (Chaos Engine) ===
    
    # 🎭 화자 페르소나 로테이션
    personas = [
        {"type": "현장 팀장 (15년 경력)", "style": "투박하지만 신뢰감 있는 현장 용어 사용. 경험 중심. '이 바닥에서 15년 구르다 보니 별의별 케이스를 다 봅니다.'"},
        {"type": "냉철한 법률 전문가", "style": "법적 절차와 증거 효력 중심. 건조하고 객관적인 톤. '저희는 합법적인 테두리 안에서만 움직입니다. 증거의 법적 효력이 최우선입니다.'"},
        {"type": "섬세한 상담 실장", "style": "의뢰인의 심리적 고통에 깊이 공감. 부드러운 해요체. '얼마나 힘드셨어요? 그 막막한 마음, 저희가 누구보다 잘 압니다.'"},
        {"type": "가상 의뢰인 (피해자 후기)", "style": "1인칭 시점, 감정에 호소하는 스토리텔링. 후기 형식. '저도 이런 일을 겪게 될 줄은 몰랐습니다. 정말 지푸라기라도 잡는 심정으로...'"},
        {"type": "데이터 분석가 출신 탐정", "style": "통계와 데이터 기반의 신뢰성 강조, 분석적 어조. '지난 5년간의 데이터를 분석해본 결과, 이 패턴은 90% 확률로...'"},
    ]
    
    # 🏗️ 구조 파괴와 재조립
    structures = [
        {"pattern": "두괄식 충격 요법", "desc": "가장 충격적인 결론(성공 사례)을 먼저 제시하고, 과정을 역순으로 설명하는 구조."},
        {"pattern": "Q&A 인터뷰 형식", "desc": "가상의 의뢰인과 전문가가 묻고 답하는 대화 형식으로 정보를 전달."},
        {"pattern": "사건 일지 보고서", "desc": "시간순 타임라인(Day 1, Day 2...)에 따라 사건 해결 과정을 보고하는 형식."},
        {"pattern": "실패 사례 분석 및 극복", "desc": "잘못된 선택(혼자 해결 시도, 타 업체 이용 실패 등)을 먼저 보여주고, 올바른 해결책을 제시하는 구조."},
    ]
    
    # 🎲 고유 변수 강제 주입 (유사문서 회피용)
    unique_variables = [
        "새벽 3시 긴급하게 걸려온 전화 한 통", "아이의 학원 시간표를 보며 느낀 위화감", "남편의 차량 블랙박스에서 발견된 낯선 목소리",
        "주말마다 반복되는 이유 없는 야근", "카드 명세서에 찍힌 낯선 지역의 숙박업소",
        "갑자기 늘어난 휴대폰 잠금 패턴 변경 빈도", "동창회 이후 달라진 배우자의 태도"
    ]
    
    # 무작위 조합 선택
    selected_persona = random.choice(personas)
    selected_structure = random.choice(structures)
    selected_variable = random.choice(unique_variables)

    # === 2. RAG Few-Shot 예제 선택 ===
    num_examples = 3
    if rag_chunks:
        # 무작위로 예시 선택하여 반복성 방지
        selected_examples = random.sample(rag_chunks, min(len(rag_chunks), num_examples))
        rag_injection = ""
        for i, example in enumerate(selected_examples):
            # 길이 제한 (각 예시당 최대 1500자)
            trimmed_example = example[:1500] + ("...(생략)..." if len(example) > 1500 else "")
            rag_injection += f"[성공 사례 예시 {i+1}]\n{trimmed_example}\n--------------------\n"
    else:
        rag_injection = "(성공 사례 데이터 없음 - 기본 스타일 적용)."

    # === 3. 프롬프트 엔지니어링 (The Blueprint) ===
    # [★핵심 수정★] 모든 요소를 통합하여 강력한 단일 프롬프트 구성 (덮어쓰기 오류 해결)

    prompt = f"""
당신은 네이버 블로그 상위 노출(SEO) 전문가이자, 흥신소/탐정 업계의 베테랑 작가입니다. 아래의 [핵심 공리]를 철저히 준수하고, [RAG 성공 사례]의 스타일과 구조를 모방하여, 주어진 [작성 지침]에 따라 블로그 포스팅을 생성해야 합니다.

=== [제 1원칙: 핵심 공리 (Ironclad Rules)] ===
(다음 규칙들은 절대적으로 준수해야 합니다. 이 규칙들을 어기면 포스팅은 실패합니다.)
{core_logic_text}
* [매우 중요] 글 전체 분량은 최소 2000자 이상이어야 합니다. 충분히 길고 상세하게 작성하세요.
* [중요] 제목과 본문에서 키워드 반복을 최소화하고 자연스럽게 녹여내야 합니다.
* [중요] 전화번호나 직접적인 연락처 유도는 글의 최하단에만 배치해야 합니다. (체류 시간 확보)

=== [제 2원칙: RAG 성공 사례 분석 (Few-Shot Context)] ===
(다음은 상위 노출된 글들의 예시입니다. 이 글들의 톤앤매너, 문체, 정보 전달 방식을 학습하고 모방하세요. 내용은 절대 복사하지 마세요. 스타일 학습용으로만 사용하세요.)
<RAG_EXAMPLES>
{rag_injection}
</RAG_EXAMPLES>

=== [제 3원칙: 무한 변주 프로토콜 (Variation Pivot)] ===
(매번 동일한 글이 생성되는 것을 막기 위해, 다음의 '화자'와 '구조' 조합을 반드시 적용하여 작성해야 합니다.)
* **화자 페르소나:** {selected_persona['type']} (스타일 가이드: "{selected_persona['style']}")
* **글 구조 패턴:** {selected_structure['pattern']} (설명: {selected_structure['desc']})
* **고유 상황 변수:** "{selected_variable}" (이 상황을 글의 도입부나 사례에 자연스럽게 녹여낼 것)

=== [작성 미션] ===
* 핵심 키워드: {keyword}
* 서브 키워드: {sub_kw}
* 기본 톤 (참고용): {tone}

=== [실행] ===
위의 3가지 원칙(공리, 성공 사례 분석, 무한 변주)을 모두 적용하여, {keyword}에 대한 블로그 포스팅(제목 포함)을 작성하십시오.
"""

    # === 4. 생성 실행 ===
    try:
        # 안전 설정 완화 (흥신소 특성상 민감 키워드 포함 가능성)
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]
        
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return response.text, selected_persona['type'], selected_structure['pattern'], selected_variable
        
    except Exception as e:
        return f"❌ 생성 실패: {e}\n\n(프롬프트 길이: {len(prompt)}자)", "N/A", "N/A", "N/A"

# ---------------------------------------
# 4. [UI 구성] 사이드바 및 메인 화면
# ---------------------------------------

# 사이드바 구성
with st.sidebar:
    st.title("🔍 BLOG-SMITH v3.0")
    st.caption("Chaos Engine Activated")
    st.markdown("---")
    
    st.subheader("📊 시스템 상태")
    
    # RAG 데이터 상태
    if rag_chunks:
        st.success(f"✅ RAG 데이터 로드됨 ({len(rag_chunks)}개 포스팅)")
    else:
        st.error("❌ RAG 데이터 없음 (blog_data_sample.txt 확인)")
    
    # 핵심 공리 상태   
    if core_logic and len(core_logic) > 50:
        st.success("✅ 핵심 공리 로드됨 (core_logic.txt)")
    else:
        st.error("❌ 핵심 공리 없음 (core_logic.txt 확인)")
    
    st.markdown("---")
    st.subheader("🎯 타겟 설정")
    
    # 흥신소 특화 키워드 프리셋 (기존 유지)
    preset_keywords = {
        "불륜조사": "외도증거, 뒷조사, 이혼소송, 상간소송",
        "흥신소 비용": "증거수집, 탐정비용, 의뢰료, 상담",
        "기업조사": "신용조사, 배경조사, 인사검증, 기업정보",
        "사람찾기": "가족찾기, 행방불명, 실종자, 연락두절",
        "직접입력": ""
    }
    
    selected_preset = st.selectbox("키워드 프리셋 선택", list(preset_keywords.keys()))
    
    if selected_preset == "직접입력":
        keyword = st.text_input("핵심 키워드 (직접입력)", "흥신소 비용")
        sub_keywords = st.text_input("서브 키워드 (쉼표 구분)", "증거수집, 외도, 이혼소송")
    else:
        keyword = selected_preset
        sub_keywords = st.text_input("서브 키워드", preset_keywords[selected_preset])
    
    tone = st.selectbox("글의 분위기 (참고용)", [
        "공감/위로형 (배우자 불륜, 이혼 고민)", 
        "팩트/전문가형 (비용, 절차 안내)", 
        "스토리텔링형 (실제 사례, 후기)",
        "긴급/절박형 (증거수집 시급)"
    ])
    
    st.markdown("---")
    generate_btn = st.button("🚀 포스팅 생성 (Chaos Engine 가동)", type="primary", use_container_width=True)

# ---------------------------------------
# 5. [메인] 작업 공간 및 결과 출력
# ---------------------------------------
st.title("🕵️‍♂️ Investigation Blog Factory v3.0")
st.caption("무한 변주 프로토콜(Chaos Engine) 탑재 - 알고리즘 교란 최적화")
st.markdown("---")

if generate_btn:
    if not rag_chunks or not core_logic:
        st.error("❌ 필수 데이터 파일(RAG 또는 핵심 공리)이 로드되지 않았습니다.")
    else:
        # 글 생성 실행 (RAG 청크를 함수에 전달)
        with st.spinner("🎲 무한 변주 프로토콜 가동 중... (핵심 공리 + RAG 데이터 모방 + 랜덤 변수 조합)"):
            # 함수 호출 시 rag_chunks 전달
            blog_post, used_persona, used_structure, used_variable = generate_investigation_post_v3(
                keyword, sub_keywords, tone, core_logic, rag_chunks
            )
            time.sleep(1) # 연출용
            
        # 결과 출력
        st.success("✅ 포스팅 생성 완료!")

        # 적용된 변주 프로토콜 표시 (★중요★)
        st.subheader("🔄 적용된 무한 변주 프로토콜 (Chaos Engine)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"🎭 화자: {used_persona}")
        with col2:
            st.info(f"🏗️ 구조: {used_structure}")
        with col3:
            st.info(f"🎲 변수: {used_variable[:30]}...")

        st.markdown("### 📝 생성된 포스팅 미리보기")
        # (블로그 미리보기 스타일 적용)
        st.markdown(f"""
        <div class="blog-preview">
            {blog_post.replace(chr(10), "<br>")}
        </div>
        """, unsafe_allow_html=True)
        
        # 복사 및 다운로드
        st.markdown("---")
        st.text_area("📋 복사하여 블로그에 붙여넣으세요", blog_post, height=300)
        
else:
    st.info("👈 왼쪽 사이드바에서 설정 후 '포스팅 생성'을 클릭하세요.")
    st.markdown("""
    ### 💡 v3.0 핵심: 무한 변주 프로토콜 (Chaos Engine)
    시스템이 매번 다른 **화자(페르소나)**, **글 구조**, **고유 상황 변수**를 무작위로 조합하고, RAG 데이터를 **Few-Shot 예제**로 활용하여 생성합니다. 
    이를 통해 핵심 공리를 준수하면서도, 유사문서 문제를 근본적으로 차단합니다.
    """)
