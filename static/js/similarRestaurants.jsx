class SimilarRestaurants extends React.Component {
	constructor(props) {
		super(props);
		this.state = {restaurants: "unchanged",
					  currentRestaurant: "",
					  similars: []};
	}

	createYelpStars = (rtg) => {
		let yelp =[];
		for (let step = 0; step < rtg; step++ ) {
			yelp.push(<i key={step} className="fas fa-star"></i>)
		}

		return yelp;
	}

	createPriceIcons = (price) => {
		let priceIcon = [];
				for (let step = 0; step < price; step++ ) {
					priceIcon.push(<i key={step} className="fas fa-dollar-sign"></i>)
				}

		return priceIcon;
	}

	createSimilarRestaurants = () => {
		let newSimilars = [];
		let idNum = 0;

		for (let r in this.state.restaurants) {
			let yelp = this.createYelpStars(this.state.restaurants[r].yelp_rating);
			let price = this.createPriceIcons(this.state.restaurants[r].price);
			newSimilars.push(
				<div className="simContainer">
					<a href={"/details/" + r}
					   id={"sim" + idNum}
					   key={idNum}
					   className="m-auto simRestaurantBox">
						<p className="address name">{this.state.restaurants[r].name}</p>
						{yelp}<br/>
						<p className="text-truncate">{price} | {this.state.restaurants[r]['categories'].join(", ")}</p>
						<p className="address">{this.state.restaurants[r].city}</p>
					</a>
				</div>
			)
			idNum++;
		}

		this.setState({similars: newSimilars});
	}
	

	changeState = (data) => {
		this.setState({restaurants: data}, this.createSimilarRestaurants);
	}

	componentDidMount() {
		
		fetch('/details.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.setState({currentRestaurant: data['name']}));

		fetch('/similar-restaurants.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.changeState(data));
	}

	render() {

		return (
			<div className="simRestaurants">
				<hr/>
				<div className="row simRow" id="simHeader"><p>Other places like {this.state.currentRestaurant}:</p></div>
				<div className="row simRow">{this.state.similars}</div>
			</div>
		);
	}
}

ReactDOM.render(
	<SimilarRestaurants />,
	document.getElementById("similarRestaurants")
);