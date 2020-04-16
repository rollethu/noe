import React from "react";
import classNames from "classnames";

export function View({ children }) {
  return (
    <div className="ViewContainer">
      <div className="View">{children}</div>
    </div>
  );
}

export function Caption({ children, ...props }) {
  const classes = classNames("Caption", { CenterText: props.center });
  return <h2 className={classes}>{children}</h2>;
}
