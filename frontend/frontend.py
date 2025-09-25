import streamlit as st
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from streamlit_image_select import image_select
import numpy
from streamlit_searchbox import st_searchbox
import joblib
from sklearn.neighbors import NearestNeighbors
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv("./.env")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")

# Spotify API initialization
sp = sp.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# Initializing ai model (ONLY FOR TEST)
# model = joblib.load('knn.pkl')

# Get track information
df = pd.read_csv('dataset.csv')
df = df.drop(["Unnamed: 0"], axis=1)

st.title("Snare - A music recommendation model")
st.markdown("Made by [Roboticol](https://github.com/Roboticol), Check out the [repo](https://github.com/Roboticol/Snare-A-Music-recommendation-AI) too!")

# Search for tracks
search = st.multiselect("Search for a track", df['track_search'].tolist())

tracks = [df[df['track_search'] == x] for x in search]
ids = [x['track_id'].values[0] for x in tracks]
track_names = [x['track_name'].values[0] for x in tracks]
track_artists = [x['artists'].values[0].split(";") for x in tracks]
track_search_names = [x['track_search'].values[0] for x in tracks]
track_albums = [x['album_name'].values[0] for x in tracks]
track_genre = [x['track_genre'].values[0] for x in tracks]
indices = [x.index for x in tracks]

track_df = df[df['track_name'].isin(track_names)]
meantrack_df = track_df.iloc[:, 4:19].mean()
# print("track_df: ", track_df)

# fetch model response
if (len(search) > 0):
    res = requests.post(url = API_URL, data = json.dumps({"inp" : meantrack_df.values.tolist()}), headers = {'Content-Type': 'application/json', 'X-API-KEY': API_KEY})
    # distance, rindices = model.kneighbors([meantrack_df], n_neighbors=9)
    rindices = json.loads(res.text)["output"]
    rindices = [x for x in rindices if x not in indices]
    if (len(rindices) > 8):
        del rindices[len(rindices)-1]

    # recommended tracks
    rtracks_df = df.iloc[rindices]
    # st.dataframe(rub)
    rtracks = [df[df.index == x] for x in rindices]
    rids = [x['track_id'].values[0] for x in rtracks]
    rtrack_names = [x['track_name'].values[0] for x in rtracks]
    rtrack_artists = [x['artists'].values[0].split(";") for x in rtracks]
    rtrack_search_names = [x['track_search'].values[0] for x in rtracks]
    rtrack_albums = [x['album_name'].values[0] for x in rtracks]
    rtrack_genre = [x['track_genre'].values[0] for x in rtracks]

    # fetch images and api info of our tracks
    track_imgs = []
    track_infos = []

    rtrack_imgs = []
    rtrack_infos = []

    for id in ids:
        track_info = sp.track(id)
        # print(track_info) 
        track_infos.append(track_info)
        image = track_info['album']['images'][1]['url']
        track_imgs.append(image)

    for id in rids:
        track_info = sp.track(id)
        # print(track_info) 
        rtrack_infos.append(track_info)
        image = track_info['album']['images'][1]['url']
        rtrack_imgs.append(image)

    # debugging stuff
    # print("names:", track_names)
    # print("images:", track_imgs)
    # print("artists:", track_artists)
    # print("--------------------")

    if (len(track_imgs) >= 1):

        # Show recommended tracks
        st.title("Recommended Tracks:")
        rimg = image_select(label = "", images=rtrack_imgs, captions=rtrack_search_names, use_container_width=False)
        rimgindex = rtrack_imgs.index(rimg)
        st.image(rimg)
        st.markdown("**" + rtrack_names[rimgindex] + "** -- " + ", ".join(rtrack_artists[rimgindex]) + "  ")
        st.markdown(f"**Album:** {rtrack_albums[rimgindex]}" + "  ")
        st.markdown(f"**Genre:** {rtrack_genre[rimgindex]}")
        st.markdown(f"[Link]({rtrack_infos[rimgindex]['album']['external_urls']['spotify']})")

        # Show selected tracks
        st.title("Selected Tracks:")
        img = image_select(label = "", images=track_imgs, captions=track_search_names, use_container_width=False)
        imgindex = track_imgs.index(img)
        st.image(img)
        st.write("**" + track_names[imgindex] + "** -- " + ", ".join(track_artists[imgindex]))
        st.write(f"**Album:** {track_albums[imgindex]}")
        st.markdown(f"**Genre:** {track_genre[imgindex]}")
        st.markdown(f"[Link]({track_infos[imgindex]['album']['external_urls']['spotify']})")
