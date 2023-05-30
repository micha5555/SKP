import { useContext, useEffect, useState } from "react";
import { API_HOST } from "../../Config/MainConfig";
import { WARNING, useAlert } from "../../Hooks/Alert";

import { Container, Table } from "react-bootstrap";
import { PencilSquare } from "react-bootstrap-icons";
import withAuthCheck from "../../Hooks/withAuthCheck";
import { ctxAuth } from "../../Hooks/Auth";

const ReportsList = () => {
    const [list, setList] = useState([]);
    const {showAlert} = useAlert();
    const {auth} = useContext(ctxAuth);

    useEffect(() => {
        fetch(API_HOST + '/problematicCase/', {
            headers: {
                "Authorization": 'Bearer ' +  AuthService.getToken(),
            },
        })
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
        <Table striped bordered hover variant="light">
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

export default withAuthCheck(ReportsList);