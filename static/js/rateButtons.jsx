// class RateButton extends React.Component {
// 	constructor(props) {
// 		super(props);
// 		this.state = {rating: 0};
// 		this.rate = this.rate.bind(this);
// 	}

// 	changeRating() {

// 		// POST request
// 		// let data = new FormData();
// 		// data.append("json", JSON.stringify({'rating': this.state.rating}));

// 		// fetch('/rate-restaurant.json',
// 		// 	  {credentials: 'include',
// 		// 	   method: 'post',
// 		// 	   body: data}).then((response) => response.json())
// 		// 				   .then((data) => console.log(data));

// 		// GET request
// 		fetch(`/rate-with-get.json?rating=${this.state.rating}`,
// 			  {credentials: 'include'}).then((response) => response.json())
// 									   .then((data) => console.log(data));
// 	}

// 	handleChange(evt) {
// 		this.props.onRateChange(evt.target.value);
// 	}

// 	rate() {
// 		this.setState({rating: Number(this.props.value)}, this.changeRating);
// 	}
	
// 	render() {
		
// 		const rating = this.props.rating;

// 		return (
// 			<div>
// 				<button className="rateButton" onClick={ this.rate }>{this.props.value}
// 				</button>
// 			</div>
// 			);
// 	}
// }

// ReactDOM.render(

// 	<div>
// 		<RateButton value="1" />
// 		<RateButton value="2" />
// 		<RateButton value="3" />
// 		<RateButton value="4" />
// 		<RateButton value="5" />
// 	</div>,
// 	document.getElementById("rating")
// 	);