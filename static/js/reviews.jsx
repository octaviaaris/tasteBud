class UserReviews extends React.Component {
	constructor(props) {
		super(props);
		this.checkFilters = this.checkFilters.bind(this);
		this.handlePriceFilter = this.handlePriceFilter.bind(this);
		this.handleRatingFilter = this.handleRatingFilter.bind(this);
		this.filterReviews = this.filterReviews.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.sortReviews = this.sortReviews.bind(this);
		this.state = {reviews: {},
					  priceFilter: new Set(),
					  ratingFilter: new Set(),
					  sortedArray: [],
					  filteredArray: []};
	}

	componentDidMount() {

		fetch('/reviews.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.setState({reviews: data}, this.sortReviews));

	}

	checkFilters(filter, evt) {
		const currentFilters = filter;
		const newValue = evt.target.value;

		if (currentFilters.has(newValue)) {
			currentFilters.delete(newValue);
		} else {
			currentFilters.add(newValue);}

		return currentFilters;
	}

	handlePriceFilter(evt) {
		const priceFilters = this.checkFilters(this.state.priceFilter, evt);
		this.setState({priceFilter: priceFilters}, this.filterReviews);
	}

	handleRatingFilter(evt) {
		const ratingFilters = this.checkFilters(this.state.ratingFilter, evt);
		this.setState({ratingFilter: ratingFilters}, this.filterReviews);
	}

	filterReviews() {
		let prices = this.state.priceFilter;
		let stars = this.state.ratingFilter;
		let filteredByPrice = [];
		let filteredByRating = [];
		let unfiltered = this.state.sortedArray;

		if (prices.size === 0 && stars.size === 0) {
			this.setState({filteredArray: unfiltered});
		} else {

			if (prices.size > 0) {
				for (let item of this.state.sortedArray) {
						if (prices.has(String(item.price))) {
							filteredByPrice.push(item);
						}
					}
			} else {
				filteredByPrice = unfiltered;}

			if (stars.size > 0) {
				for (let item of filteredByPrice) {
					if (stars.has(String(item.user_rating))) {
						filteredByRating.push(item);
					}
				}
			} else {
				filteredByRating = filteredByPrice;}

			this.setState({filteredArray: filteredByRating});
		}
	}

	handleChange(evt) {
		let params = evt.target.value.split(" ")
		this.sortReviews(params[0], params[1]);
	}

	sortReviews(key="user_rating", order="desc") {
		let unsorted = [];

		for (let review in this.state.reviews) {
			unsorted.push(this.state.reviews[review]);
		}

		let sorted = unsorted.sort(function(a, b) {
			const itemA = a[key];
			const itemB = b[key];

			let comparison = 0;
			if (itemA > itemB) {
				comparison = -1;
			} else if (itemA < itemB) {
				comparison = 1;
			}

			return ((order == 'asc') ? (comparison * -1) : comparison);
		});

		this.setState({sortedArray: sorted}, this.filterReviews);
	}
	
	render() {

		const reviews = this.state.filteredArray;
		let url = "/details/"
		let reviewArray = []
		let reviewKey = 0

		for (let review in reviews) {
			reviewKey++;
			let restaurant_id = reviews[review].restaurant_id
			let name = reviews[review].name;
			let city = reviews[review].city;
			let price = reviews[review].price;
			let userRating = reviews[review].user_rating;

			let priceIcon = [];
			for (let step = 0; step < price; step++ ) {
				priceIcon.push(<i key={step} className="fas fa-dollar-sign"></i>)
			}

			let ratingIcon = [];
			for (let step = 0; step < userRating; step++ ) {
				ratingIcon.push(<i key={step} className="fas fa-star"></i>)
				}

			reviewArray.push(
				<div className="userReview" key={reviewKey}>
				<span className="reviewName"><a href={url + restaurant_id} target="_blank">{name}</a></span> ({city})<br/>
				Price: {priceIcon} | Your review: {ratingIcon}
				</div>
			)
		}

		let sortForm = [
			<form key={1}>
				<select name="sortBy" onChange={this.handleChange}>
					<option value="user_rating">Rating</option>
					<option value="price">Price (high to low)</option>
					<option value="price asc">Price (low to high)</option>
				</select>
			</form>
		]

		const priceFilterBtns = [
			<div className="priceFilter" key={1}>
				<button value="1"
						onClick={this.handlePriceFilter}>$</button>
				<button value="2"
						onClick={this.handlePriceFilter}>$$</button>
				<button value="3" 
						onClick={this.handlePriceFilter}>$$$</button>
				<button value="4"
						onClick={this.handlePriceFilter}>$$$$</button>
			</div>
		]

		const ratingFilterBtns = [
			<div className="ratingFilter" key={1}>
				<button value="1"
						onClick={this.handleRatingFilter}>*</button>
				<button value="2"
						onClick={this.handleRatingFilter}>**</button>
				<button value="3" 
						onClick={this.handleRatingFilter}>***</button>
				<button value="4"
						onClick={this.handleRatingFilter}>****</button>
				<button value="5"
						onClick={this.handleRatingFilter}>*****</button>
			</div>
		]

		return (
			<div>
				<div id="reviewTitle"><h2>Your Reviews</h2></div>
				{sortForm}
				{priceFilterBtns}
				{ratingFilterBtns}
				{reviewArray}
			</div>
		)
	}
}

ReactDOM.render(
	<UserReviews />,
	document.getElementById("reviews")
);