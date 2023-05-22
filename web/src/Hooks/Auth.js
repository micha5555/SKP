import React, { createContext, useContext, useEffect, useState } from "react";
import { API_HOST, POST_METHOD } from "../Config/MainConfig";
import Cookies from "universal-cookie";
import { WARNING, ctxAlert } from "./Alert";

export const ctxAuth = createContext(); 

export const useAuth = () => {
    const cookies = new Cookies();
    const [auth, setAuth] = useState({
        login: '',
        token: '',
        refreshToken: '',
        isLogged: '',
    })
  
    const logging = async (login_par, password_par, showAlert) => {
        var fd = new FormData();
        fd.append('login', login_par);
        fd.append('password', password_par);
        var success = await fetch(API_HOST + '/login', {
            method: POST_METHOD,
            body: fd,
        })
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                return res.text().then(errorMsg => {
                    throw new Error(errorMsg);
                });
            }
        })
        .then(res => {
            auth.login = login_par;
            auth.isLogged = true;
            auth.token = res['auth_token'];
            auth.refreshToken = res['refresh_token'];
            setAuth(auth);
            cookies.set('auth', auth);
            return true;
        })
        .catch(err => {
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })

        return success;
    }

    const loggout = () => {
        auth.login = '';
        auth.token = '';
        auth.refreshToken = '';
        auth.isLogged = false;
        setAuth(auth);
        cookies.remove('auth');
    }

    const checkIfLogged = () => {
        let auth_c = cookies.get('auth');
        if(auth_c) {
            setAuth(auth_c);
            return true;
        }
        return false;
    }
  
    return { auth, logging, loggout, checkIfLogged };
};

