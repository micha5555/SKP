import React from "react";

 export const LOUG = 'loud';
 export const NEUTRAL = 'neutral';
 export const SLITEN = 'silent';
 export const QUIET = 'quiet';

const Button = ({
  text, 
  type = NEUTRAL, 
  handleClick = () => {console.log('brak komendy')}
}) => {
  return <button
    className={`button ${type}`}
    onClick={handleClick}  
  >
    <span>{text}</span>
  </button>
}
export default Button;