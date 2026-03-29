import React, { useState } from 'react';
import { Settings, FileText, Layers, Image as ImageIcon, DollarSign, Plus, Trash2, Download, UploadCloud, Sparkles, AlertCircle, Save, Table, Grid } from 'lucide-react';

export default function App() {
  // State Management
  const [mainMenu, setMainMenu] = useState("📝 주간업무 작성");
  const [formType, setFormType] = useState("기본 양식");
  const [mainTab, setMainTab] = useState("설비기획");
  const [subTab, setSubTab] = useState("냉장고기획");
  
  // Current Draft State
  const [items, setItems] = useState([]);
  const [level, setLevel] = useState("□ (대항목)");
  const [inputText, setInputText] = useState("");
  
  // Drag State for '※ (추가 보완)' & Photo Columns
  const [dragState, setDragState] = useState({ id: null, startX: 0, initialOffset: 0 });
  const [resizeState, setResizeState] = useState({ id: null, startX: 0, startWidth: 0 });
  
  // Dynamic Schedule Table State
  const initialTableData = [
    [
      { id: 'h1', text: '구분', border: true, isHeader: true },
      { id: 'h2', text: '검토', border: true, isHeader: true },
      { id: 'h3', text: '품의', border: true, isHeader: true },
      { id: 'h4', text: '업체선정', border: true, isHeader: true }
    ],
    [
      { id: 'd1', text: '일정', border: true, isHeader: true },
      { id: 'd2', text: '', border: true, isHeader: false },
      { id: 'd3', text: '', border: true, isHeader: false },
      { id: 'd4', text: '', border: true, isHeader: false }
    ]
  ];
  const [tableData, setTableData] = useState(initialTableData);
  const [isLineMode, setIsLineMode] = useState(false);
  const [selectedCell, setSelectedCell] = useState(null); // 추가: 현재 선택된 셀 좌표 추적
  
  const stages = ["검토", "품의", "업체선정", "발주", "제작", "운송/통관", "설치", "양산"];
  const [selectedStages, setSelectedStages] = useState([]);
  const [scheduleData, setScheduleData] = useState({});
  
  const [investAmount, setInvestAmount] = useState("");
  const [photoTitle, setPhotoTitle] = useState("");
  const [photos, setPhotos] = useState([]); 

  // Saved Blocks State
  const [savedBlocks, setSavedBlocks] = useState([]);

  // Error & Success State
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  // Departments Configuration
  const MY_DEPARTMENTS = {
    "설비기획": ["냉장고기획", "세탁기기획", "공조키친기획"],
    "물류솔루션": ["물류솔루션"], 
    "자동화기술": ["설계", "제작"],
    "설비혁신": ["운영", "설비기술Ⅰ", "설비기술Ⅱ"]
  };

  // Handlers for Current Draft
  const handleAddItem = (e) => {
    if (e.key === 'Enter' || e.type === 'click') {
      if (inputText.trim() !== "") {
        const symbol = level.split(" ")[0];
        setItems([...items, { id: Date.now() + Math.random(), symbol, text: inputText, offsetX: 0 }]);
        setInputText("");
        setErrorMsg("");
      }
    }
  };

  const handleDeleteItem = () => {
    if (items.length > 0) {
      setItems(items.slice(0, -1));
    }
  };

  // Global Mouse Handlers for Drag & Resize
  const handleGlobalMouseMove = (e) => {
    if (dragState.id) {
      const dx = e.clientX - dragState.startX;
      setItems(items.map(item => 
        item.id === dragState.id ? { ...item, offsetX: dragState.initialOffset + dx } : item
      ));
    }
    if (resizeState.id) {
      const dx = e.clientX - resizeState.startX;
      setPhotos(photos.map(photo => 
        photo.id === resizeState.id ? { ...photo, width: Math.max(100, resizeState.startWidth + dx) } : photo
      ));
    }
  };

  const handleGlobalMouseUp = () => {
    setDragState({ id: null, startX: 0, initialOffset: 0 });
    setResizeState({ id: null, startX: 0, startWidth: 0 });
  };

  // Dynamic Table Logic (기준 셀 기반으로 변경)
  const addCol = (direction) => { // 'left' | 'right'
    setTableData(prev => {
      const targetIdx = selectedCell ? (direction === 'left' ? selectedCell.cIdx : selectedCell.cIdx + 1) : prev[0].length;
      return prev.map((row, rIdx) => {
        const newRow = [...row];
        newRow.splice(targetIdx, 0, { id: `r${rIdx}c${targetIdx}_${Date.now()}`, text: '', border: true, isHeader: rIdx === 0 });
        return newRow;
      });
    });
    // 왼쪽 추가 시 선택 셀의 인덱스 보정
    if (selectedCell && direction === 'left') {
        setSelectedCell(prev => ({...prev, cIdx: prev.cIdx + 1}));
    }
  };

  const removeCol = () => {
    if (tableData[0].length <= 1) return;
    const targetIdx = selectedCell ? selectedCell.cIdx : tableData[0].length - 1;
    setTableData(prev => prev.map(row => row.filter((_, idx) => idx !== targetIdx)));
    setSelectedCell(null);
  };

  const addRow = (direction) => { // 'above' | 'below'
    setTableData(prev => {
      const targetIdx = selectedCell ? (direction === 'above' ? selectedCell.rIdx : selectedCell.rIdx + 1) : prev.length;
      const cols = prev[0].length;
      const newRow = Array.from({ length: cols }, (_, cIdx) => ({
        id: `r${targetIdx}c${cIdx}_${Date.now()}`,
        text: '',
        border: true,
        isHeader: false
      }));
      const next = [...prev];
      next.splice(targetIdx, 0, newRow);
      
      // 첫 번째 줄에 위로 추가할 경우 헤더 속성 재조정
      if (targetIdx === 0) {
        next[0].forEach(c => c.isHeader = true);
        next[1].forEach(c => c.isHeader = false);
      }
      return next;
    });
    // 위로 추가 시 선택 셀의 인덱스 보정
    if (selectedCell && direction === 'above') {
        setSelectedCell(prev => ({...prev, rIdx: prev.rIdx + 1}));
    }
  };

  const removeRow = () => {
    if (tableData.length <= 1) return;
    const targetIdx = selectedCell ? selectedCell.rIdx : tableData.length - 1;
    setTableData(prev => prev.filter((_, idx) => idx !== targetIdx));
    setSelectedCell(null);
  };

  const updateCellText = (rIdx, cIdx, val) => {
    setTableData(prev => {
      const next = [...prev];
      next[rIdx] = [...next[rIdx]];
      next[rIdx][cIdx] = { ...next[rIdx][cIdx], text: val };
      return next;
    });
  };

  const toggleCellBorder = (rIdx, cIdx) => {
    setTableData(prev => {
      const next = [...prev];
      next[rIdx] = [...next[rIdx]];
      next[rIdx][cIdx] = { ...next[rIdx][cIdx], border: !next[rIdx][cIdx].border };
      return next;
    });
  };

  const getStatusColor = (status) => {
    if (status.includes("🟢")) return { bgHtml: "#dcfce7", text: "#222" };
    if (status.includes("🟡")) return { bgHtml: "#fef08a", text: "#222" };
    return { bgHtml: "transparent", text: "#e0e0e0" };
  };

  // 💡 [핵심 연동] Schedule <-> Dynamic Table Sync
  const syncTable = (stagesArr, sData) => {
    setTableData(prev => {
      const next = prev.map(row => row.map(cell => ({...cell})));
      
      // 최소 2줄 보장 (구분, 일정)
      if (next.length < 2) {
        next.push([{ id: `auto_r1c0_${Date.now()}`, text: '일정', border: true, isHeader: true }]);
      }
      
      // 선택된 일정 항목 수만큼 열(Column) 확보
      const neededCols = Math.max(4, stagesArr.length > 0 ? stagesArr.length + 1 : next[0].length);
      next.forEach((row, rIdx) => {
        while (row.length < neededCols) {
          row.push({ id: `auto_r${rIdx}c${row.length}_${Date.now()}`, text: '', border: true, isHeader: rIdx === 0 });
        }
      });

      if (stagesArr.length > 0) {
        // 첫 번째 열 고정 텍스트
        next[0][0].text = '구분';
        next[1][0].text = '일정';
        
        stagesArr.forEach((stage, idx) => {
          const cIdx = idx + 1;
          next[0][cIdx].text = stage;
          
          const data = sData[stage];
          const rawDate = data?.date || "";
          const shortDate = rawDate ? `~${rawDate.substring(5).replace(/-/g, '.')}` : "";
          const colors = getStatusColor(data?.status || "");
          
          // 데이터 및 색상 동기화
          next[1][cIdx].text = shortDate;
          next[1][cIdx].bgColor = colors.bgHtml;
          next[1][cIdx].textColor = colors.text;
        });

        // 사용자가 일정을 해제하여 남게된 뒷부분의 잉여 열(Ghost Column) 클리어 처리
        const leftOverCol = stagesArr.length + 1;
        for (let c = leftOverCol; c < next[0].length; c++) {
           next[0][c].bgColor = 'transparent';
           next[0][c].textColor = '';
           next[1][c].bgColor = 'transparent';
           next[1][c].textColor = '';
           
           // 기존 시스템 일정 항목이었던 경우에만 텍스트 초기화 (사용자 자유 입력은 보존)
           if (stages.includes(next[0][c].text)) {
               next[0][c].text = '';
               next[1][c].text = '';
           }
        }
      } else {
         // 모든 항목이 해제되었을 경우 자유 편집 모드로 완벽 복구
         for (let c = 1; c < next[0].length; c++) {
           next[0][c].bgColor = 'transparent';
           next[0][c].textColor = '';
           next[1][c].bgColor = 'transparent';
           next[1][c].textColor = '';
         }
      }

      return next;
    });
  };

  const handleStageToggle = (stage) => {
    let newStages;
    let newData = { ...scheduleData };
    if (selectedStages.includes(stage)) {
      newStages = selectedStages.filter(s => s !== stage);
      delete newData[stage];
    } else {
      newStages = [...selectedStages, stage];
      newData[stage] = { date: new Date().toISOString().split('T')[0], status: "⚪ 기본" };
    }
    setSelectedStages(newStages);
    setScheduleData(newData);
    syncTable(newStages, newData); // 동기화 호출
  };

  const updateSchedule = (stage, field, value) => {
    const newData = {
      ...scheduleData,
      [stage]: { ...scheduleData[stage], [field]: value }
    };
    setScheduleData(newData);
    syncTable(selectedStages, newData); // 동기화 호출
  };

  // Photo Handlers (추가, 너비 조절, 삭제)
  const handleAddPhoto = () => {
    setPhotos([...photos, { id: Date.now(), title: photoTitle || "제목 미지정", width: 250 }]);
    setPhotoTitle(""); 
  };

  const handleResizeStart = (e, id, currentWidth) => {
    e.preventDefault(); 
    setResizeState({ id, startX: e.clientX, startWidth: currentWidth });
  };

  const handleRemovePhoto = (id) => {
    setPhotos(photos.filter(p => p.id !== id));
  };

  // Block Save Logic
  const handleSaveBlock = () => {
    if (items.length === 0 && tableData.every(row => row.every(cell => !cell.text))) {
      setErrorMsg("저장할 내용이 없습니다.");
      setTimeout(() => setErrorMsg(""), 3000);
      return;
    }

    const mainItem = items.find(i => i.symbol === "□");
    const blockTitle = mainItem ? mainItem.text : "제목 없음 (대항목 미지정)";

    const newBlock = {
      id: Date.now(),
      title: blockTitle,
      items: [...items],
      tableData: tableData.map(row => [...row]),
      selectedStages: [...selectedStages],
      scheduleData: { ...scheduleData },
      formType,
      photos: [...photos], 
      investAmount
    };

    setSavedBlocks([...savedBlocks, newBlock]);
    
    // 상태 초기화
    setItems([]);
    setTableData(initialTableData);
    setSelectedStages([]);
    setScheduleData({});
    setInvestAmount("");
    setPhotos([]);
    setPhotoTitle("");
    setIsLineMode(false);
    setSelectedCell(null); // 추가: 저장 시 셀 선택 초기화
    
    setSuccessMsg(`"${blockTitle}" 블록이 저장되었습니다.`);
    setTimeout(() => setSuccessMsg(""), 3000);
  };

  const handleDeleteBlock = (id) => {
    setSavedBlocks(savedBlocks.filter(b => b.id !== id));
  };

  const handleGenerateReport = () => {
    if (savedBlocks.length === 0 && items.length === 0) {
      setErrorMsg("생성할 보고서 내용이 없습니다.");
      setTimeout(() => setErrorMsg(""), 3000);
      return;
    }
    
    setSuccessMsg(`총 ${savedBlocks.length + (items.length > 0 ? 1 : 0)}개의 블록이 하나의 문서로 병합 생성되었습니다.`);
    setTimeout(() => setSuccessMsg(""), 5000);
  };

  return (
    <div 
      className="min-h-screen text-[#e0e0e0] flex font-sans select-none" 
      style={{ background: 'radial-gradient(circle at 15% 50%, #1e152e, #0b0c10 70%)' }}
      onMouseMove={handleGlobalMouseMove}
      onMouseUp={handleGlobalMouseUp}
      onMouseLeave={handleGlobalMouseUp}
    >
      
      {/* Sidebar */}
      <div className="w-64 shrink-0 border-r border-white/5 p-6 flex flex-col gap-6" style={{ background: 'rgba(15, 17, 26, 0.4)', backdropFilter: 'blur(15px)' }}>
        <h2 className="text-2xl font-bold text-white mb-4 whitespace-nowrap">💎 Menu</h2>
        
        <div className="space-y-2">
          <label className="text-sm text-gray-400 mb-2 block">기능 선택</label>
          {["📝 주간업무 작성", "🔗 작성본 합치기"].map(menu => (
            <button 
              key={menu}
              onClick={() => setMainMenu(menu)}
              className={`w-full text-left px-4 py-3 rounded-xl transition-all whitespace-nowrap ${mainMenu === menu ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-500/30' : 'hover:bg-white/5 text-gray-400'}`}
            >
              {menu}
            </button>
          ))}
        </div>

        {mainMenu === "📝 주간업무 작성" && (
          <div className="space-y-2 mt-4 pt-4 border-t border-white/10">
            <label className="text-sm text-gray-400 mb-2 block">📄 세부 양식 선택</label>
            {["기본 양식", "사진 추가", "투자비 추가"].map(type => (
              <button 
                key={type}
                onClick={() => setFormType(type)}
                className={`w-full text-left px-4 py-2 rounded-lg text-sm transition-all whitespace-nowrap ${formType === type ? 'bg-white/10 text-white border border-white/20' : 'text-gray-500 hover:text-gray-300'}`}
              >
                {type === "기본 양식" && <FileText className="inline w-4 h-4 mr-2"/>}
                {type === "사진 추가" && <ImageIcon className="inline w-4 h-4 mr-2"/>}
                {type === "투자비 추가" && <DollarSign className="inline w-4 h-4 mr-2"/>}
                {type}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col p-8 overflow-y-auto h-screen">
        <h1 className="text-4xl font-bold mb-2 pb-4 border-b border-white/5 whitespace-nowrap" style={{ background: 'linear-gradient(90deg, #fff, #9d72ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          🚀 자동화설비그룹 주간업무 작성 양식
        </h1>

        {/* Message Bars */}
        {errorMsg && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-xl mt-4 flex items-center gap-2 animate-pulse">
            <AlertCircle className="w-5 h-5"/> {errorMsg}
          </div>
        )}
        {successMsg && (
          <div className="bg-emerald-500/20 border border-emerald-500/50 text-emerald-200 px-4 py-3 rounded-xl mt-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5"/> {successMsg}
          </div>
        )}

        {mainMenu === "📝 주간업무 작성" ? (
          <div className="flex flex-col h-full mt-4">
            {/* Main Tabs */}
            <div className="flex flex-wrap gap-2 bg-black/20 p-2 rounded-2xl w-max mb-2">
              {Object.keys(MY_DEPARTMENTS).map(dept => (
                <button 
                  key={dept} 
                  onClick={() => { setMainTab(dept); setSubTab(MY_DEPARTMENTS[dept][0]); }}
                  className={`px-4 py-2 rounded-xl text-sm transition-all whitespace-nowrap ${mainTab === dept ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-500/40' : 'text-gray-400 hover:bg-white/5'}`}
                >
                  {dept}
                </button>
              ))}
            </div>

            {/* Sub Tabs */}
            <div className="flex flex-wrap gap-2 bg-white/5 p-1.5 rounded-xl w-max mb-6">
              {MY_DEPARTMENTS[mainTab].map(sub => (
                <button 
                  key={sub}
                  onClick={() => setSubTab(sub)}
                  className={`px-3 py-1.5 rounded-lg text-xs transition-all whitespace-nowrap ${subTab === sub ? 'bg-gradient-to-r from-cyan-400 to-blue-500 text-white shadow-lg shadow-cyan-500/30 border border-white/10' : 'text-gray-400 hover:bg-white/5'}`}
                >
                  {sub}
                </button>
              ))}
            </div>

            {/* Two Columns Layout */}
            <div className="flex gap-8 flex-1 min-h-0">
              
              {/* Left Column - Input */}
              <div className="flex-1 min-w-[500px] flex flex-col gap-6 overflow-y-auto pr-2 pb-10">
                <section>
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2 whitespace-nowrap">
                    <Plus className="w-5 h-5 text-indigo-400"/> 
                    <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">항목 추가</span>
                  </h3>
                  <div className="flex gap-3 mb-3">
                    <select 
                      className="bg-indigo-950/40 border border-indigo-500/40 rounded-xl px-4 py-2 text-indigo-50 outline-none focus:border-indigo-500 whitespace-nowrap shrink-0 transition-colors"
                      value={level} onChange={(e) => setLevel(e.target.value)}
                    >
                      <option className="bg-gray-900">□ (대항목)</option>
                      <option className="bg-gray-900">· (중항목)</option>
                      <option className="bg-gray-900">√ (소항목)</option>
                      <option className="bg-gray-900">※ (추가 보완)</option>
                    </select>
                    <input 
                      type="text" 
                      placeholder="내용 (입력 후 엔터↵를 치세요)" 
                      className="flex-1 min-w-[200px] bg-indigo-950/40 border border-indigo-500/40 rounded-xl px-4 py-2 text-white outline-none focus:border-indigo-500 placeholder-indigo-300/50 transition-colors"
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      onKeyDown={handleAddItem}
                    />
                  </div>
                  <div className="flex gap-2">
                    <button onClick={handleAddItem} className="flex-[2] bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl py-2.5 font-bold text-white hover:-translate-y-0.5 transition-transform shadow-lg shadow-indigo-500/30 whitespace-nowrap shrink-0">
                      ➕ 추가
                    </button>
                    <button onClick={handleDeleteItem} className="flex-1 bg-indigo-900/40 border border-indigo-500/30 text-indigo-300 rounded-xl py-2.5 font-bold hover:bg-indigo-800/60 hover:-translate-y-0.5 transition-all whitespace-nowrap shrink-0">
                      🗑️ 삭제
                    </button>
                  </div>
                </section>

                <div className="border-b border-indigo-500/20"></div>

                <section>
                  <h3 className="text-xl font-bold mb-4 whitespace-nowrap flex items-center gap-2">
                    <span className="mr-1">📅</span>
                    <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">진행 일정 구성</span>
                  </h3>
                  
                  {/* Left-Right Split within Input Panel for Schedule Controls */}
                  <div className="grid grid-cols-2 gap-4">
                    
                    {/* Left: Custom Table Controls */}
                    <div className="flex flex-col gap-3 bg-indigo-950/30 p-4 rounded-2xl border border-indigo-500/30 shadow-[0_0_15px_rgba(79,70,229,0.1)]">
                      <div className="flex flex-col">
                        <span className="text-indigo-200 font-bold text-sm">표 자유 편집</span>
                        <span className="text-indigo-300/60 text-[10px] mt-0.5 leading-tight">* 우측 표에서 기준 셀을 클릭 후 조작하세요.</span>
                      </div>
                      <div className="flex flex-col gap-2 mt-1">
                        <div className="flex flex-col gap-1.5">
                          <span className="text-indigo-300 text-[11px] font-bold px-1">행 (세로) 조절</span>
                          <div className="flex gap-1.5">
                            <button onClick={() => addRow('above')} className="flex-1 bg-indigo-900/50 border border-indigo-500/50 text-indigo-200 rounded-lg py-1.5 hover:bg-indigo-800 transition-colors text-[11px] font-bold whitespace-nowrap">
                              위 추가
                            </button>
                            <button onClick={() => addRow('below')} className="flex-1 bg-indigo-900/50 border border-indigo-500/50 text-indigo-200 rounded-lg py-1.5 hover:bg-indigo-800 transition-colors text-[11px] font-bold whitespace-nowrap">
                              아래 추가
                            </button>
                            <button onClick={removeRow} className="flex-[0.8] bg-indigo-900/40 border border-indigo-500/30 text-indigo-300 rounded-lg py-1.5 hover:bg-indigo-800/60 transition-colors text-[11px] font-bold whitespace-nowrap">
                              삭제
                            </button>
                          </div>
                        </div>
                        <div className="flex flex-col gap-1.5 mt-1">
                          <span className="text-indigo-300 text-[11px] font-bold px-1">열 (가로) 조절</span>
                          <div className="flex gap-1.5">
                            <button onClick={() => addCol('left')} className="flex-1 bg-indigo-900/50 border border-indigo-500/50 text-indigo-200 rounded-lg py-1.5 hover:bg-indigo-800 transition-colors text-[11px] font-bold whitespace-nowrap">
                              왼쪽 추가
                            </button>
                            <button onClick={() => addCol('right')} className="flex-1 bg-indigo-900/50 border border-indigo-500/50 text-indigo-200 rounded-lg py-1.5 hover:bg-indigo-800 transition-colors text-[11px] font-bold whitespace-nowrap">
                              오른쪽 추가
                            </button>
                            <button onClick={removeCol} className="flex-[0.8] bg-indigo-900/40 border border-indigo-500/30 text-indigo-300 rounded-lg py-1.5 hover:bg-indigo-800/60 transition-colors text-[11px] font-bold whitespace-nowrap">
                              삭제
                            </button>
                          </div>
                        </div>
                        <button 
                          onClick={() => { setIsLineMode(!isLineMode); setSelectedCell(null); }} 
                          className={`w-full py-2.5 mt-2 rounded-lg font-bold transition-all text-[11px] flex items-center justify-center gap-1 ${isLineMode ? 'bg-indigo-600 text-white shadow-[0_0_15px_rgba(79,70,229,0.4)]' : 'bg-indigo-900/50 border border-indigo-500/50 text-indigo-200 hover:bg-indigo-800'}`}
                        >
                          <Grid className="w-3.5 h-3.5"/>
                          {isLineMode ? "선 추가/삭제 모드 끄기" : "선 추가/삭제 모드 켜기"}
                        </button>
                      </div>
                    </div>

                    {/* Right: Predefined Stages */}
                    <div className="flex flex-col gap-3 bg-indigo-950/30 p-4 rounded-2xl border border-indigo-500/30 shadow-[0_0_15px_rgba(79,70,229,0.1)]">
                      <span className="text-indigo-200 font-bold text-sm">기본 일정 항목</span>
                      <div className="flex flex-wrap gap-1.5 overflow-y-auto max-h-[90px] pr-1 scrollbar-hide">
                        {stages.map(stage => (
                          <button 
                            key={stage}
                            onClick={() => handleStageToggle(stage)}
                            className={`px-2 py-1 rounded text-xs border transition-all whitespace-nowrap shrink-0 ${selectedStages.includes(stage) ? 'bg-indigo-600/50 border-indigo-400 text-indigo-100 shadow-[0_0_10px_rgba(99,102,241,0.3)]' : 'bg-indigo-900/30 border-indigo-500/30 text-indigo-300 hover:bg-indigo-800/40 hover:border-indigo-500/50'}`}
                          >
                            {stage}
                          </button>
                        ))}
                      </div>
                      
                      <div className="flex flex-col gap-2 overflow-y-auto max-h-[120px] pr-1">
                        {selectedStages.map(stage => (
                          <div key={stage} className="flex flex-col gap-1 bg-black/20 p-2 rounded-lg border border-indigo-500/20">
                            <span className="font-bold text-indigo-200 text-xs px-1">{stage}</span>
                            <div className="flex gap-2">
                              <input 
                                type="date" 
                                value={scheduleData[stage]?.date}
                                onChange={(e) => updateSchedule(stage, 'date', e.target.value)}
                                className="flex-[2] bg-black/40 border border-indigo-500/30 rounded px-2 py-1 text-xs outline-none text-indigo-100 color-scheme-dark focus:border-indigo-400 transition-colors"
                              />
                              <select 
                                value={scheduleData[stage]?.status}
                                onChange={(e) => updateSchedule(stage, 'status', e.target.value)}
                                className="flex-[1.5] bg-black/40 border border-indigo-500/30 rounded px-2 py-1 text-xs outline-none text-indigo-100 focus:border-indigo-400 transition-colors"
                              >
                                <option className="bg-gray-900">⚪ 기본</option>
                                <option className="bg-gray-900">🟢 정상</option>
                                <option className="bg-gray-900">🟡 지연</option>
                              </select>
                            </div>
                          </div>
                        ))}
                        {selectedStages.length === 0 && (
                          <div className="text-xs text-indigo-300/50 text-center py-4">항목을 선택하면 날짜 지정이 나타납니다.</div>
                        )}
                      </div>
                    </div>

                  </div>
                </section>

                <div className="border-b border-indigo-500/20"></div>

                {formType === "사진 추가" && (
                  <section className="flex flex-col gap-3">
                    <input 
                      type="text" 
                      placeholder="📸 사진 제목을 입력하세요" 
                      className="w-full bg-indigo-950/30 border border-indigo-500/40 rounded-xl px-4 py-3 text-white outline-none focus:border-indigo-500 placeholder-indigo-300/50 transition-all"
                      value={photoTitle}
                      onChange={(e) => setPhotoTitle(e.target.value)}
                    />
                    <div className="border-2 border-dashed border-indigo-500/30 rounded-xl p-8 text-center bg-indigo-950/20 cursor-pointer hover:bg-indigo-900/40 transition-colors"
                         onClick={handleAddPhoto}>
                      <UploadCloud className="w-8 h-8 mx-auto text-indigo-400 mb-2"/>
                      <p className="text-indigo-300/70 text-sm whitespace-nowrap">클릭하여 사진 다중 첨부 (시뮬레이션)</p>
                    </div>
                  </section>
                )}

                {formType === "투자비 추가" && (
                  <section>
                    <input 
                      type="text" 
                      placeholder="💰 예상 투자비 (예: 5.5억 원)" 
                      className="w-full bg-indigo-950/30 border border-indigo-500/40 rounded-xl px-4 py-3 text-white outline-none focus:border-indigo-500 focus:shadow-[0_0_15px_rgba(79,70,229,0.2)] placeholder-indigo-300/50 transition-all"
                      value={investAmount}
                      onChange={(e) => setInvestAmount(e.target.value)}
                    />
                  </section>
                )}

                {/* Save and Report Action Area */}
                <div className="flex gap-3 mt-auto pt-6">
                  <button onClick={handleSaveBlock} className="flex-1 bg-indigo-800/50 border border-indigo-500/40 rounded-xl py-3 font-bold text-indigo-100 text-lg hover:bg-indigo-700/50 hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2 whitespace-nowrap">
                    <Save className="w-5 h-5"/> 저장
                  </button>
                  <button onClick={handleGenerateReport} className="flex-[1.5] bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl py-3 font-bold text-white text-lg hover:-translate-y-0.5 transition-transform shadow-xl shadow-purple-500/40 flex items-center justify-center gap-2 whitespace-nowrap">
                    <Download className="w-5 h-5"/> Report 생성
                  </button>
                </div>

              </div>

              {/* Right Column - Preview & Saved Blocks */}
              <div className="flex-[1.2] flex flex-col h-full min-w-[450px]">
                <h3 className="text-xl font-bold mb-4 whitespace-nowrap flex items-center gap-2">
                  <span className="text-indigo-400">🔍</span>
                  <span className="bg-gradient-to-r from-indigo-300 to-purple-300 bg-clip-text text-transparent">미리 보기</span>
                </h3>
                <div className="flex-1 flex flex-col p-8 rounded-[24px] border border-indigo-500/20 shadow-[0_0_30px_rgba(79,70,229,0.15)] overflow-y-auto select-text" 
                     style={{ background: 'rgba(20, 22, 43, 0.7)', backdropFilter: 'blur(20px)' }}>
                  
                  {/* Current Draft Area */}
                  <h2 className="text-2xl font-bold mb-6 pb-4 border-b border-indigo-500/20 whitespace-nowrap" style={{ background: '-webkit-linear-gradient(#fff, #a5b4fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    [작성 중] {mainTab === subTab ? mainTab : `${mainTab} - ${subTab}`} 주간업무
                  </h2>

                  <div className="mb-6">
                    <b className="text-indigo-300/70 text-sm mb-4 block select-none">[ 업무 항목 ]</b>
                    
                    <div className="min-h-[60px] select-none">
                      {items.length === 0 ? (
                        <p className="text-indigo-200/30 text-sm">항목을 추가하면 표시됩니다.</p>
                      ) : (
                        items.map((item) => {
                          const isDraggable = item.symbol === '※';
                          const fontSize = isDraggable ? '10pt' : '12pt';
                          const lineHeight = 1;
                          const cursorStyle = isDraggable ? 'ew-resize' : 'default';
                          const userSelectStyle = isDraggable ? 'none' : 'auto';
                          
                          let baseMarginLeft = '0px';
                          if (item.symbol === '·') baseMarginLeft = '20px';
                          if (item.symbol === '√') baseMarginLeft = '40px';
                          const marginTop = item.symbol === '□' ? '12px' : '4px';
                          
                          return (
                            <div 
                              key={item.id} 
                              onMouseDown={(e) => isDraggable && handleMouseDown(e, item.id, item.offsetX)}
                              style={{ 
                                fontSize, 
                                lineHeight, 
                                marginTop,
                                marginLeft: baseMarginLeft,
                                transform: `translateX(${item.offsetX || 0}px)`,
                                cursor: cursorStyle,
                                userSelect: userSelectStyle,
                                color: isDraggable ? '#93c5fd' : '#e0e0e0', 
                                fontWeight: item.symbol === '□' || isDraggable ? 'bold' : 'normal'
                              }}
                            >
                              {item.symbol} {item.text}
                            </div>
                          );
                        })
                      )}
                    </div>
                  </div>

                  <div className="mb-6">
                    <b className="text-indigo-300/70 text-sm mb-4 block select-none">[ 진행 일정 ]</b>
                    
                    {/* Unified Editable Dynamic Table Rendering */}
                    <div className="overflow-x-auto pb-2">
                      <table className="w-full border-collapse text-sm text-center">
                        <tbody>
                          {tableData.map((row, rIdx) => (
                            <tr key={rIdx}>
                              {row.map((cell, cIdx) => {
                                let borderClass = "border-transparent";
                                if (cell.border) {
                                  borderClass = "border-white/20";
                                } else if (isLineMode) {
                                  borderClass = "border-white/10 border-dashed";
                                }

                                // Sync된 배경색, 헤더색, 텍스트 컬러 지정
                                let finalBg = "transparent";
                                if (cell.bgColor && cell.bgColor !== "transparent") {
                                  finalBg = cell.bgColor;
                                } else if (cell.isHeader) {
                                  finalBg = "rgba(49, 46, 129, 0.4)";
                                }

                                let finalColor = "#eef2ff";
                                if (cell.textColor) {
                                  finalColor = cell.textColor;
                                } else if (cell.isHeader) {
                                  finalColor = "#e0e7ff";
                                }

                                const isSelected = selectedCell?.rIdx === rIdx && selectedCell?.cIdx === cIdx && !isLineMode;

                                return (
                                  <td 
                                    key={cell.id} 
                                    onClick={() => {
                                      if (isLineMode) toggleCellBorder(rIdx, cIdx);
                                      else setSelectedCell({ rIdx, cIdx });
                                    }}
                                    className={`p-0 relative border transition-all duration-200 whitespace-nowrap ${borderClass} ${isSelected ? 'ring-2 ring-inset ring-indigo-400 z-10' : ''}`}
                                    style={{ 
                                      minWidth: '80px', 
                                      cursor: isLineMode ? 'pointer' : 'text',
                                      backgroundColor: finalBg,
                                      color: finalColor,
                                      fontWeight: cell.isHeader ? 'bold' : 'normal'
                                    }}
                                  >
                                    {isLineMode ? (
                                      <div className="p-3 w-full h-full select-none flex items-center justify-center min-h-[40px] whitespace-nowrap">
                                        {cell.text || '\u00A0'}
                                        <div className="absolute inset-0 hover:bg-indigo-500/20 transition-colors z-10 pointer-events-none" />
                                      </div>
                                    ) : (
                                      <input
                                        type="text"
                                        value={cell.text}
                                        onChange={(e) => updateCellText(rIdx, cIdx, e.target.value)}
                                        onFocus={() => setSelectedCell({ rIdx, cIdx })}
                                        className="w-full h-full min-h-[40px] bg-transparent outline-none text-center p-3 focus:bg-indigo-500/20 transition-colors whitespace-nowrap"
                                        placeholder="입력"
                                        style={{ color: 'inherit', fontWeight: 'inherit' }}
                                      />
                                    )}
                                  </td>
                                );
                              })}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <div className="mb-8">
                    {(formType === "사진 추가" || photos.length > 0) && (
                      <div className="mt-2 border border-indigo-500/30 rounded-xl overflow-hidden shadow-[0_0_20px_rgba(79,70,229,0.15)] bg-black/20">
                        <div className="overflow-x-auto w-full pb-1">
                          <table className="text-center text-sm border-collapse w-max min-w-full">
                            <tbody>
                              <tr>
                                <td className="bg-indigo-950/50 text-indigo-300 font-bold border border-indigo-500/30 p-3 w-[80px] shrink-0 whitespace-nowrap">
                                  구분
                                </td>
                                {photos.length === 0 ? (
                                  <td className="text-indigo-200/50 border border-indigo-500/30 p-3 w-full">사진을 추가하세요</td>
                                ) : (
                                  photos.map(photo => (
                                    <td 
                                      key={`title-${photo.id}`} 
                                      className="relative bg-indigo-950/30 text-indigo-50 border border-indigo-500/30 font-bold transition-all" 
                                      style={{ width: photo.width, minWidth: '100px' }}
                                    >
                                      <div className="p-3 overflow-hidden text-ellipsis whitespace-nowrap w-full">
                                        {photo.title}
                                      </div>
                                      <div
                                        onMouseDown={(e) => handleResizeStart(e, photo.id, photo.width)}
                                        className="absolute top-0 right-0 bottom-0 w-2 cursor-col-resize hover:bg-indigo-400/50 z-10"
                                        title="드래그하여 너비 조절"
                                      />
                                    </td>
                                  ))
                                )}
                              </tr>
                              <tr>
                                <td className="bg-indigo-950/50 text-indigo-300 font-bold border border-indigo-500/30 p-3 whitespace-nowrap">
                                  도해
                                </td>
                                {photos.length === 0 ? (
                                  <td className="border border-indigo-500/30 p-4">
                                    <span className="text-indigo-200/50 block py-4">[ 사진 대기 중 ]</span>
                                  </td>
                                ) : (
                                  photos.map(photo => (
                                    <td 
                                      key={`img-${photo.id}`} 
                                      className="relative border border-indigo-500/30 p-4" 
                                      style={{ width: photo.width, minWidth: '100px' }}
                                    >
                                      <div className="bg-black/40 border border-purple-500/30 rounded-lg flex items-center justify-center text-xs text-purple-300 overflow-hidden w-full aspect-[4/3]">
                                        📸 이미지
                                      </div>
                                      <button 
                                        onClick={() => handleRemovePhoto(photo.id)} 
                                        className="absolute top-2 right-2 bg-rose-500/80 text-white rounded-md px-2 py-1 text-xs hover:bg-rose-500 transition-colors z-10"
                                      >
                                        x
                                      </button>
                                      <div
                                        onMouseDown={(e) => handleResizeStart(e, photo.id, photo.width)}
                                        className="absolute top-0 right-0 bottom-0 w-2 cursor-col-resize hover:bg-indigo-400/50 z-10"
                                      />
                                    </td>
                                  ))
                                )}
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}
                    {(formType === "투자비 추가" || investAmount) && (
                      <div className="rounded-2xl bg-indigo-950/30 border border-indigo-500/40 p-4 mt-2 shadow-[0_0_15px_rgba(79,70,229,0.1)]">
                        <b className="text-indigo-300 text-base">💰 총 예상 투자비:</b>
                        <span className="text-white text-base ml-3">{investAmount || "미입력"}</span>
                      </div>
                    )}
                  </div>

                  {/* Saved Blocks List */}
                  <div className="mt-auto border-t border-indigo-500/20 pt-6 select-none">
                    <h3 className="text-lg font-bold text-indigo-300 mb-4 flex items-center gap-2">
                      📦 완료된 블록 리스트 ({savedBlocks.length})
                    </h3>
                    
                    {savedBlocks.length === 0 ? (
                      <div className="text-center p-8 bg-indigo-950/20 rounded-xl border border-indigo-500/10 text-indigo-200/40 text-sm">
                        저장 버튼을 눌러 작성된 내용을 블록으로 보관하세요.<br/>(저장된 블록들은 생성 시 하나의 문서로 안전하게 병합됩니다.)
                      </div>
                    ) : (
                      <div className="flex flex-col gap-3">
                        {savedBlocks.map((block, idx) => (
                          <div key={block.id} className="bg-indigo-950/30 border border-indigo-500/30 p-4 rounded-xl flex justify-between items-center hover:bg-indigo-900/40 hover:border-indigo-400/50 transition-all shadow-sm">
                            <div className="flex flex-col">
                              <div className="flex items-center gap-2">
                                <span className="bg-indigo-600/30 text-indigo-200 border border-indigo-500/30 text-xs px-2 py-1 rounded-md font-bold">
                                  Block {idx + 1}
                                </span>
                                <span className="text-indigo-50 font-bold">{block.title}</span>
                              </div>
                              <span className="text-indigo-300/70 text-xs mt-1">
                                데이터 {block.items.length}건 | 표 맵핑 완료 | 사진 {block.photos ? block.photos.length : 0}열 {block.investAmount ? `| 투자비: ${block.investAmount}` : ''}
                              </span>
                            </div>
                            <button onClick={() => handleDeleteBlock(block.id)} className="p-2 text-rose-400/70 hover:text-rose-300 hover:bg-rose-500/20 rounded-lg transition-colors">
                              <Trash2 className="w-5 h-5" />
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center select-none">
            <Layers className="w-20 h-20 text-indigo-400 mb-6 opacity-80" />
            <h2 className="text-3xl font-bold mb-4">🔗 주간업무 통합 (문서 병합)</h2>
            <p className="text-gray-400 max-w-lg mb-8">
              개별적으로 작성된 주간업무 워드 파일(.docx)들을 업로드하면 페이지가 나뉘어 하나의 파일로 병합됩니다. 
            </p>
            <div className="border-2 border-dashed border-indigo-500/30 rounded-2xl p-12 bg-indigo-950/20 w-full max-w-2xl cursor-pointer hover:bg-indigo-900/40 transition-colors">
              <UploadCloud className="w-12 h-12 mx-auto text-indigo-400 mb-4"/>
              <p className="text-lg text-indigo-100 font-bold mb-2">워드 파일들을 이곳으로 드래그 앤 드롭 하세요</p>
              <p className="text-sm text-indigo-300/70">지원 형식: .docx (최소 2개 이상 필요)</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}