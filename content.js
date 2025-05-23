
// 사이드바 생성 함수
function createSidebar(resultText) {
  const existing = document.getElementById("news-sidebar-analysis");
  if (existing) existing.remove();
  const sidebar = document.createElement("div");
  sidebar.id = "news-sidebar-analysis";
  Object.assign(sidebar.style, {
    position: "fixed",
    top: 0,
    right: 0,
    width: "350px",
    height: "100vh",
    background: "#f9f9f9",
    boxShadow: "-2px 0 5px rgba(0,0,0,0.1)",
    padding: "20px",
    overflowY: "auto",
    zIndex: 999999,
    fontFamily: "sans-serif"
  });
  sidebar.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2 style="margin:0">신뢰도 분석 결과</h2>
      <button id="closeSidebarBtn" style="background:none;border:none;font-size:20px;cursor:pointer">✕</button>
    </div>
    <hr />
    <div id="analysisContent">${resultText}</div>
  `;
  document.body.appendChild(sidebar);
  sidebar.querySelector("#closeSidebarBtn")
         .addEventListener("click", () => sidebar.remove());
}

// 분석 수행 함수 (더미 데이터 사용)
function performAnalysis() {
  const article = document.querySelector("article")?.innerText ||
                  Array.from(document.querySelectorAll("p"))
                       .map(p => p.innerText).join("\n");
  const dummy = {
    trust: "★★★★☆",
    summary: "이 기사는 신뢰할 수 있는 출처에서 작성되었으며, 주요 사실을 기반으로 합니다."
  };
  createSidebar(`신뢰도: ${dummy.trust}<br><br>${dummy.summary}`);
}

// 메시지 리스너 등록
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyze") {
    performAnalysis();
  }
});
