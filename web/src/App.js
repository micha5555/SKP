import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import StartLayout from "./layouts/StartLayout";
import MainLayout from "./layouts/MainLayout";
import Login from "./organisms/Login";
import ShowPCView from "./views/ShowPCView";


import "./app.css";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login/" element={<StartLayout />}>
          <Route index element={<Login />} />
        </Route>
        <Route path="/" element={<MainLayout />} >
          <Route index element={<ShowPCView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )  
}

export default App;