from typing import Optional, Any, Dict, Union, List

import pandas as pd

from cryptocompsdk.general.parse import from_int, from_none, from_union, from_float, from_str, to_float, from_bool, \
    from_dict, to_class, is_type, from_int_or_str, from_na, from_str_number, from_list, from_stringified_bool, \
    from_plain_dict
from cryptocompsdk.response import ResponseAPIBase, ResponseException


class RateLimit:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'RateLimit':
        assert isinstance(obj, dict)
        return RateLimit()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class Parent:
    name: Optional[str]
    url: Optional[str]
    internal_id: Optional[int]
    internal_data: Optional[dict]

    def __init__(self, name: Optional[str], url: Optional[str], internal_id: Optional[int], internal_data: Optional[dict]) -> None:
        self.name = name
        self.url = url
        self.internal_id = internal_id
        self.internal_data = internal_data

    @staticmethod
    def from_dict(obj: Any) -> 'Parent':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("Name"))
        url = from_union([from_str, from_none], obj.get("Url"))
        internal_id = from_union([from_int, from_none], obj.get("InternalId"))
        internal_data = from_union([from_plain_dict, from_none], obj.get("InternalData"))
        return Parent(name, url, internal_id, internal_data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Name"] = from_union([from_str, from_none], self.name)
        result["Url"] = from_union([from_str, from_none], self.url)
        result["InternalId"] = from_union([from_int, from_none], self.internal_id)
        result["InternalData"] = self.internal_data
        return result


class CodeRepository:
    forks: Optional[int]
    last_update: Optional[int]
    open_total_issues: Optional[int]
    subscribers: Optional[int]
    fork: Optional[bool]
    closed_pull_issues: Optional[int]
    parent: Optional[Parent]
    open_pull_issues: Optional[int]
    stars: Optional[int]
    closed_issues: Optional[int]
    url: Optional[str]
    contributors: Optional[int]
    created_at: Optional[int]
    open_issues: Optional[int]
    source: Optional[Parent]
    closed_total_issues: Optional[int]
    size: Optional[int]
    last_push: Optional[int]

    def __init__(self, forks: Optional[int], last_update: Optional[int], open_total_issues: Optional[int], subscribers: Optional[int], fork: Optional[bool], closed_pull_issues: Optional[int], parent: Optional[Parent], open_pull_issues: Optional[int], stars: Optional[int], closed_issues: Optional[int], url: Optional[str], contributors: Optional[int], created_at: Optional[int], open_issues: Optional[int], source: Optional[Parent], closed_total_issues: Optional[int], size: Optional[int], last_push: Optional[int]) -> None:
        self.forks = forks
        self.last_update = last_update
        self.open_total_issues = open_total_issues
        self.subscribers = subscribers
        self.fork = fork
        self.closed_pull_issues = closed_pull_issues
        self.parent = parent
        self.open_pull_issues = open_pull_issues
        self.stars = stars
        self.closed_issues = closed_issues
        self.url = url
        self.contributors = contributors
        self.created_at = created_at
        self.open_issues = open_issues
        self.source = source
        self.closed_total_issues = closed_total_issues
        self.size = size
        self.last_push = last_push

    @staticmethod
    def from_dict(obj: Any) -> 'CodeRepository':
        assert isinstance(obj, dict)
        forks = from_union([from_int, from_none], obj.get("forks"))
        last_update = from_union([from_none, lambda x: int(from_str(x))], obj.get("last_update"))
        open_total_issues = from_union([from_int, from_none], obj.get("open_total_issues"))
        subscribers = from_union([from_int, from_none], obj.get("subscribers"))
        fork = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("fork"))
        closed_pull_issues = from_union([from_int, from_none], obj.get("closed_pull_issues"))
        parent = from_union([Parent.from_dict, from_none], obj.get("parent"))
        open_pull_issues = from_union([from_int, from_none], obj.get("open_pull_issues"))
        stars = from_union([from_int, from_none], obj.get("stars"))
        closed_issues = from_union([from_int, from_none], obj.get("closed_issues"))
        url = from_union([from_str, from_none], obj.get("url"))
        contributors = from_union([from_int, from_none], obj.get("contributors"))
        created_at = from_union([from_none, lambda x: int(from_str(x))], obj.get("created_at"))
        open_issues = from_union([from_int, from_none], obj.get("open_issues"))
        source = from_union([Parent.from_dict, from_none], obj.get("source"))
        closed_total_issues = from_union([from_int, from_none], obj.get("closed_total_issues"))
        size = from_union([from_int, from_none], obj.get("size"))
        last_push = from_union([from_none, lambda x: int(from_str(x))], obj.get("last_push"))
        return CodeRepository(forks, last_update, open_total_issues, subscribers, fork, closed_pull_issues, parent, open_pull_issues, stars, closed_issues, url, contributors, created_at, open_issues, source, closed_total_issues, size, last_push)

    def to_dict(self) -> dict:
        result: dict = {}
        result["forks"] = from_union([from_int, from_none], self.forks)
        result["last_update"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.last_update)
        result["open_total_issues"] = from_union([from_int, from_none], self.open_total_issues)
        result["subscribers"] = from_union([from_int, from_none], self.subscribers)
        result["fork"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.fork)
        result["closed_pull_issues"] = from_union([from_int, from_none], self.closed_pull_issues)
        result["parent"] = from_union([lambda x: to_class(Parent, x), from_none], self.parent)
        result["open_pull_issues"] = from_union([from_int, from_none], self.open_pull_issues)
        result["stars"] = from_union([from_int, from_none], self.stars)
        result["closed_issues"] = from_union([from_int, from_none], self.closed_issues)
        result["url"] = from_union([from_str, from_none], self.url)
        result["contributors"] = from_union([from_int, from_none], self.contributors)
        result["created_at"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.created_at)
        result["open_issues"] = from_union([from_int, from_none], self.open_issues)
        result["source"] = from_union([lambda x: to_class(Parent, x), from_none], self.source)
        result["closed_total_issues"] = from_union([from_int, from_none], self.closed_total_issues)
        result["size"] = from_union([from_int, from_none], self.size)
        result["last_push"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.last_push)
        return result


