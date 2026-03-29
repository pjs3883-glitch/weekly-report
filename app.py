# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# [환경 설정] Streamlit 페이지 레이아웃 최적화
# =====================================================================
st.set_page_config(layout="wide", page_title="자동화설비그룹 주간업무 시스템", page_icon="🚀")

# =====================================================================
# [UI & Logic] 모든 지시사항이 융합된 통합 HTML/JS 엔진
# =====================================================================
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>자동화설비그룹 주간업무 시스템</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        body { background-color: #050510; color: #e2e8f0; font-family: 'Inter', 'Malgun Gothic', sans-serif; overflow-x: hidden; margin: 0; padding: 0; }
        .glass { background: rgba(22, 22, 42, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 1rem; }
        .purple-gradient { background: linear-gradient(135deg, #2a1b52 0%, #16162a 100%); border: 1px solid rgba(139, 92, 246, 0.3); }
        .sidebar-active { background: rgba(79, 70, 229, 0.2); color: #c084fc; font-weight: bold; border-left: 4px solid #8b5cf6; }
        .tab-active { background: #5b21b6 !important; border: 1px solid #8b5cf6 !important; color: white !important; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3); }
        
        input, select { background: #1a1a2e !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; color: white !important; text-align: center; border-radius: 6px; transition: 0.2s; }
        input:focus { border-color: #8b5cf6 !important; outline: none; box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2); }
        
        .editor-input { 
            background: rgba(22, 22, 42, 0.6) !important; 
            border: 1px solid rgba(255, 255, 255, 0.1) !important; 
            padding: 10px; 
            width: 100%; 
            border-radius: 8px;
            text-align: center;
            font-size: 11px;
            color: white;
        }
        .header-editor-input {
            background: #312e81 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            padding: 8px;
            width: 100%;
            border-radius: 6px;
            text-align: center;
            font-size: 11px;
            font-weight: 800;
            color: #c7d2fe;
        }
        .editor-input:focus, .header-editor-input:focus { border-color: #8b5cf6 !important; background: rgba(139, 92, 246, 0.1) !important; }

        .custom-scrollbar::-webkit-scrollbar { width: 5px; height: 5px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 10px; }
        .nowrap { white-space: nowrap !important; }
        .btn-blue { background: #2d2842; border: 1px solid rgba(255,255,255,0.1); transition: 0.2s; }
        .btn-blue:hover { background: #3b3554; border-color: #8b5cf6; }
        .btn-rose { background: rgba(225, 29, 72, 0.1); border: 1px solid rgba(225, 29, 72, 0.2); color: #fda4af; }
        
        .draggable-extra { cursor: grab; user-select: none; position: relative; }
        .draggable-extra:active { cursor: grabbing; }

        /* Delete button on hover */
        .item-container .delete-btn {
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.2s;
        }
        .item-container:hover .delete-btn {
            visibility: visible;
            opacity: 1;
        }
    </style>
</head>
<body>
    <div id="app" class="flex w-full min-h-screen">
        <!-- 1. SIDEBAR -->
        <div class="w-64 border-r border-white/5 flex flex-col p-8 gap-8 shrink-0 shadow-2xl">
            <h2 class="text-white text-xl font-bold text-center flex items-center justify-center gap-2">
                <span class="material-icons text-blue-400">diamond</span> Menu
            </h2>
            <div class="space-y-2">
                <div class="sidebar-item sidebar-active p-3 rounded-xl flex items-center gap-2 cursor-pointer">
                    <span class="material-icons text-sm">description</span> 주간업무 작성
                </div>
                <div class="sidebar-item p-3 rounded-xl flex items-center gap-2 text-gray-500 cursor-pointer hover:bg-white/5">
                    <span class="material-icons text-sm">link</span> 작성본 합치기
                </div>
            </div>
            <div class="mt-4">
                <p class="text-[#818cf8] text-[11px] font-black mb-4 uppercase tracking-widest">📄 세부 양식 선택</p>
                <div class="space-y-3">
                    <label class="flex items-center gap-3 cursor-pointer"><input type="radio" name="fType" value="basic" checked onchange="updateFType('basic')" class="accent-purple-500"> <span class="text-sm text-gray-300">기본 양식</span></label>
                    <label class="flex items-center gap-3 cursor-pointer text-gray-500"><input type="radio" name="fType" value="photo" onchange="updateFType('photo')" class="accent-purple-500"> <span class="text-sm">사진 추가</span></label>
                    <label class="flex items-center gap-3 cursor-pointer text-gray-500"><input type="radio" name="fType" value="invest" onchange="updateFType('invest')" class="accent-purple-500"> <span class="text-sm">투자비 추가</span></label>
                </div>
            </div>
        </div>

        <!-- 2. MAIN CONTENT -->
        <div class="flex-1 p-10" style="background: radial-gradient(circle at 50% 0%, #1e1b4b, #050510 75%);">
            <div class="max-w-7xl mx-auto space-y-6">
                <h1 class="text-3xl font-black text-[#d8b4fe] text-center mb-8">🚀 자동화설비그룹 주간업무 작성 양식</h1>

                <div id="main-tabs" class="flex justify-center gap-2 bg-black/40 p-1.5 rounded-2xl w-fit mx-auto border border-white/10 shadow-xl"></div>
                <div id="sub-tabs" class="flex justify-center gap-6 text-sm font-bold text-gray-500 mt-2"></div>

                <div class="grid grid-cols-12 gap-8 items-start">
                    <!-- LEFT PANEL -->
                    <div class="col-span-7 space-y-6">
                        <div class="glass p-6 text-center">
                            <h3 class="text-[#d8b4fe] font-bold mb-4 flex items-center justify-center gap-2"><span class="material-icons text-sm">add_circle</span> 항목 추가</h3>
                            <div class="flex gap-2">
                                <select id="item-sym" class="w-40 p-2 text-xs">
                                    <option value="□ (대항)">□ (대항목)</option>
                                    <option value="· (중항)">· (중항목)</option>
                                    <option value="√ (소항)">√ (소항목)</option>
                                    <option value="※ (보완)">※ (추가 보완)</option>
                                </select>
                                <input type="text" id="item-input" placeholder="내용 입력 후 엔터↵" class="flex-1 p-2 text-sm" onkeypress="if(event.key==='Enter') addItem()">
                                <button onclick="deleteLastItem()" class="btn-rose px-5 rounded-lg text-xs font-bold hover:bg-rose-500/20">삭제</button>
                            </div>
                        </div>

                        <h3 class="text-[#38bdf8] font-bold text-center">📅 진행 일정 구성</h3>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="glass p-5 flex flex-col items-center">
                                <p class="text-white font-bold text-sm mb-1">📋 표 자유 편집 (타겟팅 지정)</p>
                                <div class="w-full space-y-3 mt-4">
                                    <div class="space-y-1.5">
                                        <p class="text-gray-400 text-[10px] text-center font-bold">행 (세로) 조절</p>
                                        <select id="sel-row" class="w-full text-xs p-1.5"></select>
                                        <div class="grid grid-cols-3 gap-1.5">
                                            <button onclick="rowAct('up')" class="btn-blue py-1.5 rounded text-[10px] font-bold">위 추가</button>
                                            <button onclick="rowAct('down')" class="btn-blue py-1.5 rounded text-[10px] font-bold">아래 추가</button>
                                            <button onclick="rowAct('del')" class="btn-rose py-1.5 rounded text-[10px] font-bold">행 삭제</button>
                                        </div>
                                    </div>
                                    <div class="space-y-1.5 pt-2 border-t border-white/5">
                                        <p class="text-gray-400 text-[10px] text-center font-bold">열 (가로) 조절</p>
                                        <select id="sel-col" class="w-full text-xs p-1.5"></select>
                                        <div class="grid grid-cols-3 gap-1.5">
                                            <button onclick="colAct('left')" class="btn-blue py-1.5 rounded text-[10px] font-bold">왼쪽 추가</button>
                                            <button onclick="colAct('right')" class="btn-blue py-1.5 rounded text-[10px] font-bold">오른쪽 추가</button>
                                            <button onclick="colAct('del')" class="btn-rose py-1.5 rounded text-[10px] font-bold">열 삭제</button>
                                        </div>
                                    </div>
                                    <div class="flex justify-center pt-2">
                                        <label class="flex items-center gap-2 text-[11px] cursor-pointer font-bold"><input type="checkbox" id="chk-border" checked onchange="refresh()" class="accent-purple-500"> 선 표시/숨김</label>
                                    </div>
                                </div>
                            </div>
                            <div class="glass p-5 flex flex-col items-center">
                                <p class="text-white font-bold text-sm mb-1">🔗 기본 일정 항목 연동</p>
                                <div id="stage-grid" class="grid grid-cols-3 gap-y-2 gap-x-1 w-full text-[10px] mt-4"></div>
                                <div id="stage-config" class="w-full space-y-2 mt-3 pt-3 border-t border-white/5 overflow-y-auto max-h-36 custom-scrollbar"></div>
                            </div>
                        </div>

                        <div class="glass p-5">
                            <p class="text-[#818cf8] text-[11px] mb-3 font-bold text-center sm:text-left">* 아래 표(Data Editor)에서 직접 타이핑하여 내용을 수정할 수도 있습니다.</p>
                            <div class="overflow-x-auto custom-scrollbar rounded-xl bg-[#13111c]/30 p-1">
                                <table id="data-table" class="w-full text-center text-xs border-separate border-spacing-x-1 border-spacing-y-2"></table>
                            </div>
                        </div>
                        <div id="extra-form"></div>
                    </div>

                    <!-- RIGHT PREVIEW PANEL -->
                    <div class="col-span-5 glass p-10 min-h-[750px] flex flex-col shadow-[0_0_50px_rgba(79,70,229,0.15)] items-start">
                        <div class="w-full space-y-8">
                            <h2 id="prev-title" class="text-[#c084fc] font-black text-xl flex items-center gap-2"></h2>
                            
                            <div class="w-full">
                                <p class="text-[#818cf8] text-[10px] font-black uppercase tracking-widest text-left mb-4">[ 업무 항목 ]</p>
                                <div id="prev-items" class="flex flex-col items-start w-full gap-0"></div>
                            </div>

                            <div class="w-full">
                                <p class="text-[#818cf8] text-[10px] font-black uppercase tracking-widest text-left mb-4">[ 진행 일정 ]</p>
                                <div id="prev-table-area" class="w-full overflow-x-auto pb-4 custom-scrollbar"></div>
                            </div>

                            <div id="prev-extra" class="w-full text-left"></div>
                            <div id="saved-blocks" class="w-full mt-auto pt-10 space-y-3"></div>
                        </div>
                    </div>
                </div>

                <div class="flex justify-center gap-4 py-12">
                    <button onclick="saveBlock()" class="px-14 py-4 bg-[#5b21b6] hover:bg-[#4c1d95] text-white font-black rounded-2xl transition-all shadow-2xl flex items-center gap-2">
                        <span class="material-icons">save</span> 블록 임시 저장
                    </button>
                    <button class="px-14 py-4 bg-[#8b5cf6] hover:bg-[#7c3aed] text-white font-black rounded-2xl transition-all shadow-xl flex items-center gap-2">
                        <span class="material-icons">file_download</span> Report 워드 생성
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const DEPARTMENTS = {
            "설비기획": ["냉장고기획", "세탁기기획", "공조키친기획"],
            "물류솔루션": ["물류솔루션"],
            "자동화기술": ["설계", "제작"],
            "설비혁신": ["운영", "설비기술Ⅰ", "설비기술Ⅱ"]
        };
        const STAGES = ["검토", "품의", "업체선정", "발주", "제작", "운송/통관", "설치", "양산"];

        let state = {
            mTab: "설비기획", sTab: "냉장고기획", fType: "basic",
            items: [], cols: ["구분", "내용"], rows: [["", ""]],
            activeStages: {}, 
            saved: [], photoTitle: "", investText: ""
        };

        function updateFType(t) { state.fType = t; refresh(); }
        function addItem() {
            const sym = document.getElementById('item-sym').value.split(' ')[0];
            const txt = document.getElementById('item-input').value;
            if(!txt) return;
            state.items.push({ sym, txt, xOffset: 0 });
            document.getElementById('item-input').value = '';
            refresh();
        }
        function deleteLastItem() { state.items.pop(); refresh(); }
        function deleteSpecificItem(idx) { state.items.splice(idx, 1); refresh(); }

        function rowAct(act) {
            const idx = parseInt(document.getElementById('sel-row').value);
            if(act==='up') state.rows.splice(idx, 0, Array(state.cols.length).fill(""));
            else if(act==='down') state.rows.splice(idx+1, 0, Array(state.cols.length).fill(""));
            else if(act==='del' && state.rows.length > 1) state.rows.splice(idx, 1);
            refresh();
        }

        function colAct(act) {
            const cName = document.getElementById('sel-col').value;
            const idx = state.cols.indexOf(cName);
            if(act==='left') { state.cols.splice(idx, 0, "새 열"); state.rows.forEach(r => r.splice(idx, 0, "")); }
            else if(act==='right') { state.cols.splice(idx+1, 0, "새 열"); state.rows.forEach(r => r.splice(idx+1, 0, "")); }
            else if(act==='del' && state.cols.length > 1) { state.cols.splice(idx, 1); state.rows.forEach(r => r.splice(idx, 1)); }
            refresh();
        }

        function toggleStage(s) {
            if(state.activeStages[s]) {
                delete state.activeStages[s];
                const i = state.cols.indexOf(s);
                if(i>-1) { state.cols.splice(i,1); state.rows.forEach(r=>r.splice(i,1)); }
            } else {
                state.activeStages[s] = { date: "03.29", status: "⚪" };
                state.cols.push(s); state.rows.forEach(r=>r.push(""));
            }
            syncStages(); refresh();
        }

        function syncStages() {
            Object.keys(state.activeStages).forEach(s => {
                const i = state.cols.indexOf(s);
                if(i>-1 && state.rows[0]) state.rows[0][i] = `~${state.activeStages[s].date} ${state.activeStages[s].status}`;
            });
        }

        function onHeaderInput(ci, value) { state.cols[ci] = value; renderPreview(); }
        function onCellInput(ri, ci, value) { state.rows[ri][ci] = value; renderPreview(); }

        let currentDraggingIdx = -1, startX = 0;
        function startDrag(e, idx) {
            currentDraggingIdx = idx; startX = e.clientX;
            window.addEventListener('mousemove', handleDrag);
            window.addEventListener('mouseup', stopDrag);
        }
        function handleDrag(e) {
            if(currentDraggingIdx === -1) return;
            const diff = e.clientX - startX; startX = e.clientX;
            state.items[currentDraggingIdx].xOffset += diff;
            renderPreview();
        }
        function stopDrag() {
            currentDraggingIdx = -1;
            window.removeEventListener('mousemove', handleDrag);
            window.removeEventListener('mouseup', stopDrag);
        }

        function renderPreview() {
            document.getElementById('prev-title').innerText = `🔍 ${state.mTab} - ${state.sTab} 라이브 미리보기`;
            const itemsContainer = document.getElementById('prev-items');
            itemsContainer.innerHTML = '';
            
            if (state.items.length === 0) {
                itemsContainer.innerHTML = '<p class="text-gray-600 text-sm italic">작성된 항목이 없습니다.</p>';
            } else {
                state.items.forEach((it, idx) => {
                    const container = document.createElement('div');
                    container.className = "item-container group relative flex items-center w-full";
                    const p = document.createElement('p');
                    p.className = "font-bold text-left flex-1";
                    p.style.lineHeight = "1.2"; p.style.fontSize = "12pt"; p.style.color = "white";
                    if (it.sym === '·') p.style.paddingLeft = "1.5rem";
                    if (it.sym === '√') p.style.paddingLeft = "3rem";
                    if(it.sym === '※') {
                        p.className += " draggable-extra"; p.style.color = "#60a5fa"; p.style.fontSize = "10pt";
                        p.style.transform = `translateX(${it.xOffset}px)`;
                        p.onmousedown = (e) => startDrag(e, idx);
                        p.style.marginBottom = "12pt";
                    } else {
                        const nextIt = state.items[idx + 1];
                        if (nextIt && nextIt.sym === '※') p.style.marginBottom = "0px";
                        else p.style.marginBottom = "12pt";
                    }
                    p.innerText = `${it.sym} ${it.txt}`;
                    const delBtn = document.createElement('span');
                    delBtn.className = "delete-btn material-icons text-rose-400 cursor-pointer text-sm ml-2 hover:text-rose-600 transition-colors";
                    delBtn.innerText = "cancel";
                    delBtn.onclick = (e) => { e.stopPropagation(); deleteSpecificItem(idx); };
                    container.appendChild(p); container.appendChild(delBtn);
                    itemsContainer.appendChild(container);
                });
            }
            
            const b = document.getElementById('chk-border').checked ? '1px solid rgba(79,70,229,0.3)' : 'none';
            let prevHtml = `<table style="width:100%; border-collapse:collapse; color:#e0e0e0; text-align:center; font-size:12px;"><tr style="background:rgba(49, 46, 129, 0.5); font-weight:bold; color:#c7d2fe;">` 
                + state.cols.map(c => `<th style="padding:10px; border:${b}" class="nowrap text-center">${c}</th>`).join('') + `</tr>`;
            prevHtml += state.rows.map(row => `<tr>` + row.map(cell => {
                let style = `padding:10px; border:${b};`;
                if(cell.includes('🟢')) style += "background:rgba(16,185,129,0.15); color:#10b981; font-weight:bold;";
                if(cell.includes('🟡')) style += "background:rgba(245,158,11,0.15); color:#fbbf24; font-weight:bold;";
                return `<td style="${style}" class="nowrap text-center">${cell}</td>`;
            }).join('') + `</tr>`).join('') + `</table>`;
            document.getElementById('prev-table-area').innerHTML = prevHtml;

            const prevEx = document.getElementById('prev-extra');
            if(state.fType === 'invest' && state.investText) {
                prevEx.innerHTML = `<div class="purple-gradient p-4 rounded-xl text-center"><b class="text-[#c084fc]">💰 예상 투자비:</b> <span class="ml-2 text-white font-bold">${state.investText}</span></div>`;
            } else if(state.fType === 'photo' && state.photoTitle) {
                prevEx.innerHTML = `<p class="text-[#818cf8] text-[10px] font-black text-left mb-4 mt-6">[ 사진 및 도해 ]</p>
                    <table style="width:100%; border-collapse:collapse; color:#e0e0e0; text-align:center; font-size:12px;">
                        <tr style="background:rgba(49, 46, 129, 0.5); font-weight:bold; color:#c7d2fe;"><td style="padding:10px; border:${b}; width:80px;">구분</td><td style="padding:10px; border:${b}; font-weight:bold; color:white;">${state.photoTitle}</td></tr>
                        <tr><td style="padding:10px; border:${b}; color:#c7d2fe;">도해</td><td style="padding:10px; border:${b};"><div style="width:100%; height:120px; background:rgba(0,0,0,0.3); border:1px dashed rgba(255,255,255,0.1); border-radius:10px; display:flex; align-items:center; justify-content:center; color:#6b7280; font-size:11px;"><span class="material-icons" style="margin-right:8px;">photo</span> 로컬 이미지 삽입 영역</div></td></tr>
                    </table>`;
            } else { prevEx.innerHTML = ''; }
        }

        function refresh() {
            document.getElementById('main-tabs').innerHTML = Object.keys(DEPARTMENTS).map(d => 
                `<button onclick="state.mTab='${d}'; state.sTab='${DEPARTMENTS[d][0]}'; refresh()" class="px-6 py-2 rounded-xl text-xs font-bold transition-all ${state.mTab===d?'tab-active':'text-gray-500 hover:text-white'}">${d}</button>`
            ).join('');
            document.getElementById('sub-tabs').innerHTML = DEPARTMENTS[state.mTab].map(s => 
                `<button onclick="state.sTab='${s}'; refresh()" class="${state.sTab===s?'text-white border-b-2 border-indigo-500 pb-1':'hover:text-gray-300'} transition-all">${s}</button>`
            ).join('');
            document.getElementById('sel-row').innerHTML = state.rows.map((_,i)=>`<option value="${i}">${i+1}행</option>`).join('');
            document.getElementById('sel-col').innerHTML = state.cols.map(c=>`<option value="${c}">${c}</option>`).join('');
            document.getElementById('stage-grid').innerHTML = STAGES.map(s => 
                `<label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" ${state.activeStages[s]?'checked':''} onchange="toggleStage('${s}')" class="accent-purple-500"> ${s}</label>`
            ).join('');
            document.getElementById('stage-config').innerHTML = Object.keys(state.activeStages).map(s => `
                <div class="flex items-center gap-2 bg-white/5 p-2 rounded-lg"><span class="w-16 text-[#38bdf8] font-bold text-[10px] text-center">${s}</span>
                <input type="text" value="${state.activeStages[s].date}" oninput="state.activeStages['${s}'].date=this.value; syncStages(); renderPreview()" class="w-16 p-1 text-[10px]">
                <select onchange="state.activeStages['${s}'].status=this.value; syncStages(); renderPreview()" class="flex-1 p-1 text-[10px]">
                    <option value="⚪" ${state.activeStages[s].status==='⚪'?'selected':''}>⚪ 기본</option>
                    <option value="🟢" ${state.activeStages[s].status==='🟢'?'selected':''}>🟢 정상</option>
                    <option value="🟡" ${state.activeStages[s].status==='🟡'?'selected':''}>🟡 지연</option>
                </select></div>`).join('');
            let editHtml = `<tr class="nowrap">` + state.cols.map((c, ci)=>(`<th class="p-0.5"><input type="text" value="${c}" oninput="onHeaderInput(${ci}, this.value)" class="header-editor-input"></th>`)).join('') + `</tr>`;
            editHtml += state.rows.map((r, ri) => `<tr>` + r.map((c, ci) => `<td class="p-0.5"><input type="text" value="${c}" oninput="onCellInput(${ri}, ${ci}, this.value)" class="editor-input"></td>`).join('') + `</tr>`).join('');
            document.getElementById('data-table').innerHTML = editHtml;

            const ex = document.getElementById('extra-form');
            if(state.fType==='photo') {
                ex.innerHTML = `<div class="glass p-6 text-center space-y-4 mt-6">
                    <h3 class="text-[#a5b4fc] font-bold flex items-center justify-center gap-2"><span class="material-icons text-sm">photo</span> 사진 및 도해 추가 (1:1 매핑)</h3>
                    <input type="text" placeholder="이미지 제목" oninput="state.photoTitle=this.value; renderPreview()" value="${state.photoTitle}" class="w-full p-2 text-sm">
                    <div class="w-full h-24 border-2 border-dashed border-white/10 rounded-xl flex flex-col items-center justify-center text-gray-500 text-xs gap-2 cursor-pointer hover:bg-white/5 transition-all">
                        <span class="material-icons">cloud_upload</span><span>파일 찾아보기</span></div></div>`;
            } else if(state.fType==='invest') {
                ex.innerHTML = `<div class="glass p-6 text-center space-y-4 mt-6">
                    <h3 class="text-[#06b6d4] font-bold flex items-center justify-center gap-2"><span class="material-icons text-sm">payments</span> 투자비 입력</h3>
                    <input type="text" placeholder="예상 투자비" oninput="state.investText=this.value; renderPreview()" value="${state.investText}" class="w-full p-2 text-sm"></div>`;
            } else { ex.innerHTML = ''; }
            renderPreview();
        }
        function saveBlock() {
            const title = state.items.find(i=>i.sym==='□')?.txt || "제목없음";
            state.saved.push({ title, count: state.items.length });
            state.items = []; state.activeStages = {}; state.cols = ["구분", "내용"]; state.rows = [["",""]];
            state.investText = ""; state.photoTitle = "";
            refresh();
        }
        refresh();
    </script>
</body>
</html>
"""

# =====================================================================
# [실행] Streamlit Native 호출 (포트 충돌 방지)
# =====================================================================
components.html(HTML_CONTENT, height=1200, scrolling=True)