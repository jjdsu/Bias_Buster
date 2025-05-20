import Layout from "./Layout";
import ArticleInput from "./ArticleInput";
import { useState } from "react";

export default function AnalysisTab() {
  const [result, setResult] = useState(null);
  
  return (
    <Layout>
      <h2>분석</h2>
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
