import { useEffect, useState } from "react";
import { API_HOST, PSC_EDIT_LINK } from "../../Config/MainConfig";
import { WARNING, useAlert } from "../../Hooks/Alert";

import { Container, Table } from "react-bootstrap";
import { PencilSquare } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const ListPsc = () => {
    const [list, setList] = useState([]);
    const {showAlert} = useAlert();
    const navigate = useNavigate();

    const handleClick = (id) => {
        navigate(PSC_EDIT_LINK + id);
    }

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
    )
}

export default ListPsc;