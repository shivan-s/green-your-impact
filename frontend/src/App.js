import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Navbar from "./components/layout/navbar";
import Login from "./views/auth/Login";
import Signup from "./views/auth/Signup";
import Logout from "./views/auth/Logout";

const App = () => {
	return (
		<div className="App">
			<Router>
				<Navbar />
				<Switch>
					<Route path="/login" component={Login} exact />
					<Route path="/signup" component={Signup} exact />
					<Route path="/logout" component={Logout} exact />
				</Switch>
			</Router>
		</div>
	);
};

export default App;
