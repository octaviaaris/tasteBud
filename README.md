![tasteBud homepage](https://github.com/octaviaaris/tasteBud/blob/master/static/images/tasteBudhomepage.png)<br/>
tasteBud uses restaurant data pulled using the Yelp Fusion API and user ratings to tailor new restaurant recommendations to the user's unique taste. Its front-end is implemented in React.
## Table of Contents

* [Technologies](#technologies)
* [Features](#features)
* [Installation](#installation)
* [2.0](#future)
* [About the Developer](#aboutme)

## <a name="technologies"></a>Technologies
**Backend**: Python, Flask, SQLAlchemy, PostgreSQL<br/>
**Frontend**: JavaScript, jQuery, React, Bootstrap, Jinja, HTML, CSS<br/>
**APIs**: Yelp Fusion<br/>

## <a name="features"></a>Features
**Top Picks**:<br/>
tasteBud's recommendation machine uses collaborative filtering. For users, the recommender calculates the Pearson Correlation between a given user and others based on rating histories and saves the top-rated restaurants from the most similar users. For restaurants, the percent overlap in rating, price and categories is calculated to find places that best match a given user’s favorite restaurants. It then combines these outputs, filters out places the user already rated, and samples 5 random restaurants from the final list.<br/>

This two-pronged approach leverages the large sample size of restaurants in the database so that recommendations can still be generated even if there aren't enough similar users.<br/>
![tasteBud toppicks](https://github.com/octaviaaris/tasteBud/blob/master/static/images/tasteBudtoppicks.png)<br/>


**Filtering and Sorting**:<br/>
Users can also filter and sort their past reviews and search results by price and rating.<br/>
![tasteBud filter/sort](https://github.com/octaviaaris/tasteBud/blob/master/static/images/tasteBudfiltersort.png)<br/>

## <a name="installation"></a>Installation
Forthcoming...

## <a name="aboutme"></a>About the Developer
Before becoming a software engineer, Octavia led communications for an open source forest monitoring platform. Working with engineers in that role made her realize she'd rather be building the kinds of products she was helping to promote.

In her free time, Octavia plays Ultimate Frisbee competitively. She is a three-time national champion and two-time world champion. One of her favorite parts of competing around the world is getting to explore restaurants and cuisines with teammates in new places. tasteBud is Octavia's first project and was inspired by her experiences of discovering some of her favorite restaurants in different cities and countries with her friends.

Octavia currently lives in the Bay Area. Visit her on [LinkedIn](https://www.linkedin.com/in/octaviaaris).