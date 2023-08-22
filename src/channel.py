import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        youtube = self.get_service()
        self._channel_id = channel_id
        self._channel_info = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self._title = self._channel_info['items'][0]['snippet']['title']
        self._description = self._channel_info['items'][0]['snippet']['description']
        self._url = f'https://www.youtube.com/channel/{self._channel_id}'
        self._subscribers = self._channel_info['items'][0]['statistics']['subscriberCount']
        self._video_count = self._channel_info['items'][0]['statistics']['videoCount']
        self._view_count = self._channel_info['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(filename, 'w', encoding='utf-8') as feedsjson:
            entry = {
                'title': self._title,
                'description': self._description,
                'url': self._url,
                'subscribers': self._subscribers,
                'video_count': self._view_count,
                'view_count': self._view_count
            }
            data.append(entry)
            json.dump(data, feedsjson, ensure_ascii=False)

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return self._title

    @property
    def video_count(self):
        return self._video_count
