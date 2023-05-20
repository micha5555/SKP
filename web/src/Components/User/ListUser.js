import { useContext, useEffect, useState } from "react";
import { API_HOST, DELETE_METHOD, USER_ADD_LINK, USER_EDIT_LINK } from "../../Config/MainConfig";
import { INFO, SUCCESS, WARNING, ctxAlert, useAlert } from "../../Hooks/Alert";
import { CheckLg, PencilSquare, Trash3Fill, XLg } from "react-bootstrap-icons";
import { Button, Container, Table } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const UserList = () => {
    const [list, setList] = useState([]);
    const {showAlert} = useContext(ctxAlert);
    const navigate = useNavigate();
    
    const handleDelete = (idx, id) => {
        fetch(API_HOST + '/user/del/' + id, {
            method: DELETE_METHOD
        })
        .then(res => {
            if (res.ok) {
                return res.json();
            } else {
                throw new Error();
            }
        })
        .then(res => {
            setList(list.filter(elem => elem.id !== id));
            showAlert('Usunięto użytkownika.', SUCCESS);
        })
        .catch(err => {
            showAlert('Nie usunięto użytkownika.', WARNING);
        })
    }

    const handleEdit = (id) => {
        navigate(USER_EDIT_LINK + id)
    }

    useEffect(() => {
        fetch(API_HOST + '/user')
        .then(res => {
            if(res.ok) {
                return res.json()
            } else {
                throw new Error('nie działa')
            }
        })
        .then(res => setList(res))
        .catch(err => showAlert(err, WARNING))
    }, [])

    return (
        <Container>
        <div>
            <Button onClick={() => navigate(USER_ADD_LINK)}>Dodaj urzytkownika</Button>
        </div>
        <Table>
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Imie</th>
                    <th>Nazwisko</th>
                    <th>Login</th>
                    <th>Admin</th>
                    <th>Kontroler</th>
                    <th>Edytuj</th>
                    <th>Usuń</th>
                </tr>   
            </thead>
            <tbody>
                {list.map((elem, idx) => <tr key={idx}>
                    <td>{elem['id']}</td>
                    <td>{elem['first_name']}</td>
                    <td>{elem['last_name']}</td>
                    <td>{elem['login']}</td>
                    <td>{elem['is_admin'] === true ? <CheckLg /> : <XLg />}</td>
                    <td>{elem['is_controller'] === true ? <CheckLg /> : <XLg />}</td>
                    <td onClick={() => handleEdit(elem['id'])}><PencilSquare /></td>
                    <td onClick={() => handleDelete(idx, elem['id'])}><Trash3Fill /></td>
                </tr>)}
            </tbody>
        </Table>
        </Container>
    )
}

export default UserList;