import {
  legacy_createStore as createStore,
  combineReducers,
  applyMiddleware,
} from "redux";
import thunk from "redux-thunk";
import { composeWithDevTools } from "redux-devtools-extension";
import {
  productListReducers,
  productDetailsReducers,
} from "./reducers/ProductReducers";
import { cartReducer } from "./reducers/CartReducers";
import {
  userLoginReducers,
  userRegisterReducers,
} from "./reducers/UserReducers";

const reducer = combineReducers({
  productList: productListReducers,
  productDetails: productDetailsReducers,
  cart: cartReducer,
  userLogin: userLoginReducers,
  userRegister: userRegisterReducers,
});

let cartItemsFromStorage = [];
if (localStorage.getItem("cartItems")) {
  try {
    cartItemsFromStorage = JSON.parse(localStorage.getItem("cartItems"));
  } catch (e) {
    console.log("Error parsing cart items from local storage:", e);
    cartItemsFromStorage = [];
  }
} else {
  localStorage.setItem("cartItems", JSON.stringify(cartItemsFromStorage));
}

const userInfoFromStorage = localStorage.getItem("userInfo")
  ? JSON.parse(localStorage.getItem("userInfo"))
  : null;

const initialState = {
  cart: { cartItems: cartItemsFromStorage },
  userLogin: { userInfo: userInfoFromStorage },
};

const middleware = [thunk];

const store = createStore(
  reducer,
  initialState,
  composeWithDevTools(applyMiddleware(...middleware))
);

export default store;
