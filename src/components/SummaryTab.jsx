import { useState } from "react";
import Layout from "./Layout";
import ArticleInput from "./ArticleInput";
import Card from "./Card";

export default function SummaryTab() {
  const [result, setResult] = useState(null);

  return (
    <Layout>
      <h2>요약</h2>
      <ArticleInput onResult={(data) => setResult(data)} />
      <Card>
        {result && (
          <div>
            <p><strong>요약 결과:</strong></p>
            <p>{result.summary}</p>
          </div>
        )}
      </Card>
    </Layout>
  );
}
