import { useContext, useEffect, useState } from "react";
import { API_HOST, PSC_EDIT_LINK, PSC_LINK, PUT_METHOD } from "../../Config/MainConfig";
import { isRouteErrorResponse, useNavigate, useParams } from "react-router-dom";
import { SUCCESS, WARNING, ctxAlert } from "../../Hooks/Alert";
import { Container, InputGroup, Form, Button } from "react-bootstrap";

const NPC = 'not_possible_to_check';
const CPA = 'check_if_paid_again';


const EditPsc = () => {
    const navigate = useNavigate();
    const {showAlert} = useContext(ctxAlert);
    const {id} = useParams();

    const [register, setRegister] = useState('');
    const [date, setDate] = useState('');
    const [location, setLocation] = useState('');
    const [image, setImage] = useState('');
    const [probability, setProbability] = useState('');

    const handleCancel = () => {
        navigate(PSC_LINK);
    }

    const handleSave = (status) => {
        const fd = new FormData();
        fd.append('registration', register)
        fd.append('status', status)
        fetch(API_HOST + '/problematicCase/edit/' + id, {
            method: PUT_METHOD,
            body: fd,
        })
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                throw new Error();
            }
        })
        .then(res => {
            showAlert('Zapisano zmiany', SUCCESS);
            navigate(PSC_LINK);
        })
        .catch(err => {
            showAlert('Nie zapisano zmian', WARNING);
        })
    }

    useEffect(() => {
        fetch(API_HOST + '/problematicCase/' + id)
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                throw new Error();
            }
        })
        .then(res => {
            setRegister(res['registration'])
            setDate(res['creation_time'])
            setLocation(res['localization'])
            setImage(res['image'])
            setProbability(res['probability'])
        })
        .catch(err => {
            console.log('nie')
        })
    }, [])

    return (
        <Container>

            <div>
                image viewer
                <img alt="" src="" />
            </div>

            <InputGroup className="mb-3">
                <InputGroup.Text id="Rejestracja">Rejestracja</InputGroup.Text>
                <Form.Control
                    placeholder="Rejestracja"
                    aria-label="Rejestracja"
                    value={register}
                    onChange={(e) => setRegister(e.target.value)}
                />  
            </InputGroup>

            <InputGroup className="mb-3">
                <InputGroup.Text id="Czas rejestracji">Czas rejestracji</InputGroup.Text>
                <Form.Control
                    placeholder="Czas rejestracji"
                    aria-label="Czas rejestracji"
                    disabled
                    readOnly
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />  
            </InputGroup>
            
            <InputGroup className="mb-3">
                <InputGroup.Text id="Lokalizajca">Lokalizajca</InputGroup.Text>
                <Form.Control
                    placeholder="Lokalizajca"
                    aria-label="Lokalizajca"
                    disabled
                    readOnly
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                />  
            </InputGroup>

            <InputGroup className="mb-3">
                <InputGroup.Text id="Prawdopodobieństwo">Prawdopodobieństwo</InputGroup.Text>
                <Form.Control
                    placeholder="Prawdopodobieństwo"
                    aria-label="Prawdopodobieństwo"
                    disabled
                    readOnly
                    value={probability}
                    onChange={(e) => setProbability(e.target.value)}
                />  
            </InputGroup>

            <div className="d-flex">
                <Button onClick={handleCancel} variant="danger">Anuluj</Button>
                <Button onClick={() => handleSave(NPC)} variant="secondary">Nie możliwe potwierdzenie</Button>
                <Button onClick={() => handleSave(CPA)} variant="primary">Zapisz poprawienie</Button>
            </div>

        </Container>
    )
}

export default EditPsc;