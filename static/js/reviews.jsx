class UserReviews extends React.Component {
	constructor(props) {
		super(props);
		this.state = {reviews: {}};
	}

	componentDidMount() {

		fetch('/reviews.json',
			  {credentials: 'include'}).then((response) => response.json())
									   .then((data) => this.setState({reviews: data}));
	}
	
	render() {

		let url = "/details/"
		let reviewArray = []
		let reviewKey = 0

		for (let review in this.state.reviews) {
			reviewKey++;
			reviewArray.push(
				<p key={reviewKey}><a href={url + review} target="_blank">{this.state.reviews[review][0]}</a> | Price: {this.state.reviews[review][1]} | Your review: {this.state.reviews[review][2]}</p>
				)
		}

		return (
			<div>
				<h2>Reviews</h2>
				{reviewArray}
			</div>
			)
	}
}

ReactDOM.render(
	<UserReviews />,
	document.getElementById("reviews")
);