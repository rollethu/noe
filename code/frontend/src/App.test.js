import { normalizeLicencePlate } from "./utils";

test("licence plate normalization", () => {
  expect(normalizeLicencePlate("a")).toBe("A");
  expect(normalizeLicencePlate("a ")).toBe("A");
  expect(normalizeLicencePlate("a b")).toBe("AB");
  expect(normalizeLicencePlate("a b1")).toBe("AB1");
  expect(normalizeLicencePlate("a b1$2")).toBe("AB12");
  expect(normalizeLicencePlate("a b1$--2")).toBe("AB12");
});
