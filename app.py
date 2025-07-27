import pickle
import streamlit as st
import requests
import pandas as pd

# TMDB API key
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch the API key
API_KEY = os.getenv("TMDB_API_KEY")

# Load movie data and similarity
movies = pd.DataFrame(pickle.load(open('movie_dict.pkl', 'rb')))
similarity = pd.DataFrame(pickle.load(open('similarity.pkl', 'rb')))

# Fetch poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend movies and fetch posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Streamlit page config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 20px;
        font-family: 'Segoe UI', sans-serif;
    }
    .movie-card {
        background-color: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    }
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
    }
    img {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #262730;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Selectbox
selected_movie = st.selectbox("🔍 Type or select a movie", movies['title'].values)

# Button
if st.button('🎥 Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("### 💡 You might also like:")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"""
                <div class='movie-card'>
                    <img src="{recommended_movie_posters[i]}" width="100%" height="auto">
                    <div class='movie-title'>{recommended_movie_names[i]}</div>
                </div>
            """, unsafe_allow_html=True)