class CodeRepositories:
    list: Optional[List[CodeRepository]]
    points: Optional[int]

    def __init__(self, list: Optional[List[CodeRepository]], points: Optional[int]) -> None:
        self.list = list
        self.points = points

    @staticmethod
    def from_dict(obj: Any) -> 'CodeRepositories':
        assert isinstance(obj, dict)
        list = from_union([lambda x: from_list(CodeRepository.from_dict, x), from_none], obj.get("List"))
        points = from_union([from_int, from_none], obj.get("Points"))
        return CodeRepositories(list, points)

    def to_dict(self) -> dict:
        result: dict = {}
        result["List"] = from_union([lambda x: from_list(lambda x: to_class(CodeRepository, x), x), from_none], self.list)
        result["Points"] = from_union([from_int, from_none], self.points)
        return result


class PageViewsSplit:
    overview: Optional[int]
    markets: Optional[int]
    analysis: Optional[int]
    charts: Optional[int]
    trades: Optional[int]
    orderbook: Optional[int]
    forum: Optional[int]
    influence: Optional[int]
    news: Optional[int]
    timeline: Optional[int]

    def __init__(self, overview: Optional[int], markets: Optional[int], analysis: Optional[int], charts: Optional[int], trades: Optional[int], orderbook: Optional[int], forum: Optional[int], influence: Optional[int], news: Optional[int], timeline: Optional[int]) -> None:
        self.overview = overview
        self.markets = markets
        self.analysis = analysis
        self.charts = charts
        self.trades = trades
        self.orderbook = orderbook
        self.forum = forum
        self.influence = influence
        self.news = news
        self.timeline = timeline

    @staticmethod
    def from_dict(obj: Any) -> 'PageViewsSplit':
        assert isinstance(obj, dict)
        overview = from_union([from_int, from_none], obj.get("Overview"))
        markets = from_union([from_int, from_none], obj.get("Markets"))
        analysis = from_union([from_int, from_none], obj.get("Analysis"))
        charts = from_union([from_int, from_none], obj.get("Charts"))
        trades = from_union([from_int, from_none], obj.get("Trades"))
        orderbook = from_union([from_int, from_none], obj.get("Orderbook"))
        forum = from_union([from_int, from_none], obj.get("Forum"))
        influence = from_union([from_int, from_none], obj.get("Influence"))
        news = from_union([from_int, from_none], obj.get("News"))
        timeline = from_union([from_int, from_none], obj.get("Timeline"))
        return PageViewsSplit(overview, markets, analysis, charts, trades, orderbook, forum, influence, news, timeline)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Overview"] = from_union([from_int, from_none], self.overview)
        result["Markets"] = from_union([from_int, from_none], self.markets)
        result["Analysis"] = from_union([from_int, from_none], self.analysis)
        result["Charts"] = from_union([from_int, from_none], self.charts)
        result["Trades"] = from_union([from_int, from_none], self.trades)
        result["Orderbook"] = from_union([from_int, from_none], self.orderbook)
        result["Forum"] = from_union([from_int, from_none], self.forum)
        result["Influence"] = from_union([from_int, from_none], self.influence)
        result["News"] = from_union([from_int, from_none], self.news)
        result["Timeline"] = from_union([from_int, from_none], self.timeline)
        return result


