select distinct(people.name) from stars
JOIN movies ON stars.movie_id = movies.id
JOIN people ON stars.person_id = people.id
where movies.year = 2004
order by birth asc