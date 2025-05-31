// 네이버 뉴스 전용
function extractNaver(): string {
  const articleEl = document.querySelector('article') 
                || document.querySelector('.article-body')
                || document.body
        const text = articleEl.innerText
  return text;
}
// 그외 뉴스 <p> 태그 기반 본문 파악
function extractGeneric(): string {
  // 1) 페이지의 모든 <p> 요소를 수집
  const allPs = Array.from(document.querySelectorAll('p'))
  const containerCount = new Map<HTMLElement, number>()

  // 2) 각 <p> 의 가장 가까운 상위 컨테이너(Article, Section, Div) 기준으로 카운트
  allPs.forEach(p => {
    const parent = p.closest('article, section, div') as HTMLElement || document.body
    containerCount.set(parent, (containerCount.get(parent) || 0) + 1)
  })

  // 3) 카운트가 가장 높은 컨테이너를 선택
  let bestParent = document.body
  let maxCount = 0
  for (const [parent, count] of containerCount.entries()) {
    if (count > maxCount) {
      bestParent = parent
      maxCount = count
    }
  }

  // 4) 그 컨테이너 안의 <p> 들만 가져와서 텍스트로 조합
  const paragraphs = Array.from(bestParent.querySelectorAll('p'))
    .filter(p => p.closest('article, section, div') === bestParent)
    .map(p => p.innerText.trim())
    .filter(t => t.length > 0)

  return paragraphs.join('\n\n')
}

// 도메인별 분기
export function getArticleText(): string {
  const host = location.hostname;
  if (host.includes('news.naver.com')) {
    const t = extractNaver();
    if (t) return t;
  }
  return extractGeneric();
}
