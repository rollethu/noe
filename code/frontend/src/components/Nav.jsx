import React from "react";
import { Link } from "react-router-dom";

let defaultShowNav = false;
if (process.env.NODE_ENV === "development") {
  defaultShowNav = true;
}

export default function Nav({ routes }) {
  const [showNav, setShowNav] = React.useState(defaultShowNav);

  if (!showNav) {
    return null;
  }

  return (
    <div className="Nav">
      <button onClick={() => setShowNav(false)}>Close</button>
      <ul>
        {routes.map((route) => (
          <Link to={route.path} key={route.path}>
            <li>{route.path}</li>
          </Link>
        ))}
      </ul>
    </div>
  );
}
