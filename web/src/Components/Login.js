import { useContext, useState } from "react";
import { Button, Container, Form, InputGroup } from "react-bootstrap"
import { ctxAuth } from "../Hooks/Auth";
import { useNavigate } from "react-router-dom";
import { API_HOST, POST_METHOD, PSC_LINK } from "../Config/MainConfig";
import { WARNING, ctxAlert } from "../Hooks/Alert";
import Cookies from "universal-cookie";
import AuthService from "../Service/AuthService";

const Login = () => {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    // const { auth, setAuth } = useContext(ctxAuth);
    const { showAlert } = useContext(ctxAlert);
    const navigate = useNavigate();
    const cookies = new Cookies();
    const [refresh, setRefresh] = useState(false);

    const handleClick = async () => {
        var res = await logging(login, password, showAlert);
        if(res) {
            setRefresh(!refresh);
            navigate(PSC_LINK);
        }
    }

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
            AuthService.setToken(res['auth_token']);
            return true;
        })
        .catch(err => {
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })

        return success;
    }

    return (
        <>
        <h1 className="pageTitle container">Logowanie</h1>
        <div className="w-100 line"></div>
        <Container>
            <div className="center w-50">
            <InputGroup className="mb-3">
                <InputGroup.Text>Login</InputGroup.Text>
                <Form.Control
                    placeholder="Podaj login"
                    aria-label="Login"
                    type="text"
                    value={login}
                    onChange={(e) => setLogin(e.target.value)}
                />
            </InputGroup>
            <InputGroup className="mb-3">
                <InputGroup.Text>Hasło</InputGroup.Text>
                <Form.Control
                    placeholder="Podaj hasło"
                    aria-label="Hasło"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </InputGroup>

            <Button onClick={handleClick}>Logowanie</Button>
            </div>
        </Container>
        </>
    )
}

export default Login;