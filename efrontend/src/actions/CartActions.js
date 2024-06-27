import axios from "axios";
import { CART_ADD_ITEM, CART_REMOVE_ITEM } from "../constants/CartConstants";

export const addToCart = (id, quantity) => async (dispatch, getState) => {
  const { data } = await axios.get(`/api/products/${id}`);
  const { userInfo } = getState().userLogin;

  const cartItem = {
    product: data._id,
    name: data.name,
    image: data.image,
    price: data.price,
    countInStock: data.countInStock,
    quantity,
  };

  dispatch({
    type: CART_ADD_ITEM,
    payload: cartItem,
  });

  const cartItems = getState().cart.cartItems.filter(
    (item) => item.user === userInfo._id
  );
  localStorage.setItem("cartItems", JSON.stringify(cartItems));
};

export const removeFromCart = (id) => (dispatch, getState) => {
  dispatch({
    type: CART_REMOVE_ITEM,
    payload: id,
  });

  const { userInfo } = getState().userLogin;
  const cartItems = getState().cart.cartItems.filter(
    (item) => item.user === userInfo._id
  );
  localStorage.setItem("cartItems", JSON.stringify(cartItems));
};
