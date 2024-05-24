import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage/LoginPage";
import MainPage from "./pages/MainPasge/MainPage";
import NewMeetPage from "./pages/NewMeetPage/NewMeetPage";
import MyTeamsPage from "./pages/MyTeamsPage/MyTeamsPage";
import ActiveMeetPage from "./pages/ActiveMeetPage/ActiveMeetPage";
import Nav from "./components/Nav/Nav";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/main" element={<><Nav /><MainPage /></>} />
        <Route path="/new_meeting" element={<><Nav /><NewMeetPage /></>} />
        <Route path="/my_teams" element={<><Nav /><MyTeamsPage /></>}/>
        <Route path="/active_meetings" element={<><Nav /><ActiveMeetPage /></>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
