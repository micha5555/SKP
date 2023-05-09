import React, { useState } from "react";
import Input from "../atoms/Input";
import Label from '../atoms/Label';

import "./css/inputLabel.css";

const InputLabel = ({
  labelValue,
  inputValue,
  setInputValue,
  placeholder,
}) => {

  return <div
    className="inputLabel"
  >
    <Label value={labelValue + ":"} />
    <Input value={inputValue} setValue={setInputValue} placeholder={placeholder} />
  </div>
}

export default InputLabel;