import React from "react";

export function View({ children }) {
  return <div className="View">{children}</div>;
}

export function Caption({ children }) {
  return <h2 className="Caption">{children}</h2>;
}
