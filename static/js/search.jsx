"use strict";

class SearchForm extends React.Component {
	constructor(props) {
		super(props);
		this.state = {searchString: '',
					  city: '',
					  citiesArray: '',
					  price: 0,
					  article: "near",
					  submitCity: "San Francisco",
					  submitSearch: "Restaurants",
					  submitted: false,
					  reroute: "false",
					  results: {}};
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(evt) {
		this.setState({[evt.target.name]: evt.target.value});
	}

	handleSubmit(evt) {
		evt.preventDefault();

		let search_string = this.state.searchString;
		if (search_string) {
			this.setState({submitSearch: search_string});
		} else {
			this.setState({submitSearch: "Restaurants"})
		}
		let city = this.state.city;
		if (city) {
			this.setState({submitCity: city, article: "in"});
		} else {
			this.setState({submitCity: "San Francisco", article: "near"});
		}
		this.setState({submitted: true});


		fetch(`/search.json?search_string=${search_string}&city=${city}`).then((response) => response.json())
																		 .then((data) => this.setState({results: data}));

	}

	componentDidMount() {
		fetch('/cities.json').then((response) => response.json())
							 .then((data) => {
							 	let cities = []
							 	for (let city of data.cities) {
							 		cities.push(city);
							 	}
							 	this.setState({citiesArray: cities});
							 });
	}

	render() {
		if (!this.state.citiesArray) {
			return <div></div>
		}
		
		let cityOptionIndex = 0;
		const cityOptions = this.state.citiesArray.map(function(city) {
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
					<option value="">Choose a city</option>
					{cityOptions}
				</select>
				</label>
				<input type="submit" value="Search" />
			</form>

			<SearchResults 
				results={this.state.results} 
				submitCity={this.state.submitCity}
				submitSearch={this.state.submitSearch}
				submitted={this.state.submitted}
				article={this.state.article} />
			</div>
		);
	}
}

class SearchResults extends React.Component {

	render() {
		
		// if (this.props.reroute == true) {
		// 	this.props.submitSearch()
		// }

		let url = "/details/"
		let resultArray = []
		let resultKey = 0

		for (let result in this.props.results) {
			resultKey++;
			resultArray.push(<p key={resultKey}>
				<a href={url + result} target="_blank">{this.props.results[result].name}</a>
				 &nbsp;({this.props.results[result].price})</p>)
		}


		if (resultArray.length > 0) {
			return (
				<div>
				<h3>{this.props.submitSearch} {this.props.article} {this.props.submitCity}</h3>
				{resultArray}
				</div>);
		}

		else if (resultArray.length == 0 && this.props.submitted == true) {
			return (<div><p>No results for "{this.props.submitSearch}" {this.props.article} {this.props.submitCity}.</p></div>);
		}
		else {
			return (<div></div>)
		}

	}
}

ReactDOM.render(
	<SearchForm reroute={false} />,
	document.getElementById("root")
);