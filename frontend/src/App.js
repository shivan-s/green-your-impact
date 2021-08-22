import React, { Component } from 'react';

const list = [
	{
		"user": "Shivan",
		"transport_type": "WALK",
		"distance_travelled": "10.00",
		"description": "Biked to work"
	},
	{
		"user": "Saxon",
		"transport_type": "BIKE",
		"distance_travelled": "100.00",
		"description": "Walked to work"
	},
	{
		"user": "Deb",
		"transport_type": "WALK",
		"distance_travelled": "99.98",
		"description": "Biked to work"
	},
	{
		"user": "Dave",
		"transport_type": "PUBL",
		"distance_travelled": "500.00",
		"description": "I love the bus"
	}
]

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
