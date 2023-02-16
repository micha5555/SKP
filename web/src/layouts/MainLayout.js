import React from "react";
import { Outlet } from "react-router";
import Navigation from "../organisms/Navigation"
import Top from "../organisms/Top";

import './css/mainLayout.css';

const MainLayout = () => {
  return <div
    className="mainLayout"
  >
    <Top />
    <div className="content">
      <Navigation />
      <Outlet />
    </div>
  </div>
}

export default MainLayout;