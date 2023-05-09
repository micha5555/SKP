import React from "react"; 
import Login from "../organisms/Login";
import Top from "../organisms/Top";

import './css/startLayout.css';

const StartLayout = () => {
  return <div
    className="startLayout"
  >
    <Top />
    <Login />
  </div>
}

export default StartLayout;