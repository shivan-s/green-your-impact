import React, { useState, useEffect } from "react";
import {
	Switch,
	Route,
	Link,
	useParams,
	useRouteMatch,
} from "react-router-dom";

function App() {
	return (
		<div className="container mt-4">
			<Switch>
				<Route exact path="/users">
					<Users />
				</Route>
				<Route path="/users/:id">
					<User />
				</Route>
				<Route exact path="/">
					<Home />
				</Route>
				<Route path="*">
					<NoMatch />
				</Route>
			</Switch>
		</div>
	);
}

function Home() {
	return (
		<div>
			<h1>Home</h1>
		</div>
	);
}

function Users() {
	let { path, url } = useRouteMatch();
	const [data, setData] = useState(false);
	useEffect(() => {
		fetch(`http://127.0.0.1:8000/api/v1/users/users`)
			.then((response) => response.json())
			.then(setData);
	}, []);
	console.log(url);
	if (data) {
		return (
			<div>
				{data.map((datum, i) => (
					<h1 key={i}>
						<Link to={`users/${datum.username}`}>{datum.username}</Link>
					</h1>
				))}
			</div>
		);
	}
	return <div>...loading</div>;
}

function User() {
	const params = useParams();
	const [data, setData] = useState(false);
	useEffect(() => {
		fetch(`http://127.0.0.1:8000/api/v1/users/${params.id}`)
			.then((response) => response.json())
			.then(setData);
	}, []);
	console.log(data);

	if (data) {
		return (
			<div>
				<h1>{data.username}</h1>
				<p>Total Carbon Saved: {data.total_carbon_saved}</p>

				{data.event_set.map((events) => (
					<div>
						<h2>
							<Link to={events.url}>{events.transport_type}</Link>
						</h2>
						<p>{events.description}</p>
					</div>
				))}
			</div>
		);
	}
	return <div>...loading</div>;
}

function NoMatch() {
	return (
		<div>
			<h1>No match</h1>
		</div>
	);
}

export default App;
