import React, { useContext } from 'react';
import Login from '../Components/Login';
import AuthService from '../Service/AuthService';

const withAuthCheck = (WrappedComponent) => {
  const AuthCheckComponent = (props) => {    
    if (AuthService.getToken() != null) {
      return <WrappedComponent {...props} />;
    } else {
      return <Login />;
    }
  };

  return AuthCheckComponent;
};

export default withAuthCheck;
