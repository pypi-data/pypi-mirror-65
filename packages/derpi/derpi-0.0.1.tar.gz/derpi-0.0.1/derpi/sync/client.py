#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

from luckydonaldUtils.logger import logging
from luckydonaldUtils.exceptions import assert_type_or_raise

from typing import Union, List, Dict
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



class DerpiClient(object):
    """
    Synchronous client for Derpibooru.org
    """
    _base_url = 'https://derpibooru.org'

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
        url: str = self._base_url + f'/api/v1/json/comments/{comment_id}'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['comment']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Comment = Comment.from_dict(result)
        return result
    # end def comment
    
    def image(
        self, 
        image_id: int,
        key: Union[str, None] = None,
        filter_id: Union[int, None] = None,
    ) -> Image:
        """
        Fetches an **image response** for the image ID referenced by the `image_id` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/images/:image_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/images/1

        The API should return json looking like `{"image":Image}` which will then be parsed to the python result `Image`.
        
        :param image_id: the variable image_id part of the url.
        :type  image_id: int
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :param filter_id: Assuming the user can access the filter ID given by the parameter, overrides the current filter for this request. This is primarily useful for unauthenticated API access.
        :type  filter_id: int|None
        
        :return: The parsed result from the API.
        :rtype:  Image
        """
        url: str = self._base_url + f'/api/v1/json/images/{image_id}'
        resp: internet.Response = internet.request('GET', url, params={
            'key': key,
            'filter_id': filter_id,
        })
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['image']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Image = Image.from_dict(result)
        return result
    # end def image
    
    def featured_images(
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
        url: str = self._base_url + f'/api/v1/json/images/featured'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['image']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Image = Image.from_dict(result)
        return result
    # end def featured_images
    
    def tag(
        self, 
        tag_id: int,
    ) -> Tag:
        """
        Fetches a **tag response** for the **tag slug** given by the `tag_id` URL parameter. The tag's ID is **not** used.

        A request will be sent to the following endpoint: `/api/v1/json/tags/:tag_id`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/tags/artist-colon-atryl

        The API should return json looking like `{"tag":Tag}` which will then be parsed to the python result `Tag`.
        
        :param tag_id: the variable tag_id part of the url.
        :type  tag_id: int
        
        :return: The parsed result from the API.
        :rtype:  Tag
        """
        url: str = self._base_url + f'/api/v1/json/tags/{tag_id}'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['tag']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Tag = Tag.from_dict(result)
        return result
    # end def tag
    
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
        url: str = self._base_url + f'/api/v1/json/posts/{post_id}'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['post']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Post = Post.from_dict(result)
        return result
    # end def post
    
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
        url: str = self._base_url + f'/api/v1/json/profiles/{user_id}'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['user']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: User = User.from_dict(result)
        return result
    # end def user
    
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
        url: str = self._base_url + f'/api/v1/json/filters/{filter_id}'
        resp: internet.Response = internet.request('GET', url, params={
            'key': key,
        })
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['filter']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Filter = Filter.from_dict(result)
        return result
    # end def filter
    
    def system_filters(
        self, 
        page: int,
    ) -> List[Filter]:
        """
        Fetches a list of **filter responses** that are flagged as being **system** filters (and thus usable by anyone).

        A request will be sent to the following endpoint: `/api/v1/json/filters/system`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/filters/system

        The API should return json looking like `{"filters":[Filter]}` which will then be parsed to the python result `List[Filter]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :return: The parsed result from the API.
        :rtype:  List[Filter]
        """
        url: str = self._base_url + f'/api/v1/json/filters/system'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['filters']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Filter] = [
            Filter.from_dict(item)
            for item in result
        ]
        return result
    # end def system_filters
    
    def user_filters(
        self, 
        page: int,
        key: Union[str, None] = None,
    ) -> List[Filter]:
        """
        Fetches a list of **filter responses** that belong to the user given by **key**. If no **key** is given or it is invalid, will return a **403 Forbidden** error.

        A request will be sent to the following endpoint: `/api/v1/json/filters/user`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/filters/user

        The API should return json looking like `{"filters":[Filter]}` which will then be parsed to the python result `List[Filter]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Filter]
        """
        url: str = self._base_url + f'/api/v1/json/filters/user'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
            'key': key,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['filters']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Filter] = [
            Filter.from_dict(item)
            for item in result
        ]
        return result
    # end def user_filters
    
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
        url: str = self._base_url + f'/api/v1/json/oembed'
        resp: internet.Response = internet.request('GET', url, params={
            'url': url,
        })
        self._check_response(resp)
        result: Dict = resp.json()
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Oembed = Oembed.from_dict(result)
        return result
    # end def oembed
    
    def search_comments(
        self, 
        page: int,
        key: Union[str, None] = None,
    ) -> List[Comment]:
        """
        Executes the search given by the `q` query parameter, and returns **comment responses** sorted by descending creation time.

        A request will be sent to the following endpoint: `/api/v1/json/search/comments`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/comments?q=image_id:1000000

        The API should return json looking like `{"comments":[Comment]}` which will then be parsed to the python result `List[Comment]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Comment]
        """
        url: str = self._base_url + f'/api/v1/json/search/comments'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
            'key': key,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['comments']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Comment] = [
            Comment.from_dict(item)
            for item in result
        ]
        return result
    # end def search_comments
    
    def search_galleries(
        self, 
        page: int,
        key: Union[str, None] = None,
    ) -> List[Gallery]:
        """
        Executes the search given by the `q` query parameter, and returns **gallery responses** sorted by descending creation time.

        A request will be sent to the following endpoint: `/api/v1/json/search/galleries`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/galleries?q=title:mean*

        The API should return json looking like `{"galleries":[Gallery]}` which will then be parsed to the python result `List[Gallery]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Gallery]
        """
        url: str = self._base_url + f'/api/v1/json/search/galleries'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
            'key': key,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['galleries']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Gallery] = [
            Gallery.from_dict(item)
            for item in result
        ]
        return result
    # end def search_galleries
    
    def search_posts(
        self, 
        page: int,
        key: Union[str, None] = None,
    ) -> List[Post]:
        """
        Executes the search given by the `q` query parameter, and returns **post responses** sorted by descending creation time.

        A request will be sent to the following endpoint: `/api/v1/json/search/posts`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/posts?q=subject:time wasting thread

        The API should return json looking like `{"posts":[Post]}` which will then be parsed to the python result `List[Post]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Post]
        """
        url: str = self._base_url + f'/api/v1/json/search/posts'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
            'key': key,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['posts']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Post] = [
            Post.from_dict(item)
            for item in result
        ]
        return result
    # end def search_posts
    
    def search_images(
        self, 
        page: int,
        per_page: int,
        q: str,
        sd: str,
        sf: str,
        key: Union[str, None] = None,
        filter_id: Union[int, None] = None,
    ) -> List[Image]:
        """
        Executes the search given by the `q` query parameter, and returns **image responses**.

        A request will be sent to the following endpoint: `/api/v1/json/search/images`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/images?q=safe

        The API should return json looking like `{"images":[Image]}` which will then be parsed to the python result `List[Image]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :param per_page: Controls the number of results per page, up to a limit of 50, if the response is paginated. The default is 25.
        :type  per_page: int
        
        :param q: The current search query, if the request is a search request.
        :type  q: str
        
        :param sd: The current sort direction, if the request is a search request.
        :type  sd: str
        
        :param sf: The current sort field, if the request is a search request.
        :type  sf: str
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :param filter_id: Assuming the user can access the filter ID given by the parameter, overrides the current filter for this request. This is primarily useful for unauthenticated API access.
        :type  filter_id: int|None
        
        :return: The parsed result from the API.
        :rtype:  List[Image]
        """
        url: str = self._base_url + f'/api/v1/json/search/images'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
            'per_page': per_page,
            'q': q,
            'sd': sd,
            'sf': sf,
            'key': key,
            'filter_id': filter_id,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['images']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Image] = [
            Image.from_dict(item)
            for item in result
        ]
        return result
    # end def search_images
    
    def search_tags(
        self, 
        page: int,
    ) -> List[Tag]:
        """
        Executes the search given by the `q` query parameter, and returns **tag responses** sorted by descending image count.

        A request will be sent to the following endpoint: `/api/v1/json/search/tags`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/search/tags?q=analyzed_name:wing

        The API should return json looking like `{"tags":[Tag]}` which will then be parsed to the python result `List[Tag]`.
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :return: The parsed result from the API.
        :rtype:  List[Tag]
        """
        url: str = self._base_url + f'/api/v1/json/search/tags'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['tags']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Tag] = [
            Tag.from_dict(item)
            for item in result
        ]
        return result
    # end def search_tags
    
    def search_reverse(
        self, 
        url: str,
        distance: float,
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
        :type  distance: float
        
        :param key: An optional authentication token. If omitted, no user will be authenticated.

                    You can find your authentication token in your [account settings](https://derpibooru.org/registration/edit).
        :type  key: str|None
        
        :return: The parsed result from the API.
        :rtype:  List[Image]
        """
        url: str = self._base_url + f'/api/v1/json/search/reverse'
        resp: internet.Response = internet.request('POST', url, params={
            'url': url,
            'distance': distance,
            'key': key,
        })
        self._check_response(resp)
        result: Dict[str, List[Dict]] = resp.json()
        result: List[Dict] = result['images']
        assert_type_or_raise(result, list, parameter_name='result')
        result: List[Image] = [
            Image.from_dict(item)
            for item in result
        ]
        return result
    # end def search_reverse
    
    def forums(
        self, 
    ) -> Forum:
        """
        Fetches a list of **forum responses**.

        A request will be sent to the following endpoint: `/api/v1/json/forums`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums

        The API should return json looking like `{"forums":Forum}` which will then be parsed to the python result `Forum`.
        
        :return: The parsed result from the API.
        :rtype:  Forum
        """
        url: str = self._base_url + f'/api/v1/json/forums'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['forums']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Forum = Forum.from_dict(result)
        return result
    # end def forums
    
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
        url: str = self._base_url + f'/api/v1/json/forums/{short_name}'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['forum']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Forum = Forum.from_dict(result)
        return result
    # end def forum
    
    def forum_topics(
        self, 
        short_name: str,
        page: int,
    ) -> Topic:
        """
        Fetches a list of **topic responses** for the abbreviated forum name given by the `short_name` URL parameter.

        A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics

        The API should return json looking like `{"topics":Topic}` which will then be parsed to the python result `Topic`.
        
        :param short_name: the variable short_name part of the url.
        :type  short_name: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :return: The parsed result from the API.
        :rtype:  Topic
        """
        url: str = self._base_url + f'/api/v1/json/forums/{short_name}/topics'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
        })
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['topics']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Topic = Topic.from_dict(result)
        return result
    # end def forum_topics
    
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
        url: str = self._base_url + f'/api/v1/json/forums/{short_name}/topics/{topic_slug}'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['topic']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Topic = Topic.from_dict(result)
        return result
    # end def forum_topic
    
    def forum_posts(
        self, 
        short_name: str,
        topic_slug: str,
        page: int,
    ) -> Post:
        """
        Fetches a list of **post responses** for the abbreviated forum name given by the `short_name` and topic given by `topic_slug` URL parameters.

        A request will be sent to the following endpoint: `/api/v1/json/forums/:short_name/topics/:topic_slug/posts`
        It will take in account `self._base_url` and fill in all url variables and append the data parameters as needed,
        which would for example look like this: https://derpibooru.org/api/v1/json/forums/dis/topics/ask-the-mods-anything/posts

        The API should return json looking like `{"posts":Post}` which will then be parsed to the python result `Post`.
        
        :param short_name: the variable short_name part of the url.
        :type  short_name: str
        
        :param topic_slug: the variable topic_slug part of the url.
        :type  topic_slug: str
        
        :param page: Controls the current page of the response, if the response is paginated. Empty values default to the first page.
        :type  page: int
        
        :return: The parsed result from the API.
        :rtype:  Post
        """
        url: str = self._base_url + f'/api/v1/json/forums/{short_name}/topics/{topic_slug}/posts'
        resp: internet.Response = internet.request('GET', url, params={
            'page': page,
        })
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['posts']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Post = Post.from_dict(result)
        return result
    # end def forum_posts
    
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
        url: str = self._base_url + f'/api/v1/json/forums/{short_name}/topics/{topic_slug}/posts/{post_id}'
        resp: internet.Response = internet.request('GET', url)
        self._check_response(resp)
        result: Dict[str, Dict] = resp.json()
        result: Dict = result['post']
        assert_type_or_raise(result, dict, parameter_name='result')
        result: Post = Post.from_dict(result)
        return result
    # end def forum_post
    
# end class