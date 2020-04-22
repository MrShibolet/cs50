select movies.title from people
join stars ON people.id = stars.person_id
join movies ON stars.movie_id = movies.id
join ratings on movies.id = ratings.movie_id
WHERE people.name = "Chadwick Boseman"
order by rating desc limit 5
