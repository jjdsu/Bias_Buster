
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import GlobalStyle from "./GlobalStyle";
import theme from "./theme";

import Navbar from "./components/Navbar";
import TrustTab from "./components/TrustTab";
import SummaryTab from "./components/SummaryTab";
import AnalysisTab from "./components/AnalysisTab";
import Topbar from "./components/Topbar"

function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <Router>
        <Topbar/>
        <Navbar />
        <Routes>
          <Route path="/" element={<TrustTab />} />
          <Route path="/trust" element={<TrustTab />} />
          <Route path="/summary" element={<SummaryTab />} />
          <Route path="/analysis" element={<AnalysisTab />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
