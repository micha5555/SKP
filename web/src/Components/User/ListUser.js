import { useContext, useEffect, useState } from "react";
import { API_HOST, DELETE_METHOD, USER_ADD_LINK, USER_EDIT_LINK } from "../../Config/MainConfig";
import { INFO, SUCCESS, WARNING, ctxAlert, useAlert } from "../../Hooks/Alert";
import { CheckLg, PencilSquare, Trash3Fill, XLg } from "react-bootstrap-icons";
import { Button, Container, Dropdown, Form, InputGroup, Table, SplitButton, DropdownButton } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import withAuthCheck from "../../Hooks/withAuthCheck";

const UserList = () => {
    const [list, setList] = useState([]);
    const {showAlert} = useContext(ctxAlert);
    const [sorter, setsorter] = useState('id');
    const [sorterValue, setsorterValue] = useState('Id');
    const [type, setType] = useState('asc');
    const [typeValue, setTypeValue] = useState('Rosnąco');
    const [filter, setFilter] = useState('');
    const [filterValue, setFilterValue] = useState('Id');
    const [filterSearch, setFilterSearch] = useState('');
    const [onPage, setOnPage] = useState(15);
    const [page, setPage] = useState(1);
    const navigate = useNavigate();

    const handleDelete = (idx, id) => {
        var userDelete = window.confirm("Czy na pewno chcesz usunąć użytkownika o id = " + id + ".");
        if ( !userDelete) {
            return;
        }
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

    const handlesorter = (type, value) => {
        setsorter(type);
        setsorterValue(value);
    }

    const handleFilter = (type, value) => {
        setFilter(type);
        setFilterValue(value);
    }

    const handleType = (type, value) => {
        setType(type);
        setTypeValue(value);
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
        <>
        <h1 className="pageTitle container">Użytkownicy</h1>
        <div className="w-100 line"></div>
        <Container>
        <div className="d-flex">
            <InputGroup className="mb-3 mt-3">
                <Button variant="dark">Sortuj</Button>
                <DropdownButton
                variant="dark"
                title={sorterValue}
                id="segmented-button-dropdown-1"
                >
                    <Dropdown.Item onClick={() => handlesorter('id', 'Id')} >Id</Dropdown.Item>
                    <Dropdown.Item onClick={() => handlesorter('first_name', 'Imie')}>Imie</Dropdown.Item>
                    <Dropdown.Item onClick={() => handlesorter('last_name', 'Nazwisko')}>Nazwisko</Dropdown.Item>
                    <Dropdown.Item onClick={() => handlesorter('login', 'Login')}>Login</Dropdown.Item>
                    <Dropdown.Item onClick={() => handlesorter('is_admin', 'Admin')}>Admin</Dropdown.Item>
                    <Dropdown.Item onClick={() => handlesorter('is_controller', 'Kontroler')}>Kontroler</Dropdown.Item>
                </DropdownButton>
                <DropdownButton
                variant="dark"
                className="disable"
                title={typeValue}
                id="segmented-button-dropdown-1"
                >
                    <Dropdown.Item onClick={() => handleType('asc', 'Rosnąco')} >Rosnąco</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleType('desc', 'Malejąco')}>Malejąco</Dropdown.Item>
                </DropdownButton>
            </InputGroup>

            <InputGroup className="mb-3 mt-3">
                <Button variant="dark">Wyświetlaj po</Button>
                <DropdownButton
                variant="dark"
                title={onPage}
                id="segmented-button-dropdown-1"
                >
                    <Dropdown.Item onClick={() => setOnPage(15)} >15</Dropdown.Item>
                    <Dropdown.Item onClick={() => setOnPage(25)} >25</Dropdown.Item>
                    <Dropdown.Item onClick={() => setOnPage(50)} >50</Dropdown.Item>
                </DropdownButton>
            </InputGroup>

            <InputGroup className="mb-3 mt-3">
                <Button variant="dark">Filtruj</Button>
                <DropdownButton
                variant="dark"
                title={filterValue}
                id="segmented-button-dropdown-1"
                >
                    <Dropdown.Item onClick={() => handleFilter('id', 'Id')} >Id</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFilter('first_name', 'Imie')}>Imie</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFilter('last_name', 'Nazwisko')}>Nazwisko</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFilter('login', 'Login')}>Login</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFilter('is_admin', 'Admin')}>Admin</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFilter('is_controller', 'Kontroler')}>Kontroler</Dropdown.Item>
                </DropdownButton>
                <Form.Control aria-label="Example text with two button addons" />
            </InputGroup>
        </div>
        <Table striped bordered hover variant="light">
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
                {list.sort((a,b) => a[sorter] > b[sorter]).map((elem, idx) => <tr key={idx}>
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
        </>
    )
}

export default withAuthCheck(UserList);