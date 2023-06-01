import { useContext, useEffect, useState } from "react";
import { API_HOST } from "../../Config/MainConfig";
import { WARNING, useAlert } from "../../Hooks/Alert";

import { Button, Container, Dropdown, DropdownButton, Form, InputGroup, Table } from "react-bootstrap";
import { Download, PencilSquare, Trash3Fill } from "react-bootstrap-icons";
import withAuthCheck from "../../Hooks/withAuthCheck";
import AuthService from "../../Service/AuthService";

const ReportsList = () => {
    const [list, setList] = useState([]);
    const [fromDate, setFromDate] = useState('');
    const [toDate, setToDate] = useState('');
    const {showAlert} = useAlert();

    const [sorter, setsorter] = useState('id');
    const [sorterValue, setsorterValue] = useState('Id');
    const [type, setType] = useState('asc');
    const [typeValue, setTypeValue] = useState('Rosnąco');
    const [filter, setFilter] = useState('');
    const [filterValue, setFilterValue] = useState('Id');
    const [filterSearch, setFilterSearch] = useState('');
    const [onPage, setOnPage] = useState(15);
    const [page, setPage] = useState(1);

    useEffect(() => {
        fetch(API_HOST + '/report/', {
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
        .then(res => setList(res))
        .catch(err => {
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })
    }, [])

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
        <h1 className="pageTitle container">Raporty</h1>
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
                    <Dropdown.Item onClick={() => handlesorter('creation_date', 'Data')}>Data</Dropdown.Item>
                    <Dropdown.Item onClick={() => handlesorter('start_period', 'Od')}>Do</Dropdown.Item>
                    <Dropdown.Item onClick={() => handlesorter('end_period', 'Do')}>Od</Dropdown.Item>
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
                    <Dropdown.Item onClick={() => handleFilter('creation_date', 'Data')}>Imie</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFilter('start_period', 'Od')}>Od</Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFilter('end_period', 'Do')}>Do</Dropdown.Item>
                </DropdownButton>
                <Form.Control aria-label="Example text with two button addons" />
            </InputGroup>
        </div>
        <div className="d-flex justify-content-between">
            <Button
                variant="dark"
            >
                Stwórz raport
            </Button>
            <div className="d-flex w-25">
                <Button 
                    variant="dark"
                    className="opacity"
                    disabled
                >Data do
                </Button>
                <Form.Control 
                    type="date"  
                    value={fromDate}
                    onChange={(e) => setFromDate(e.target.value)}
                />
            </div>
            <div className="d-flex w-25">
                <Button 
                    variant="dark"
                    className="opacity"
                    disabled
                >Data od
                </Button>
                <Form.Control 
                    type="date" 
                    value={toDate}
                    onChange={(e) => setToDate(e.target.value)}
                />
            </div>
        </div>
        <Table striped bordered hover variant="light">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Data utworzenia</th>
                    <th>Od</th>
                    <th>Do</th>
                    <th>Pobierz</th>
                    <th>Usuń</th>
                </tr>
            </thead>
            <tbody>
                {list.map((elem, idx) => <tr key={idx}>
                    <td>{elem['id']}</td>
                    <td>{elem['creation_date']}</td>
                    <td>{elem['start_period']}</td>
                    <td>{elem['end_period']}</td>
                    <td><Download /></td>
                    <td><Trash3Fill /></td>
                </tr>)}
            </tbody>
        </Table>
        </Container>
        </>
    )
}

export default withAuthCheck(ReportsList);