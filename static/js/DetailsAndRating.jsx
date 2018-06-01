class RatingParent extends React.Component {
	constructor(props) {
		super(props);
		this.handleRatingChange = this.handleRatingChange.bind(this);
		this.state = {currentRating: "Rate below"};
	}

	componentDidMount() {

		fetch('/user-rating.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => (data) ? this.setState({currentRating: '*'.repeat(data['userRating'])}) 
									   						  : this.setState({currentRating: "Rate below"}));

	}

	handleRatingChange(newRating) {
		this.setState({currentRating: '*'.repeat(newRating)});
	}

	render () {

		const currentRating = this.state.currentRating;

		return (
			<div>
				<RestaurantDetails 
					rating={currentRating} />
				<div className="rateButtons">
					<RateButton value="1"
								className="rateBtn"
								rating={currentRating}
								onRatingChange={this.handleRatingChange} />
					<RateButton value="2"
								className="rateBtn"
								rating={currentRating}
								onRatingChange={this.handleRatingChange} />
					<RateButton value="3" 
								className="rateBtn"
								rating={currentRating}
								onRatingChange={this.handleRatingChange} />
					<RateButton value="4"
								className="rateBtn"
								rating={currentRating}
								onRatingChange={this.handleRatingChange} />
					<RateButton value="5"
								className="rateBtn"
								rating={currentRating}
								onRatingChange={this.handleRatingChange} />
				</div>
			</div>
		);
	}
}

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
	}

	render() {

		const rating = this.props.rating;

		return (
			<div>
				<h3>{this.state.details['name']}</h3>
				Yelp: {'*'.repeat(this.state.details['yelp_rating'])} | You: {rating}
				<p>{'$'.repeat(this.state.details['price'])} | {this.state.categories.join(", ")}</p>
				<p>Address:</p>
				{this.state.details['address1']}<br/>
				{this.state.details['city']}, {this.state.details['state']} {this.state.details['zipcode']}
				<p><a href={this.state.details['yelp_url']} target="_blank">Go to yelp page</a></p>
			</div>
			)
	}
}

class RateButton extends React.Component {
	constructor(props) {
		super(props);
		this.rate = this.rate.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.state = {rating: 0};
	}

	handleChange(data) {
		let newRating = data['rating'];
		this.props.onRatingChange(newRating);
	}

	changeRating() {

		///////////////////////////// POST request //////////////////////////////
		// let data = new FormData();										   //
		// data.append("json", JSON.stringify({'rating': this.state.rating})); //
		//         														       //
		// fetch('/rate-restaurant.json',									   //
		// 	  {credentials: 'include',										   //
		// 	   method: 'post',												   //
		// 	   body: data}).then((response) => response.json())				   //
		// 				   .then((data) => console.log(data));				   //
		/////////////////////////////////////////////////////////////////////////

		// GET request
		fetch(`/rate-restaurant.json?rating=${this.state.rating}`,
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.handleChange(data));


	}

	rate() {
		this.setState({rating: Number(this.props.value)}, this.changeRating);
	}
	
	render() {
		
		return (
			<div>
				<button className="rateButton" onClick={ this.rate }>{this.props.value}
				</button>
			</div>
			);
	}
}

ReactDOM.render(
	<RatingParent />,
	document.getElementById("ratingParent")
);