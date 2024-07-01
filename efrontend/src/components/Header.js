import React from "react";
import {
  Navbar,
  Nav,
  Container,
  NavDropdown,
  Form,
  Button,
} from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { logout } from "../actions/UserActions";
import { useDispatch, useSelector } from "react-redux";
import { DarkModeSwitch } from "react-toggle-dark-mode";

function Header({ theme, setTheme, searchResults, setSearchResults }) {
  const handleSearch = (e) => {
    setSearchResults(e.target.value);
  };

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const dispatch = useDispatch();

  const logoutHandler = () => {
    dispatch(logout());
  };

  const toggleDarkMode = (checked: boolean) => {
    setTheme(checked ? "dark" : "light");
  };

  return (
    <div>
      <Navbar
        bg={theme === "light" ? "light" : "dark"}
        variant={theme === "light" ? "light" : "dark"}
      >
        <Container>
          <LinkContainer to="/">
            <Navbar.Brand>eCommerce</Navbar.Brand>
          </LinkContainer>
          <Form
            className="d-flex"
            onSubmit={(e) => {
              e.preventDefault();
              setSearchResults(searchResults);
            }}
          >
            <Form.Control
              type="search"
              placeholder="Enter your search here"
              className="me-2 custom-search-input"
              aria-label="Search"
              onChange={handleSearch}
            />
            <Button
              className="custom-search-btn"
              variant="outline-success"
              type="submit"
            >
              Search
            </Button>
          </Form>
          <Navbar.Toggle aria-controls="navbarScroll" />
          <Navbar.Collapse id="navbarScroll">
            <Nav
              className="ms-auto my-2 my-lg-0"
              // style={{ maxHeight: "100px" }}
              navbarScroll
            >
              <LinkContainer to="/">
                <Nav.Link>
                  <i className="fas fa-home"></i> Home
                </Nav.Link>
              </LinkContainer>
              <LinkContainer to="/cart">
                <Nav.Link>
                  <i className="fas fa-shopping-cart"></i> Cart
                </Nav.Link>
              </LinkContainer>
              {userInfo ? (
                <NavDropdown
                  title={userInfo.name}
                  id="username"
                  className="navCstm"
                >
                  <LinkContainer to="/profile">
                    <NavDropdown.Item>Profile</NavDropdown.Item>
                  </LinkContainer>

                  <NavDropdown.Item onClick={logoutHandler}>
                    Logout
                  </NavDropdown.Item>
                </NavDropdown>
              ) : (
                <LinkContainer to="/login">
                  <Nav.Link>
                    <i className="fas fa-user"></i> Login
                  </Nav.Link>
                </LinkContainer>
              )}
              <Nav.Link>
                <DarkModeSwitch
                  //style={{ marginTop: "0rem" }}
                  checked={theme === "dark"}
                  onChange={toggleDarkMode}
                  size={25}
                />
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
}

export default Header;
