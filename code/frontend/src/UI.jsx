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

export function Field({
  value,
  name,
  label,
  type,
  register,
  errors: allErrors,
}) {
  const errors = allErrors[name];
  if (type === "checkbox") {
    return (
      <InputGroup>
        <Label className="Inline">
          <input
            className="Input Inline"
            name={name}
            ref={register()}
            type={type}
            value={value} // Value instead of true
          />
          {label}
        </Label>
        {errors && <HelpBlock error>{errors.message}</HelpBlock>}
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
      {errors && <HelpBlock error>{errors.message}</HelpBlock>}
    </InputGroup>
  );
}

export function InputGroup({ children }) {
  return <div className="InputGroup">{children}</div>;
}

export function Label({ children, className }) {
  return <label className={`Label ${className || ""}`}>{children}</label>;
}

export function Button({ children, type, onClick }) {
  return (
    <button className="Button" type={type || "button"} onClick={onClick}>
      {children}
    </button>
  );
}

export function HelpBlock({ children, error }) {
  return <p>{children}</p>;
}

export function Text({ children, center }) {
  const classes = classNames("Text", { CenterText: center });
  return <p className={classes}>{children}</p>;
}

