import React, { useEffect } from "react";
//import products from "../../products";
import { Row, Col } from "react-bootstrap";
import Product from "../Product";
import { useDispatch, useSelector } from "react-redux";
import { listProducts } from "../../actions/ProductAction";
import Message from "../Message";
//import { SearchContext } from "../App";

function HomeScreen() {
  //const searchResults = useContext(SearchContext);
  const dispatch = useDispatch();
  const productList = useSelector((state) => state.productList);
  const { error, products } = productList;

  useEffect(() => {
    dispatch(listProducts());
  }, [dispatch]);

  return (
    <div>
      <h1 className="text-center">Latest Products</h1>
      {/* {searchResults.length > 0 ? (
        <Row>
          {searchResults.map((product) => (
            <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
              <Product product={product} />
            </Col>
          ))}
        </Row>
      ) : ( */}
      <Row>
        {products &&
          products.map((product) => (
            <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
              {/* <h3>{product.name}</h3> */}
              <Product product={product} />
            </Col>
          ))}
      </Row>
    </div>
  );
}

export default HomeScreen;
