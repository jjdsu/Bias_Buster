
import styled from "styled-components";

const Card = styled.div`
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-top: 16px;
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-4px);
  }
`;

export default Card;
