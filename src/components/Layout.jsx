
import styled from "styled-components";

const Container = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 16px;
  background-color: #FFF8E1;
  border: 2px solid rgb(133, 42, 12);
  border-radius: 0%;
`;

export default function Layout({ children }) {
  return <Container>{children}</Container>;
}
