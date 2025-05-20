
import { useState } from "react";
import Layout from "./Layout";
import ArticleInput from "./ArticleInput";

export default function TrustTab() {
  const [result, setResult] = useState(null);

  return (
    <Layout>
      <h2>기사 신뢰도 측정</h2>
      <ArticleInput onResult={(data) => setResult(data)} />
      {result && (
        <div>
          <p><strong>신뢰도 점수:</strong> {result.trustScore}</p>
          <p><strong>설명:</strong> {result.explanation}</p>
        </div>
      )}
    </Layout>
  );
}
