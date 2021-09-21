
import React from 'react';
import { Route, Redirect } from 'react-router-dom';

export function PrivateRoute({ component: Component = null, isAuthenticated, render: Render = null, ...rest }) {


  return (
    <Route
      {...rest}
      render={props =>
        isAuthenticated ? (
          Render ? (
            Render(props)
          ) : Component ? (
            <Component {...props} />
          ) : null
        ) : (
          <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
        )
      }
    />
  );
}
export default PrivateRoute;