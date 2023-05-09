import React from "react";

import './css/loginButton.css';

const Button = ({text}) => {
  return <button
    className={`loginButton`}
  >
    <span>{text}</span>
  </button>
}
export default Button;