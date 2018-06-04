class UserReviews extends React.Component {
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
		this.handlePriceFilter = this.handlePriceFilter.bind(this);
		this.handleRatingFilter = this.handleRatingFilter.bind(this);
		this.sortReviews = this.sortReviews.bind(this);
		this.filterReviews = this.filterReviews.bind(this);
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

	handlePriceFilter(evt) {
		let priceFilters = this.state.priceFilter;

		if (priceFilters.has(evt.target.value)) {
			priceFilters.delete(evt.target.value);
		} else {
			priceFilters.add(evt.target.value);
		}

		this.setState({priceFilter: priceFilters}, this.filterReviews);
	}

	handleRatingFilter(evt) {
		let ratingFilters = this.state.ratingFilter;

		if (ratingFilters.has(evt.target.value)) {
			ratingFilters.delete(evt.target.value);
		} else {
			ratingFilters.add(evt.target.value);
		}

		this.setState({ratingFilter: ratingFilters}, this.filterReviews);
	}

	filterReviews() {
		let prices = this.state.priceFilter;
		let stars = this.state.ratingFilter;
		let filterOne = [];
		let filterTwo = [];
		let unfiltered = this.state.sortedArray;
		console.log(prices);
		console.log(stars);

		if (prices.size === 0 && stars.size === 0) {
			this.setState({filteredArray: unfiltered});
		} else {

			if (prices.size > 0) {
				for (let item of this.state.sortedArray) {
						if (prices.has(String(item.price))) {
							filterOne.push(item);
						}
					}
			
			} else {
				filterOne = unfiltered;
			}

			if (stars.size > 0) {
				for (let record of filterOne) {
					if (stars.has(String(record.user_rating))) {
						filterTwo.push(record);
					}
				}
			} else {
				filterTwo = filterOne;
			}

			this.setState({filteredArray: filterTwo});
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


		let url = "/details/"
		let reviewArray = []
		let reviewKey = 0

		for (let review in this.state.filteredArray) {
			reviewKey++;
			let restaurant_id = this.state.filteredArray[review].restaurant_id
			let name = this.state.filteredArray[review].name;
			let city = this.state.filteredArray[review].city;
			let price = this.state.filteredArray[review].price;
			let userRating = this.state.filteredArray[review].user_rating;

		reviewArray.push(
			<p key={reviewKey}><a href={url + restaurant_id} target="_blank">{name}</a> ({city}) | Price: {price} | Your review: {userRating}</p>
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
				<h2>Reviews</h2>
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