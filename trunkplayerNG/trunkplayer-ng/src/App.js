import React, { Component } from 'react';
import { HashRouter, Route, Switch, Redirect } from 'react-router-dom';
import './scss/style.scss';
import PrivateRoute  from  './reusable/PrivateRoute';


const loading = (
  <div className="pt-3 text-center">
    <div className="sk-spinner sk-spinner-pulse"></div>
  </div>
)

// Containers
const TheLayout = React.lazy(() => import('./containers/TheLayout'));

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'));
const Register = React.lazy(() => import('./views/pages/register/Register'));
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'));
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'));

export const UserContext = React.createContext();

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      logged_in: localStorage.getItem('token') ? true : false,
      username: ''
    };
  }
  handle_login = (e, data, sst) => {
    console.log(data)
    e.preventDefault();
    fetch('http://127.0.0.1:8080/token-auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => {
        if (!res.ok){
          throw new Error("Login Failed");
        }
       return res.json()
      })
      .then(json => {
        console.log(json.token)
        localStorage.setItem('token', json.token);
        sst({failed: true, success: false})
        this.setState({
          logged_in: true,
          username: data.username
        });
        this.context.router.history.push('/');
})
    //   }).catch(function() {
    //     sst({failed: false, success: true})
    // });
  };



  render() {
    return (
      <HashRouter>
          <React.Suspense fallback={loading}>
            <Switch>
              <Route exact path="/login" name="Login Page" render={props => <Login  {...props} failed={this.failed} handle_login={this.handle_login} />} />
              <Route exact path="/register" name="Register Page" render={props => <Register {...props}/>} />
              <Route exact path="/404" name="Page 404" render={props => <Page404 {...props}/>} />
              <Route exact path="/500" name="Page 500" render={props => <Page500 {...props}/>} />
              <PrivateRoute isAuthenticated={this.state.logged_in} path="/" name="Home" render={props => <TheLayout  {...props}/>} />
            </Switch>
          </React.Suspense>
      </HashRouter>
    );
  }
}

export default App;
