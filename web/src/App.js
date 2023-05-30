import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

import "./app.css";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import MainLayout from './Layouts/MainLayout';
import { LOGIN_LINK, PSC, PSC_EDIT_LINK, PSC_LINK, REPORT, REPORT_LINK, USER, USER_ADD_LINK, USER_EDIT_LINK, USER_LINK } from './Config/MainConfig';
import UserList from './Components/User/ListUser';
import PscList from './Components/ProblematicCase/ListPsc';
import AddUser from './Components/User/AddUser';
import EditUser from './Components/User/EditUser';
import { ctxAlert, useAlert } from './Hooks/Alert';
import EditPsc from './Components/ProblematicCase/EditPsc';
import ListPsc from './Components/ProblematicCase/ListPsc';
import { useAuth, ctxAuth } from './Hooks/Auth';
import Login from './Components/Login';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<MainLayout />}>
      <Route path={USER_LINK} element={<UserList />} />
      <Route path={USER_ADD_LINK} element={<AddUser />} />
      <Route path={USER_EDIT_LINK + ":id"} element={<EditUser />} />

      <Route path={PSC_LINK} element={<ListPsc data={PSC} />} />
      <Route path={PSC_EDIT_LINK + ':id'} element={<EditPsc data={PSC} />} />

      {/* <Route path={REPORT_LINK} element={<MyTable data={REPORT} />} /> */}

      <Route path={LOGIN_LINK} element={<Login />} />
 
      <Route index element={<PscList data={PSC} />} />
    </Route>
  )
);

const App = () => {
  const {show, message, type, showAlert} = useAlert();
  const {auth, setAuth, logging, loggout, checkIfLogged } = useAuth();

  return (
    <ctxAuth.Provider value={{auth, setAuth, logging, loggout, checkIfLogged}}>
    <ctxAlert.Provider value={{show, message, type, showAlert}}>
      <RouterProvider router={router} />  
    </ctxAlert.Provider>
    </ctxAuth.Provider>
  )  
}

export default App;