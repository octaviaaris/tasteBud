class RestaurantDetails extends React.Component {
	constructor(props) {
		super(props);
		this.state = {details: {},
					  categories: [],
					  userRating: "Rate below"};
	}

	componentDidMount() {

		fetch('/details.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.setState({details: data, categories: data['categories']}));

		fetch('/user-rating.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => (data) ? this.setState({userRating: '*'.repeat(data['userRating'])}) 
									   						  : this.setState({userRating: "Changed"}));

	}

	render() {

		return (
			<div>
				<h3>{this.state.details['name']}</h3>
				Yelp: {'*'.repeat(this.state.details['yelp_rating'])} | You: {this.state.userRating}
				<p>{'$'.repeat(this.state.details['price'])} | {this.state.categories.join(", ")}</p>
				<p>Address:</p>
				{this.state.details['address1']}<br/>
				{this.state.details['city']}, {this.state.details['state']} {this.state.details['zipcode']}
				<p><a href={this.state.details['yelp_url']} target="_blank">Go to yelp page</a></p>
			</div>
			)
	}
}

ReactDOM.render(
	<RestaurantDetails />,
	document.getElementById("details")
);