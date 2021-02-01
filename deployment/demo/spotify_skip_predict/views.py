from django.shortcuts import render
from django.views.generic import View
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_skip_predict.forms import UserInputForm
import os
import pandas as pd
import numpy as np
from .preprocessing_pipeline import CustomPreprocessor
from .utils import update_index, merge_session_with_track_feature, generating_target
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Model Libaries
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import lightgbm as lgb


CLIENT_ID = 'XXX'
CLIENT_SECRET = 'XXX'

# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET

def audio_features(features_from_api, popularity=0):
    features = {}
    #Add new key-values to store audio features
    features['acousticness'] = features_from_api['acousticness']
    features['danceability'] = features_from_api['danceability']
    features['energy'] = features_from_api['energy']
    features['instrumentalness'] = features_from_api['instrumentalness']
    features['liveness'] = features_from_api['liveness']
    features['loudness'] = features_from_api['loudness']
    features['speechiness'] = features_from_api['speechiness']
    features['tempo'] = features_from_api['tempo']
    features['valence'] = features_from_api['valence']
    features['key'] = features_from_api['key']
    features['time_signature'] = features_from_api['time_signature']
    features['us_popularity_estimate'] = popularity
    return features

def get_predictions(record):
    data = pd.read_csv("spotify_skip_predict\sample_data.csv")
    df = data.append(record, ignore_index=True)
    df.set_index('Unnamed: 0', inplace=True)
    preprocessing = CustomPreprocessor()
    preprocessing.fit(df)
    X = preprocessing.transform(df)
    model = pickle.load(open('spotify_skip_predict\spotify_skip_prediction_model.pkl', 'rb'))
    y_pred = model.predict(X.tail(1))
    y_pred = y_pred.round(0)
    return int(y_pred[-1])

# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        form = UserInputForm()
        context = {}
        context['form'] = form
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        query = self.request.GET.get('query')
        if query is not None:
            results = sp.search(q=query, limit=1)['tracks']['items']
            if results != []:
                for idx, track in enumerate(results):
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                context['track_name'] =  track_name
                context['track_artist'] = track_artist
                popularity = results[0]['popularity']
                features = sp.audio_features(results[0]['id'])
                features = audio_features(features[0], popularity)
            else:
                context['track_name'] =  None
                context['track_artist'] = None
            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html',context)

    def post(self, request, *args, **kwargs):
        form = UserInputForm()
        context = {}
        context['form'] = form
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        query = self.request.GET.get('query')
        # submit = self.request.GET.get('submit')
        if query is not None:
            results = sp.search(q=query, limit=1)['tracks']['items']
            if results != []:
                for idx, track in enumerate(results):
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                context['track_name'] =  track_name
                context['track_artist'] = track_artist
                popularity = results[0]['popularity']
                features = sp.audio_features(results[0]['id'])
                features = audio_features(features[0], popularity)
                
                form = UserInputForm(self.request.POST)
                session_data = {}
                if form.is_valid():
                    session_data['session_length'] = int(form.cleaned_data['session_length'])
                    session_data['context_type'] = form.cleaned_data['context_type']
                    session_data['hist_user_behavior_reason_start'] = form.cleaned_data['hist_user_behavior_reason_start']
                    session_data['hist_user_behavior_reason_end'] = form.cleaned_data['hist_user_behavior_reason_end']
                    session_data['mode'] = form.cleaned_data['mode']
                    session_data['premium'] = bool(form.cleaned_data['premium'])
                    session_data.update(features)
                    record = pd.Series(session_data)
                    prediction = get_predictions(record)
                    context['predict'] = prediction
                    
            else:
                context['track_name'] =  None
                context['track_artist'] = None
            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html',context)

