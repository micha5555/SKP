import React from "react";
import Title from "../atoms/Title";
import LoginButton from "../atoms/LoginButton";

import './css/top.css';

const Top = () => {
  return <div
    className="top"
  >
    <Title />
    <LoginButton text={'login'}/>
  </div>
}

export default Top;