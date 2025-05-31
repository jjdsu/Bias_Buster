import React, { useEffect, useState } from 'react'
import styled, {ThemeProvider} from 'styled-components'
import { analyzeArticle, AnalysisResult, CategoryScore } from '../utils/fetchAnalysis'
import {theme} from '../theme'
import BiasBar from './BiasBar'
import { getArticleText } from '../utils/extractArticleText'

const PanelWrapper = styled.div`
  position: fixed;
  top: 0; right: 0;
  width: 400px; height: 100%;
  background: ${({ theme }) => theme.colors.secondary};
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.2);
  z-index: 9999;
  display: flex;
  flex-direction: column;
`

const Header = styled.div`
  padding: ${({ theme }) => theme.spacing.s};
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textLight};
  display: flex;
  justify-content: space-between;
  align-items: center;
`

const CloseBtn = styled.button`
  background: transparent;
  border: none;
  color: ${({ theme }) => theme.colors.textLight};
  font-size: 1.2rem;
  cursor: pointer;
`

const Content = styled.div`
  flex: 1;
  padding: ${({ theme }) => theme.spacing.m};
  color: ${({ theme }) => theme.colors.textDark};
  overflow-y: auto;
  line-height: 1.5;
`
const Suspicious = styled.div`
  border: 4px solid #800020;
  border-radius: 10px;
  background-color: white;
`

type Props = { onClose: () => void }

export default function AnalysisPanel({ onClose }: { onClose: () => void }) {
  const [loading, setLoading] = useState(true)
  const [data, setData]     = useState<AnalysisResult | null>(null)

  useEffect(() => {
    ;(async () => {
      try {
        const text = getArticleText();
        const result = await analyzeArticle(text)
        setData(result)
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    })()
  }, [])

  // scores 배열에서 left/center/right 점수 꺼내기
  const getScore = (cat: string) =>
    data?.scores.find((s:CategoryScore) => s.category === cat)?.score ?? 0

  const leftScore   = getScore('좌파/진보')
  const centerScore = getScore('중도')
  const rightScore  = getScore('우파/보수')
  
  console.log(data?.trust_issues)

  return (
    <ThemeProvider theme={theme}>
      <PanelWrapper>
        <Header>
          <h3>분석 결과</h3>
          <CloseBtn onClick={onClose}>×</CloseBtn>
        </Header>

        <Content>
          {loading || !data ? (
            '데이터 불러오는 중…'
          ) : (
            <>
              <h1>B.B.</h1>
              <br/>
              {/* 주제 표현 */}
              <p style={{ marginBottom: theme.spacing.m }}>
                <strong>{data.summary}</strong>
              </p>

              {/* 진보·보수 비율 */}
              <h2>1. 성향 분석</h2>
              <BiasBar
                segments={[
                { ratio: rightScore   , color: '#CD1039' /* 진보 */ },
                { ratio: centerScore , color: 'silver' /* 중도 */ },
                { ratio: leftScore  , color: '#0078FF' /* 보수 */ }
              ]}
              />
              <p>
                보수 <strong>{Math.round(rightScore   * 100)}%</strong>  |  
                중도 <strong>{Math.round(centerScore * 100)}%</strong>  |  
                진보 <strong>{Math.round(leftScore  * 100)}%</strong>
              </p>
              {/* 의심요소 목록 */}
              <br/>
              <div>
                <h2>2. 신뢰도 분석</h2>
                <Suspicious>
                  {data.trust_issues.length > 0 && (
                  <>
                    <h4 style={{ marginBottom: theme.spacing.s }}>의심요소</h4>
                    <ol style={{ marginLeft: theme.spacing.m, color: theme.colors.textDark }}>
                      {data.trust_issues.map((item, idx) => (
                        <li key={idx} style={{ marginBottom: theme.spacing.s }}>
                          <strong>{item.reason}</strong><br />
                          <em>"{item.phrase}"</em><br />
                          <span>{item.note}</span>
                        </li>
                      ))}
                    </ol>
                  </>
                    )
                  }
                </Suspicious>
              </div>
            </>
          )}
        </Content>
      </PanelWrapper>
    </ThemeProvider>
  )
}