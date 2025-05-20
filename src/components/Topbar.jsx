import { Link, useLocation } from "react-router-dom";
import styled from "styled-components";

const Nav = styled.div`
  display: flex;
  justify-content: center;
  background-color:rgb(133, 42, 12);
  color: #fff3e0;
  padding: 16px;
  gap: 20px;
`;


export default function Navbar() {
  const location = useLocation();

  return (
    <Nav>Bias Buster</Nav>
  );
}