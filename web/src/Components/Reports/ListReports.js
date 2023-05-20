import { useEffect, useState } from "react";
import { API_HOST } from "../../Config/MainConfig";
import { WARNING, useAlert } from "../../Hooks/Alert";

import { Container, Table } from "react-bootstrap";
import { PencilSquare } from "react-bootstrap-icons";

const ReportsList = () => {
    const [list, setList] = useState([]);
    const {showAlert} = useAlert();

    useEffect(() => {
        fetch(API_HOST + '/problematicCase/')
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
        <Table>
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Data utworzenia</th>
                    <th>Opis</th>
                    <th>Pobierz</th>
                    <th>Usuń</th>
                </tr>
            </thead>
            <tbody>
                {list.map((elem, idx) => <tr key={idx}>
                    <td>{elem['id']}</td>
                    <td>{elem['date']}</td>
                    <td>{elem['description']}</td>
                    <td><Download /></td>
                    <td><Trash3Fill /></td>
                </tr>)}
            </tbody>
        </Table>
        </Container>
    )
}

export default ReportsList;