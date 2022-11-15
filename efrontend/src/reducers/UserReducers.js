import {
  USER_LOGIN_REQUEST,
  USER_LOGIN_SUCCESS,
  USER_LOGIN_FAIL,
  USER_LOGOUT,
} from "../constants/UserConstants";

export const userLoginReducers = (state = { userInfo: [] }, action) => {
  switch (action.type) {
    case USER_LOGIN_REQUEST:
      return { loading: true, user: [] };

    case USER_LOGIN_SUCCESS:
      return { loading: false, userInfo: action.payload };

    case USER_LOGIN_FAIL:
      return {
        loading: false,
        error: action.payload,
      };

    case USER_LOGOUT:
      return {};

    default:
      return state;
  }
};
