#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

from luckydonaldUtils.logger import logging
from luckydonaldUtils.exceptions import assert_type_or_raise

from typing import Union, List, Dict, Type
from .models import *

# import either requests or httpx
# as internet
try:
    import requests as internet
except ImportError:
    try:
        import httpx as internet
    except ImportError:
        raise ImportError('Neither "requests" nor "httpx" could be found. Make sure either of them is installed.')
    # end try
# end try

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if


def comment(
    comment_id: int,
) -> Comment:
    """
    Fetches a **comment response** for the comment ID referenced by the `comment_id` URL parameter.

    A request will be sent to the following endpoint: `/api/v1/json/comments/:comment_id`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/comments/1000

    The API should return json looking like `{"comment":Comment}` which will then be parsed to the python result `Comment`.
    
    :param comment_id: the variable comment_id part of the url.
    :type  comment_id: int
    
    :return: The parsed result from the API.
    :rtype:  Comment
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/comments/{comment_id}'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['comment']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Comment = Comment.from_dict(result)
    return result
# end def comment


def image(
    image_id: int,
    filter_id: Union[int, None] = None,
    key: Union[str, None] = None,
) -> Image:
    """
    Fetches an **image response** for the image ID referenced by the `image_id` URL parameter.

    A request will be sent to the following endpoint: `/api/v1/json/images/:image_id`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/images/1

    The API should return json looking like `{"image":Image}` which will then be parsed to the python result `Image`.
    
    :param image_id: the variable image_id part of the url.
    :type  image_id: int
    
    :param filter_id: Assuming the user can access the filter ID given by the parameter, overrides the current filter for this request. This is primarily useful for unauthenticated API access.
    :type  filter_id: int|None
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str|None
    
    :return: The parsed result from the API.
    :rtype:  Image
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/images/{image_id}'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'filter_id': filter_id,
        'key': key,
    })
    result: Dict[str, Dict] = response.json()
    result: Dict = result['image']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Image = Image.from_dict(result)
    return result
# end def image


def featured_image(
) -> Image:
    """
    Fetches an **image response** for the for the current featured image.

    A request will be sent to the following endpoint: `/api/v1/json/images/featured`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/images/featured

    The API should return json looking like `{"image":Image}` which will then be parsed to the python result `Image`.
    
    :return: The parsed result from the API.
    :rtype:  Image
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/images/featured'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['image']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Image = Image.from_dict(result)
    return result
# end def featured_image


def tag(
    tag_id: str,
) -> Tag:
    """
    Fetches a **tag response** for the **tag slug** given by the `tag_id` URL parameter. The tag's ID is **not** used. For getting a tag by ID the search endpoint can be used like `search/tags?q=id:4458`.

    A request will be sent to the following endpoint: `/api/v1/json/tags/:tag_id`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/tags/artist-colon-atryl

    The API should return json looking like `{"tag":Tag}` which will then be parsed to the python result `Tag`.
    
    :param tag_id: the variable tag_id part of the url.
    :type  tag_id: str
    
    :return: The parsed result from the API.
    :rtype:  Tag
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/tags/{tag_id}'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['tag']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Tag = Tag.from_dict(result)
    return result
# end def tag


def post(
    post_id: int,
) -> Post:
    """
    Fetches a **post response** for the post ID given by the `post_id` URL parameter.

    A request will be sent to the following endpoint: `/api/v1/json/posts/:post_id`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/posts/2730144

    The API should return json looking like `{"post":Post}` which will then be parsed to the python result `Post`.
    
    :param post_id: the variable post_id part of the url.
    :type  post_id: int
    
    :return: The parsed result from the API.
    :rtype:  Post
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/posts/{post_id}'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['post']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Post = Post.from_dict(result)
    return result
# end def post


def user(
    user_id: int,
) -> User:
    """
    Fetches a **profile response** for the user ID given by the `user_id` URL parameter.

    A request will be sent to the following endpoint: `/api/v1/json/profiles/:user_id`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/profiles/216494

    The API should return json looking like `{"user":User}` which will then be parsed to the python result `User`.
    
    :param user_id: the variable user_id part of the url.
    :type  user_id: int
    
    :return: The parsed result from the API.
    :rtype:  User
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/profiles/{user_id}'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['user']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: User = User.from_dict(result)
    return result
# end def user


