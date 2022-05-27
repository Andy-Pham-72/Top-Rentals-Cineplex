# create rating_list
rating_list = []

rating_null = 'null'

# assign titles into a variable
top_imdb_list = top_df.select('title').toPandas()['title']

for n in range(len(top_imdb_list)):
    title = top_imdb_list[n]
    print(title)
    # assign imdb id for the corresponding movie title
    imdb_id = top_df.select(top_df.imdb_id).filter(top_df.title == title).collect()[0][0]
    if imdb_id[:2] == 'tt':
        movie_scraper = MovieScraper(movie_title=title.lower())
        # slower the script
        time.sleep(1)
        # logger
        logger.info("Getting the imdb unique id: {}".format(imdb_id))
        # search movie info by the title
        try:
            movie_scraper = MovieScraper(movie_title= title.lower())
            # slower the script
            time.sleep(1)
            # logger
            #logger.info("Getting the imdb unique id: {}".format(imdb_id))

        except Exception as err:
            logger.warning("A warning message: {}".format(err))

        # get the imdb rating for the corresponding imdb_id
        try:
            imdb_rating = imdb_df.select('averageRating').where(imdb_df.tconst == imdb_id).collect()[0][0]
            print("imdb rating for title: {} is: {}".format(title, imdb_rating))
        except IndexError as err:
            logger.warning("A warning message: {}".format(err))
            logger.info("Adding Null values in 'imdb_rating' for the title: {}".format(title))
            imdb_rating = rating_null
            
        try:
            # get the rotten tomatoes movie ratings
            movie_scraper.extract_metadata()
            
            tomato_meter = movie_scraper.metadata['Score_Rotten']
            audience_score = movie_scraper.metadata['Score_Audience']
            if tomato_meter == '':
                tomato_meter = "null"
            elif audience_score == '':
                audience_score = 'null'
            else:
                pass
            
        except Exception as err:
            logger.warning("A warning message: {}".format(err))

            # create a search link for the alternate url due to timeout issue from the code above
            link = search_url + title.split()[0] 

            for k in range(len(title.split()[1:])):
                link= link + "%20" +title.split()[1:][k] # combine the components of the search link by adding "%20" eg: "https://www.rottentomatoes.com/search?search=the%20batman"
            # logger
            logger.info("Getting the search rotten tomatoes url for the alternate critic url: {}".format(link))
            # initialize the chrome browser
            driver_1 = init_chrome_browser(download_path, chrome_path, link)
            # get the alternate url
            url = WebDriverWait(driver_1, 10).until(EC.visibility_of_element_located((By.XPATH, alternate_class))).get_attribute("href")
            rotten_name = url[33:] # only get the movie title 
            movie_scraper = MovieScraper(movie_title= rotten_name.title()) # capitalize first letter eg: old => Old for the movie title
            movie_scraper.extract_metadata()

            # get the rotten tomatoes movie ratings
            tomato_meter = movie_scraper.metadata['Score_Rotten']
            audience_score = movie_scraper.metadata['Score_Audience']

        # append rating_list
        rating_list.append((imdb_id, imdb_rating, tomato_meter, audience_score ))
    
    else:
        print(imdb_id)
        rating_list.append((imdb_id, rating_null, rating_null, rating_null ))
        logger.info("Adding Null values for the title: {} that does not have 'imdb_id'".format(title))
        
# create a list for dataframe column's names
columns = ['imdb_id', 'imdb_rating', 'tomato_meter', 'audience_score']
table = spark.createDataFrame(data=rating_list,schema =columns)
table = table.withColumn("index", row_number().over(Window.orderBy(monotonically_increasing_id()))-1)
logger.info("Finished retrieving all the top critic review from the top rental movie list")

try:
    file_name = file_name + datetime.today().strftime('%Y-%m-%d')
    table.write.parquet("wasbs://{}@{}.blob.core.windows.net/top_rental_movie_rating/{}.parquet".format(container_name, storage_name,file_name))
    logger.info("Saved %s.parquet to azure 'top_rental_movie_rating' blob"%(file_name))
except Exception as err:
    logger.warning("A warning message: {}".format(err))
    
# transfer log file to azure blob storage
dbutils.fs.cp('file:%s'%(log_dir), 'wasbs://%s@%s.blob.core.windows.net//log/%s'%(container_name, storage_name, log_name))