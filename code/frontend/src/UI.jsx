import React from "react";

export function View({ children }) {
  return (
    <div className="ViewContainer">
      <div className="View">{children}</div>
    </div>
  );
}

export function Caption({ children }) {
  return <h2 className="Caption">{children}</h2>;
}
