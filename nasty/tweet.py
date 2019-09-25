"""
Class collection containing the main Tweet class.
As well as a class for Hashtag, UserMention and TweetURLMapping
"""
from datetime import datetime
from typing import Dict, List, Tuple


class Hashtag:
    def __init__(self, text: str, indices: Tuple[int, int]):
        # e.g. "brexit"
        self.text = text
        # e.g. (16, 22)
        self.indices = indices

    def __repr__(self):
        return type(self).__name__ + repr(self.to_json())

    def to_json(self) -> Dict:
        return {
            'text': self.text,
            'indices': self.indices,
        }

    @classmethod
    def from_json(cls, obj: Dict) -> 'Hashtag':
        return cls(text=obj['text'],
                   indices=tuple(obj['indices']))


class UserMention:
    def __init__(self, screen_name: str, id_: str, indices: Tuple[int, int]):
        # e.g. OHiwi-2
        self.screen_name = screen_name
        # e.g. "1117712996795658241"
        self.id = id_
        # e.g. (14, 21)
        self.indices = indices

    def __repr__(self):
        return type(self).__name__ + repr(self.to_json())

    def to_json(self) -> Dict:
        return {
            'screen_name': self.screen_name,
            'id_str': self.id,
            'indices': self.indices,
        }

    @classmethod
    def from_json(cls, obj: Dict) -> 'UserMention':
        return cls(screen_name=obj['screen_name'],
                   id_=obj['id_str'],
                   indices=tuple(obj['indices']))


class TweetUrlMapping:
    def __init__(self,
                 url: str,
                 expanded_url: str,
                 display_url: str,
                 indices: Tuple[int, int]):
        # e.g. "https:\/\/t.co\/Dw84m8xRGw" | short t.co link
        self.url = url
        # e.g. "http:\/\/google.com" | the whole unchanged link
        self.expanded_url = expanded_url
        # e.g. "google.com" | the displayed part of the whole unchanged link
        self.display_url = display_url
        # e.g. (18,41)
        self.indices = indices

    def __repr__(self):
        return type(self).__name__ + repr(self.to_json())

    def to_json(self) -> Dict:
        return {
            'url': self.url,
            'expanded_url': self.expanded_url,
            'display_url': self.display_url,
            'indices': self.indices,
        }

    @classmethod
    def from_json(cls, obj: Dict) -> 'TweetUrlMapping':
        return cls(url=obj['url'],
                   expanded_url=obj['expanded_url'],
                   display_url=obj['display_url'],
                   indices=tuple(obj['indices']))


class Tweet:
    # TODO: Do we want to carry a source flag whether a Tweet is from the API or from the advanced search?

    def __init__(self,
                 created_at: datetime,
                 id_: str,
                 full_text: str,
                 name: str,
                 screen_name: str,
                 hashtags: List[Hashtag],
                 user_mentions: List[UserMention],
                 urls: List[TweetUrlMapping]) -> None
        self.created_at = created_at
        self.id = id_
        self.full_text = full_text
        self.hashtags = hashtags
        self.user_mentions = user_mentions
        self.urls = urls
        self.name = name
        self.screen_name = screen_name

    def __repr__(self):
        return type(self).__name__ + repr(self.to_json())

    @property
    def permalink(self) -> str:
        return 'https://twitter.com/{}/status/{}'.format(self.screen_name,
                                                         self.id)

    def to_json(self) -> Dict:
        result = {
            'created_at':
                self.created_at.strftime('%a %b %d %H:%M:%S +0000 %Y'),
            'id_str': self.id,
            'full_text': self.full_text,
            'entities': {
                'hashtags': [hashtag.to_json() for hashtag in self.hashtags],
                'user_mentions': [user_mention.to_json()
                                  for user_mention in self.user_mentions],
                'urls': [url.to_json() for url in self.urls]
            },
            'user': {
                'name': self.name,
                'screen_name': self.screen_name,
            }
        }

        return result

    @classmethod
    def from_json(cls, obj: Dict) -> 'Tweet':
        return cls(created_at=obj['created_at'],
                   id_=obj['id_str'],
                   full_text=obj['full_text'],
                   name=obj['user']['name'],
                   screen_name=obj['user']['screen_name'],
                   hashtags=[Hashtag.from_json(hashtag)
                             for hashtag in obj['entities']['hashtags']],
                   user_mentions=[UserMention.from_json(user_mention)
                                  for user_mention
                                  in obj['entities']['user_mentions']],
                   urls=[TweetUrlMapping.from_json(url)
                         for url in obj['entities']['urls']])

    @classmethod
    def calc_created_at_time_from_id(cls, id_: str) -> datetime:
        # Set microsecond to zero to match Twitter API.
        return datetime.utcfromtimestamp(
            ((int(id_) >> 22) + 1288834974657) / 1000).replace(microsecond=0)
