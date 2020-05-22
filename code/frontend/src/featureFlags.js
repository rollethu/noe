const isStaging = process.env.REACT_APP_NODE_ENV === "staging";
const isProduction = process.env.NODE_ENV === "production";

// export const useFeatureSimplePay = !isProduction || isStaging;
export const useFeatureSimplePay = false;
