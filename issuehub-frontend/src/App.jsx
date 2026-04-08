import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Projects from "./pages/Projects";
import Issues from "./pages/Issues";
import IssueDetail from "./pages/IssueDetail";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/projects" element={<Projects />} />
      <Route path="/issues/:projectId" element={<Issues />} />
      <Route path="/issue/:id" element={<IssueDetail />} />
    </Routes>
  );
}

export default App;