import React, { Component } from 'react';

class App extends Component {
	constructor(props) {
		super(props);
		this.state = { list };
	}

	render() {
		return (
			<div>
			{this.state.list.map(item => (
				<div>
				<h1>{item.user}</h1>
				<h2>{item.transport_type}</h2>
				<span>{item.distance_travelled}</span>
				<span>{item.description}</span>
				</div>
			))}
			</div>
		);
	}
}

export default App;
