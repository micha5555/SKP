import React, { useState } from "react";
import InputLabel from "../molecules/InputLabel";
import Button from "../atoms/Button";
import { NEUTRAL } from "../atoms/Button";

import './css/login.css';

const Login = () => {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  const authorization = () => {
    console.log('not inplemented')
  }

  return <div
    className="login"
  >
    <InputLabel labelValue={"Login"} inputValue={login} setInputValue={setLogin} placeholder={"Wprowadz login"} />
    <InputLabel labelValue={"Hasło"} inputValue={password} setInputValue={setPassword} placeholder={"Wprowadz hasło"} />
    <Button text={"Logowanie"} type={`${NEUTRAL} authButton`} click={authorization} />
  </div>
}

export default Login;