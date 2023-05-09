import React from "react";

import './css/label.css';

const Label = ({value}) => {
  return <span
    className="label"
  >
    {value}
  </span>
}

export default Label;