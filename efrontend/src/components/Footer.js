import React from "react";
import { Container, Row, Col } from "react-bootstrap";

function Footer() {
  return (
    <footer>
      <Container>
        <Row>
          <Col className="text-center py-0">
            Copyrights @copy Khaled Ben Yahya 2022
          </Col>
        </Row>
      </Container>
    </footer>
  );
}

export default Footer;
