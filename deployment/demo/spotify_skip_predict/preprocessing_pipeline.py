import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class CustomPreprocessor(BaseEstimator, TransformerMixin):
  """
    CustomPreprocessor: It is generic steps to process the data that suit model like processing the datatypes, encoding the data, feature engineering and other things.
    After transform we receive the data to which we can provide to model and start training our model on it.

    >>>preprocessor = CustomPreprocessor()
    >>>preprocessor.fit(X)
    >>>preprocessed_X = preprocessor.transform(X)


  """
  def __init__(self):
    self.X = None
    self.y = None
  
  def fit(self, X, y=None):
    return self

  def transform(self, X, y=None):
    # libary for encoding
    import category_encoders as ce

    self.X = X.copy()  # making a copy so we won't effect the actual data
    self.X["premium"] = self.X["premium"].astype("bool")
    # changing the bool to interger 1/0
    for column in self.X.columns:
        if self.X[column].dtype == "bool":
          self.X[column] = self.X[column].astype("int32")
    
    # rename columns us_popularity_estimate to popularity
    self.X.rename(columns={'us_popularity_estimate':'popularity'}, inplace=True)


    # print(self.X.columns.to_list())

    # converting objects data to numeric data
    self.X[[
          'session_length', 
          'acousticness', 
          'danceability','popularity',
          'energy', 'instrumentalness', 
          'liveness', 'loudness', 
          'speechiness', 'tempo', 
          'valence', 'key',
          'time_signature',
          ]] = self.X[[
          'session_length', 
          'acousticness', 
          'danceability','popularity',
          'energy', 'instrumentalness', 
          'liveness', 'loudness', 
          'speechiness', 'tempo', 
          'valence', 'key',
          'time_signature',
          ]].apply(pd.to_numeric)

    # encoding the mode
    self.X['mode'] = self.X['mode'].replace({
        'major': 1,
        'minor': 0
    }).astype("int32")

    # encoding categorical columns
    categorical_cols = ['context_type', 'hist_user_behavior_reason_start', 'hist_user_behavior_reason_end']


    # setting one hot encoding for categorical columns (Nominal Columns)
    one_hot_encoder= ce.OneHotEncoder(cols=categorical_cols,handle_unknown='return_nan',return_df=True,use_cat_names=True)
    self.X = one_hot_encoder.fit_transform(self.X)

    return self.X