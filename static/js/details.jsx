class RestaurantDetails extends React.Component {
	constructor(props) {
		super(props);
		this.state = {details: {}};
	}

	componentDidMount() {

		fetch('/details.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.setState({details: data}));
	}

	render() {

		let url = "/details/"
		let detailArray = []
		let detailObject = {}
		let detailKey = 0

		for (let detail in this.state.details) {
			detailKey++;
			detailArray.push(
				<p key={detailKey}>{detail, this.state.details[detail]}</p>
				)
		}

		for (let key in this.state.details) {
			detailObject[key] = this.state.details[key];
		}

		// name = this.state.details['name'];
		// categories = this.state.details['categories'];
		// price = this.state.details['price'];
		// yelp_rating = this.state.details['yelp_rating'];
		// address1 = this.state.details['address1'];
		// city = this.state.details['city'];
		// state = this.state.details['state'];
		// zipcode = this.state.details['zipcode'];

		return (
			<div>
				{/*<h3>{name}</h3>*/}
				<p>React details</p>
				<h3>{detailObject['name']}</h3>
				<p>{detailObject['categories']}</p>
				<p>Price: {detailObject['price']}</p>
				<p>Yelp Rating: {detailObject['yelp_rating']}</p>
				<p>Address:</p>
				<p>{detailObject['address1']}</p>
				<p>{detailObject['city']}, {detailObject['state']} {detailObject['zipcode']}</p>
			</div>
			)
	}
}

ReactDOM.render(
	<RestaurantDetails />,
	document.getElementById("details")
);