import { useNavigate, useParams } from "react-router-dom";
import { API_HOST, PUT_METHOD, USER_LINK } from "../../Config/MainConfig";
import { SUCCESS, WARNING, ctxAlert, useAlert } from "../../Hooks/Alert";
import { useContext, useEffect, useState } from "react";
import { Button, Container, InputGroup, Form } from "react-bootstrap";
import withAuthCheck from "../../Hooks/withAuthCheck";
import { ctxAuth } from "../../Hooks/Auth";
import AuthService from "../../Service/AuthService";

const EditUser = () => {
    const navigate = useNavigate();
    const {showAlert} = useContext(ctxAlert);
    const {auth} = useContext(ctxAuth);

    const {id} = useParams()
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');
    const [login, setLogin] = useState('');
    const [is_admin, setIsAdmin] = useState(false);
    const [is_controller, setIsController] = useState(false);

    useEffect(() => {
        fetch(API_HOST + '/user/' + id, {
            headers: {
                "Authorization": 'Bearer ' +  AuthService.getToken(),
            },
        })
        .then(res => {
            if (res.ok) {
                return res.json();
            } else {
                return res.text().then(errorMsg => {
                    throw new Error(errorMsg);
                });
            }
        }) 
        .then(res => {
            setFirstName(res['first_name']);
            setLastName(res['last_name']);
            setLogin(res['login']);
            setIsAdmin(res['is_admin']);

            setIsController(res['is_controller']);
        })
        .catch(err => {
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })
    }, []);

    const safeUser = () => {
        var safe = window.confirm("Czy na pewno chcesz zapisać zmiany.");
        if ( !safe) {
            return;
        }
        const fd = new FormData();
        fd.append('first_name', first_name);
        fd.append('last_name', last_name);
        fd.append('login', login);
        fd.append('is_admin', is_admin);
        fd.append('is_controller', is_controller);
        fetch(API_HOST + '/user/edit/' + id, {
            body: fd,
            method: PUT_METHOD,
            headers: {
                "Authorization": 'Bearer ' +  AuthService.getToken(),
            },
        })
        .then(res => {
            console.log(res)
            if (res.ok) {
                return res.json();
            } else {
                return res.text().then(errorMsg => {
                    throw new Error(errorMsg);
                });
            }
        })
        .then(res => {
            console.log('eee')
            showAlert('Użytkownik zapisany.', SUCCESS);
            navigate(USER_LINK);
        })
        .catch(err => {
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })
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
        <h1 className="pageTitle container">Edytuj użytkownika</h1>
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
                <Form.Control
                    type="text"
                    placeholder="Admin"
                    aria-label="Admin"
                    disabled
                    readOnly 
                    className="borderDisable"
                />
                <InputGroup.Checkbox aria-label="Admin" checked={is_admin} onChange={(e) => setIsAdmin(!is_admin)}  />
                <Form.Control
                    type="text"
                    placeholder="Kontroler"
                    aria-label="Kontroler"
                    disabled
                    readOnly 
                    className="borderDisable"
                />
                <InputGroup.Checkbox aria-label="Kontroler" checked={is_controller} onChange={(e) => setIsController(!is_controller)}  />
            </InputGroup>

            <div className="d-flex justify-content-between">
                <Button className="my_button" variant="danger" onClick={canel}>Anuluj</Button>
                <Button className="my_button" variant="primary" onClick={safeUser}>Zapisz</Button>
            </div>
        </Container>
        </>
    )
}

export default withAuthCheck(EditUser);