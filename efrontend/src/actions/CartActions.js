import axios from "axios";
import { CART_ADD_ITEM, CART_REMOVE_ITEM } from "../constants/CartConstants";

export const addToCart = (id, quantity) => async (dispatch, getState) => {
  try {
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
  } catch (error) {
    console.log("Failed to add item to cart:", error);
  }
};

export const removeFromCart = (id) => (dispatch, getState) => {
  try {
    dispatch({
      type: CART_REMOVE_ITEM,
      payload: id,
    });

    const { userInfo } = getState().userLogin;
    const cartItems = getState().cart.cartItems.filter(
      (item) => item.user === userInfo._id
    );
    localStorage.setItem("cartItems", JSON.stringify(cartItems));
  } catch (error) {
    console.error("Failed to remove item from cart:", error);
  }
};
