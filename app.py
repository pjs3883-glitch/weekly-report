import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from io import BytesIO
import datetime
from docx import Document

try:
    from docxcompose.composer import Composer
    HAS_COMPOSE = True
except ImportError:
    HAS_COMPOSE = False

# =====================================================================
# 💡 [사용자 지정 구역] 원하는 부서와 하위 탭을 직접 입력하세요!
# =====================================================================
MY_DEPARTMENTS = {
    "설비기획": ["냉장고기획", "세탁기기획", "공조키친기획"],
    "물류솔루션": ["물류솔루션"], 
    "자동화기술": ["설계", "제작"],
    "설비혁신": ["운영", "설비기술Ⅰ", "설비기술Ⅱ"]
}
# =====================================================================

st.set_page_config(page_title="자동화설비그룹 주간업무 작성 양식", page_icon="🤖", layout="wide")

def add_item_on_enter(state_key, text_key, level_key):
    text = st.session_state[text_key]
    level = st.session_state[level_key]
    if text.strip(): 
        symbol = level.split()[0]
        st.session_state[state_key].append({"symbol": symbol, "text": text})
        st.session_state[text_key] = "" 

# --- 2. 프리미엄 스타일 CSS ---
st.markdown("""
<style>
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
header { visibility: hidden; } 
div[data-testid="stHorizontalBlock"] { align-items: stretch !important; }
div[data-testid="column"] { display: flex; flex-direction: column; }
div[data-testid="column"]:nth-of-type(1) { justify-content: space-between; }
div[data-testid="column"]:nth-of-type(2) > div[data-testid="stVerticalBlock"] { flex-grow: 1; display: flex; flex-direction: column; height: 100%; }
.element-container:has(.preview-box) { flex-grow: 1; display: flex; flex-direction: column; }
.stMarkdown:has(.preview-box) { flex-grow: 1; display: flex; flex-direction: column; }

[data-testid="stAppViewContainer"] { background: radial-gradient(circle at 15% 50%, #1e152e, #0b0c10 70%); color: #e0e0e0; }
[data-testid="stSidebar"] { background: rgba(15, 17, 26, 0.4) !important; backdrop-filter: blur(15px); border-right: 1px solid rgba(255, 255, 255, 0.05); }

.stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: rgba(0, 0, 0, 0.2); padding: 10px; border-radius: 16px; }
.stTabs [data-baseweb="tab"] { background-color: transparent; border-radius: 12px !important; color: #888; padding: 8px 16px; transition: all 0.3s ease; }
.stTabs [aria-selected="true"] { background: linear-gradient(90deg, #6c3add, #4a00e0) !important; color: white !important; box-shadow: 0 4px 15px rgba(108, 58, 221, 0.4); }

.stTabs .stTabs [data-baseweb="tab-list"] { background-color: rgba(255, 255, 255, 0.03); padding: 6px; border-radius: 12px; margin-top: 5px; }
.stTabs .stTabs [data-baseweb="tab"] { font-size: 14px; padding: 6px 12px; }
.stTabs .stTabs [aria-selected="true"] { background: linear-gradient(90deg, #00c6ff, #0072ff) !important; color: white !important; box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3) !important; border: 1px solid rgba(255,255,255,0.1) !important; }

div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 12px !important; color: white !important; }
.stButton > button { background: linear-gradient(90deg, #8a2be2, #4a00e0) !important; color: white !important; border: none !important; border-radius: 14px !important; padding: 10px 24px !important; font-weight: bold !important; box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4) !important; transition: all 0.3s ease !important; }

.preview-box { display: flex; flex-direction: column; flex-grow: 1; height: 100%; background: rgba(25, 26, 40, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 24px; padding: 40px; font-family: 'Malgun Gothic', sans-serif; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
.preview-title { font-size: 26px; font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; background: -webkit-linear-gradient(#fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.item-l1 { font-size: 16px; font-weight: bold; margin-top: 12px; color: #fff; }
.item-l2 { font-size: 15px; margin-left: 20px; margin-top: 6px; color: #ddd; }
.item-l3 { font-size: 14px; margin-left: 40px; margin-top: 4px; color: #aaa; }
.main-title { font-size: 36px; font-weight: bold; margin-bottom: 5px; background: linear-gradient(90deg, #fff, #9d72ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.line { border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; }

.table-container { overflow-x: auto; margin-top: 15px; }
.schedule-table-h { width: 100%; border-collapse: collapse; font-size: 14px; text-align: center; }
.schedule-table-h th, .schedule-table-h td { border: 1px solid rgba(255,255,255,0.2); padding: 12px 6px; white-space: nowrap; }
.schedule-table-h th { background: rgba(255,255,255,0.08); color: #e0e0e0; font-weight: bold; }
.header-col { background: rgba(255,255,255,0.05); font-weight: bold; color: #ccc; }
</style>
""", unsafe_allow_html=True)

