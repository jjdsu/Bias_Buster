import { Link, useLocation } from "react-router-dom";
import styled from "styled-components";

const Nav = styled.div`
  display: flex;
  justify-content: center;
  background-color: #fff3e0;
  padding: 16px;
  gap: 20px;
`;

const Tab = styled(Link)`
  font-weight: bold;
  color: ${({ active }) => (active ? "#d32f2f" : "#888")};
  text-decoration: none;
  border-bottom: ${({ active }) => (active ? "2px solid #d32f2f" : "none")};
  padding-bottom: 4px;
`;

export default function Navbar() {
  const location = useLocation();

  return (
    <Nav>
      <Tab to="/trust" active={location.pathname === "/trust" ? 1 : 0}>신뢰도 측정</Tab>
      <Tab to="/summary" active={location.pathname === "/summary" ? 1 : 0}>기사 요약</Tab>
      <Tab to="/analysis" active={location.pathname === "/analysis" ? 1 : 0}>기사 분석</Tab>
    </Nav>
  );
}