class SimilarItem:
    id: Optional[int]
    name: Optional[str]
    full_name: Optional[str]
    image_url: Optional[str]
    url: Optional[str]
    following_type: Optional[int]

    def __init__(self, id: Optional[int], name: Optional[str], full_name: Optional[str], image_url: Optional[str], url: Optional[str], following_type: Optional[int]) -> None:
        self.id = id
        self.name = name
        self.full_name = full_name
        self.image_url = image_url
        self.url = url
        self.following_type = following_type

    @staticmethod
    def from_dict(obj: Any) -> 'SimilarItem':
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("Id"))
        name = from_union([from_str, from_none], obj.get("Name"))
        full_name = from_union([from_str, from_none], obj.get("FullName"))
        image_url = from_union([from_str, from_none], obj.get("ImageUrl"))
        url = from_union([from_str, from_none], obj.get("Url"))
        following_type = from_union([from_int, from_none], obj.get("FollowingType"))
        return SimilarItem(id, name, full_name, image_url, url, following_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.id)
        result["Name"] = from_union([from_str, from_none], self.name)
        result["FullName"] = from_union([from_str, from_none], self.full_name)
        result["ImageUrl"] = from_union([from_str, from_none], self.image_url)
        result["Url"] = from_union([from_str, from_none], self.url)
        result["FollowingType"] = from_union([from_int, from_none], self.following_type)
        return result


