import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def update_index(session_data):
  """
  This function is used for creating a new column for track index and adding multiple index for session.
  Index for output dataframe will be session_id and track_index.
  """
  session_data["track_index"] = session_data["session_position"]
  session_data.set_index(["session_id", "track_index"], inplace=True)
  session_data.sort_index(inplace=True)
  return session_data


def merge_session_with_track_feature(session_data, track_features):
  """
    rename the track_id_clean from session_data and merging by left join on track_features
    return the merged_data
  """
  spotify_session = session_data.rename(columns={'track_id_clean':'track_id'})
  merged_data = spotify_session.merge(track_features, left_on="track_id", right_on="track_id", how="left")
  merged_data.drop("track_id", axis=1, inplace=True)
  return merged_data

def glimpse(data, get_corr=True):
  """
    prints the missing value percentage in data, data types of columns and correlation heatmap.
  """
  describe = pd.DataFrame(
      {
       'Missing (%cent)': ((data.isnull().sum())/data.shape[0])*100,
       'Data types': data.dtypes,     
  })
  if corr is True:
    corr_metrics = data.corr()
    sns.heatmap(corr_metrics)
    plt.show()
  return describe


def label_encoding_boolean_column(data):
  """
    changing the True/False of Boolean to 1/0.
  """
  for column in data.columns:
      if data[column].dtype == "bool":
        data[column] = data[column].astype("int32")
  return data