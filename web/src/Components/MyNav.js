import { Button, Container, Nav, NavDropdown, Navbar } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { LOGIN_LINK, PSC_LINK, REPORT_LINK, USER_LINK } from "../Config/MainConfig";
import { useContext } from "react";
import { ctxAuth } from "../Hooks/Auth";

const MyNav = () => {
    const { auth, loggout } = useContext(ctxAuth);
    const navigate = useNavigate();

    const handleClick = () => {
      if(auth.isLogged) {
        var log = window.confirm("Czy na pewno chcesz się wylogować.");
        if ( !log) {
            return;
        }
        loggout();
      }
      navigate(LOGIN_LINK);
    }

    return (
        <Navbar bg="dark" expand="lg" variant='dark'>
        <Container>
          <Navbar.Brand>System Kontroil Parkowania</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="d-flex basic-navbar-nav">
            <Nav className="me-auto d-flex nav align-items-center">
              <Link className="link " to={USER_LINK}>Użytkownicy</Link>
              <Link className="link" to={PSC_LINK}>Problematyczne przypadki</Link>
              <Link className="link" to={REPORT_LINK}>Raporty</Link>
              <div className="loginlogout">
                {/* <p className="login">{auth.isLogged ? "Zalogowany jako " + auth.login : null}</p> */}
                <Button variant="dark" onClick={handleClick}>{auth.isLogged ? "Wyloguj" : "Zaloguj"}</Button>
              </div>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    )
}

export default MyNav;