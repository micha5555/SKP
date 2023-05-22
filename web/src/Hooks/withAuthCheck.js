import React, { useContext } from 'react';
import { ctxAuth } from './Auth';
import { useNavigate } from 'react-router-dom';
import { LOGIN_LINK } from '../Config/MainConfig';
import Login from '../Components/Login';

const withAuthCheck = (WrappedComponent) => {
  const AuthCheckComponent = (props) => {
    const { auth, checkIfLogged } = useContext(ctxAuth);
    
    if (auth.isLogged || checkIfLogged()) {
      return <WrappedComponent {...props} />;
    } else {
      return <Login />;
    }
  };

  return AuthCheckComponent;
};

export default withAuthCheck;
