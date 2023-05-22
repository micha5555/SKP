import { useNavigate } from "react-router-dom";
import { API_HOST, USER_LINK } from "../../Config/MainConfig";
import { SUCCESS, WARNING, ctxAlert, useAlert } from "../../Hooks/Alert";
import { useContext, useState } from "react";
import { Button, Container, InputGroup, Form } from "react-bootstrap";
import withAuthCheck from "../../Hooks/withAuthCheck";

const AddUser = () => {
    const navigate = useNavigate();
    const {showAlert} = useContext(ctxAlert);

    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [passwordRe, setPasswordRe] = useState('');
    const [is_admin, setIsAdmin] = useState(false);
    const [is_controller, setIsController] = useState(false);

    const addUser = async () => {
        var userAdd = window.confirm("Czy na pewno chcesz zatwierdzić.");
        if ( !userAdd) {
            return;
        }
        const fd = new FormData();
        fd.append('first_name', first_name);
        fd.append('last_name', last_name);
        fd.append('login', login);
        fd.append('password', password);
        fd.append('is_admin', is_admin);
        fd.append('is_controller', is_controller);
        fetch(API_HOST + '/user/add', {
            body: fd,
        })
        .then(res => {
            if (res.ok) {
                return res.json();
            } else {
                throw new Error(res.statusText)
            }
        })
        .then(res => {
            showAlert('Użytkownik utworzony.', SUCCESS);
            navigate(USER_LINK);
        })
        .catch(err => showAlert("nie utworzono", WARNING))
    }

    const canel = () => {
        var cancel = window.confirm("Czy na pewno chcesz anulować.");
        if ( !cancel) {
            return;
        }
        navigate(USER_LINK);
    }

    return (
        <>
        <h1 className="pageTitle container">Dodaj użytkownika</h1>
        <div className="w-100 line"></div>
        <Container className="mt-4 w-50">
            <InputGroup className="mb-3">
                <InputGroup.Text>Imie i Nazwisko</InputGroup.Text>
                <Form.Control
                    placeholder="Imie"
                    aria-label="Imie"
                    value={first_name}
                    onChange={(e) => setFirstName(e.target.value)}
                />
                <Form.Control
                    placeholder="Nazwisko"
                    aria-label="Nazwisko"
                    value={last_name}
                    onChange={(e) => setLastName(e.target.value)}
                />
            </InputGroup>

            <InputGroup className="mb-3">
                <InputGroup.Text id="Login">Login</InputGroup.Text>
                <Form.Control
                    placeholder="Login"
                    aria-label="Login"
                    value={login}
                    onChange={(e) => setLogin(e.target.value)}
                />
            </InputGroup>

            <InputGroup className="mb-3">
                <InputGroup.Text>Hasło</InputGroup.Text>
                <Form.Control
                    placeholder="Hasło"
                    aria-label="Hasło"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Form.Control
                    placeholder="Powtórz hasło"
                    aria-label="Powtórz hasło"
                    type="password"
                    value={passwordRe}
                    onChange={(e) => setPasswordRe(e.target.value)}
                />
            </InputGroup>

            <InputGroup className="mb-3">
                <Form.Control
                    type="text"
                    placeholder="Admin"
                    aria-label="Admin"
                    disabled
                    readOnly 
                    className="borderDisable"
                />
                <InputGroup.Checkbox aria-label="Admin" value={is_admin} onChange={(e) => setIsAdmin(!is_admin)}  />
                <Form.Control
                    type="text"
                    placeholder="Kontroler"
                    aria-label="Kontroler"
                    disabled
                    readOnly 
                    className="borderDisable"
                />
                <InputGroup.Checkbox aria-label="Kontroler" value={is_controller} onChange={(e) => setIsController(!is_controller)}  />
            </InputGroup>

            <div className="d-flex justify-content-between">
                <Button className="my_button" variant="danger" onClick={canel}>Anuluj</Button>
                <Button className="my_button" variant="primary" onClick={addUser}>Zatwierdź</Button>
            </div>
        </Container>
        </>
    )
}

export default  withAuthCheck(AddUser);