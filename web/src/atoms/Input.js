import React from "react";

import './css/input.css';

const Input = ({value, setValue, placeholder}) => {
  const handleChange = (e) => {
    setValue(e.target.value);
  }
  
  return <input 
    className="input"
    placeholder={placeholder}
    value={value}
    onChange={handleChange}
  />
}

export default Input;