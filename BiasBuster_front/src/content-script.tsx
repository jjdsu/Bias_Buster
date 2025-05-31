import React from 'react'
import { createRoot } from 'react-dom/client'
import AnalysisPanel from './components/AnalysisPanel'
import { ThemeProvider } from 'styled-components'
import { theme } from './theme'

const PANEL_ID = 'bb-analysis-panel'
let panelRoot: ReturnType<typeof createRoot> | null = null

// 사이드 패널 열기/닫기 함수
function togglePanel() {
  const existing = document.getElementById(PANEL_ID)
  if (existing) {
    // 이미 열려 있으면 닫기
    panelRoot!.unmount()
    existing.remove()
    panelRoot = null
    return
  }
  // 새로 열기
  const panel = document.createElement('div')
  panel.id = PANEL_ID
  panel.style.cssText = `
    position: fixed;
    top: 0; right: 0;
    width: 400px; height: 100%;
    background: white;
    box-shadow: -2px 0 4px rgba(0,0,0,0.2);
    z-index: 9999;
    overflow: auto;
  `
  document.body.appendChild(panel)
  panelRoot = createRoot(panel)
  panelRoot.render(
    <ThemeProvider theme={theme}>
      <AnalysisPanel onClose={togglePanel} />
    </ThemeProvider>
  )
}

// 스크립트가 주입되는 순간 토글 트리거
togglePanel()
