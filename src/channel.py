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
        self._subscribers =int(self._channel_info['items'][0]['statistics']['subscriberCount'])
        self._video_count = self._channel_info['items'][0]['statistics']['videoCount']
        self._view_count = int(self._channel_info['items'][0]['statistics']['viewCount'])

    def __str__(self):
        """
        Вывод вида : Название канала(ссылка)
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """
        Сложение подписчиков
        """
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        """
        Вычитание подписчиков
        """
        return self.subscribers - other.subscribers

    def __le__(self, other):
        """
        Возвращает True если у 1го меньше или равно подписчиков
        """
        return self.subscribers <= other.subscribers

    def __lt__(self, other):
        """
        Возвращает True если 1го меньше подписчиков
        """
        return self.subscribers < other.subscribers

    def __gt__(self, other):
        """
        Возвращает True если у 1го больше подписчиков
        """
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        """
        Возвращает True если у 1го больше или равно подписчиков
        """
        return self.subscribers >= other.subscribers

    def __eq__(self, other):
        """
        Возвращает True если равное количество подписчиков
        """
        return self.subscribers == other.subscribers

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

    @property
    def view_count(self):
        return self._view_count

    @property
    def subscribers(self):
        return self._subscribers
