import { placeholder } from "@babel/types";
import React, { useState } from "react";

import Input from "../atoms/Input";
import Label from '../atoms/Label'

const InputLabel = ({
  labelValue,
  inputValue,
  placeholder,
}) => {
  const [inputValue, setInputValue] = useState(inputValue);

  return <div
    className="inputValue"
  >
    <Label value={labelValue} />
    <Input value={inputValue} setValue={setInputValue} placeholder={placeholder} />
  </div>
}

export default InputLabel;