class CryptoCompare:
    points: Optional[int]
    followers: Optional[int]
    posts: Optional[int]
    similar_items: Optional[List[SimilarItem]]
    comments: Optional[int]
    page_views_split: Optional[PageViewsSplit]
    page_views: Optional[int]
    cryptopian_followers: Optional[List[Any]]

    def __init__(self, points: Optional[int], followers: Optional[int], posts: Optional[int], similar_items: Optional[List[SimilarItem]], comments: Optional[int], page_views_split: Optional[PageViewsSplit], page_views: Optional[int], cryptopian_followers: Optional[List[Any]]) -> None:
        self.points = points
        self.followers = followers
        self.posts = posts
        self.similar_items = similar_items
        self.comments = comments
        self.page_views_split = page_views_split
        self.page_views = page_views
        self.cryptopian_followers = cryptopian_followers

    @staticmethod
    def from_dict(obj: Any) -> 'CryptoCompare':
        assert isinstance(obj, dict)
        points = from_union([from_int, from_none], obj.get("Points"))
        followers = from_union([from_int, from_none], obj.get("Followers"))
        posts = from_union([from_int, from_none], obj.get("Posts"))
        similar_items = from_union([lambda x: from_list(SimilarItem.from_dict, x), from_none], obj.get("SimilarItems"))
        comments = from_union([from_int, from_none], obj.get("Comments"))
        page_views_split = from_union([PageViewsSplit.from_dict, from_none], obj.get("PageViewsSplit"))
        page_views = from_union([from_int, from_none], obj.get("PageViews"))
        cryptopian_followers = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("CryptopianFollowers"))
        return CryptoCompare(points, followers, posts, similar_items, comments, page_views_split, page_views, cryptopian_followers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Points"] = from_union([from_int, from_none], self.points)
        result["Followers"] = from_union([from_int, from_none], self.followers)
        result["Posts"] = from_union([from_int, from_none], self.posts)
        result["SimilarItems"] = from_union([lambda x: from_list(lambda x: to_class(SimilarItem, x), x), from_none], self.similar_items)
        result["Comments"] = from_union([from_int, from_none], self.comments)
        result["PageViewsSplit"] = from_union([lambda x: to_class(PageViewsSplit, x), from_none], self.page_views_split)
        result["PageViews"] = from_union([from_int, from_none], self.page_views)
        result["CryptopianFollowers"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.cryptopian_followers)
        return result


class Facebook:
    points: Optional[int]
    talking_about: Optional[int]
    is_closed: Optional[bool]
    likes: Optional[int]
    name: Optional[str]
    link: Optional[str]

    def __init__(self, points: Optional[int], talking_about: Optional[int], is_closed: Optional[bool], likes: Optional[int], name: Optional[str], link: Optional[str]) -> None:
        self.points = points
        self.talking_about = talking_about
        self.is_closed = is_closed
        self.likes = likes
        self.name = name
        self.link = link

    @staticmethod
    def from_dict(obj: Any) -> 'Facebook':
        assert isinstance(obj, dict)
        points = from_union([from_int, from_none], obj.get("Points"))
        talking_about = from_union([from_int, from_none], obj.get("talking_about"))
        is_closed = from_union([from_none, lambda x: from_stringified_bool(from_str(x))], obj.get("is_closed"))
        likes = from_union([from_int, from_none], obj.get("likes"))
        name = from_union([from_str, from_none], obj.get("name"))
        link = from_union([from_str, from_none], obj.get("link"))
        return Facebook(points, talking_about, is_closed, likes, name, link)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Points"] = from_union([from_int, from_none], self.points)
        result["talking_about"] = from_union([from_int, from_none], self.talking_about)
        result["is_closed"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(bool, x))(x)).lower())(x))], self.is_closed)
        result["likes"] = from_union([from_int, from_none], self.likes)
        result["name"] = from_union([from_str, from_none], self.name)
        result["link"] = from_union([from_str, from_none], self.link)
        return result


