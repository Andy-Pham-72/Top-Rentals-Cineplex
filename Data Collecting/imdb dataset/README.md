## Metadata

Each dataset is contained in a gzipped, which is stored at [raw_data](https://github.com/Andy-Pham-72/Top-Rentals-Cineplex/tree/master/Data%20Collecting/imdb%20dataset/raw_data), tab-separated-values (TSV) formatted file, which is stored at [extracted_data](https://github.com/Andy-Pham-72/Top-Rentals-Cineplex/tree/master/Data%20Collecting/imdb%20dataset/extracted_data) in the UTF-8 character set. I also attached the google drive link so you can download from that easily.

The first line in each file contains headers that describe what is in each column. A ‘\N’ is used to denote that a particular field is missing or null for that title/name. The snippets of the datasets are as follows:



---------------------------------

**title.basics.tsv** - Contains the following information for titles:

* tconst (string) (changed to) => `imdb_id` - alphanumeric unique identifier of the title
* titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
* primaryTitle (string) – the more popular title / the title used by the filmmakers on promotional materials at the point of release
* originalTitle (string) - original title, in the original language
* isAdult (boolean) - 0: non-adult title; 1: adult title
* startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is the series start year
* endYear (YYYY) – TV Series end year. ‘\N’ for all other title types
* runtimeMinutes – primary runtime of the title, in minutes
* genres (string array) – includes up to three genres associated with the title


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tconst</th>
      <th>titleType</th>
      <th>primaryTitle</th>
      <th>originalTitle</th>
      <th>isAdult</th>
      <th>startYear</th>
      <th>endYear</th>
      <th>runtimeMinutes</th>
      <th>genres</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>tt0000001</td>
      <td>short</td>
      <td>Carmencita</td>
      <td>Carmencita</td>
      <td>0</td>
      <td>1894</td>
      <td>\N</td>
      <td>1</td>
      <td>Documentary,Short</td>
    </tr>
    <tr>
      <th>1</th>
      <td>tt0000002</td>
      <td>short</td>
      <td>Le clown et ses chiens</td>
      <td>Le clown et ses chiens</td>
      <td>0</td>
      <td>1892</td>
      <td>\N</td>
      <td>5</td>
      <td>Animation,Short</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tt0000003</td>
      <td>short</td>
      <td>Pauvre Pierrot</td>
      <td>Pauvre Pierrot</td>
      <td>0</td>
      <td>1892</td>
      <td>\N</td>
      <td>4</td>
      <td>Animation,Comedy,Romance</td>
    </tr>
    <tr>
      <th>3</th>
      <td>tt0000004</td>
      <td>short</td>
      <td>Un bon bock</td>
      <td>Un bon bock</td>
      <td>0</td>
      <td>1892</td>
      <td>\N</td>
      <td>12</td>
      <td>Animation,Short</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tt0000005</td>
      <td>short</td>
      <td>Blacksmith Scene</td>
      <td>Blacksmith Scene</td>
      <td>0</td>
      <td>1893</td>
      <td>\N</td>
      <td>1</td>
      <td>Comedy,Short</td>
    </tr>
  </tbody>
</table>
</div>

---------------------------------

**title.crew.tsv** – Contains the director and writer information for all the titles in IMDb. Fields include:

* tconst (string) (changed to) => `imdb_id` - alphanumeric unique identifier of the title
* directors (array of nconsts) (changed to) => `director_id` - director(s) of the given title
* writers (array of nconsts) (changed to) => `writer_id` – writer(s) of the given title


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tconst</th>
      <th>directors</th>
      <th>writers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>tt0000001</td>
      <td>nm0005690</td>
      <td>\N</td>
    </tr>
    <tr>
      <th>1</th>
      <td>tt0000002</td>
      <td>nm0721526</td>
      <td>\N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tt0000003</td>
      <td>nm0721526</td>
      <td>\N</td>
    </tr>
    <tr>
      <th>3</th>
      <td>tt0000004</td>
      <td>nm0721526</td>
      <td>\N</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tt0000005</td>
      <td>nm0005690</td>
      <td>\N</td>
    </tr>
  </tbody>
</table>
</div>

---------------------------------

**title.principals.tsv** – Contains the principal cast/crew for titles

* tconst (string) (changed to) => `imdb_id` - alphanumeric unique identifier of the title
* ordering (integer) – a number to uniquely identify rows for a given titleId
* nconst (string) - alphanumeric unique identifier of the name/person
* category (string) - the category of job that person was in
* job (string) - the specific job title if applicable, else '\N'
* characters (string) - the name of the character played if applicable, else '\N'

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tconst</th>
      <th>ordering</th>
      <th>nconst</th>
      <th>category</th>
      <th>job</th>
      <th>characters</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>tt0000001</td>
      <td>1</td>
      <td>nm1588970</td>
      <td>self</td>
      <td>\N</td>
      <td>["Self"]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>tt0000001</td>
      <td>2</td>
      <td>nm0005690</td>
      <td>director</td>
      <td>\N</td>
      <td>\N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tt0000001</td>
      <td>3</td>
      <td>nm0374658</td>
      <td>cinematographer</td>
      <td>director of photography</td>
      <td>\N</td>
    </tr>
    <tr>
      <th>3</th>
      <td>tt0000002</td>
      <td>1</td>
      <td>nm0721526</td>
      <td>director</td>
      <td>\N</td>
      <td>\N</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tt0000002</td>
      <td>2</td>
      <td>nm1335271</td>
      <td>composer</td>
      <td>\N</td>
      <td>\N</td>
    </tr>
  </tbody>
</table>
</div>

---------------------------------

**title.ratings.tsv** – Contains the IMDb rating and votes information for titles

* tconst (string) (changed to) => `imdb_id` - alphanumeric unique identifier of the title
* averageRating – weighted average of all the individual user ratings
* numVotes - number of votes the title has received


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tconst</th>
      <th>averageRating</th>
      <th>numVotes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>tt0000001</td>
      <td>5.7</td>
      <td>1831</td>
    </tr>
    <tr>
      <th>1</th>
      <td>tt0000002</td>
      <td>6.0</td>
      <td>236</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tt0000003</td>
      <td>6.5</td>
      <td>1591</td>
    </tr>
    <tr>
      <th>3</th>
      <td>tt0000004</td>
      <td>6.0</td>
      <td>153</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tt0000005</td>
      <td>6.2</td>
      <td>2407</td>
    </tr>
  </tbody>
</table>
</div>

---------------------------------

**name.basics.tsv.gz** – Contains the following information for names:

* nconst (string) - alphanumeric unique identifier of the name/person
* primaryName (string)– name by which the person is most often credited
* birthYear – in YYYY format
* deathYear – in YYYY format if applicable, else '\N'
* primaryProfession (array of strings)– the top-3 professions of the person
* knownForTitles (array of tconsts) – titles the person is known for (used as `imdb_id` collection)


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>nconst</th>
      <th>primaryName</th>
      <th>birthYear</th>
      <th>deathYear</th>
      <th>primaryProfession</th>
      <th>knownForTitles</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>nm0000001</td>
      <td>Fred Astaire</td>
      <td>1899</td>
      <td>1987</td>
      <td>soundtrack,actor,miscellaneous</td>
      <td>tt0072308,tt0050419,tt0053137,tt0031983</td>
    </tr>
    <tr>
      <th>1</th>
      <td>nm0000002</td>
      <td>Lauren Bacall</td>
      <td>1924</td>
      <td>2014</td>
      <td>actress,soundtrack</td>
      <td>tt0071877,tt0117057,tt0037382,tt0038355</td>
    </tr>
    <tr>
      <th>2</th>
      <td>nm0000003</td>
      <td>Brigitte Bardot</td>
      <td>1934</td>
      <td>\N</td>
      <td>actress,soundtrack,music_department</td>
      <td>tt0054452,tt0056404,tt0057345,tt0049189</td>
    </tr>
    <tr>
      <th>3</th>
      <td>nm0000004</td>
      <td>John Belushi</td>
      <td>1949</td>
      <td>1982</td>
      <td>actor,soundtrack,writer</td>
      <td>tt0077975,tt0072562,tt0078723,tt0080455</td>
    </tr>
    <tr>
      <th>4</th>
      <td>nm0000005</td>
      <td>Ingmar Bergman</td>
      <td>1918</td>
      <td>2007</td>
      <td>writer,director,actor</td>
      <td>tt0050976,tt0083922,tt0060827,tt0050986</td>
    </tr>
  </tbody>
</table>
</div>
