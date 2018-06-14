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
					  priceFilter: new Set(),
					  results: {},
					  sortedArray: [],
					  filteredArray: []};
	}

	sortResults = (key="yelp_rating", order="desc") => {
		
		let unsorted = [];

		for (let result in this.state.results) {
			unsorted.push(this.state.results[result]);
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

		this.setState({sortedArray: sorted}, this.filterResults);
	}

	handleChange = (evt) => {
		this.setState({[evt.target.name]: evt.target.value});
	}

	handleSubmit = (evt) => {
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
																		 .then((data) => this.setState({results: data, priceFilter: new Set()}, this.sortResults));
	}

	handleSortChange = (evt) => {
		let params = evt.target.value.split(" ");
		this.sortResults(params[0], params[1]);
	}

	handlePriceFilter = (evt) => {
		let filters = this.state.priceFilter;

		if (filters.has(evt.target.value)) {
			filters.delete(evt.target.value);
		} else {
			filters.add(evt.target.value);
		}

		this.setState({priceFilter: filters}, this.filterResults);
	}

	filterResults = () => {
		let filters = this.state.priceFilter;
		let filtered = [];
		let unfiltered = this.state.sortedArray;

		if (filters.size > 0) {for (let item of this.state.sortedArray) {
			if (filters.has(String(item.price))) {
				filtered.push(item);
			}
		}
			this.setState({filteredArray: filtered});
		} else {
			this.setState({filteredArray: unfiltered})
		}
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

		const searchForm = [
			<div className="searchForm">
				<form key={1} onSubmit={this.handleSubmit}>
					<label>
						<input name="searchString"
									className="form-control form-control-sm"
									type="text" 
									placeholder="japanese, asian, Tacorea" 
									value={this.state.searchString} 
									onChange={this.handleChange} />
					</label>
					<label>
						<select name="city"
								className="form-control form-control-sm"
								value={this.state.city} 
								onChange={this.handleChange}>
							<option value="">Choose a city</option>
							{cityOptions}
						</select>
					</label>
					<button className="btn btn-primary search ml-auto" type="submit">Search</button>
				</form>
			</div>
		]

		const sortForm = [
			<div>
				<form key={1}>
					<select name="sortBy"
							className="form-control form-control-sm"
							onChange={this.handleSortChange}>
						<option value="yelp_rating">Rating</option>
						<option value="price">Price (high to low)</option>
						<option value="price asc">Price (low to high)</option>
					</select>
				</form>
			</div>
		]

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

		return(
			<div className="row filterPanelContainer">
				<div className="col-5 filterPanel search">
					<div className="filterPanelBorder">
						<div>
							<div className="filterLabels">Find</div>
							{searchForm}
						</div>
						<div className="filterDivide search"></div>
						<div>
							<div className="filterLabels">Sort Results</div>
							{sortForm}
							<div className="filterDivide"></div>
							<div className="filterLabels">Filter By Price</div>
							{priceFilterBtns}
						</div>
					</div>
				</div>
				<div className="col-6">
				<SearchResults 
					results={this.state.results} 
					submitCity={this.state.submitCity}
					submitSearch={this.state.submitSearch}
					submitted={this.state.submitted}
					article={this.state.article}
					filteredArray={this.state.filteredArray} />
				</div>
			</div>
		);
	}
}

class SearchResults extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {

		const results = this.props.filteredArray;
		let url = "/details/";
		let resultArray = [];
		let resultKey = 0;
		
		for (let result in results) {
			resultKey++;
			let restaurant_id = results[result].restaurant_id
			let name = results[result].name;
			let city = results[result].city;
			let price = results[result].price;
			let yelp_rating = results[result].yelp_rating;
			let img = results[result].image;

			let priceIcon = [];
			for (let step = 0; step < price; step++ ) {
				priceIcon.push(<i key={step} className="fas fa-dollar-sign"></i>)
			}

			let ratingIcon = [];
			for (let step = 0; step < yelp_rating; step++ ) {
				if (yelp_rating - step == 0.5) {
					ratingIcon.push(<i key={step} className="fas fa-star-half"></i>)
				} else {
					ratingIcon.push(<i key={step} className="fas fa-star"></i>)
				}
			}

			resultArray.push(
				<div className="searchResult" key={resultKey}>
					<a href={url + restaurant_id}
					   target="_blank"
					   className="searchResultsTest noColorChange">
						<img className="imgThumbnail" src={img}/>
						<div className="searchResultBody">
							<span id="searchResultName">{name}</span><br/>
							Price: {priceIcon} | Yelp Rating: {ratingIcon}
						</div>
					</a>
				</div>
			)
		}


		if (resultArray.length > 0) {
			return (
				<div>
				<h4 className="searchHeader">{this.props.submitSearch} {this.props.article} {this.props.submitCity}</h4>
				{resultArray}
				</div>
			);
		}

		else if (resultArray.length == 0 && this.props.submitted == true) {
			return (<div><p className="searchHeader">No results for "{this.props.submitSearch}" {this.props.article} {this.props.submitCity}.</p></div>);
		}

		else {
			return (<div></div>)
		}

	}
}

ReactDOM.render(
	<SearchForm />,
	document.getElementById("root")
);