for m_dept, s_depts in MY_DEPARTMENTS.items():
    for s_dept in s_depts:
        key_name = f"items_{m_dept}_{s_dept}"
        if key_name not in st.session_state:
            st.session_state[key_name] = []
        inv_key = f"invest_{m_dept}_{s_dept}"
        if inv_key not in st.session_state:
            st.session_state[inv_key] = ""

# --- 4. 왼쪽 사이드바 ---
with st.sidebar:
    st.markdown("<h2 style='color: white;'>💎 Menu</h2>", unsafe_allow_html=True)
    main_menu = st.radio("기능 선택", ["📝 주간업무 작성", "🔗 작성본 합치기"], label_visibility="collapsed")
    
    form_type = "기본 양식"
    if main_menu == "📝 주간업무 작성":
        st.markdown("<div style='margin-top: 15px; margin-bottom: 5px; color: #888; font-size: 14px;'>📄 세부 양식 선택</div>", unsafe_allow_html=True)
        form_type = st.radio("세부 양식", ["기본 양식", "사진 추가", "투자비 추가"], label_visibility="collapsed")

st.markdown('<div class="main-title">🚀 자동화설비그룹 주간업무 작성 양식</div><div class="line"></div>', unsafe_allow_html=True)


# ==============================================================================
# 1. [주간업무 작성] 모드
# ==============================================================================
if main_menu == "📝 주간업무 작성":
    
    show_photo_upload = (form_type == "사진 추가")
    show_invest_input = (form_type == "투자비 추가")
    
    main_tabs = st.tabs(list(MY_DEPARTMENTS.keys()))

    for i, m_dept in enumerate(MY_DEPARTMENTS.keys()):
        with main_tabs[i]:
            sub_depts = MY_DEPARTMENTS[m_dept]
            sub_tabs = st.tabs(sub_depts)
            
            for j, s_dept in enumerate(sub_depts):
                with sub_tabs[j]:
                    display_dept = f"{m_dept} - {s_dept}" if m_dept != s_dept else m_dept
                    state_key = f"items_{m_dept}_{s_dept}"
                    inv_key = f"invest_{m_dept}_{s_dept}"
                    
                    col_input, col_preview = st.columns([1, 1], gap="large")

                    # --- 왼쪽: 입력 구역 ---
                    with col_input:
                        st.markdown("### 📝 항목 추가")
                        level = st.selectbox("수준", ["□ (대항목)", "· (중항목)", "√ (소항목)"], key=f"lvl_{i}_{j}")
                        
                        txt_key = f"txt_{i}_{j}"
                        st.text_input(
                            "내용 (입력 후 엔터↵를 치세요)", 
                            key=txt_key, 
                            on_change=add_item_on_enter, 
                            args=(state_key, txt_key, f"lvl_{i}_{j}")
                        )
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("➕ 추가", key=f"add_{i}_{j}", use_container_width=True):
                                add_item_on_enter(state_key, txt_key, f"lvl_{i}_{j}")
                                st.rerun()
                        with c2:
                            if st.button("🗑️ 삭제", key=f"del_{i}_{j}", use_container_width=True):
                                if st.session_state[state_key]:
                                    st.session_state[state_key].pop()
                                    st.rerun()

                        st.markdown("<div class='line' style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        
                        st.markdown("### 📅 진행 일정")
                        stages = ["검토", "품의", "DR", "제작", "운송", "설치", "안정화"]
                        selected_stages = st.multiselect("진행할 단계를 선택하세요", stages, key=f"ms_{i}_{j}")
                        selected_schedules = []
                        
                        if selected_stages:
                            for stage in selected_stages:
                                sc1, sc2, sc3 = st.columns([1, 2, 2])
                                with sc1:
                                    st.markdown(f"<div style='margin-top:8px;'><b>{stage}</b></div>", unsafe_allow_html=True)
                                with sc2:
                                    s_date = st.date_input("날짜", key=f"d_{i}_{j}_{stage}", label_visibility="collapsed")
                                with sc3:
                                    s_color = st.selectbox("상태", ["⚪ 기본", "🟢 정상", "🟡 지연"], key=f"c_{i}_{j}_{stage}", label_visibility="collapsed")
                                
                                if "🟢" in s_color:
                                    bg_html, bg_word = "#dcfce7", "DCFCE7"
                                elif "🟡" in s_color:
                                    bg_html, bg_word = "#fef08a", "FEF08A"
                                else:
                                    bg_html, bg_word = "transparent", "FFFFFF"
                                
                                selected_schedules.append({
                                    "stage": stage,
                                    "date": f"~{s_date.strftime('%y.%m.%d')}",
                                    "bg_html": bg_html,
                                    "bg_word": bg_word
                                })

                        st.markdown("<div class='line' style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        
                        uploaded_img = None
                        invest_amount = ""
                        
                        if show_photo_upload:
                            uploaded_img = st.file_uploader("📸 사진 첨부", type=['jpg', 'png'], key=f"img_{i}_{j}")
                        
                        if show_invest_input:
                            invest_amount = st.text_input("💰 예상 투자비 (예: 5.5억 원)", key=f"inv_input_{i}_{j}")
                            st.session_state[inv_key] = invest_amount
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        submit_btn = st.button(f"⚡ Report 생성 ({s_dept})", use_container_width=True, key=f"submit_{i}_{j}")

                    # --- 오른쪽: 실시간 프리뷰 ---
                    with col_preview:
                        st.markdown("### 🔍 Live Preview")
                        
                        items_html = ""
                        for item in st.session_state[state_key]:
                            if "□" in item['symbol']: items_html += f"<div class='item-l1'>{item['symbol']} {item['text']}</div>"
                            elif "·" in item['symbol']: items_html += f"<div class='item-l2'>{item['symbol']} {item['text']}</div>"
                            elif "√" in item['symbol']: items_html += f"<div class='item-l3'>{item['symbol']} {item['text']}</div>"

                        if selected_schedules:
                            th_cells, td_cells = "", ""
                            for s in selected_schedules:
                                th_cells += f"<th>{s['stage']}</th>"
                                txt_color = "#e0e0e0" if s['bg_html'] == "transparent" else "#222"
                                td_cells += f"<td style='background-color: {s['bg_html']}; color: {txt_color}; font-weight: bold;'>{s['date']}</td>"
                            schedule_html = f'<div class="table-container"><table class="schedule-table-h"><tr><td class="header-col">구분</td>{th_cells}</tr><tr><td class="header-col">일정</td>{td_cells}</tr></table></div>'
                        else:
                            schedule_html = "<p style='color: rgba(255,255,255,0.3);'>선택된 일정이 없습니다.</p>"

                        # 💡 들여쓰기 문제를 해결한 한 줄 코드 작성 방식
                        bottom_html = "<div style='margin-top: auto;'></div>"
                        if show_photo_upload:
                            img_status = f"<b style='color:#9d72ff;'>📸 {uploaded_img.name} 첨부됨</b>" if uploaded_img else "[ 사진 대기 중 ]"
                            bottom_html = f"<div style='margin-top: auto; border: 1px dashed rgba(255,255,255,0.15); border-radius: 16px; background: rgba(0,0,0,0.2); text-align: center; padding: 30px; color: #888;'>{img_status}</div>"
                        elif show_invest_input:
                            inv_status = st.session_state[inv_key] if st.session_state[inv_key] else "미입력"
                            bottom_html = f"<div style='margin-top: auto; border-radius: 16px; background: rgba(0, 198, 255, 0.1); border: 1px solid rgba(0, 198, 255, 0.3); padding: 25px;'><b style='color:#00c6ff; font-size: 18px;'>💰 총 예상 투자비:</b><span style='color:white; font-size: 18px; margin-left: 10px;'>{inv_status}</span></div>"

                        # 💡 마크다운 버그가 없도록 HTML 태그를 플랫하게 유지
                        preview_box = f"""
<div class="preview-box">
<div class="preview-title">{display_dept} 주간업무</div>
<div style="margin-bottom: 20px;"><b style="color:#aaa;">[ 업무 항목 ]</b></div>
<div style="margin-bottom: 30px;">{items_html if items_html else '<p style="color: rgba(255,255,255,0.3);">항목을 추가하면 표시됩니다.</p>'}</div>
<div style="margin-bottom: 10px;"><b style="color:#aaa;">[ 진행 일정 ]</b></div>
<div style="margin-bottom: 20px;">{schedule_html}</div>
{bottom_html}
</div>
                        """
                        st.markdown(preview_box, unsafe_allow_html=True)

                    # --- 문서 생성 로직 ---
                    if submit_btn:
                        if not st.session_state[state_key]:
                            st.warning("⚠️ 작성된 업무 항목이 없습니다.")
                        else:
                            try:
                                doc = DocxTemplate("template.docx")
                                
                                full_content = ""
                                for item in st.session_state[state_key]:
                                    indent = ""
                                    if "·" in item['symbol']: indent = "    "
                                    elif "√" in item['symbol']: indent = "        "
                                    full_content += f"{indent}{item['symbol']} {item['text']}\n"
                                
                                image_obj = InlineImage(doc, uploaded_img, width=Mm(150)) if uploaded_img else None
                                
                                context_data = {
                                    'dept': display_dept, 
                                    'content': full_content, 
                                    'image': image_obj if image_obj else "",
                                    'invest': st.session_state[inv_key]
                                }
                                
                                for idx in range(1, 8):
                                    if idx <= len(selected_schedules):
                                        context_data[f"state{idx}"] = selected_schedules[idx-1]["stage"]
                                        context_data[f"date{idx}"] = selected_schedules[idx-1]["date"]
                                        context_data[f"color{idx}"] = selected_schedules[idx-1]["bg_word"]
                                    else:
                                        context_data[f"state{idx}"] = ""
                                        context_data[f"date{idx}"] = ""
                                        context_data[f"color{idx}"] = "FFFFFF"
                                
                                doc.render(context_data)
                                bio = BytesIO()
                                doc.save(bio)
                                
                                file_suffix = form_type.replace(" ", "")
                                st.success("✅ 보고서가 생성되었습니다.")
                                st.download_button(
                                    label="📥 파일 다운로드", data=bio.getvalue(),
                                    file_name=f"[{display_dept}]_주간업무_{file_suffix}.docx", key=f"dl_{i}_{j}"
                                )
                            except Exception as e:
                                st.error(f"오류: {e}")

# ==============================================================================
# 2. [작성본 합치기] 모드 
# ==============================================================================
elif main_menu == "🔗 작성본 합치기":
    st.markdown("### 🔗 주간업무 통합 (문서 병합)")
    st.info("개별적으로 작성된 주간업무 워드 파일(.docx)들을 업로드하면 하나의 파일로 합쳐줍니다. **(문서 중간이 잘리지 않도록 페이지가 분리됩니다.)**")
    
    uploaded_docs = st.file_uploader("합칠 워드 파일들을 순서대로 업로드하세요", type=['docx'], accept_multiple_files=True)
    
    if st.button("⚡ 문서 합치기", use_container_width=True):
        if not uploaded_docs or len(uploaded_docs) < 2:
            st.warning("⚠️ 최소 2개 이상의 워드 파일을 업로드해 주세요.")
        elif not HAS_COMPOSE:
            st.error("❌ 'docxcompose' 라이브러리가 설치되지 않았습니다. 터미널에 `pip install docxcompose`를 입력하여 설치 후 다시 시도해 주세요.")
        else:
            with st.spinner("문서들을 하나로 취합하는 중입니다..."):
                try:
                    master = Document(uploaded_docs[0])
                    composer = Composer(master)
                    
                    for file in uploaded_docs[1:]:
                        master.add_page_break()
                        doc_next = Document(file)
                        composer.append(doc_next)
                    
                    bio = BytesIO()
                    composer.doc.save(bio)
                    
                    st.success("✅ 문서 병합이 완벽하게 완료되었습니다!")
                    st.download_button(
                        label="📥 통합 주간업무 다운로드",
                        data=bio.getvalue(),
                        file_name=f"통합_주간업무보고서_{datetime.date.today().strftime('%Y%m%d')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    st.balloons()
                except Exception as e:
                    st.error(f"병합 중 오류가 발생했습니다: {e}")