def filter(
    filter_id: int,
    key: Union[str, None] = None,
) -> Filter:
    """
    Fetches a **filter response** for the filter ID given by the `filter_id` URL parameter.

    A request will be sent to the following endpoint: `/api/v1/json/filters/:filter_id`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/filters/56027

    The API should return json looking like `{"filter":Filter}` which will then be parsed to the python result `Filter`.
    
    :param filter_id: the variable filter_id part of the url.
    :type  filter_id: int
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str|None
    
    :return: The parsed result from the API.
    :rtype:  Filter
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/filters/{filter_id}'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'key': key,
    })
    result: Dict[str, Dict] = response.json()
    result: Dict = result['filter']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Filter = Filter.from_dict(result)
    return result
# end def filter


def system_filters(
    page: Union[int, None] = None,
) -> List[Filter]:
    """
    Fetches a list of **filter responses** that are flagged as being **system** filters (and thus usable by anyone).

    A request will be sent to the following endpoint: `/api/v1/json/filters/system`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/filters/system

    The API should return json looking like `{"filters":[Filter]}` which will then be parsed to the python result `List[Filter]`.
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :return: The parsed result from the API.
    :rtype:  List[Filter]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/filters/system'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'page': page,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['filters']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Filter] = [
        Filter.from_dict(item)
        for item in result
    ]
    return result
# end def system_filters


def user_filters(
    key: str,
    page: Union[int, None] = None,
) -> List[Filter]:
    """
    Fetches a list of **filter responses** that belong to the user given by **key**. If no **key** is given or it is invalid, will return a **403 Forbidden** error.

    A request will be sent to the following endpoint: `/api/v1/json/filters/user`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/filters/user

    The API should return json looking like `{"filters":[Filter]}` which will then be parsed to the python result `List[Filter]`.
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :return: The parsed result from the API.
    :rtype:  List[Filter]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/filters/user'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'key': key,
        'page': page,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['filters']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Filter] = [
        Filter.from_dict(item)
        for item in result
    ]
    return result
# end def user_filters


def oembed(
    url: str,
) -> Oembed:
    """
    Fetches an **oEmbed response** for the given app link or CDN URL.

    A request will be sent to the following endpoint: `/api/v1/json/oembed`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/oembed?url=https://derpicdn.net/img/2012/1/2/3/full.png

    The API should return json looking like `Oembed` which will then be parsed to the python result `Oembed`.
    
    :param url: Link a deviantART page, a Tumblr post, or the image directly.
    :type  url: str
    
    :return: The parsed result from the API.
    :rtype:  Oembed
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/oembed'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'url': url,
    })
    result: Dict = response.json()
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Oembed = Oembed.from_dict(result)
    return result
# end def oembed


def search_comments(
    query: str,
    page: Union[int, None] = None,
    key: Union[str, None] = None,
) -> List[Comment]:
    """
    Executes the search given by the `q` query parameter (case insensitive and stemming is applied. If you search for **best pony** results like **Best Ponies** are also be returned), and returns **comment responses** sorted by descending creation time.

    A request will be sent to the following endpoint: `/api/v1/json/search/comments`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/search/comments?q=image_id:1000000

    The API should return json looking like `{"comments":[Comment]}` which will then be parsed to the python result `List[Comment]`.
    
    :param query: The current search query, if the request is a search request.
                  Note, on derpibooru's side this parameter is called `q`.
    :type  query: str
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str|None
    
    :return: The parsed result from the API.
    :rtype:  List[Comment]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/search/comments'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'q': query,
        'page': page,
        'key': key,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['comments']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Comment] = [
        Comment.from_dict(item)
        for item in result
    ]
    return result
# end def search_comments


def search_galleries(
    query: str,
    page: Union[int, None] = None,
    key: Union[str, None] = None,
) -> List[Gallery]:
    """
    Executes the search given by the `q` query parameter, and returns **gallery responses** sorted by descending creation time.

    A request will be sent to the following endpoint: `/api/v1/json/search/galleries`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/search/galleries?q=title:mean*

    The API should return json looking like `{"galleries":[Gallery]}` which will then be parsed to the python result `List[Gallery]`.
    
    :param query: The current search query, if the request is a search request.
                  Note, on derpibooru's side this parameter is called `q`.
    :type  query: str
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str|None
    
    :return: The parsed result from the API.
    :rtype:  List[Gallery]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/search/galleries'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'q': query,
        'page': page,
        'key': key,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['galleries']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Gallery] = [
        Gallery.from_dict(item)
        for item in result
    ]
    return result
