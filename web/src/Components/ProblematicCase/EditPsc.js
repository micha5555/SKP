import { useContext, useEffect, useMemo, useState } from "react";
import { API_HOST, PSC, PSC_LINK, PUT_METHOD } from "../../Config/MainConfig";
import { useNavigate, useParams } from "react-router-dom";
import { SUCCESS, WARNING, ctxAlert } from "../../Hooks/Alert";
import { Container, InputGroup, Form, Button } from "react-bootstrap";
import withAuthCheck from "../../Hooks/withAuthCheck";
import ReactImageMagnify from "react-image-magnify";
import AuthService from "../../Service/AuthService";
import Map from "../GoogleApiWrapper";

const NPC = 'not_possible_to_check';
const CPA = 'check_if_paid_again';


const EditPsc = () => {
    const navigate = useNavigate();
    const {showAlert} = useContext(ctxAlert);
    const {id} = useParams();

    const [register, setRegister] = useState('');
    const [date, setDate] = useState('');
    const [location, setLocation] = useState(null);
    const [image, setImage] = useState('');
    const [probability, setProbability] = useState('');

    const handleCancel = () => {
        var cancel = window.confirm("Czy na pewno chcesz anulować.");
        if ( !cancel ) {
            return;
        }
        navigate(PSC_LINK);
    }

    const handleSave = (status) => {
        var save = window.confirm("Czy na pewno chcesz zapisać.");
        if ( !save) {
            return;
        }
        const fd = new FormData();
        fd.append('registration', register)
        fd.append('status', status)
        fetch(API_HOST + '/problematicCase/edit/' + id, {
            method: PUT_METHOD,
            headers: {
                "Authorization": 'Bearer ' +  AuthService.getToken(),
            },
            body: fd,
        })
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                return res.text().then(errorMsg => {
                    throw new Error(errorMsg);
                });
            }
        })
        .then(res => {
            showAlert('Zapisano zmiany', SUCCESS);
            navigate(PSC_LINK);
        })
        .catch(err => {
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })
    }

    useEffect(() => {
        fetch(API_HOST + '/problematicCase/' + id, {
            headers: {
                "Authorization": 'Bearer ' +  AuthService.getToken(),
            },
        })
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                return res.text().then(errorMsg => {
                    throw new Error(errorMsg);
                });
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
            console.log(err.message)
            showAlert(err.message, WARNING);
            return false;
        })
    }, [])

    return (
        <>
        <h1 className="pageTitle container">Edytuj przypadek</h1>
        <div className="w-100 line"></div>
        <Container className="mt-4 w-50">

            <div className="w-50 mb-3">
                <ReactImageMagnify
                {...{
                    smallImage: {
                        src: API_HOST + "/" + PSC + "/images/" + image,
                        isFluidWidth: true,
                        className: "image"
                    },
                    largeImage: {
                        src: API_HOST + "/" + PSC + "/images/" + image,
                        width: 600,
                        height: 600,
                    }
                }} />
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
            
            {/* <InputGroup className="mb-3">
                <InputGroup.Text id="Lokalizajca">Lokalizajca</InputGroup.Text>
                <Form.Control
                    placeholder="Lokalizajca"
                    aria-label="Lokalizajca"
                    disabled
                    readOnly
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                />  
            </InputGroup> */}

            {/* <InputGroup className="mb-3">
                <InputGroup.Text id="Prawdopodobieństwo">Prawdopodobieństwo</InputGroup.Text>
                <Form.Control
                    placeholder="Prawdopodobieństwo"
                    aria-label="Prawdopodobieństwo"
                    disabled
                    readOnly
                    value={probability}
                    onChange={(e) => setProbability(e.target.value)}
                />  
            </InputGroup> */}

            {
                location != null 
                ? <Map center={location.split(',').map(p => parseFloat(p))} />
                : null
            }

            <div className="d-flex mb-3 justify-content-between">
                <Button className="my_button" onClick={handleCancel} variant="danger">Anuluj</Button>
                <Button  onClick={() => handleSave(NPC)} variant="secondary">Nie możliwe potwierdzenie</Button>
                <Button className="my_button" onClick={() => handleSave(CPA)} variant="primary">Zapisz poprawienie</Button>
            </div>

        </Container>
        </>
    )
}

export default withAuthCheck(EditPsc);