import { useEffect, useState } from "react";
import { API_HOST, PSC_EDIT_LINK } from "../../Config/MainConfig";
import { WARNING, useAlert } from "../../Hooks/Alert";

import { Form, Button, Container, Dropdown, DropdownButton, InputGroup, Table } from "react-bootstrap";
import { PencilSquare } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";
import withAuthCheck from "../../Hooks/withAuthCheck";
import { ctxAuth, useAuth } from "../../Hooks/Auth";
import AuthService from "../../Service/AuthService";

const ListPsc = () => {
    const [list, setList] = useState([]);
    const {showAlert} = useAlert();
    const navigate = useNavigate();

    const [sorter, setsorter] = useState('id');
    const [sorterValue, setsorterValue] = useState('Id');
    const [type, setType] = useState('asc');
    const [typeValue, setTypeValue] = useState('Rosnąco');
    const [filter, setFilter] = useState('id');
    const [filterValue, setFilterValue] = useState('Id');
    const [filterSearch, setFilterSearch] = useState('');
    const [onPage, setOnPage] = useState(15);
    const [page, setPage] = useState(1);

    const handleClick = (id) => {
        navigate(PSC_EDIT_LINK + id);
    }

    useEffect(() => {
        handleExecution();
    }, [])

    const handleExecution = (mode = 0) => {
        var url = API_HOST + '/problematicCase/';
        if (mode === 1) {
            url += buildURL();
        }
        fetch(url, {
            headers: {
                "Authorization": 'Bearer ' +  AuthService.getToken(),
            },
        })
        .then(res => {
            if(res.ok) {
                return res.json()
            } else {
                return res.text().then(errorMsg => {
                    throw new Error(errorMsg);
                });
            }
        })
        .then(res => setList([...res]))
        .catch(err => {
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })
    } 

    const buildURL = () => `?filter=${filter}:${filterSearch}&sort_by=${sorter}&order=${type}&per_page=${onPage}&page=${page}`;

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

    return (
        <>
        <h1 className="pageTitle container">Przypadki problematyczne</h1>
        <div className="w-100 line"></div>
        <Container>
            <div className="d-flex">
                <InputGroup className="mb-3 mt-3">
                    <Button onClick={() => handleExecution(1)} variant="dark">Sortuj</Button>
                    <DropdownButton
                    variant="dark"
                    title={sorterValue}
                    id="segmented-button-dropdown-1"
                    >
                        <Dropdown.Item onClick={() => handlesorter('id', 'Id')} >Id</Dropdown.Item>
                        <Dropdown.Item onClick={() => handlesorter('registration', 'Rejestracja')}>Rejestracja</Dropdown.Item>
                        <Dropdown.Item onClick={() => handlesorter('creation_time', 'Data utworzenia')}>Data utworzenia</Dropdown.Item>
                        <Dropdown.Item onClick={() => handlesorter('probability', 'Prawdopodobieństwo')}>Prawdopodobieństwo</Dropdown.Item>
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
                    <Button onClick={() => handleExecution(1)} variant="dark">Wyświetlaj po</Button>
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
                    <Button onClick={() => handleExecution(1)} variant="dark">Filtruj</Button>
                    <DropdownButton
                    variant="dark"
                    title={filterValue}
                    id="segmented-button-dropdown-1"
                    >
                        <Dropdown.Item onClick={() => handleFilter('id', 'Id')} >Id</Dropdown.Item>
                        <Dropdown.Item onClick={() => handleFilter('registration', 'Rejestracja')}>Rejestracja</Dropdown.Item>
                        <Dropdown.Item onClick={() => handleFilter('creation_time', 'Data utworzenia')}>Data utworzenia</Dropdown.Item>
                        <Dropdown.Item onClick={() => handleFilter('probability', 'Prawdopodobieństwo')}>Prawdopodobieństwo</Dropdown.Item>
                    </DropdownButton>
                    <Form.Control aria-label="Example text with two button addons" value={filterSearch} onChange={(e) => setFilterSearch(e.target.value)} />
                </InputGroup>
            </div>

            <Table striped bordered hover variant="light">
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Rejestracja</th>
                        <th>Data utworzenia</th>
                        <th>Lokalizajca</th>
                        <th>Prawdopodobieństwo</th>
                        <th>Rozpatrz</th>
                    </tr>
                </thead>
                <tbody>
                    {list.map((elem, idx) => <tr key={idx}>
                        <td>{elem['id']}</td>
                        <td>{elem['registration']}</td>
                        <td>{elem['creation_time']}</td>
                        <td>{elem['localization']}</td>
                        <td>{elem['probability']}</td>
                        <td onClick={() => handleClick(elem['id'])}><PencilSquare /></td>
                    </tr>)}
                </tbody>
            </Table>
        </Container>
        </>
    )
}

export default withAuthCheck(ListPsc);