# %%
# pip install google-api-python-client
# pip install oauth2client

# %%
from googleapiclient.discovery import build

# %%
youTubeApiKey="AIzaSyAC7mWnqrsycOKvMAKmdG5r3BB-3PpFPjk" #Input your youTubeApiKey
youtube=build('youtube','v3',developerKey=youTubeApiKey)
youtubeVideoParts = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
youtubeVideoChart = 'mostPopular'
youtubeVideoID = 'vtPK0feHhSs'
youtubeVideoMaxResults = 1000

# %%
import json
import pandas as pd
import numpy as np

# %%
listFile=[
          'scraping_data_01.txt',
          'scraping_data_02.txt',
          'scraping_data.txt'
]

out = open("/content/list_id.txt", "w")
listIDs = []
for file in [listFile[-2], listFile[-1], listFile[-3]]:
  f = open(file, "r")
  print(f)
  urls = f.readlines()
  
  for url in urls:
    id = url.split('?v=')[1]
    if id in listIDs:
      continue
    listIDs.append(id)
    print(id)
for id in listIDs:
  out.write(id)
print(len(listIDs))

# %%
def getInfoYouTubeVideo(id):
  request = youtube.videos().list(
          part=youtubeVideoParts,
          id=id,
          regionCode="VN"
      )
  response = request.execute()
  return response

df = []
for id in listIDs:
  id = id.split('\n')[0]
  response = getInfoYouTubeVideo(id)
  print(len(response['items']))
  if len(response['items']) == 0:
    continue
  i = 0
  videoID = response['items'][i]['id']
  videoTitle = response['items'][i]['snippet']['title']
  videoPublishAt = response['items'][i]['snippet']['publishedAt']
  videoDescription = response['items'][i]['snippet']['description']
  videoChannelTitle = response['items'][i]['snippet']['channelTitle']
  videoTags = response['items'][i]['snippet'].get('tags')
  videoCategoryId = response['items'][i]['snippet']['categoryId']
  if response['items'][i]['snippet'].get('defaultAudioLanguage') is None: 
    videoDefaultAudioLanguage = ""
  else:  
    videoDefaultAudioLanguage = response['items'][i]['snippet']['defaultAudioLanguage']
  if 'defaultAudioLanguage' in response['items'][i]:
    print('hello')
  videoDuration = response['items'][i]['contentDetails']['duration']
  videoDimension = response['items'][i]['contentDetails']['dimension']
  videoDefinition = response['items'][i]['contentDetails']['definition']
  videoCaption = response['items'][i]['contentDetails']['caption']
  videoPrivacyStatus = response['items'][i]['status']['privacyStatus']
  videoEmbeddable = response['items'][i]['status']['embeddable']
  videoMakeForKids = response['items'][i]['status']['madeForKids']
  videoViewCount = response['items'][i]['statistics']['viewCount']
  videoLikeCount = response['items'][i]['statistics'].get('likeCount')
  videoDislikeCount = response['items'][i]['statistics'].get('dislikeCount')
  videoFavoriteCount = response['items'][i]['statistics'].get('favoriteCount')
  videoCommentCount = response['items'][i]['statistics'].get('commentCount')
  videoTopicCategories = response['items'][i].get('topicDetails')
  if videoTopicCategories is None:
    videoTopicCategories=""
  else:
    videoTopicCategories = videoTopicCategories.get('topicCategories')
  videoDict = {
    'id': videoID,
    'publishAt': videoPublishAt,
    'title': videoTitle,
    'description': videoDescription,
    'channelTitle': videoChannelTitle,
    'tags': videoTags,
    'categoryId': videoCategoryId,
    'defaultAudioLanguage': videoDefaultAudioLanguage,
    'duration': videoDuration,
    'dimension': videoDimension,
    'definition': videoDefinition,
    'caption': videoCaption,
    'privacyStatus':videoPrivacyStatus,
    'embeddable': videoEmbeddable,
    'madeForKids': videoMakeForKids,
    'viewCount': videoViewCount,
    'likeCount': videoLikeCount,
    'dislikeCount': videoDislikeCount,
    'favoriteCount': videoFavoriteCount,
    'commentCount': videoCommentCount,
    'topicCategories': videoTopicCategories
  }
  df.append(videoDict)
display(pd.DataFrame(df))

# %%
pd.DataFrame(df).to_csv('list_info_02.csv', index=False)

# %%
pd.DataFrame(df).shape

# %%
videoDict = {
    'id': [videoID],
    'publishAt': [videoPublishAt],
    'title': [videoTitle],
    'description': [videoDescription],
    'channelTitle': [videoChannelTitle],
    'tags': [videoTags],
    'categoryId': [videoCategoryId],
    'defaultAudioLanguage': [videoDefaultAudioLanguage],
    'duration': [videoDuration],
    'dimension': [videoDimension],
    'definition': [videoDefinition],
    'caption': [videoCaption],
    'privacyStatus': [videoPrivacyStatus],
    'embeddable': [videoEmbeddable],
    'madeForKids': [videoMakeForKids],
    'viewCount': [videoViewCount],
    'likeCount': [videoLikeCount],
    'dislikeCount': [videoDislikeCount],
    'favoriteCount': [videoFavoriteCount],
    'commentCount': [videoCommentCount],
    'topicCategories': [videoTopicCategories]
}


