import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/popup.css';

function Popup() {
  const analyzePage = () => {
    console.log('분석 요청 전송');
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'analyze' });
    });
  };

  return (
    <div className="popup">
      <button onClick={analyzePage}>이 페이지 분석</button>
    </div>
  );
}

const container = document.getElementById('root');
createRoot(container).render(<Popup />);