import "./App.css";
import "./index.css";
import { Container } from "react-bootstrap";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Footer from "./components/Footer";
import Header from "./components/Header";
import LoginScreen from "./components/screens/LoginScreen";
import RegisterScreen from "./components/screens/RegisterScreen";
import Loader from "./components/Loader";
import React, { lazy, Suspense } from "react";
const Home = lazy(() => import("./components/screens/HomeScreen"));
const Cart = lazy(() => import("./components/screens/CartSreen"));
const Product = lazy(() => import("./components/screens/ProductScreen"));

function App() {
  return (
    <Router>
      <Header />
      <main className="my-3">
        <Suspense fallback={<Loader />}>
          <Container>
            <Route path="/" component={Home} exact />
            <Route path="/login" component={LoginScreen} exact />
            <Route path="/register" component={RegisterScreen} exact />
            <Route path="/product/:id" component={Product} exact />
            <Route path="/cart/:id?" component={Cart} exact />
          </Container>
        </Suspense>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
