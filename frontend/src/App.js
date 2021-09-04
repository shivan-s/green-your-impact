import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";

class App extends Component {
	state = {
		events: [],
	};

	async componentDidMount() {
		try {
			const res = await fetch("http://127.0.0.1:8000/api/v1/events/events");
			const events = await res.json();
			this.setState({
				events,
			});
		} catch (e) {
			console.log(e);
		}
	}

	render() {
		return (
			<div className="container">
				{this.state.events.map((one_event) => (
					<div key={one_event.id}>
						<h1>
							<a href={one_event.custom_user}>{one_event.custom_user_name}</a>
						</h1>
						<p>
							{one_event.transport_type} - {one_event.distance_travelled}
						</p>
						<p>{one_event.description}</p>
					</div>
				))}
			</div>
		);
	}
}

export default App;
