
import { createGlobalStyle } from "styled-components";

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    background-color: ${({ theme }) => theme.colors.background};
    font-family: 'Arial', sans-serif;
    color: ${({ theme }) => theme.colors.text};
  }
`;

export default GlobalStyle;
