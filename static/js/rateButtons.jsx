class RateButton extends React.Component {
	constructor(props) {
		super(props);
		this.state = {rating: 0};
		this.rate = this.rate.bind(this);
	}

	rate() {
		let rating = Number(this.props.value);
		this.setState({rating: this.props.value})

		data = {'rating': this.state.rating,
				'restaurant_id': REPLACE}
		console.log(data);

		fetch('/rate-restaurant',
			  {method: 'post',
			   body: JSON.stringify(data)});
	}

	render() {
		return (
			<button className="rateButton" onClick={ this.rate }>{this.state.rating}
			</button>
			);
	}

}

ReactDOM.render(

	<div>
		<RateButton value="1" />
		<RateButton value="2" />
		<RateButton value="3" />
		<RateButton value="4" />
		<RateButton value="5" />
	</div>,
	document.getElementById("rating")

	);