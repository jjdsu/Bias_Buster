import React from 'react';
import styled from 'styled-components';
import { RadialBarChart, RadialBar } from 'recharts';

// 사이드 패널 컨테이너
const Panel = styled.div`
  position: fixed;
  top: 0;
  right: 0;
  width: 350px;
  height: 100vh;
  background-color: #fff;
  box-shadow: -2px 0 8px rgba(0,0,0,0.1);
  padding: 16px;
  overflow-y: auto;
  z-index: 9999;
`;

// 각 섹션 스타일
const Section = styled.div`
  margin-bottom: 24px;
`;
const SectionTitle = styled.h2`
  font-size: 1.2rem;
  margin-bottom: 8px;
`;
const Topic = styled.p`
  font-size: 1rem;
  margin-bottom: 16px;
`;
const GaugeWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
`;
const SuspicionList = styled.ul`
  list-style-type: disc;
  padding-left: 20px;
  margin-top: 8px;
`;

// Props: topic (string), biasPercentage (number), biasDirection ("진보" | "보수"), credibility ("상" | "중" | "하"), suspicionItems (string[])
const SidePanel = ({ topic, biasPercentage, biasDirection, credibility, suspicionItems }) => {
  const gaugeData = [
    { name: biasDirection, value: biasPercentage }
  ];

  return (
    <Panel>
      <Section>
        <Topic>이 기사는 <strong>{topic}</strong> 주제로 한 기사입니다.</Topic>
      </Section>

      <Section>
        <SectionTitle>1. 성향 분석</SectionTitle>
        <GaugeWrapper>
          <RadialBarChart
            width={120}
            height={120}
            cx={60}
            cy={60}
            innerRadius={40}
            outerRadius={60}
            barSize={10}
            data={gaugeData}
            startAngle={180}
            endAngle={0}
          >
            <RadialBar
              minAngle={15}
              background
              clockWise
              dataKey="value"
              fill={biasDirection === '진보' ? '#4ade80' : '#f87171'}
            />
          </RadialBarChart>
        </GaugeWrapper>
        <p>이 기사는 <strong>{biasDirection}</strong> 성향을 <strong>{biasPercentage}%</strong> 띄고 있습니다.</p>
      </Section>

      <Section>
        <SectionTitle>2. 신뢰도 분석</SectionTitle>
        <p>이 뉴스의 신뢰도는 <strong>{credibility}</strong> 입니다.</p>
        {suspicionItems.length > 0 && (
          <>
            <p>의심 요소:</p>
            <SuspicionList>
              {suspicionItems.map((item, idx) => <li key={idx}>{item}</li>)}
            </SuspicionList>
          </>
        )}
      </Section>
    </Panel>
  );
};

export default SidePanel;
