import React from "react";

const Input = ({value, setValue, placeholder, type}) => {
  return <input 
    className="input"
    type={type}
    placeholder={placeholder}
    value={value}
    onChange={setValue}
  />
}

export default Input;