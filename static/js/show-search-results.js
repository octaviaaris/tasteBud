"use strict";

// Show search results

function showSearchResults(evt) {
	evt.preventDefault();
	let payload = {
		"search_string": $("#search-string-field").val(),
		"city": $("#city-field").val()
	}

	// Get response from '/search-results'
	$.get('/search.json', payload,
		
		function(result) {

			$("#show-results").empty();

			if ($.isEmptyObject(result)) {
				$("#show-results").html(`No results.`);

			} else {
				let restaurants_ids = Object.keys(result);
				for (let i = 0; i <= restaurants_ids.length - 1; i++) {
					$("#show-results").append(`<p>
						<a href="/details/${restaurants_ids[i]}">
						${result[restaurants_ids[i]]['name']} 
									 	 (${result[restaurants_ids[i]]['price']})</a></p>`);
				}
			}
		})
}

$("#search-form").on("submit", showSearchResults);