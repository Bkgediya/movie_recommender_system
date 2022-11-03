import streamlit as st
import pickle
import pandas as pd
import requests

movies_dictionary = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dictionary)


def fetchPoster(movieId):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}.?api_key=8265bd1679663a7ea12ac168da84d2e8'.format(movieId))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_poster = []
    for movie in movies_list:
        movie_id = movies.iloc[movie[0]].movie_id
        recommend_movies.append(movies.iloc[movie[0]].title)
        recommend_movies_poster.append(fetchPoster(movie_id))
    return recommend_movies, recommend_movies_poster


# 8265bd1679663a7ea12ac168da84d2e8
#

st.title('Movie Recommender System')

option = st.selectbox('How would you like to be contacted?', movies['title'].values)
if st.button('Recommend'):
    movies, posters = recommend(option)
    column = 5

    col1, col2, col3, col4, col5 = st.columns(column)
    with col1:
        st.text(movies[0])
        st.image(posters[0])
    with col2:
        st.text(movies[1])
        st.image(posters[1])
    with col3:
        st.text(movies[2])
        st.image(posters[2])
    with col4:
        st.text(movies[3])
        st.image(posters[3])
    with col5:
        st.text(movies[4])
        st.image(posters[4])
