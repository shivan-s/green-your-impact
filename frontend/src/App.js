import logo from "./logo.svg";
import "./App.css";
import React, { Component } from "react";

class App extends Component {
	state = {
		users: [],
	};

	async componentDidMount() {
		try {
			const res = await fetch("http://127.0.0.1:8000/api/v1/users/users");
			const users = await res.json();
			this.setState({
				users,
			});
		} catch (e) {
			console.log(e);
		}
	}

	render() {
		return (
			<div>
				{this.state.users.map((user) => (
					<div key={user.id}>
						<h1>{user.username}</h1>
						<p>{user.total_carbon_saved}</p>
					</div>
				))}
			</div>
		);
	}
}

export default App;
