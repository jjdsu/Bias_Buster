import { useState } from "react";
import Layout from "./Layout";
import ArticleInput from "./ArticleInput";
import Card from "./Card";

export default function TrustTab() {
  const [result, setResult] = useState(null);

  return (
    <Layout>
      <h2>기사 신뢰도 측정</h2>
      <ArticleInput onResult={(data) => setResult(data)} />
      <Card>
        {result && (
          <div>
            <p><strong>신뢰도 점수:</strong> {result.trustScore}</p>
            <p><strong>설명:</strong> {result.explanation}</p>
          </div>
        )}
      </Card>
      <Card>
        <h2>신뢰도 측정 기준</h2>
        <p>
          <ul>
            <li>기사를 제공하는 매체나 기관이 공신력이 있는 곳인가?</li>
            <li>기사에서 인용형 정보나 데이터의 출처가 명확하게 제시되었는가?</li>
            <li>기사가 특정 편향 없이 공정하게 작성되었는가?</li>
            <li>해당 기사의 관련자들이 충분한 지식과 경험을 갖추었는가?</li>
            <li>최신 정보를 사용하고 있는가?</li>
          </ul>
        </p>
      </Card>
    </Layout>
  );
}
