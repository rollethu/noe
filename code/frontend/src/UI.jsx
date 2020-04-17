import React from "react";
import classNames from "classnames";
import { Link } from "react-router-dom";

export function View({ children }) {
  return (
    <div className="ViewContainer">
      <div className="View">{children}</div>
    </div>
  );
}

export function Caption({ children, ...props }) {
  const classes = classNames("Caption", "Text", { CenterText: props.center });
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
  options,
  hidden,
}) {
  const errors = allErrors[name];
  return (
    <InputGroup hidden={hidden}>
      {type === "checkbox" ? (
        <Label htmlFor={name}>
          <Input
            value={value}
            name={name}
            label={label}
            type={type}
            register={register}
            options={options}
            id={name}
          />
          {label}
        </Label>
      ) : (
        <>
          {label && <Label htmlFor={name}>{label}</Label>}
          <Input
            value={value}
            name={name}
            label={label}
            type={type}
            register={register}
            options={options}
            id={name}
          />
        </>
      )}
      {errors && <HelpBlock error>{errors.message}</HelpBlock>}
    </InputGroup>
  );
}

export function Input({ value, name, type, register, options }) {
  if (type === "checkbox") {
    return (
      <input
        id={name}
        className="Input Inline"
        name={name}
        ref={register()}
        type={type}
        value={value} // Value instead of true
      />
    );
  } else if (type === "select") {
    return (
      <select className="Input" name={name} ref={register()} type={type}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.text}
          </option>
        ))}
      </select>
    );
  }
  return (
    <input
      className="Input"
      name={name}
      ref={register()}
      type={type || "text"}
    />
  );
}

export function InputGroup({ children, hidden }) {
  const classes = classNames("InputGroup", { Hidden: hidden });
  return <div className={classes}>{children}</div>;
}

export function Label({ children, className, htmlFor }) {
  return (
    <label className={`Label ${className || ""}`} htmlFor={htmlFor}>
      {children}
    </label>
  );
}

export function Button({
  children,
  type,
  onClick,
  toCenter,
  inverse,
  disabled,
}) {
  const classes = classNames("Button", {
    ToCenter: toCenter,
    Inverse: inverse,
    Disabled: disabled,
  });
  return (
    <button
      className={classes}
      type={type || "button"}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

export function HelpBlock({ children, error }) {
  return <p>{children}</p>;
}

export function Text({ children, center, highlight, toCenter, light, strong }) {
  const classes = classNames("Text", {
    CenterText: center,
    HighlightText: highlight,
    ToCenter: toCenter,
    Light: light,
    Strong: strong,
  });
  return <p className={classes}>{children}</p>;
}

export function HighlightText({ children, center, ...props }) {
  const classes = classNames("Text", { CenterText: center });
  return (
    <Text highlight {...props}>
      {children}
    </Text>
  );
}

export function Image({ src }) {
  return (
    <div className="ImageContainer">
      <img src={src} />
    </div>
  );
}

export function LinkButton({ to, toCenter, inverse, children }) {
  const classes = classNames("Button", {
    ToCenter: toCenter,
    Inverse: inverse,
  });
  return (
    <Link className={classes} to={to}>
      {children}
    </Link>
  );
}

export function DataRow({ children }) {
  return <div className="DataRow">{children}</div>;
}

export function HR() {
  return <hr className="HR" />;
}
