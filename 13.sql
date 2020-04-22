select distinct(name) from people
join stars on people.id = stars.person_id
join movies on stars.movie_id = movies.id
where movies.title in(select distinct(movies.title)from people
join stars on people.id = stars.person_id
join movies on stars.movie_ID = movies.id
where people.name like "Kevin bacon" and people.birth = 1958) AND people.name != "Kevin Bacon"