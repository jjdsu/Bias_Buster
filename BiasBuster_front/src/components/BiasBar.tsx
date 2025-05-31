import React from 'react'
import styled from 'styled-components'
import { theme } from '../theme'

const Container = styled.div`
  width: 100%;
  height: 12px;
  background: ${({ theme }) => theme.colors.secondary};
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: ${({ theme }) => theme.spacing.s};
`

const Segment = styled.div<{ width: number; color: string }>`
  width: ${({ width }) => width}%;
  height: 100%;
  background: ${({ color }) => color};
  float: left;
`
export type SegmentInfo = {
  ratio: number;   // 0~1
  color: string;
}

export default function BiasBar({ segments }: { segments: SegmentInfo[] }) {
  return (
    <Container>
      {segments.map((seg, i) => (
        <Segment
          key={i}
          width={seg.ratio * 100}
          color={seg.color}
        />
      ))}
    </Container>
  )
}
