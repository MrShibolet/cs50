select distinct(name) from people
JOIN movies ON directors.movie_id = movies.id
JOIN ratings on movies.id = ratings.movie_id
JOIN directors ON people.id = directors.person_id
where rating >= 9