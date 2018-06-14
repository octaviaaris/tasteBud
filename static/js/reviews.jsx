class UserReviews extends React.Component {
	constructor(props) {
		super(props);
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

	checkFilters = (filter, evt) => {
		const currentFilters = filter;
		const newValue = evt.target.value;

		if (currentFilters.has(newValue)) {
			currentFilters.delete(newValue);
		} else {
			currentFilters.add(newValue);}

		return currentFilters;
	}

	handlePriceFilter = (evt) => {
		const priceFilters = this.checkFilters(this.state.priceFilter, evt);
		this.setState({priceFilter: priceFilters}, this.filterReviews);
	}

	handleRatingFilter = (evt) => {
		const ratingFilters = this.checkFilters(this.state.ratingFilter, evt);
		this.setState({ratingFilter: ratingFilters}, this.filterReviews);
	}

	filterReviews = () => {
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

	handleChange = (evt) => {
		let params = evt.target.value.split(" ")
		this.sortReviews(params[0], params[1]);
	}

	sortReviews = (key="user_rating", order="desc") => {
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

	showReviews = () => {
		const reviews = this.state.filteredArray;
		let url = "/details/"
		let reviewArray = []
		let reviewKey = 0

		if (reviews.length != 0) {
			for (let review in reviews) {
				reviewKey++;
				let restaurant_id = reviews[review].restaurant_id
				let name = reviews[review].name;
				let city = reviews[review].city;
				let price = reviews[review].price;
				let userRating = reviews[review].user_rating;
				let img = reviews[review].image;

				let priceIcon = [];
				for (let step = 0; step < price; step++ ) {
					priceIcon.push(<i key={step} className="fas fa-dollar-sign"></i>)
				}

				let ratingIcon = [];
				for (let step = 0; step < userRating; step++ ) {
					ratingIcon.push(<i key={step} className="fas fa-star"></i>)
					}

				reviewArray.push(
					// <div className="userReview" key={reviewKey}>
					// <span className="reviewName"><a href={url + restaurant_id}>{name}</a></span> ({city})<br/>
					// Price: {priceIcon} | Your review: {ratingIcon}
					// </div>

					<div className="reviewResults" key={reviewKey}>
						<a href={url + restaurant_id}
						   className="reviewResultsInfo noColorChange">
						   <img className="imgThumbnail" src={img}/>
						   <span className="reviewName">{name}</span> ({city})<br/>
						   Price: {priceIcon} | Your review: {ratingIcon}
						</a>
					</div>
				)
			}
		} else {
			reviewArray.push(<div className="userReview" key={reviewKey}>"No reviews match your criteria. Try removing one or more filters."</div>);
		}

		return reviewArray;
	}

	createPriceFilter = () => {
		let priceFilterBtns = [];

		for (let step = 1; step < 5; step++) {
			let prices = this.state.priceFilter;
			if (prices.has(String(step))) {
				priceFilterBtns.push(<button key={step}
									   value={step}
									   onClick={this.handlePriceFilter}
									   className="btn btn-outline-info pricefilter selected">{"$".repeat(step)}</button>)
			} else {
				priceFilterBtns.push(<button key={step}
									   value={step}
									   onClick={this.handlePriceFilter}
									   className="btn btn-outline-info pricefilter">{"$".repeat(step)}</button>)
			}
		}

		return priceFilterBtns;
	}

	createRatingFilter = () => {

		let ratingFilterBtns = [];
		for (let step = 1; step < 6; step++) {
			let ratings = this.state.ratingFilter;
			if (ratings.has(String(step))) {
				ratingFilterBtns.push(<button key={step}
									   value={step}
									   onClick={this.handleRatingFilter}
									   className="btn btn-outline-info btn-work ratingfilter selected">{"*".repeat(step)}</button>)
			} else {
				ratingFilterBtns.push(<button key={step}
									   value={step}
									   onClick={this.handleRatingFilter}
									   className="btn btn-outline-info btn-work ratingfilter">{"*".repeat(step)}</button>)
			}
		}

		return ratingFilterBtns;
	}

	otherFilter = () => {
		let otherFilter = [];
		let ratings = this.state.ratingFilter;

		for (let step = 5; step >= 0; step--) {
			let stars = [];
			if (ratings.has(String(step))) {
				for (let star = 1; star <= step; star++) {
					stars.push(
						<i key={star} className="fas fa-star"></i>
						)	
				}
				
				otherFilter.push(
					<div key={step} className="filterStars selected">{stars}</div>
					)
			} else {

				for (let star = 1; star <= step; star++) {
					stars.push(
						<i key={star} className="far fa-star"></i>
						)	
				}
				
				otherFilter.push(
					<div key={step} className="filterStars">{stars}</div>
					)
			}
		}

		return otherFilter;
	}
	
	render() {

		let sortForm = [
			<form key={1}>
				<select name="sortBy" onChange={this.handleChange} className="form-control form-control-sm">
					<option value="user_rating">Rating</option>
					<option value="price">Price (high to low)</option>
					<option value="price asc">Price (low to high)</option>
				</select>
			</form>
		]

		let priceFilterBtns = this.createPriceFilter();
		let ratingFilterBtns = this.createRatingFilter();
		let otherFilter = this.otherFilter();
		let reviewArray = this.showReviews();

		return (
			<div className="row">
				<div className="col-5 filterPanel reviews">
					<div className="filterPanelBorder reviews">
						<div className="filterLabels">Sort</div>
						<div className="filterDivide"></div>
						{sortForm}
						<div className="filterDivide sort"></div>
						<div className="filterLabels">Filter By Price</div>
						<div className="filterDivide"></div>
						{priceFilterBtns}
						<div className="filterDivide"></div>
						<div className="filterLabels">Filter By Rating</div>
						<div className="filterDivide"></div>
						{ratingFilterBtns}
						<div className="filterDivide"></div>
					</div>
				</div>
				<div className="col-7 userReviews">
					<div id="reviewTitle"><h2>Your Reviews</h2></div>
					{reviewArray}
				</div>
			</div>
		)
	}
}

ReactDOM.render(
	<UserReviews />,
	document.getElementById("reviews")
);