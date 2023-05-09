import React from "react";

import './css/navElem.css';

const NavElem = ({text, type}) => {
  return <div
    className={`navElem`}
  >
    <span>{text}</span>
  </div>
}

export default NavElem;