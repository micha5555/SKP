import React, { createContext, useContext, useEffect, useState } from "react";

export const INFO = 'primary';
export const WARNING = 'danger';
export const SUCCESS = 'success';

export const ctxAlert = createContext(); 

export const useAlert = () => {
    const [show, setShow] = useState(false);
    const [message, setMessage] = useState('');
    const [type, setType] = useState(INFO);
  
    const showAlert = (msg, alertType = INFO) => {
      setShow(true);
      setMessage(msg);
      setType(alertType);
      setTimeout(() => setShow(false), 5000);
    };
  
    return { show, message, type, showAlert };
  };

const Alert = () => {
    const {show, message, type, showAlert} = useContext(ctxAlert);

    return (
      <div>
        {show && (
          <div className={`alert alert-${type}`} role="alert">
            {message}
          </div>
        )}
      </div>
    );
};

export default Alert;