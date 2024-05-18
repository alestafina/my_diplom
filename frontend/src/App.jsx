import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage/LoginPage";
import MainPage from "./pages/MainPasge/MainPage";
import NewMeetPage from "./pages/NewMeetPage/NewMeetPage";
import Nav from "./components/Nav/Nav";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/main" element={<><Nav /><MainPage /></>} />
        <Route path="/new_meeting" element={<><Nav /><NewMeetPage /></>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
