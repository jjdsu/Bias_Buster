
import styled from "styled-components";

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 16px;
`;

export default function Layout({ children }) {
  return <Container>{children}</Container>;
}
