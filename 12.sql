select movies.title from people
join stars on people.id=stars.person_id
join movies on stars.movie_id = movies.id
where people.name like "Helena Bonham Carter"
intersect
select movies.title from people
join stars on people.id=stars.person_id
join movies on stars.movie_id = movies.id
where people.name like "Johnny Depp"