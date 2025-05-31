import React from 'react'
import { createRoot } from 'react-dom/client'
import styled, { ThemeProvider } from 'styled-components'
import { theme } from './theme'

const PopupWrapper = styled.div`
  padding: ${({ theme }) => theme.spacing.m};
  background: ${({ theme }) => theme.colors.secondary};
  width: 200px;
`

const AnalyzeBtn = styled.button`
  width: 100%;
  padding: ${({ theme }) => theme.spacing.s} 0;
  font-size: 1rem;
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textLight};
  border: none;
  border-radius: 4px;
  cursor: pointer;
`

function Popup() {
  const handleAnalyze = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
    if (!tab?.id) return
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content-script.js']
    })
    window.close()
  }

  return (
    <ThemeProvider theme={theme}>
      <PopupWrapper>
        <h1>Bias Buster</h1>
        <AnalyzeBtn onClick={handleAnalyze}>기사 분석</AnalyzeBtn>
      </PopupWrapper>
    </ThemeProvider>
  )
}

const container = document.getElementById('popup-root')!
createRoot(container).render(<Popup />)
