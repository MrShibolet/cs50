select name from people
join movies on stars.movie_id = movies.id
join stars on people.id = stars.person_id
where movies.title like "Toy story"