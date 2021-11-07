# Note

* In order to run [**`imdb_datasets_download.py`**](https://github.com/Andy-Pham-72/Top-Rentals-Cineplex/blob/master/Data%20Collecting/imdb_datasets_download.py) and [**`top_rentals_cineplex_scapper.py`**](https://github.com/Andy-Pham-72/Top-Rentals-Cineplex/blob/master/Data%20Collecting/top_rentals_cineplex_scapper.py), we have to install the `Selenium` package or you can refer to this [link](https://selenium-python.readthedocs.io/installation.html#drivers) for more information:

```bash
pip install selenium
```

* We also have to find the right chrome driver which is corresponding to your current chrome browser version in your computer which you can find in this [link](https://sites.google.com/chromium.org/driver/).

* In case you are using different browsers, you can find your proper driver in this [link](https://selenium-python.readthedocs.io/installation.html#drivers).

### Future work:

* Edits the string format of movie titles of the top rentals Cineplex to match with the imdb dataset's movie titles format.
* Incorporates API python script to gather additional data from [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction).
* Scrapes some additional critics data which is corresponding to the top rental movies in Cineplex from [RottenTomatoes](https://www.rottentomatoes.com/).
