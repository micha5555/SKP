import React from "react";

const Button = ({text}) => {
  return <button
    className={`loginButton`}
  >
    <span>{text}</span>
  </button>
}
export default Button;