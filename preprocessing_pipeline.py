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

    # changing the bool to interger 1/0
    for column in self.X.columns:
        if self.X[column].dtype == "bool":
          self.X[column] = self.X[column].astype("int32")


    # adding new skipped column and dropping skip_1, skip_2 and skip_3
    self.X["skipped"] = self.X["skip_1"]*self.X["skip_2"]*self.X["skip_3"]
    self.X.drop(labels=["skip_1", "skip_2", "skip_3", "not_skipped"], inplace=True, axis=1)

    # converting objects data to numeric data
    self.X[['duration', 'release_year', 'us_popularity_estimate', 'acousticness',
          'beat_strength', 'bounciness', 'danceability', 'dyn_range_mean',
          'energy', 'flatness', 'instrumentalness', 'key', 'liveness', 'loudness',
          'mechanism', 'organism', 'speechiness', 'tempo',
          'time_signature', 'valence', 'acoustic_vector_0', 'acoustic_vector_1',
          'acoustic_vector_2', 'acoustic_vector_3', 'acoustic_vector_4',
          'acoustic_vector_5', 'acoustic_vector_6', 'acoustic_vector_7',
          'skipped']
          ] = self.X[
            ['duration', 'release_year', 'us_popularity_estimate', 'acousticness',
          'beat_strength', 'bounciness', 'danceability', 'dyn_range_mean',
          'energy', 'flatness', 'instrumentalness', 'key', 'liveness', 'loudness',
          'mechanism', 'organism', 'speechiness', 'tempo',
          'time_signature', 'valence', 'acoustic_vector_0', 'acoustic_vector_1',
          'acoustic_vector_2', 'acoustic_vector_3', 'acoustic_vector_4',
          'acoustic_vector_5', 'acoustic_vector_6', 'acoustic_vector_7',
          'skipped']
          ].apply(pd.to_numeric)

    # encoding the mode
    self.X['mode'] = self.X['mode'].replace({
        'major': 1,
        'minor': 0
    }).astype("int32")

    # chaning the date to weekday and droping the date column
    self.X["date"] = pd.to_datetime(self.X["date"])
    self.X['wkdy'] = self.X["date"].dt.dayofweek
    self.X.drop("date", inplace=True, axis=1)

    # encoding categorical columns
    categorical_cols = ["hist_user_behavior_reason_end","hist_user_behavior_reason_start", "context_type"]

    # iterating for each categorical column
    for col in categorical_cols:
      # merging labels if they are less than threshold (< 0.001)
      counts = self.X[col].value_counts(normalize=True)
      labels_less_then_threshold = counts[counts < 0.001].index.to_list()
      where_to_replace = self.X[col].isin(labels_less_then_threshold).copy()
      self.X.loc[where_to_replace, col] = 'merged'

    # setting one hot encoding for categorical columns (Nominal Columns)
    one_hot_encoder= ce.OneHotEncoder(cols=categorical_cols,handle_unknown='return_nan',return_df=True,use_cat_names=True)
    self.X = one_hot_encoder.fit_transform(self.X)

    return self.X