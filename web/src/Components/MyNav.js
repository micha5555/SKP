import { Container, Nav, NavDropdown, Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";
import { PSC_LINK, REPORT_LINK, USER_LINK } from "../Config/MainConfig";

const MyNav = () => {

    return (
        <Navbar bg="dark" expand="lg" variant='dark'>
        <Container>
          <Navbar.Brand>React-Bootstrap</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Link to={USER_LINK}>Użytkownicy</Link>
              <Link to={PSC_LINK}>Problematyczne przypadki</Link>
              <Link to={REPORT_LINK}>Raporty</Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    )
}

export default MyNav;