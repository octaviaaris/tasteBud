"use strict";

class SearchForm extends React.Component {
	constructor(props) {
		super(props);
		this.state = {searchString: '', city: ''};
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(evt) {
		this.setState({[evt.target.name]: evt.target.value})
	}

	handleSubmit(event) {

		alert('You want some ' + this.state.searchString + ' in ' + this.state.city + '.')
		event.preventDefault();
	}

	render() {

		return(
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
					<option value="Oakland">Oakland</option>
				</select>
				</label>
				<input type="submit" value="Search" />
			</form>
		);
	}
}

ReactDOM.render(
	<SearchForm />,
	document.getElementById("root")
);

