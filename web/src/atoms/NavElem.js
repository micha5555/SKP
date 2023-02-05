import React from "react";

export const ACTIVE = 'active';
export const NOTACTIVE = '';

const NavElem = ({text, type}) => {
  return <div
    className={`navElem ${type}`}
  >
    <span>{text}</span>
  </div>
}

export default NavElem;