class General:
    points: Optional[int]
    name: Optional[str]
    coin_name: Optional[str]
    type: Optional[str]

    def __init__(self, points: Optional[int], name: Optional[str], coin_name: Optional[str], type: Optional[str]) -> None:
        self.points = points
        self.name = name
        self.coin_name = coin_name
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'General':
        assert isinstance(obj, dict)
        points = from_union([from_int, from_none], obj.get("Points"))
        name = from_union([from_str, from_none], obj.get("Name"))
        coin_name = from_union([from_str, from_none], obj.get("CoinName"))
        type = from_union([from_str, from_none], obj.get("Type"))
        return General(points, name, coin_name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Points"] = from_union([from_int, from_none], self.points)
        result["Name"] = from_union([from_str, from_none], self.name)
        result["CoinName"] = from_union([from_str, from_none], self.coin_name)
        result["Type"] = from_union([from_str, from_none], self.type)
        return result


class Reddit:
    points: Optional[int]
    posts_per_hour: Optional[float]
    comments_per_hour: Optional[float]
    comments_per_day: Optional[float]
    active_users: Optional[int]
    link: Optional[str]
    community_creation: Optional[int]
    posts_per_day: Optional[float]
    name: Optional[str]
    subscribers: Optional[int]

    def __init__(self, points: Optional[int], posts_per_hour: Optional[float], comments_per_hour: Optional[float], comments_per_day: Optional[float], active_users: Optional[int], link: Optional[str], community_creation: Optional[int], posts_per_day: Optional[float], name: Optional[str], subscribers: Optional[int]) -> None:
        self.points = points
        self.posts_per_hour = posts_per_hour
        self.comments_per_hour = comments_per_hour
        self.comments_per_day = comments_per_day
        self.active_users = active_users
        self.link = link
        self.community_creation = community_creation
        self.posts_per_day = posts_per_day
        self.name = name
        self.subscribers = subscribers

    @staticmethod
    def from_dict(obj: Any) -> 'Reddit':
        assert isinstance(obj, dict)
        points = from_union([from_int, from_none], obj.get("Points"))
        posts_per_hour = from_union([from_float, from_none], obj.get("posts_per_hour"))
        comments_per_hour = from_union([from_float, from_none], obj.get("comments_per_hour"))
        comments_per_day = from_union([from_float, from_none], obj.get("comments_per_day"))
        active_users = from_union([from_int, from_none], obj.get("active_users"))
        link = from_union([from_str, from_none], obj.get("link"))
        community_creation = from_union([from_none, lambda x: int(from_str(x))], obj.get("community_creation"))
        posts_per_day = from_union([from_float, from_none], obj.get("posts_per_day"))
        name = from_union([from_str, from_none], obj.get("name"))
        subscribers = from_union([from_int, from_none], obj.get("subscribers"))
        return Reddit(points, posts_per_hour, comments_per_hour, comments_per_day, active_users, link, community_creation, posts_per_day, name, subscribers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Points"] = from_union([from_int, from_none], self.points)
        result["posts_per_hour"] = from_union([to_float, from_none], self.posts_per_hour)
        result["comments_per_hour"] = from_union([to_float, from_none], self.comments_per_hour)
        result["comments_per_day"] = from_union([to_float, from_none], self.comments_per_day)
        result["active_users"] = from_union([from_int, from_none], self.active_users)
        result["link"] = from_union([from_str, from_none], self.link)
        result["community_creation"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.community_creation)
        result["posts_per_day"] = from_union([to_float, from_none], self.posts_per_day)
        result["name"] = from_union([from_str, from_none], self.name)
        result["subscribers"] = from_union([from_int, from_none], self.subscribers)
        return result


class Twitter:
    points: Optional[int]
    account_creation: Optional[int]
    followers: Optional[int]
    statuses: Optional[int]
    link: Optional[str]
    lists: Optional[int]
    favourites: Optional[int]
    following: Optional[int]
    name: Optional[str]

    def __init__(self, points: Optional[int], account_creation: Optional[int], followers: Optional[int], statuses: Optional[int], link: Optional[str], lists: Optional[int], favourites: Optional[int], following: Optional[int], name: Optional[str]) -> None:
        self.points = points
        self.account_creation = account_creation
        self.followers = followers
        self.statuses = statuses
        self.link = link
        self.lists = lists
        self.favourites = favourites
        self.following = following
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Twitter':
        assert isinstance(obj, dict)
        points = from_union([from_int, from_none], obj.get("Points"))
        account_creation = from_union([from_none, lambda x: int(from_str(x))], obj.get("account_creation"))
        followers = from_union([from_int, from_none], obj.get("followers"))
        statuses = from_union([from_int, from_none], obj.get("statuses"))
        link = from_union([from_str, from_none], obj.get("link"))
        lists = from_union([from_int, from_none], obj.get("lists"))
        favourites = from_union([from_int, from_none], obj.get("favourites"))
        following = from_union([from_int, from_none], obj.get("following"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Twitter(points, account_creation, followers, statuses, link, lists, favourites, following, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Points"] = from_union([from_int, from_none], self.points)
        result["account_creation"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.account_creation)
        result["followers"] = from_union([from_int, from_none], self.followers)
        result["statuses"] = from_union([from_int, from_none], self.statuses)
        result["link"] = from_union([from_str, from_none], self.link)
        result["lists"] = from_union([from_int, from_none], self.lists)
        result["favourites"] = from_union([from_int, from_none], self.favourites)
        result["following"] = from_union([from_int, from_none], self.following)
        result["name"] = from_union([from_str, from_none], self.name)
        return result


class SocialData:
    general: Optional[General]
    crypto_compare: Optional[CryptoCompare]
    twitter: Optional[Twitter]
    reddit: Optional[Reddit]
    facebook: Optional[Facebook]
    code_repository: Optional[CodeRepositories]

    def __init__(self, general: Optional[General], crypto_compare: Optional[CryptoCompare], twitter: Optional[Twitter], reddit: Optional[Reddit], facebook: Optional[Facebook], code_repository: Optional[CodeRepositories]) -> None:
        self.general = general
        self.crypto_compare = crypto_compare
        self.twitter = twitter
        self.reddit = reddit
        self.facebook = facebook
        self.code_repository = code_repository

    @staticmethod
    def from_dict(obj: Any) -> 'SocialData':
        assert isinstance(obj, dict)
        general = from_union([General.from_dict, from_none], obj.get("General"))
        crypto_compare = from_union([CryptoCompare.from_dict, from_none], obj.get("CryptoCompare"))
        twitter = from_union([Twitter.from_dict, from_none], obj.get("Twitter"))
        reddit = from_union([Reddit.from_dict, from_none], obj.get("Reddit"))
        facebook = from_union([Facebook.from_dict, from_none], obj.get("Facebook"))
        code_repository = from_union([CodeRepositories.from_dict, from_none], obj.get("CodeRepository"))
        return SocialData(general, crypto_compare, twitter, reddit, facebook, code_repository)

    def to_dict(self) -> dict:
        result: dict = {}
        result["General"] = from_union([lambda x: to_class(General, x), from_none], self.general)
        result["CryptoCompare"] = from_union([lambda x: to_class(CryptoCompare, x), from_none], self.crypto_compare)
        result["Twitter"] = from_union([lambda x: to_class(Twitter, x), from_none], self.twitter)
        result["Reddit"] = from_union([lambda x: to_class(Reddit, x), from_none], self.reddit)
        result["Facebook"] = from_union([lambda x: to_class(Facebook, x), from_none], self.facebook)
        result["CodeRepository"] = from_union([lambda x: to_class(CodeRepositories, x), from_none], self.code_repository)
        return result


class SocialLatest(ResponseAPIBase):
    response: Optional[str]
    message: Optional[str]
    has_warning: Optional[bool]
    type: Optional[int]
    rate_limit: Optional[RateLimit]
    data: Optional[SocialData]

    def __init__(self, response: Optional[str], message: Optional[str], has_warning: Optional[bool], type: Optional[int], rate_limit: Optional[RateLimit], data: Optional[SocialData]) -> None:
        self.response = response
        self.message = message
        self.has_warning = has_warning
        self.type = type
        self.rate_limit = rate_limit
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'SocialLatest':
        assert isinstance(obj, dict)
        response = from_union([from_str, from_none], obj.get("Response"))
        message = from_union([from_str, from_none], obj.get("Message"))
        has_warning = from_union([from_bool, from_none], obj.get("HasWarning"))
        type = from_union([from_int, from_none], obj.get("Type"))
        rate_limit = from_union([RateLimit.from_dict, from_none], obj.get("RateLimit"))
        data = from_union([SocialData.from_dict, from_none], obj.get("Data"))
        return SocialLatest(response, message, has_warning, type, rate_limit, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Response"] = from_union([from_str, from_none], self.response)
        result["Message"] = from_union([from_str, from_none], self.message)
        result["HasWarning"] = from_union([from_bool, from_none], self.has_warning)
        result["Type"] = from_union([from_int, from_none], self.type)
        result["RateLimit"] = from_union([lambda x: to_class(RateLimit, x), from_none], self.rate_limit)
        result["Data"] = from_union([lambda x: to_class(SocialData, x), from_none], self.data)
        return result


def social_latest_from_dict(s: Any) -> SocialLatest:
    return SocialLatest.from_dict(s)


def social_latest_to_dict(x: SocialLatest) -> Any:
    return to_class(SocialLatest, x)


class CouldNotGetSocialLatestException(ResponseException):
    pass
