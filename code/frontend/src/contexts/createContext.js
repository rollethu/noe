/* sources:
    https://medium.com/@tristifano/using-react-context-and-hooks-to-make-handling-state-easy-d5f7274b8a8f
    https://www.udemy.com/course/the-complete-react-native-and-redux-course
*/
import React from "react";

export default (reducer, actions, defaultValue) => {
  const Context = React.createContext();
  const Provider = ({ children, injectState }) => {
    const [state, dispatch] = React.useReducer(reducer, {
      ...defaultValue,
      ...injectState,
    });

    const boundActions = {};
    for (let key in actions) {
      boundActions[key] = actions[key](dispatch);
    }

    return (
      <Context.Provider value={{ state, ...boundActions }}>
        {children}
      </Context.Provider>
    );
  };

  return { Context, Provider };
};
