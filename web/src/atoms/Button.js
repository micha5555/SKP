import React from "react";

import './css/button.css';

export const LOUG = 'loud';
export const NEUTRAL = 'neutral';
export const SLITEN = 'silent';
export const QUIET = 'quiet';

const Button = ({
  text, 
  type = NEUTRAL, 
  click,
}) => {
  return <button
    className={`button ${type}`}
    onClick={click}  
  >
    <span>{text}</span>
  </button>
}
export default Button;