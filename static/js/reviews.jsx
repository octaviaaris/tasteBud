class UserReviews extends React.Component {
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
		this.sortReviews = this.sortReviews.bind(this);
		this.state = {reviews: {},
					  sortedArray: []};
	}

	componentDidMount() {

		fetch('/reviews.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.setState({reviews: data}, this.sortReviews));

	}

	handleChange(evt) {
		console.log(evt.target.value);
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

		this.setState({sortedArray: sorted});
	}
	
	render() {

		let url = "/details/"
		let reviewArray = []
		let reviewKey = 0

		for (let review in this.state.sortedArray) {
			reviewKey++;
			let restaurant_id = this.state.sortedArray[review].restaurant_id
			let name = this.state.sortedArray[review].name;
			let city = this.state.sortedArray[review].city;
			let price = this.state.sortedArray[review].price;
			let userRating = this.state.sortedArray[review].user_rating;

		reviewArray.push(
			<p key={reviewKey}><a href={url + restaurant_id} target="_blank">{name}</a> ({city}) | Price: {price} | Your review: {userRating}</p>
			)
		}

		let sortPrice = [
			<form key={1} onSubmit={this.handleSubmit}>
				<select name="sortBy" onChange={this.handleChange}>
					<option value="user_rating">Rating</option>
					<option value="price">Price (high to low)</option>
					<option value="price asc">Price (low to high)</option>
				</select>
			</form>
		]

		return (
			<div>
				<h2>Reviews</h2>
				{sortPrice}
				{reviewArray}
			</div>
			)
	}
}

ReactDOM.render(
	<UserReviews />,
	document.getElementById("reviews")
);