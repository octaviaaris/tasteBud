class TopPicks extends React.Component {
	constructor(props) {
		super(props);
		this.state = {topPicks: []};
	}

	componentDidMount() {
		fetch(`/top-picks.json`).then((response) => response.json())
								.then((data) => {
									let recs = []
									for (let rec of data.recs) {
										recs.push(rec)
									}
									this.setState({topPicks: recs});
								});

		console.log(this.state.topPicks);
	}

	render() {

		// console.log(this.sate.topPicks);
		return ("hi")
	}
}

ReactDOM.render(
	<TopPicks />,
	document.getElementById("recommendations")
	)