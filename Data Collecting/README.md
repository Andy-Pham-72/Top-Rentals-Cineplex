# Note

* In order to run [**`imdb_datasets_download.py`**](https://github.com/Andy-Pham-72/Top-Rentals-Cineplex/blob/master/Data%20Collecting/imdb_datasets_download.py) and [**`top_rentals_cineplex_scapper.py`**](https://github.com/Andy-Pham-72/Top-Rentals-Cineplex/blob/master/Data%20Collecting/top_rentals_cineplex_scapper.py), we have to install the `Selenium` package or you can refer to this [link](https://selenium-python.readthedocs.io/installation.html#drivers) for more information:

```bash
pip install selenium
```

* We also have to find the right chrome driver which is corresponding to your current chrome browser version in your computer which you can find in this [link](https://sites.google.com/chromium.org/driver/).

* In case you are using different browsers, you can find your proper driver in this [link](https://selenium-python.readthedocs.io/installation.html#drivers).

# Data Management

**imdb_datasets_downloader** : 
* Automates the official data sets downloading process from IMDB website. (using Selenium)
* Extracts gz files and convert tsv files to parquet files. (using PySpark)
* Saves files to Azure Blob Storage (ABS) as data warehouse.

**top_rentals_cineplex_scrapper** : 
* Scrapes Top 36 movie rentals’ titles on Cineplex website save as parquet file to ABS (using PySpark).
* Applies Slowly Changing Dimension Type 2 for table structure that stores and manages the current and historical data over time in terms of the top titles orders (e.g: Top 1, 2 ,3 ,.. and the data is current or not current with date, time)

**theMovieDb_and_RottenTomatoes_data_scraper** :
* Scrapes synopsis from themoviedb.org (using API) and top critics from rottentomatoes.com (using Selenium).
* Saves table as parquet file to ABS (using PySpark).

**top_rental_rating_from_imdb_and_rotten_tomatoes_data** :
* Extracts imdb_rating from IMDB data set and merge with Tomatometer and Audience Score from rottentomatoes.com into 1 table with corresponding imdb_id of the Top 36 movie rentals (using PySpark).
* Saves as parquet file to ABS.

![Screen Shot 2022-06-12 at 7 23 03 PM](https://user-images.githubusercontent.com/70767722/173257809-33cbe4e1-c515-4176-861a-8819dfd682dc.png)
