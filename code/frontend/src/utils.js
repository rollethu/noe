export function normalizeLicencePlate(licencePlate) {
  return licencePlate.toUpperCase().replace(/[^A-Z0-9]/g, "");
}
