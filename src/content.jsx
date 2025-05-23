import React from 'react';
import { createRoot } from 'react-dom/client';
import SidePanel from './SidePanel';

// 메시지 수신 후 사이드 패널 렌더링
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'analyze') {
    const container = document.createElement('div');
    document.body.append(container);
    const root = createRoot(container);
    // TODO: 실제 API 호출 후 결과로 props 전달
    root.render(
      <SidePanel
        topic="정치"
        biasPercentage={65}
        biasDirection="진보"
        credibility="중"
        suspicionItems={["출처 불분명", "과도한 주관적 표현"]}
      />
    );
  }
});