from googleapiclient.discovery import build
import os


class Video:

    def __init__(self, video_id):
        youtube = self.get_service()
        self.__video_id = video_id
        self._video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=self.__video_id
                                                     ).execute()
        self._video_title = self._video_response['items'][0]['snippet']['title']
        self._url = f'https://youtu.be/{self.__video_id}'
        self._view_count = self._video_response['items'][0]['statistics']['viewCount']
        self._like_count = self._video_response['items'][0]['statistics']['likeCount']
        self._comment_count = self._video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self._video_title

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
