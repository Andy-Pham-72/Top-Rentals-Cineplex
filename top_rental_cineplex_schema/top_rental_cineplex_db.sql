create schema top_rental_cineplex;

set schema 'top_rental_cineplex';
-- The IMDB Data sets

drop table if exists top_rental_cineplex.dim_title_basic;
create table top_rental_cineplex.dim_title_basic(
        imdb_id VARCHAR not null,
        prime_title VARCHAR,
        original_title VARCHAR,
        is_adult BOOLEAN,
        start_year VARCHAR,
        end_year VARCHAR,
        runtime_minutes smallint,
        genres VARCHAR,
        
        primary key (imdb_id)

) ;

drop table if exists top_rental_cineplex.name_basic;
create table top_rental_cineplex.name_basic(
        name_id VARCHAR not null,
        primary_name VARCHAR,
        birt_year VARCHAR,
        death_year VARCHAR,
        primary_profession VARCHAR,
        known_for_titles VARCHAR,
        primary key (name_id)
);


drop table if exists top_rental_cineplex.title_principal;
create table top_rental_cineplex.title_principal (
        imdb_id VARCHAR not null,
        ordering smallint,
        name_id VARCHAR not NULL,
        category VARCHAR,
        job VARCHAR,
        characters VARCHAR,
        
        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id),
         
        foreign key (name_id)
         references top_rental_cineplex.name_basic(name_id)
        
);

drop table if exists top_rental_cineplex.title_rating;
create table top_rental_cineplex.title_rating(
        imdb_id VARCHAR not null,
        average_rating FLOAT,
        num_votes smallint,
        
        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id)

);

drop table if exists top_rental_cineplex.dim_top_cineplex_rental_list;
create table top_rental_cineplex.dim_top_cineplex_rental_list(
        imdb_id VARCHAR not null,
        ordering smallint not null,
        title VARCHAR,
        is_current BOOLEAN,
        start_date DATE,
        end_date DATE,
        rental_id int not null,
        
        primary key (rental_id),
        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id)
);

drop table if exists top_rental_cineplex.dim_top_rental_rating;
create table top_rental_cineplex.dim_top_rental_rating(
        imdb_id VARCHAR not null,
        imdb_rating FLOAT,
        tomato_meter FLOAT,
        audience_score FLOAT,
        rating_id int NOT NULL,
        
		primary key (rating_id),
        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id)
);

drop table if exists top_rental_cineplex.dim_top_rental_critic;
create table top_rental_cineplex.dim_top_rental_critic(
        review_id int not NULL,
        imdb_id VARCHAR not NULL,
        reviewer VARCHAR,
        review VARCHAR,
        
        primary key (review_id),
        
        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id)
         );
         
drop table if exists top_rental_cineplex.title_crew;
create table top_rental_cineplex.title_crew(
        imdb_id VARCHAR not null,
        director_id VARCHAR not null,
        writer_id VARCHAR,
        
        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id),
         
        foreign key (director_id)
         references top_rental_cineplex.name_basic(name_id),

        foreign key (writer_id)
         references top_rental_cineplex.name_basic(name_id)
);

drop table if exists top_rental_cineplex.dim_synopsis;
create table top_rental_cineplex.dim_synopsis(
        imdb_id VARCHAR not null,
        synopsis VARCHAR,
        synopsis_id int not null,
	
		primary key (synopsis_id),
        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id)
);

drop table if exists top_rental_cineplex.fact_top_rental_detail;
create table top_rental_cineplex.fact_top_rental_detail(
        imdb_id VARCHAR not null,
        rental_id int not null,
        rating_id int not null,
        title VARCHAR not null,
        ordering smallint not null,
        imdb_rating FLOAT,
        tomato_meter FLOAT,
        audience_score FLOAT,

        foreign key (imdb_id)
         references top_rental_cineplex.dim_title_basic(imdb_id),
        foreign key (rental_id)
         references top_rental_cineplex.dim_top_cineplex_rental_list(rental_id),
        foreign key (rating_id)
         references top_rental_cineplex.dim_top_rental_rating(rating_id)
);