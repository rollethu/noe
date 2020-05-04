jest.mock("axios");

import axios from "axios";
import { verifyToken } from "./appointmentContext";

test("Successful verification sets Auth header", async () => {
  axios.post.mockResolvedValue({ data: {} });
  const fakeToken = "fake-token";
  await verifyToken(jest.fn())(fakeToken); // does API call
  expect(axios.defaults.headers.common.Authorization).toBe(
    "Apptoken fake-token"
  );
});
