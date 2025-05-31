export type Category = '좌파/진보' | '중도' | '우파/보수';
export type Class = 'reason' | 'phrase' | 'note';

export interface CategoryScore {
  category: Category;
  score: number;          // 0 ~ 1 사이
}

export interface Trust {
  reason: string;
  phrase: string;
  note: string;          // 0 ~ 1 사이
}

export interface AnalysisResult {
  summary: string;
  scores: CategoryScore[]; // 진보·중도·보수 점수 배열
  trust_issues: Trust[];
}

export async function analyzeArticle(text: string): Promise<AnalysisResult> {
  const base = import.meta.env.VITE_API_URL
  console.log('API URL:', base);
  const response = await fetch(`${base}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  console.log('[분석 결과]', response.body)
  if (!response.ok) throw new Error('분석 실패');
  // topic이 포함된 JSON을 그대로 파싱
  return await response.json();
}
