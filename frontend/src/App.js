import React, { setState, useEffect } from "react";
// import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";

function App() {
	const [data, setData] = setState(false);
	useEffect(() => {
		fetch(`http://127.0.0.1:8000/api/v1/events/events`)
			.then((response) => response.json())
			.then(setData);
	}, []);
	console.log(data);

	if (data) {
		return <div className="container">{data}</div>;
	}
	return <div>...loading</div>;
}

export default App;
