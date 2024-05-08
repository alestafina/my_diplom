import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage/LoginPage";
import MainPage from "./pages/MainPasge/MainPage";


function App() {
  
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={ <LoginPage /> } />
          <Route path="/main" element={ <MainPage /> } />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
