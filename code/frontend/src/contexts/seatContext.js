import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  seats: [
    {
      url:
        "http://localhost:8000/api/seats/44145d4a-017a-4075-8097-552391da39b5/",
      created_at: "2020-04-23T13:16:44.451737+02:00",
      full_name: "User1",
      birth_date: "1231-12-03",
      healthcare_number: "",
      identity_card_number: "123",
      post_code: "123",
      city: "123",
      address_line1: "1231",
      address_line2: "",
      has_doctor_referral: false,
      email: "asd@asd.com",
      phone_number: "+36 20 123 1231",
      appointment:
        "http://localhost:8000/api/appointments/35bd70e1-831b-41b4-812c-b0b45b4abd0f/",
    },
  ],
  activeSeat: {
    url:
      "http://localhost:8000/api/seats/44145d4a-017a-4075-8097-552391da39b5/",
    created_at: "2020-04-23T13:16:44.451737+02:00",
    full_name: "User1",
    birth_date: "1231-12-03",
    healthcare_number: "",
    identity_card_number: "123",
    post_code: "123",
    city: "123",
    address_line1: "1231",
    address_line2: "",
    has_doctor_referral: false,
    email: "asd@asd.com",
    phone_number: "+36 20 123 1231",
    appointment:
      "http://localhost:8000/api/appointments/35bd70e1-831b-41b4-812c-b0b45b4abd0f/",
  }, // To update existing seat
};

const seatReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_SEATS:
      return {
        ...state,
        seats: [...state.seats, ...action.payload],
      };
    case consts.ADD_SEAT:
      return {
        ...state,
        seats: [...state.seats, action.payload],
        activeSeat: action.payload,
      };
    case consts.DELETE_SEAT:
      return {
        ...state,
        seats: state.seats.filter((seat) => seat.url !== action.payload),
      };
    case consts.SET_ACTIVE_SEAT:
      return {
        ...state,
        activeSeat: action.payload,
      };
    case consts.UPDATE_SEAT:
      return {
        ...state,
        seats: state.seats.map((seat) => {
          if (seat.url === action.payload.url) {
            return action.payload;
          }
          return seat;
        }),
      };
    default:
      return state;
  }
};

const createSeat = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.SEAT_LIST_URL, values);
    dispatch({ type: consts.ADD_SEAT, payload: response.data });
    response.error = false;
    return response;
  } catch (error) {
    const { response } = error;
    if (!response) {
      return {
        error: true,
      };
    }
    response.error = true;
    response.errors = response.data;
    return response;
  }
};

const updateSeat = (dispatch) => async (seatUrl, values) => {
  try {
    const response = await axios.patch(seatUrl, values);
    dispatch({ type: consts.UPDATE_SEAT, payload: response.data });
    response.error = false;
    return response;
  } catch (error) {
    const { response } = error;
    if (!response) {
      return {
        error: true,
      };
    }
    response.error = true;
    response.errors = response.data;
    return response;
  }
};

const deleteSeat = (dispatch) => async (seatUrl) => {
  try {
    const response = await axios.delete(seatUrl);
    dispatch({ type: consts.DELETE_SEAT, payload: seatUrl });
    response.error = false;
    return response;
  } catch (error) {
    const { response } = error;
    if (!response) {
      return {
        error: true,
      };
    }
    response.error = true;
    response.errors = response.data;
    return response;
  }
};

const setActiveSeat = (dispatch) => (seat) => {
  dispatch({ type: consts.SET_ACTIVE_SEAT, payload: seat });
};

export const { Provider, Context } = createContext(
  seatReducer,
  {
    createSeat,
    deleteSeat,
    setActiveSeat,
    updateSeat,
  },
  initialState
);
