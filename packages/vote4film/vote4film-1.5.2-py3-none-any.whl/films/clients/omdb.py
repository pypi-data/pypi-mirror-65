import requests

from films.core import types


def get_film(api_key, url: str) -> types.Film:
    url = normalise_url(url)
    if not url.startswith("https://www.imdb.com/title/"):
        raise ValueError("Must be a direct link to a specific IMDB film")

    imdb_id = url[len("https://www.imdb.com/title/") :].partition("/")[0]

    response = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}")
    response.raise_for_status()
    json = response.json()

    title = json["Title"]
    year = int(json["Year"])

    if json["Rated"].lower() in ("not rated", "n/a"):
        # TODO: Retrieve age rating from BBFC
        age_rating = None
    else:
        age_rating = types.AgeRating(
            json["Rated"]
            .replace("PG-13", "12")
            .replace("TV-MA", "18")  # Compromise between 15 and 18
            .replace("R", "18")
        )
    imdb_rating = float(json["imdbRating"])
    genre = json["Genre"]
    runtime_mins = None
    if "min" in json["Runtime"]:
        runtime_mins = int(json["Runtime"].split()[0])
    plot = json["Plot"]
    poster_url = json["Poster"]

    return types.Film(
        imdb=url,
        title=title,
        year=year,
        imdb_rating=imdb_rating,
        imdb_age=age_rating,
        genre=genre,
        runtime_mins=runtime_mins,
        plot=plot,
        poster_url=poster_url,
    )


def normalise_url(url):
    if url.startswith("https://m.imdb.com"):
        url = url[len("https://m.imdb.com") :]
        url = "https://www.imdb.com" + url
    return url
