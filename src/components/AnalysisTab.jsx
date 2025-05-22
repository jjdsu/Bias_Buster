import Layout from "./Layout";
import ArticleInput from "./ArticleInput";
import { useState } from "react";
import Card from "./Card";

export default function AnalysisTab() {
  const [result, setResult] = useState(null);
  
  return (
    <Layout>
      <h2>분석</h2>
      <ArticleInput onResult={(data) => setResult(data)} />
      <Card>
        {result && (
          <div>
            <p><strong>분석 결과:</strong></p>
            <p>{result.analysis}</p>
          </div>
        )}
      </Card>
    </Layout>
  );
}