# end def search_galleries


def search_posts(
    query: str,
    page: Union[int, None] = None,
    key: Union[str, None] = None,
) -> List[Post]:
    """
    Executes the search given by the `q` query parameter, and returns **post responses** sorted by descending creation time.

    A request will be sent to the following endpoint: `/api/v1/json/search/posts`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/search/posts?q=subject:time wasting thread

    The API should return json looking like `{"posts":[Post]}` which will then be parsed to the python result `List[Post]`.
    
    :param query: The current search query, if the request is a search request.
                  Note, on derpibooru's side this parameter is called `q`.
    :type  query: str
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str|None
    
    :return: The parsed result from the API.
    :rtype:  List[Post]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/search/posts'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'q': query,
        'page': page,
        'key': key,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['posts']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Post] = [
        Post.from_dict(item)
        for item in result
    ]
    return result
# end def search_posts


def search_images(
    query: str,
    filter_id: Union[int, None] = None,
    page: Union[int, None] = None,
    per_page: Union[int, None] = None,
    sort_direction: Union[str, None] = None,
    sort_field: Union[str, None] = None,
    key: Union[str, None] = None,
) -> List[Image]:
    """
    Executes the search given by the `q` query parameter, and returns **image responses**.

    A request will be sent to the following endpoint: `/api/v1/json/search/images`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/search/images?q=safe

    The API should return json looking like `{"images":[Image]}` which will then be parsed to the python result `List[Image]`.
    
    :param query: The current search query, if the request is a search request.
                  Note, on derpibooru's side this parameter is called `q`.
    :type  query: str
    
    :param filter_id: Assuming the user can access the filter ID given by the parameter, overrides the current filter for this request. This is primarily useful for unauthenticated API access.
    :type  filter_id: int|None
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :param per_page: Controls the number of results per page, up to a limit of 50, if the response is paginated. The default is 25.
    :type  per_page: int|None
    
    :param sort_direction: The current sort direction, if the request is a search request.
                           Note, on derpibooru's side this parameter is called `sd`.
    :type  sort_direction: str|None
    
    :param sort_field: The current sort field, if the request is a search request.
                       Note, on derpibooru's side this parameter is called `sf`.
    :type  sort_field: str|None
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str|None
    
    :return: The parsed result from the API.
    :rtype:  List[Image]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/search/images'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'q': query,
        'filter_id': filter_id,
        'page': page,
        'per_page': per_page,
        'sd': sort_direction,
        'sf': sort_field,
        'key': key,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['images']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Image] = [
        Image.from_dict(item)
        for item in result
    ]
    return result
# end def search_images


