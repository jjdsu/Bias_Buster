import { useState } from "react";
import styled from "styled-components";
import axios from "axios";

const InputBox = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
`;

const Button = styled.button`
  background-color: ${({ theme }) => theme.colors.primary};
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
`;

export default function ArticleInput({ onResult }) {
  const [url, setUrl] = useState("");

  const handleSubmit = async () => {
    try {
      const res = await axios.post("http://localhost:5000/analyze", { url });
      onResult(res.data);
    } catch (err) {
      console.error("분석 실패:", err);
      alert("URL 읽기에 실패했습니다.");
    }
  };

  return (
    <InputBox>
      <Input
        type="text"
        placeholder="뉴스 기사 URL을 입력하세요"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <Button onClick={handleSubmit}>확인</Button>
    </InputBox>
  );
}
