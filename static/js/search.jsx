"use strict";

class SearchForm extends React.Component {
	constructor(props) {
		super(props);
		this.state = {searchString: '', city: 'San Francisco', cities_array: '', results: {}};
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(evt) {
		this.setState({[evt.target.name]: evt.target.value})
	}

	handleSubmit(event) {
		event.preventDefault();
		// send data to /search.json

		let search_string = this.state.searchString;
		let city = this.state.city;

		fetch(`/search.json?search_string=${search_string}&city=${city}`).then((response) => response.json())
																		  .then((data) => this.setState({results: data}));

		// let fake_result = [['2QGpLQwpzcPK99JfS5G4cQ', 'name', 'Kingza', 'price', 4], ['2QGpLQwpzcPK99JfS5G4cQ', 'name', 'Kingza', 'price', 4]];
		// this.setState({results: fake_result});

	}

	componentDidMount() {
		fetch('/cities.json').then((response) => response.json())
							 .then((data) => {
							 	let cities = []
							 	for (let city of data.cities) {
							 		cities.push(city[0]);
							 	}
							 	this.setState({cities_array: cities});
							 });
	}

	render() {
		for (let result in this.state.results) {
			console.log(result);
			console.log(this.state.results[result].name);
			console.log(this.state.results[result].price);
		}

		if (!this.state.cities_array) {
			return <div>No cities</div>
		}
		
		let cityOptionIndex = 0;
		const cityOptions = this.state.cities_array.map(function(city) {
			cityOptionIndex++;
			return (<option key={cityOptionIndex} value={city}>{city}</option>);
		});

		return(
			<div>
			<form onSubmit={this.handleSubmit}>
				<label>
				Find <input name="searchString"
							type="text" 
							placeholder="japanese, asian, Tacorea" 
							value={this.state.searchString} 
							onChange={this.handleChange} />
				</label>
				<label>
				<select name="city"
						value={this.state.city} 
						onChange={this.handleChange}>
					<option value="San Francisco">Choose a city</option>
					{cityOptions}
				</select>
				</label>
				<input type="submit" value="Search" />
			</form>

			<SearchResults results={this.state.results} />
			</div>
		);
	}
}

class SearchResults extends React.Component {

	render() {

		let result_array = []
		let result_key = 0
		for (let result in this.props.results) {
			result_key++;
			result_array.push(<p key={result_key}>{this.props.results[result].name} {this.props.results[result].price}</p>)
		}
		
		return (<div>{result_array}</div>)
	}
}

ReactDOM.render(
	<SearchForm />,
	document.getElementById("root")
);
