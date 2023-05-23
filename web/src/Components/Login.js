import { useContext, useState } from "react";
import { Button, Container, Form, InputGroup } from "react-bootstrap"
import { ctxAuth } from "../Hooks/Auth";
import { useNavigate } from "react-router-dom";
import { PSC_LINK } from "../Config/MainConfig";
import { ctxAlert } from "../Hooks/Alert";

const Login = () => {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const { logging } = useContext(ctxAuth);
    const { showAlert } = useContext(ctxAlert);
    const navigate = useNavigate();

    const handleClick = async () => {
        var res = await logging(login, password, showAlert);
        if(res) {
            navigate(PSC_LINK);
        }
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