def search_tags(
    query: str,
    page: Union[int, None] = None,
) -> List[Tag]:
    """
    Executes the search given by the `q` query parameter, and returns **tag responses** sorted by descending image count.

    A request will be sent to the following endpoint: `/api/v1/json/search/tags`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/search/tags?q=analyzed_name:wing

    The API should return json looking like `{"tags":[Tag]}` which will then be parsed to the python result `List[Tag]`.
    
    :param query: The current search query, if the request is a search request.
                  Note, on derpibooru's side this parameter is called `q`.
    :type  query: str
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :return: The parsed result from the API.
    :rtype:  List[Tag]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/search/tags'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'q': query,
        'page': page,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['tags']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Tag] = [
        Tag.from_dict(item)
        for item in result
    ]
    return result
# end def search_tags


def search_reverse(
    url: str,
    distance: Union[float, None] = None,
    key: Union[str, None] = None,
) -> List[Image]:
    """
    Returns **image responses** based on the results of reverse-searching the image given by the `url` query parameter.

    A request will be sent to the following endpoint: `/api/v1/json/search/reverse`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/search/reverse?url=https://derpicdn.net/img/2019/12/24/2228439/full.jpg

    The API should return json looking like `{"images":[Image]}` which will then be parsed to the python result `List[Image]`.
    
    :param url: Link a deviantART page, a Tumblr post, or the image directly.
    :type  url: str
    
    :param distance: Match distance (suggested values: between 0.2 and 0.5).
    :type  distance: float|None
    
    :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
    :type  key: str|None
    
    :return: The parsed result from the API.
    :rtype:  List[Image]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/search/reverse'
    response: internet.Response = DerpiClient.request('POST', _url, params={
        'url': url,
        'distance': distance,
        'key': key,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['images']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Image] = [
        Image.from_dict(item)
        for item in result
    ]
    return result
# end def search_reverse


def forums(
) -> List[Forum]:
    """
    Fetches a list of **forum responses**.

    A request will be sent to the following endpoint: `/api/v1/json/forums`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/forums

    The API should return json looking like `{"forums":[Forum]}` which will then be parsed to the python result `List[Forum]`.
    
    :return: The parsed result from the API.
    :rtype:  List[Forum]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/forums'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['forums']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Forum] = [
        Forum.from_dict(item)
        for item in result
    ]
    return result
# end def forums


def forum(
    short_name: str,
) -> Forum:
    """
    Fetches a **forum response** for the abbreviated name given by the `short_name` URL parameter.

    A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis

    The API should return json looking like `{"forum":Forum}` which will then be parsed to the python result `Forum`.
    
    :param short_name: the variable short_name part of the url.
    :type  short_name: str
    
    :return: The parsed result from the API.
    :rtype:  Forum
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/forums/{short_name}'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['forum']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Forum = Forum.from_dict(result)
    return result
# end def forum


def forum_topics(
    short_name: str,
    page: Union[int, None] = None,
) -> List[Topic]:
    """
    Fetches a list of **topic responses** for the abbreviated forum name given by the `short_name` URL parameter.

    A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics

    The API should return json looking like `{"topics":[Topic]}` which will then be parsed to the python result `List[Topic]`.
    
    :param short_name: the variable short_name part of the url.
    :type  short_name: str
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :return: The parsed result from the API.
    :rtype:  List[Topic]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/forums/{short_name}/topics'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'page': page,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['topics']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Topic] = [
        Topic.from_dict(item)
        for item in result
    ]
    return result
# end def forum_topics


def forum_topic(
    short_name: str,
    topic_slug: str,
) -> Topic:
    """
    Fetches a **topic response** for the abbreviated forum name given by the `short_name` and topic given by `topic_slug` URL parameters.

    A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics/:topic_slug`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics/ask-the-mods-anything

    The API should return json looking like `{"topic":Topic}` which will then be parsed to the python result `Topic`.
    
    :param short_name: the variable short_name part of the url.
    :type  short_name: str
    
    :param topic_slug: the variable topic_slug part of the url.
    :type  topic_slug: str
    
    :return: The parsed result from the API.
    :rtype:  Topic
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/forums/{short_name}/topics/{topic_slug}'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['topic']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Topic = Topic.from_dict(result)
    return result
# end def forum_topic


def forum_posts(
    short_name: str,
    topic_slug: str,
    page: Union[int, None] = None,
) -> List[Post]:
    """
    Fetches a list of **post responses** for the abbreviated forum name given by the `short_name` and topic given by `topic_slug` URL parameters.

    A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics/:topic_slug/posts`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics/ask-the-mods-anything/posts

    The API should return json looking like `{"posts":[Post]}` which will then be parsed to the python result `List[Post]`.
    
    :param short_name: the variable short_name part of the url.
    :type  short_name: str
    
    :param topic_slug: the variable topic_slug part of the url.
    :type  topic_slug: str
    
    :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
    :type  page: int|None
    
    :return: The parsed result from the API.
    :rtype:  List[Post]
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/forums/{short_name}/topics/{topic_slug}/posts'
    response: internet.Response = DerpiClient.request('GET', _url, params={
        'page': page,
    })
    result: Dict[str, List[Dict]] = response.json()
    result: List[Dict] = result['posts']
    assert_type_or_raise(result, list, parameter_name='result')
    result: List[Post] = [
        Post.from_dict(item)
        for item in result
    ]
    return result
# end def forum_posts


def forum_post(
    short_name: str,
    topic_slug: str,
    post_id: int,
) -> Post:
    """
    Fetches a **post response** for the abbreviated forum name given by the `short_name`, topic given by `topic_slug` and post given by `post_id` URL parameters.

    A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics/:topic_slug/posts/:post_id`
    It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
    which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics/ask-the-mods-anything/posts/2761095

    The API should return json looking like `{"post":Post}` which will then be parsed to the python result `Post`.
    
    :param short_name: the variable short_name part of the url.
    :type  short_name: str
    
    :param topic_slug: the variable topic_slug part of the url.
    :type  topic_slug: str
    
    :param post_id: the variable post_id part of the url.
    :type  post_id: int
    
    :return: The parsed result from the API.
    :rtype:  Post
    """
    _url: str = DerpiClient._base_url + f'/api/v1/json/forums/{short_name}/topics/{topic_slug}/posts/{post_id}'
    response: internet.Response = DerpiClient.request('GET', _url)
    result: Dict[str, Dict] = response.json()
    result: Dict = result['post']
    assert_type_or_raise(result, dict, parameter_name='result')
    result: Post = Post.from_dict(result)
    return result
# end def forum_post


class DerpiClient(object):
    """
    Synchronous client for Derpibooru.org
    """
    _base_url = 'https://derpibooru.org'

    def __init__(self, key):
        """
        :param key: API key
        """
        self.__key = key
    # end def

    @classmethod
    def request(cls: Type['DerpiClient'], method, url, params=None) -> internet.Response:
        response: internet.Response = internet.request(method=method, url=url, params=params)
        cls._check_response(response)
        return response
    # end def

    @staticmethod
    def _check_response(response: internet.Response) -> None:
        """
        Makes sure a server response looks valid,
        or raise the appropriate errors if not.

        :param response: A requests/httpx response.
        :type  response: requests.Response|httpx.Response
        """
        assert response.status_code == 200  # TODO
        assert response.headers['content-type'] == 'application/json; charset=utf-8'
    # end def

    
    # noinspection PyMethodMayBeStatic
    def comment(
        self, 
        comment_id: int,
    ) -> Comment:
        """
        Fetches a **comment response** for the comment ID referenced by the `comment_id` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/comments/:comment_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/comments/1000

        The API should return json looking like `{"comment":Comment}` which will then be parsed to the python result `Comment`.
        
        :param comment_id: the variable comment_id part of the url.
        :type  comment_id: int
        
        :return: The parsed result from the API.
        :rtype:  Comment
        """
        return comment(
            comment_id=comment_id,
        )
    # end def comment
    
    # noinspection PyMethodMayBeStatic
    def image(
        self, 
        image_id: int,
        filter_id: Union[int, None] = None,
        key: Union[str, None] = None,
    ) -> Image:
        """
        Fetches an **image response** for the image ID referenced by the `image_id` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/images/:image_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/images/1

        The API should return json looking like `{"image":Image}` which will then be parsed to the python result `Image`.
        
        :param image_id: the variable image_id part of the url.
        :type  image_id: int
        
        :param filter_id: Assuming the user can access the filter ID given by the parameter, overrides the current filter for this request. This is primarily useful for unauthenticated API access.
        :type  filter_id: int|None
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  Image
        """
        return image(
            image_id=image_id,
            filter_id=filter_id,
            key=self.__key,
        )
    # end def image
    
    # noinspection PyMethodMayBeStatic
    def featured_image(
        self, 
    ) -> Image:
        """
        Fetches an **image response** for the for the current featured image.

        A request will be sent to the following endpoint: `/api/v1/json/images/featured`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/images/featured

        The API should return json looking like `{"image":Image}` which will then be parsed to the python result `Image`.
        
        :return: The parsed result from the API.
        :rtype:  Image
        """
        return featured_image(
        )
    # end def featured_image
    
    # noinspection PyMethodMayBeStatic
    def tag(
        self, 
        tag_id: str,
    ) -> Tag:
        """
        Fetches a **tag response** for the **tag slug** given by the `tag_id` URL parameter. The tag's ID is **not** used. For getting a tag by ID the search endpoint can be used like `search/tags?q=id:4458`.

        A request will be sent to the following endpoint: `/api/v1/json/tags/:tag_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/tags/artist-colon-atryl

        The API should return json looking like `{"tag":Tag}` which will then be parsed to the python result `Tag`.
        
        :param tag_id: the variable tag_id part of the url.
        :type  tag_id: str
        
        :return: The parsed result from the API.
        :rtype:  Tag
        """
        return tag(
            tag_id=tag_id,
        )
    # end def tag
    
    # noinspection PyMethodMayBeStatic
    def post(
        self, 
        post_id: int,
    ) -> Post:
        """
        Fetches a **post response** for the post ID given by the `post_id` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/posts/:post_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/posts/2730144

        The API should return json looking like `{"post":Post}` which will then be parsed to the python result `Post`.
        
        :param post_id: the variable post_id part of the url.
        :type  post_id: int
        
        :return: The parsed result from the API.
        :rtype:  Post
        """
        return post(
            post_id=post_id,
        )
    # end def post
    
    # noinspection PyMethodMayBeStatic
    def user(
        self, 
        user_id: int,
    ) -> User:
        """
        Fetches a **profile response** for the user ID given by the `user_id` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/profiles/:user_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/profiles/216494

        The API should return json looking like `{"user":User}` which will then be parsed to the python result `User`.
        
        :param user_id: the variable user_id part of the url.
        :type  user_id: int
        
        :return: The parsed result from the API.
        :rtype:  User
        """
        return user(
            user_id=user_id,
        )
    # end def user
    
    # noinspection PyMethodMayBeStatic
    def filter(
        self, 
        filter_id: int,
        key: Union[str, None] = None,
    ) -> Filter:
        """
        Fetches a **filter response** for the filter ID given by the `filter_id` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/filters/:filter_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/filters/56027

        The API should return json looking like `{"filter":Filter}` which will then be parsed to the python result `Filter`.
        
        :param filter_id: the variable filter_id part of the url.
        :type  filter_id: int
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  Filter
        """
        return filter(
            filter_id=filter_id,
            key=self.__key,
        )
    # end def filter
    
    # noinspection PyMethodMayBeStatic
    def system_filters(
        self, 
        page: Union[int, None] = None,
    ) -> List[Filter]:
        """
        Fetches a list of **filter responses** that are flagged as being **system** filters (and thus usable by anyone).

        A request will be sent to the following endpoint: `/api/v1/json/filters/system`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/filters/system

        The API should return json looking like `{"filters":[Filter]}` which will then be parsed to the python result `List[Filter]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :return: The parsed result from the API.
        :rtype:  List[Filter]
        """
        return system_filters(
            page=page,
        )
    # end def system_filters
    
    # noinspection PyMethodMayBeStatic
    def user_filters(
        self, 
        key: str,
        page: Union[int, None] = None,
    ) -> List[Filter]:
        """
        Fetches a list of **filter responses** that belong to the user given by **key**. If no **key** is given or it is invalid, will return a **403 Forbidden** error.

        A request will be sent to the following endpoint: `/api/v1/json/filters/user`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/filters/user

        The API should return json looking like `{"filters":[Filter]}` which will then be parsed to the python result `List[Filter]`.
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :return: The parsed result from the API.
        :rtype:  List[Filter]
        """
        return user_filters(
            key=self.__key,
            page=page,
        )
    # end def user_filters
    
    # noinspection PyMethodMayBeStatic
    def oembed(
        self, 
        url: str,
    ) -> Oembed:
        """
        Fetches an **oEmbed response** for the given app link or CDN URL.

        A request will be sent to the following endpoint: `/api/v1/json/oembed`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/oembed?url=https://derpicdn.net/img/2012/1/2/3/full.png

        The API should return json looking like `Oembed` which will then be parsed to the python result `Oembed`.
        
        :param url: Link a deviantART page, a Tumblr post, or the image directly.
        :type  url: str
        
        :return: The parsed result from the API.
        :rtype:  Oembed
        """
        return oembed(
            url=url,
        )
    # end def oembed
    
    # noinspection PyMethodMayBeStatic
    def search_comments(
        self, 
        query: str,
        page: Union[int, None] = None,
        key: Union[str, None] = None,
    ) -> List[Comment]:
        """
        Executes the search given by the `q` query parameter (case insensitive and stemming is applied. If you search for **best pony** results like **Best Ponies** are also be returned), and returns **comment responses** sorted by descending creation time.

        A request will be sent to the following endpoint: `/api/v1/json/search/comments`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/comments?q=image_id:1000000

        The API should return json looking like `{"comments":[Comment]}` which will then be parsed to the python result `List[Comment]`.
        
        :param query: The current search query, if the request is a search request.
        :type  query: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Comment]
        """
        return search_comments(
            query=query,
            page=page,
            key=self.__key,
        )
    # end def search_comments
    
    # noinspection PyMethodMayBeStatic
    def search_galleries(
        self, 
        query: str,
        page: Union[int, None] = None,
        key: Union[str, None] = None,
    ) -> List[Gallery]:
        """
        Executes the search given by the `q` query parameter, and returns **gallery responses** sorted by descending creation time.

        A request will be sent to the following endpoint: `/api/v1/json/search/galleries`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/galleries?q=title:mean*

        The API should return json looking like `{"galleries":[Gallery]}` which will then be parsed to the python result `List[Gallery]`.
        
        :param query: The current search query, if the request is a search request.
        :type  query: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Gallery]
        """
        return search_galleries(
            query=query,
            page=page,
            key=self.__key,
        )
    # end def search_galleries
    
    # noinspection PyMethodMayBeStatic
    def search_posts(
        self, 
        query: str,
        page: Union[int, None] = None,
        key: Union[str, None] = None,
    ) -> List[Post]:
        """
        Executes the search given by the `q` query parameter, and returns **post responses** sorted by descending creation time.

        A request will be sent to the following endpoint: `/api/v1/json/search/posts`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/posts?q=subject:time wasting thread

        The API should return json looking like `{"posts":[Post]}` which will then be parsed to the python result `List[Post]`.
        
        :param query: The current search query, if the request is a search request.
        :type  query: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Post]
        """
        return search_posts(
            query=query,
            page=page,
            key=self.__key,
        )
    # end def search_posts
    
    # noinspection PyMethodMayBeStatic
    def search_images(
        self, 
        query: str,
        filter_id: Union[int, None] = None,
        page: Union[int, None] = None,
        per_page: Union[int, None] = None,
        sort_direction: Union[str, None] = None,
        sort_field: Union[str, None] = None,
        key: Union[str, None] = None,
    ) -> List[Image]:
        """
        Executes the search given by the `q` query parameter, and returns **image responses**.

        A request will be sent to the following endpoint: `/api/v1/json/search/images`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/images?q=safe

        The API should return json looking like `{"images":[Image]}` which will then be parsed to the python result `List[Image]`.
        
        :param query: The current search query, if the request is a search request.
        :type  query: str
        
        :param filter_id: Assuming the user can access the filter ID given by the parameter, overrides the current filter for this request. This is primarily useful for unauthenticated API access.
        :type  filter_id: int|None
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :param per_page: Controls the number of results per page, up to a limit of 50, if the response is paginated. The default is 25.
        :type  per_page: int|None
        
        :param sort_direction: The current sort direction, if the request is a search request.
        :type  sort_direction: str|None
        
        :param sort_field: The current sort field, if the request is a search request.
        :type  sort_field: str|None
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Image]
        """
        return search_images(
            query=query,
            filter_id=filter_id,
            page=page,
            per_page=per_page,
            sort_direction=sort_direction,
            sort_field=sort_field,
            key=self.__key,
        )
    # end def search_images
    
    # noinspection PyMethodMayBeStatic
    def search_tags(
        self, 
        query: str,
        page: Union[int, None] = None,
    ) -> List[Tag]:
        """
        Executes the search given by the `q` query parameter, and returns **tag responses** sorted by descending image count.

        A request will be sent to the following endpoint: `/api/v1/json/search/tags`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/tags?q=analyzed_name:wing

        The API should return json looking like `{"tags":[Tag]}` which will then be parsed to the python result `List[Tag]`.
        
        :param query: The current search query, if the request is a search request.
        :type  query: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :return: The parsed result from the API.
        :rtype:  List[Tag]
        """
        return search_tags(
            query=query,
            page=page,
        )
    # end def search_tags
    
    # noinspection PyMethodMayBeStatic
    def search_reverse(
        self, 
        url: str,
        distance: Union[float, None] = None,
        key: Union[str, None] = None,
    ) -> List[Image]:
        """
        Returns **image responses** based on the results of reverse-searching the image given by the `url` query parameter.

        A request will be sent to the following endpoint: `/api/v1/json/search/reverse`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/reverse?url=https://derpicdn.net/img/2019/12/24/2228439/full.jpg

        The API should return json looking like `{"images":[Image]}` which will then be parsed to the python result `List[Image]`.
        
        :param url: Link a deviantART page, a Tumblr post, or the image directly.
        :type  url: str
        
        :param distance: Match distance (suggested values: between 0.2 and 0.5).
        :type  distance: float|None
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Image]
        """
        return search_reverse(
            url=url,
            distance=distance,
            key=self.__key,
        )
    # end def search_reverse
    
    # noinspection PyMethodMayBeStatic
    def forums(
        self, 
    ) -> List[Forum]:
        """
        Fetches a list of **forum responses**.

        A request will be sent to the following endpoint: `/api/v1/json/forums`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums

        The API should return json looking like `{"forums":[Forum]}` which will then be parsed to the python result `List[Forum]`.
        
        :return: The parsed result from the API.
        :rtype:  List[Forum]
        """
        return forums(
        )
    # end def forums
    
    # noinspection PyMethodMayBeStatic
    def forum(
        self, 
        short_name: str,
    ) -> Forum:
        """
        Fetches a **forum response** for the abbreviated name given by the `short_name` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis

        The API should return json looking like `{"forum":Forum}` which will then be parsed to the python result `Forum`.
        
        :param short_name: the variable short_name part of the url.
        :type  short_name: str
        
        :return: The parsed result from the API.
        :rtype:  Forum
        """
        return forum(
            short_name=short_name,
        )
    # end def forum
    
    # noinspection PyMethodMayBeStatic
    def forum_topics(
        self, 
        short_name: str,
        page: Union[int, None] = None,
    ) -> List[Topic]:
        """
        Fetches a list of **topic responses** for the abbreviated forum name given by the `short_name` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics

        The API should return json looking like `{"topics":[Topic]}` which will then be parsed to the python result `List[Topic]`.
        
        :param short_name: the variable short_name part of the url.
        :type  short_name: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :return: The parsed result from the API.
        :rtype:  List[Topic]
        """
        return forum_topics(
            short_name=short_name,
            page=page,
        )
    # end def forum_topics
    
    # noinspection PyMethodMayBeStatic
    def forum_topic(
        self, 
        short_name: str,
        topic_slug: str,
    ) -> Topic:
        """
        Fetches a **topic response** for the abbreviated forum name given by the `short_name` and topic given by `topic_slug` URL parameters.

        A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics/:topic_slug`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics/ask-the-mods-anything

        The API should return json looking like `{"topic":Topic}` which will then be parsed to the python result `Topic`.
        
        :param short_name: the variable short_name part of the url.
        :type  short_name: str
        
        :param topic_slug: the variable topic_slug part of the url.
        :type  topic_slug: str
        
        :return: The parsed result from the API.
        :rtype:  Topic
        """
        return forum_topic(
            short_name=short_name,
            topic_slug=topic_slug,
        )
    # end def forum_topic
    
    # noinspection PyMethodMayBeStatic
    def forum_posts(
        self, 
        short_name: str,
        topic_slug: str,
        page: Union[int, None] = None,
    ) -> List[Post]:
        """
        Fetches a list of **post responses** for the abbreviated forum name given by the `short_name` and topic given by `topic_slug` URL parameters.

        A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics/:topic_slug/posts`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics/ask-the-mods-anything/posts

        The API should return json looking like `{"posts":[Post]}` which will then be parsed to the python result `List[Post]`.
        
        :param short_name: the variable short_name part of the url.
        :type  short_name: str
        
        :param topic_slug: the variable topic_slug part of the url.
        :type  topic_slug: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page. The first page is `1`.
        :type  page: int|None
        
        :return: The parsed result from the API.
        :rtype:  List[Post]
        """
        return forum_posts(
            short_name=short_name,
            topic_slug=topic_slug,
            page=page,
        )
    # end def forum_posts
    
    # noinspection PyMethodMayBeStatic
    def forum_post(
        self, 
        short_name: str,
        topic_slug: str,
        post_id: int,
    ) -> Post:
        """
        Fetches a **post response** for the abbreviated forum name given by the `short_name`, topic given by `topic_slug` and post given by `post_id` URL parameters.

        A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics/:topic_slug/posts/:post_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics/ask-the-mods-anything/posts/2761095

        The API should return json looking like `{"post":Post}` which will then be parsed to the python result `Post`.
        
        :param short_name: the variable short_name part of the url.
        :type  short_name: str
        
        :param topic_slug: the variable topic_slug part of the url.
        :type  topic_slug: str
        
        :param post_id: the variable post_id part of the url.
        :type  post_id: int
        
        :return: The parsed result from the API.
        :rtype:  Post
        """
        return forum_post(
            short_name=short_name,
            topic_slug=topic_slug,
            post_id=post_id,
        )
    # end def forum_post
    
# end class