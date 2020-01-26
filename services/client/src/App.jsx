import React, { Component } from "react";
import { Route, Switch } from "react-router-dom";
import axios from "axios";

import UsersList from "./components/UsersList";
import AddUser from "./components/AddUser";
import About from "./components/About";
import NavBar from "./components/NavBar";
import RegisterForm from "./components/RegisterForm";
import LoginForm from "./components/LoginForm";

class App extends Component {
  constructor() {
    super();

    this.state = {
      users: [],
      title: "Flask TDD Docker",
      accessToken: null
    };
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        this.setState({ users: res.data });
      })
      .catch(err => {
        console.log(err);
      });
  }

  isAuthenticated() {
    if (this.state.accessToken) {
      return true;
    }
    return false;
  }

  addUser = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then(res => {
        this.getUsers();
        this.setState({ username: "", email: "" });
      })
      .catch(err => {
        console.log(err);
      });
  };

  handleRegisterFormSubmit = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/register`, data)
      .then(res => {
        console.log(res.data);
      })
      .catch(err => {
        console.log(err);
      });
  };

  handleLoginFormSubmit = data => {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/auth/login`, data)
      .then(res => {
        this.setState({ accessToken: res.data.access_token });
      })
      .catch(err => {
        console.log(err);
      });
  };

  render() {
    return (
      <div>
        <NavBar title={this.state.title} />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-half">
                <br />
                <Switch>
                  <Route
                    exact
                    path="/"
                    render={() => (
                      <div>
                        <h1 className="title is-1 is-1">Users</h1>
                        <hr />
                        <br />
                        <AddUser addUser={this.addUser} />
                        <hr />
                        <br />
                        <UsersList users={this.state.users} />
                      </div>
                    )}
                  />
                  <Route exact path="/about" component={About} />
                  <Route
                    exact
                    path="/register"
                    render={() => (
                      <RegisterForm
                        handleRegisterFormSubmit={this.handleRegisterFormSubmit}
                      />
                    )}
                  />
                  <Route
                    exact
                    path="/login"
                    render={() => (
                      <LoginForm
                        handleLoginFormSubmit={this.handleLoginFormSubmit}
                      />
                    )}
                  />
                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
