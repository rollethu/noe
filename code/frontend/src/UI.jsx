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

export function Form({ children, onSubmit }) {
  return (
    <form className="Form" onSubmit={onSubmit}>
      {children}
    </form>
  );
}

export function Field({ name, label, type, register }) {
  if (type === "checkbox") {
    return (
      <InputGroup>
        <Label className="Inline">
          <input
            className="Input Inline"
            name={name}
            ref={register()}
            type={type}
          />
          {label}
        </Label>
      </InputGroup>
    );
  }
  return (
    <InputGroup>
      {label && <Label>{label}</Label>}
      <input
        className="Input"
        name={name}
        ref={register()}
        type={type || "text"}
      />
    </InputGroup>
  );
}

export function InputGroup({ children }) {
  return <div className="InputGroup">{children}</div>;
}
export function Label({ children, className }) {
  return <label className={`Label ${className || ""}`}>{children}</label>;
}
