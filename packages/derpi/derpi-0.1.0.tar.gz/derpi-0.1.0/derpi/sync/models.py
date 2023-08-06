#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import iso8601

from datetime import datetime
from typing import Union, List, Dict, Type, TypeVar, Generic

from luckydonaldUtils.logger import logging
from luckydonaldUtils.typing import JSONType
from luckydonaldUtils.exceptions import assert_type_or_raise


__author__ = 'luckydonald'
__all__ = ['DerpiModel', 'SearchResult', 'Image', 'Representations', 'Intensities', 'Comment', 'Forum', 'Topic', 'Post', 'Tag', 'User', 'Filter', 'Links', 'Awards', 'Gallery', 'Oembed']

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if

T = TypeVar('T')


class DerpiModel(object):
    """
    Base class for all models
    """

    _assert_consuming_all_params = True  # If set to true we check that we have consumed all arguments.

    @classmethod
    def prepare_dict(cls: Type[DerpiModel], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the DerpiModel constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        return {}
    # end def prepare_dict
# end class DerpiModel


class SearchResult(DerpiModel, Generic[T]):
    """
    A parsed SearchResult response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param hits: List of results
    :type  hits: List[T]
    
    :param total: Total amount of results, e.g. for pagination.
    :type  total: int
    
    """

    
    """ List of results """
    hits: List[T]
    
    """ Total amount of results, e.g. for pagination. """
    total: int
    
    def __init__(
        self, 
        hits: List[T],
        total: int,
    ):
        """
        A parsed SearchResult response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param hits: List of results
        :type  hits: List[T]
        
        :param total: Total amount of results, e.g. for pagination.
        :type  total: int
        
        """
        self.hits = hits
        self.total = total
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[SearchResult], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the SearchResult constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['hits'] = List[T].from_dict(data['hits'])
        arguments['total'] = data['total']
        
        del data['hits']
        del data['total']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[SearchResult], data: Union[Dict, None, List[Dict]]) -> Union[SearchResult, None]:
        """
        Deserialize a new SearchResult from a given dictionary.

        :return: new SearchResult instance.
        :rtype: SearchResult|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: SearchResult = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(searchresult_instance)`
        """
        return "{s.__class__.__name__}(hits={s.hits!r}, total={s.total!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(searchresult_instance)`
        """
        
        return "{s.__class__.__name__}(hits={s.hits!r}, total={s.total!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `searchresult_instance_a == searchresult_instance_b`
        """
        if not (hasattr(other, 'hits') and hasattr(other, 'total')):
            return False
        # end if
        return self.hits == other.hits and self.total == other.total
    # end __eq__
# end class


class Image(DerpiModel):
    """
    A parsed Image response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param aspect_ratio: The image's width divided by its height.
    :type  aspect_ratio: float
    
    :param comment_count: The number of comments made on the image.
    :type  comment_count: int
    
    :param created_at: The creation time, in UTC, of the image.
    :type  created_at: datetime
    
    :param deletion_reason: The hide reason for the image, or `null` if none provided. This will only have a value on images which are deleted for a rule violation.
    :type  deletion_reason: str
    
    :param description: The image's description.
    :type  description: str
    
    :param downvotes: The number of downvotes the image has.
    :type  downvotes: int
    
    :param duplicate_of: The ID of the target image, or `null` if none provided. This will only have a value on images which are merged into another image.
    :type  duplicate_of: int
    
    :param faves: The number of faves the image has.
    :type  faves: int
    
    :param first_seen_at: The time, in UTC, this image was first seen (before any duplicate merging).
    :type  first_seen_at: datetime
    
    :param format: The file extension of this image. One of `"gif", "jpg", "jpeg", "png", "svg", "webm"`.
    :type  format: str
    
    :param height: The image's height, in pixels.
    :type  height: int
    
    :param hidden_from_users: Whether this image is hidden. An image is hidden if it is merged or deleted for a rule violation.
    :type  hidden_from_users: bool
    
    :param id: The image's ID.
    :type  id: int
    
    :param intensities: Optional object of [internal image intensity data](https://derpibooru.orghttps://github.com/derpibooru/cli_intensities) for deduplication purposes. May be `null` if intensities have not yet been generated.
    :type  intensities: Intensities|None
    
    :param mime_type: The MIME type of this image. One of `"image/gif", "image/jpeg", "image/png", "image/svg+xml", "video/webm"`.
    :type  mime_type: str
    
    :param name: The filename that this image was uploaded with.
    :type  name: str
    
    :param orig_sha512_hash: The SHA512 hash of this image as it was originally uploaded.
    :type  orig_sha512_hash: str
    
    :param processed: Whether the image has finished optimization.
    :type  processed: bool
    
    :param representations: A mapping of representation names to their respective URLs. Contains the keys `"full", "large", "medium", "small", "tall", "thumb", "thumb_small", "thumb_tiny"`.
    :type  representations: Representations
    
    :param score: The image's number of upvotes minus the image's number of downvotes.
    :type  score: int
    
    :param sha512_hash: The SHA512 hash of this image after it has been processed.
    :type  sha512_hash: str
    
    :param source_url: The current source URL of the image.
    :type  source_url: str
    
    :param spoilered: Whether this image is hit by the current filter.
    :type  spoilered: bool
    
    :param tag_count: The number of tags present on this image.
    :type  tag_count: int
    
    :param tag_ids: A list of tag IDs this image contains.
    :type  tag_ids: list
    
    :param tags: A list of tag names this image contains.
    :type  tags: list
    
    :param thumbnails_generated: Whether this image has finished thumbnail generation. Do not attempt to load images from `view_url` or `representations` if this is false.
    :type  thumbnails_generated: bool
    
    :param updated_at: The time, in UTC, the image was last updated.
    :type  updated_at: datetime
    
    :param uploader: The image's uploader.
    :type  uploader: str
    
    :param uploader_id: The ID of the image's uploader.
    :type  uploader_id: int
    
    :param upvotes: The image's number of upvotes.
    :type  upvotes: int
    
    :param view_url: The image's view URL, including tags.
    :type  view_url: str
    
    :param width: The image's width, in pixels.
    :type  width: int
    
    :param wilson_score: The lower bound of the [Wilson score interval](https://derpibooru.orghttps://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval) for the image, based on its upvotes and downvotes, given a z-score corresponding to a confidence of 99.5%.
    :type  wilson_score: float
    
    """

    
    """ The image's width divided by its height. """
    aspect_ratio: float
    
    """ The number of comments made on the image. """
    comment_count: int
    
    """ The creation time, in UTC, of the image. """
    created_at: datetime
    
    """ The hide reason for the image, or `null` if none provided. This will only have a value on images which are deleted for a rule violation. """
    deletion_reason: str
    
    """ The image's description. """
    description: str
    
    """ The number of downvotes the image has. """
    downvotes: int
    
    """ The ID of the target image, or `null` if none provided. This will only have a value on images which are merged into another image. """
    duplicate_of: int
    
    """ The number of faves the image has. """
    faves: int
    
    """ The time, in UTC, this image was first seen (before any duplicate merging). """
    first_seen_at: datetime
    
    """ The file extension of this image. One of `"gif", "jpg", "jpeg", "png", "svg", "webm"`. """
    format: str
    
    """ The image's height, in pixels. """
    height: int
    
    """ Whether this image is hidden. An image is hidden if it is merged or deleted for a rule violation. """
    hidden_from_users: bool
    
    """ The image's ID. """
    id: int
    
    """ Optional object of [internal image intensity data](https://derpibooru.orghttps://github.com/derpibooru/cli_intensities) for deduplication purposes. May be `null` if intensities have not yet been generated. """
    intensities: Union[Intensities, None]
    
    """ The MIME type of this image. One of `"image/gif", "image/jpeg", "image/png", "image/svg+xml", "video/webm"`. """
    mime_type: str
    
    """ The filename that this image was uploaded with. """
    name: str
    
    """ The SHA512 hash of this image as it was originally uploaded. """
    orig_sha512_hash: str
    
    """ Whether the image has finished optimization. """
    processed: bool
    
    """ A mapping of representation names to their respective URLs. Contains the keys `"full", "large", "medium", "small", "tall", "thumb", "thumb_small", "thumb_tiny"`. """
    representations: Representations
    
    """ The image's number of upvotes minus the image's number of downvotes. """
    score: int
    
    """ The SHA512 hash of this image after it has been processed. """
    sha512_hash: str
    
    """ The current source URL of the image. """
    source_url: str
    
    """ Whether this image is hit by the current filter. """
    spoilered: bool
    
    """ The number of tags present on this image. """
    tag_count: int
    
    """ A list of tag IDs this image contains. """
    tag_ids: list
    
    """ A list of tag names this image contains. """
    tags: list
    
    """ Whether this image has finished thumbnail generation. Do not attempt to load images from `view_url` or `representations` if this is false. """
    thumbnails_generated: bool
    
    """ The time, in UTC, the image was last updated. """
    updated_at: datetime
    
    """ The image's uploader. """
    uploader: str
    
    """ The ID of the image's uploader. """
    uploader_id: int
    
    """ The image's number of upvotes. """
    upvotes: int
    
    """ The image's view URL, including tags. """
    view_url: str
    
    """ The image's width, in pixels. """
    width: int
    
    """ The lower bound of the [Wilson score interval](https://derpibooru.orghttps://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval) for the image, based on its upvotes and downvotes, given a z-score corresponding to a confidence of 99.5%. """
    wilson_score: float
    
    def __init__(
        self, 
        aspect_ratio: float,
        comment_count: int,
        created_at: datetime,
        deletion_reason: str,
        description: str,
        downvotes: int,
        duplicate_of: int,
        faves: int,
        first_seen_at: datetime,
        format: str,
        height: int,
        hidden_from_users: bool,
        id: int,
        mime_type: str,
        name: str,
        orig_sha512_hash: str,
        processed: bool,
        representations: Representations,
        score: int,
        sha512_hash: str,
        source_url: str,
        spoilered: bool,
        tag_count: int,
        tag_ids: list,
        tags: list,
        thumbnails_generated: bool,
        updated_at: datetime,
        uploader: str,
        uploader_id: int,
        upvotes: int,
        view_url: str,
        width: int,
        wilson_score: float,
        intensities: Union[Intensities, None] = None,
    ):
        """
        A parsed Image response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param aspect_ratio: The image's width divided by its height.
        :type  aspect_ratio: float
        
        :param comment_count: The number of comments made on the image.
        :type  comment_count: int
        
        :param created_at: The creation time, in UTC, of the image.
        :type  created_at: datetime
        
        :param deletion_reason: The hide reason for the image, or `null` if none provided. This will only have a value on images which are deleted for a rule violation.
        :type  deletion_reason: str
        
        :param description: The image's description.
        :type  description: str
        
        :param downvotes: The number of downvotes the image has.
        :type  downvotes: int
        
        :param duplicate_of: The ID of the target image, or `null` if none provided. This will only have a value on images which are merged into another image.
        :type  duplicate_of: int
        
        :param faves: The number of faves the image has.
        :type  faves: int
        
        :param first_seen_at: The time, in UTC, this image was first seen (before any duplicate merging).
        :type  first_seen_at: datetime
        
        :param format: The file extension of this image. One of `"gif", "jpg", "jpeg", "png", "svg", "webm"`.
        :type  format: str
        
        :param height: The image's height, in pixels.
        :type  height: int
        
        :param hidden_from_users: Whether this image is hidden. An image is hidden if it is merged or deleted for a rule violation.
        :type  hidden_from_users: bool
        
        :param id: The image's ID.
        :type  id: int
        
        :param intensities: Optional object of [internal image intensity data](https://derpibooru.orghttps://github.com/derpibooru/cli_intensities) for deduplication purposes. May be `null` if intensities have not yet been generated.
        :type  intensities: Intensities|None
        
        :param mime_type: The MIME type of this image. One of `"image/gif", "image/jpeg", "image/png", "image/svg+xml", "video/webm"`.
        :type  mime_type: str
        
        :param name: The filename that this image was uploaded with.
        :type  name: str
        
        :param orig_sha512_hash: The SHA512 hash of this image as it was originally uploaded.
        :type  orig_sha512_hash: str
        
        :param processed: Whether the image has finished optimization.
        :type  processed: bool
        
        :param representations: A mapping of representation names to their respective URLs. Contains the keys `"full", "large", "medium", "small", "tall", "thumb", "thumb_small", "thumb_tiny"`.
        :type  representations: Representations
        
        :param score: The image's number of upvotes minus the image's number of downvotes.
        :type  score: int
        
        :param sha512_hash: The SHA512 hash of this image after it has been processed.
        :type  sha512_hash: str
        
        :param source_url: The current source URL of the image.
        :type  source_url: str
        
        :param spoilered: Whether this image is hit by the current filter.
        :type  spoilered: bool
        
        :param tag_count: The number of tags present on this image.
        :type  tag_count: int
        
        :param tag_ids: A list of tag IDs this image contains.
        :type  tag_ids: list
        
        :param tags: A list of tag names this image contains.
        :type  tags: list
        
        :param thumbnails_generated: Whether this image has finished thumbnail generation. Do not attempt to load images from `view_url` or `representations` if this is false.
        :type  thumbnails_generated: bool
        
        :param updated_at: The time, in UTC, the image was last updated.
        :type  updated_at: datetime
        
        :param uploader: The image's uploader.
        :type  uploader: str
        
        :param uploader_id: The ID of the image's uploader.
        :type  uploader_id: int
        
        :param upvotes: The image's number of upvotes.
        :type  upvotes: int
        
        :param view_url: The image's view URL, including tags.
        :type  view_url: str
        
        :param width: The image's width, in pixels.
        :type  width: int
        
        :param wilson_score: The lower bound of the [Wilson score interval](https://derpibooru.orghttps://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval) for the image, based on its upvotes and downvotes, given a z-score corresponding to a confidence of 99.5%.
        :type  wilson_score: float
        
        """
        self.aspect_ratio = aspect_ratio
        self.comment_count = comment_count
        self.created_at = created_at
        self.deletion_reason = deletion_reason
        self.description = description
        self.downvotes = downvotes
        self.duplicate_of = duplicate_of
        self.faves = faves
        self.first_seen_at = first_seen_at
        self.format = format
        self.height = height
        self.hidden_from_users = hidden_from_users
        self.id = id
        self.intensities = intensities
        self.mime_type = mime_type
        self.name = name
        self.orig_sha512_hash = orig_sha512_hash
        self.processed = processed
        self.representations = representations
        self.score = score
        self.sha512_hash = sha512_hash
        self.source_url = source_url
        self.spoilered = spoilered
        self.tag_count = tag_count
        self.tag_ids = tag_ids
        self.tags = tags
        self.thumbnails_generated = thumbnails_generated
        self.updated_at = updated_at
        self.uploader = uploader
        self.uploader_id = uploader_id
        self.upvotes = upvotes
        self.view_url = view_url
        self.width = width
        self.wilson_score = wilson_score
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Image], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Image constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['aspect_ratio'] = data['aspect_ratio']
        arguments['comment_count'] = data['comment_count']
        arguments['created_at'] = iso8601.parse_date(data['created_at'])
        arguments['deletion_reason'] = data['deletion_reason']
        arguments['description'] = data['description']
        arguments['downvotes'] = data['downvotes']
        arguments['duplicate_of'] = data['duplicate_of']
        arguments['faves'] = data['faves']
        arguments['first_seen_at'] = iso8601.parse_date(data['first_seen_at'])
        arguments['format'] = data['format']
        arguments['height'] = data['height']
        arguments['hidden_from_users'] = data['hidden_from_users']
        arguments['id'] = data['id']
        arguments['intensities'] = Intensities.from_dict(data['intensities']) if data.get('intensities', None) is not None else None
        arguments['mime_type'] = data['mime_type']
        arguments['name'] = data['name']
        arguments['orig_sha512_hash'] = data['orig_sha512_hash']
        arguments['processed'] = data['processed']
        arguments['representations'] = Representations.from_dict(data['representations'])
        arguments['score'] = data['score']
        arguments['sha512_hash'] = data['sha512_hash']
        arguments['source_url'] = data['source_url']
        arguments['spoilered'] = data['spoilered']
        arguments['tag_count'] = data['tag_count']
        arguments['tag_ids'] = data['tag_ids']
        arguments['tags'] = data['tags']
        arguments['thumbnails_generated'] = data['thumbnails_generated']
        arguments['updated_at'] = iso8601.parse_date(data['updated_at'])
        arguments['uploader'] = data['uploader']
        arguments['uploader_id'] = data['uploader_id']
        arguments['upvotes'] = data['upvotes']
        arguments['view_url'] = data['view_url']
        arguments['width'] = data['width']
        arguments['wilson_score'] = data['wilson_score']
        
        del data['aspect_ratio']
        del data['comment_count']
        del data['created_at']
        del data['deletion_reason']
        del data['description']
        del data['downvotes']
        del data['duplicate_of']
        del data['faves']
        del data['first_seen_at']
        del data['format']
        del data['height']
        del data['hidden_from_users']
        del data['id']
        if 'intensities' in data:
            del data['intensities']
        # end if
        del data['mime_type']
        del data['name']
        del data['orig_sha512_hash']
        del data['processed']
        del data['representations']
        del data['score']
        del data['sha512_hash']
        del data['source_url']
        del data['spoilered']
        del data['tag_count']
        del data['tag_ids']
        del data['tags']
        del data['thumbnails_generated']
        del data['updated_at']
        del data['uploader']
        del data['uploader_id']
        del data['upvotes']
        del data['view_url']
        del data['width']
        del data['wilson_score']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Image], data: Union[Dict, None, List[Dict]]) -> Union[Image, None]:
        """
        Deserialize a new Image from a given dictionary.

        :return: new Image instance.
        :rtype: Image|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Image = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(image_instance)`
        """
        return "{s.__class__.__name__}(aspect_ratio={s.aspect_ratio!r}, comment_count={s.comment_count!r}, created_at={s.created_at!r}, deletion_reason={s.deletion_reason!r}, description={s.description!r}, downvotes={s.downvotes!r}, duplicate_of={s.duplicate_of!r}, faves={s.faves!r}, first_seen_at={s.first_seen_at!r}, format={s.format!r}, height={s.height!r}, hidden_from_users={s.hidden_from_users!r}, id={s.id!r}, intensities={s.intensities!r}, mime_type={s.mime_type!r}, name={s.name!r}, orig_sha512_hash={s.orig_sha512_hash!r}, processed={s.processed!r}, representations={s.representations!r}, score={s.score!r}, sha512_hash={s.sha512_hash!r}, source_url={s.source_url!r}, spoilered={s.spoilered!r}, tag_count={s.tag_count!r}, tag_ids={s.tag_ids!r}, tags={s.tags!r}, thumbnails_generated={s.thumbnails_generated!r}, updated_at={s.updated_at!r}, uploader={s.uploader!r}, uploader_id={s.uploader_id!r}, upvotes={s.upvotes!r}, view_url={s.view_url!r}, width={s.width!r}, wilson_score={s.wilson_score!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(image_instance)`
        """
        
        return "{s.__class__.__name__}(aspect_ratio={s.aspect_ratio!r}, comment_count={s.comment_count!r}, created_at={s.created_at!r}, deletion_reason={s.deletion_reason!r}, description={s.description!r}, downvotes={s.downvotes!r}, duplicate_of={s.duplicate_of!r}, faves={s.faves!r}, first_seen_at={s.first_seen_at!r}, format={s.format!r}, height={s.height!r}, hidden_from_users={s.hidden_from_users!r}, id={s.id!r}, intensities={s.intensities!r}, mime_type={s.mime_type!r}, name={s.name!r}, orig_sha512_hash={s.orig_sha512_hash!r}, processed={s.processed!r}, representations={s.representations!r}, score={s.score!r}, sha512_hash={s.sha512_hash!r}, source_url={s.source_url!r}, spoilered={s.spoilered!r}, tag_count={s.tag_count!r}, tag_ids={s.tag_ids!r}, tags={s.tags!r}, thumbnails_generated={s.thumbnails_generated!r}, updated_at={s.updated_at!r}, uploader={s.uploader!r}, uploader_id={s.uploader_id!r}, upvotes={s.upvotes!r}, view_url={s.view_url!r}, width={s.width!r}, wilson_score={s.wilson_score!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `image_instance_a == image_instance_b`
        """
        if not (hasattr(other, 'aspect_ratio') and hasattr(other, 'comment_count') and hasattr(other, 'created_at') and hasattr(other, 'deletion_reason') and hasattr(other, 'description') and hasattr(other, 'downvotes') and hasattr(other, 'duplicate_of') and hasattr(other, 'faves') and hasattr(other, 'first_seen_at') and hasattr(other, 'format') and hasattr(other, 'height') and hasattr(other, 'hidden_from_users') and hasattr(other, 'id') and hasattr(other, 'intensities') and hasattr(other, 'mime_type') and hasattr(other, 'name') and hasattr(other, 'orig_sha512_hash') and hasattr(other, 'processed') and hasattr(other, 'representations') and hasattr(other, 'score') and hasattr(other, 'sha512_hash') and hasattr(other, 'source_url') and hasattr(other, 'spoilered') and hasattr(other, 'tag_count') and hasattr(other, 'tag_ids') and hasattr(other, 'tags') and hasattr(other, 'thumbnails_generated') and hasattr(other, 'updated_at') and hasattr(other, 'uploader') and hasattr(other, 'uploader_id') and hasattr(other, 'upvotes') and hasattr(other, 'view_url') and hasattr(other, 'width') and hasattr(other, 'wilson_score')):
            return False
        # end if
        return self.aspect_ratio == other.aspect_ratio and self.comment_count == other.comment_count and self.created_at == other.created_at and self.deletion_reason == other.deletion_reason and self.description == other.description and self.downvotes == other.downvotes and self.duplicate_of == other.duplicate_of and self.faves == other.faves and self.first_seen_at == other.first_seen_at and self.format == other.format and self.height == other.height and self.hidden_from_users == other.hidden_from_users and self.id == other.id and self.intensities == other.intensities and self.mime_type == other.mime_type and self.name == other.name and self.orig_sha512_hash == other.orig_sha512_hash and self.processed == other.processed and self.representations == other.representations and self.score == other.score and self.sha512_hash == other.sha512_hash and self.source_url == other.source_url and self.spoilered == other.spoilered and self.tag_count == other.tag_count and self.tag_ids == other.tag_ids and self.tags == other.tags and self.thumbnails_generated == other.thumbnails_generated and self.updated_at == other.updated_at and self.uploader == other.uploader and self.uploader_id == other.uploader_id and self.upvotes == other.upvotes and self.view_url == other.view_url and self.width == other.width and self.wilson_score == other.wilson_score
    # end __eq__
# end class


class Representations(DerpiModel):
    """
    A parsed Representations response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param full: The url to the image in original resolution.
    :type  full: str
    
    :param large: The url to the image in large resolution.
    :type  large: str
    
    :param medium: The url to the image in medium resolution.
    :type  medium: str
    
    :param small: The url to the image in small resolution.
    :type  small: str
    
    :param tall: The url to the image in tall resolution.
    :type  tall: str
    
    :param thumb: The url to the image thumbnail in normal resolution.
    :type  thumb: str
    
    :param thumb_small: The url to the image thumbnail in small resolution.
    :type  thumb_small: str
    
    :param thumb_tiny: The url to the image thumbnail in tiny resolution.
    :type  thumb_tiny: str
    
    :param mp4: Optional. The url to the animated image as mp4 format.
    :type  mp4: str|None
    
    :param webm: Optional. The url to the animated image as webm format.
    :type  webm: str|None
    
    """

    
    """ The url to the image in original resolution. """
    full: str
    
    """ The url to the image in large resolution. """
    large: str
    
    """ The url to the image in medium resolution. """
    medium: str
    
    """ The url to the image in small resolution. """
    small: str
    
    """ The url to the image in tall resolution. """
    tall: str
    
    """ The url to the image thumbnail in normal resolution. """
    thumb: str
    
    """ The url to the image thumbnail in small resolution. """
    thumb_small: str
    
    """ The url to the image thumbnail in tiny resolution. """
    thumb_tiny: str
    
    """ Optional. The url to the animated image as mp4 format. """
    mp4: Union[str, None]
    
    """ Optional. The url to the animated image as webm format. """
    webm: Union[str, None]
    
    def __init__(
        self, 
        full: str,
        large: str,
        medium: str,
        small: str,
        tall: str,
        thumb: str,
        thumb_small: str,
        thumb_tiny: str,
        mp4: Union[str, None] = None,
        webm: Union[str, None] = None,
    ):
        """
        A parsed Representations response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param full: The url to the image in original resolution.
        :type  full: str
        
        :param large: The url to the image in large resolution.
        :type  large: str
        
        :param medium: The url to the image in medium resolution.
        :type  medium: str
        
        :param small: The url to the image in small resolution.
        :type  small: str
        
        :param tall: The url to the image in tall resolution.
        :type  tall: str
        
        :param thumb: The url to the image thumbnail in normal resolution.
        :type  thumb: str
        
        :param thumb_small: The url to the image thumbnail in small resolution.
        :type  thumb_small: str
        
        :param thumb_tiny: The url to the image thumbnail in tiny resolution.
        :type  thumb_tiny: str
        
        :param mp4: Optional. The url to the animated image as mp4 format.
        :type  mp4: str|None
        
        :param webm: Optional. The url to the animated image as webm format.
        :type  webm: str|None
        
        """
        self.full = full
        self.large = large
        self.medium = medium
        self.small = small
        self.tall = tall
        self.thumb = thumb
        self.thumb_small = thumb_small
        self.thumb_tiny = thumb_tiny
        self.mp4 = mp4
        self.webm = webm
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Representations], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Representations constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['full'] = data['full']
        arguments['large'] = data['large']
        arguments['medium'] = data['medium']
        arguments['small'] = data['small']
        arguments['tall'] = data['tall']
        arguments['thumb'] = data['thumb']
        arguments['thumb_small'] = data['thumb_small']
        arguments['thumb_tiny'] = data['thumb_tiny']
        arguments['mp4'] = data['mp4'] if data.get('mp4', None) is not None else None
        arguments['webm'] = data['webm'] if data.get('webm', None) is not None else None
        
        del data['full']
        del data['large']
        del data['medium']
        del data['small']
        del data['tall']
        del data['thumb']
        del data['thumb_small']
        del data['thumb_tiny']
        if 'mp4' in data:
            del data['mp4']
        # end if
        if 'webm' in data:
            del data['webm']
        # end if

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Representations], data: Union[Dict, None, List[Dict]]) -> Union[Representations, None]:
        """
        Deserialize a new Representations from a given dictionary.

        :return: new Representations instance.
        :rtype: Representations|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Representations = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(representations_instance)`
        """
        return "{s.__class__.__name__}(full={s.full!r}, large={s.large!r}, medium={s.medium!r}, small={s.small!r}, tall={s.tall!r}, thumb={s.thumb!r}, thumb_small={s.thumb_small!r}, thumb_tiny={s.thumb_tiny!r}, mp4={s.mp4!r}, webm={s.webm!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(representations_instance)`
        """
        
        return "{s.__class__.__name__}(full={s.full!r}, large={s.large!r}, medium={s.medium!r}, small={s.small!r}, tall={s.tall!r}, thumb={s.thumb!r}, thumb_small={s.thumb_small!r}, thumb_tiny={s.thumb_tiny!r}, mp4={s.mp4!r}, webm={s.webm!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `representations_instance_a == representations_instance_b`
        """
        if not (hasattr(other, 'full') and hasattr(other, 'large') and hasattr(other, 'medium') and hasattr(other, 'small') and hasattr(other, 'tall') and hasattr(other, 'thumb') and hasattr(other, 'thumb_small') and hasattr(other, 'thumb_tiny') and hasattr(other, 'mp4') and hasattr(other, 'webm')):
            return False
        # end if
        return self.full == other.full and self.large == other.large and self.medium == other.medium and self.small == other.small and self.tall == other.tall and self.thumb == other.thumb and self.thumb_small == other.thumb_small and self.thumb_tiny == other.thumb_tiny and self.mp4 == other.mp4 and self.webm == other.webm
    # end __eq__
# end class


class Intensities(DerpiModel):
    """
    A parsed Intensities response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param ne: Northeast intensity. Whatever that means…
    :type  ne: float
    
    :param nw: Northwest intensity. Whatever that means…
    :type  nw: float
    
    :param se: Southeast intensity. Whatever that means…
    :type  se: float
    
    :param sw: Southwest intensity. Whatever that means…
    :type  sw: float
    
    """

    
    """ Northeast intensity. Whatever that means… """
    ne: float
    
    """ Northwest intensity. Whatever that means… """
    nw: float
    
    """ Southeast intensity. Whatever that means… """
    se: float
    
    """ Southwest intensity. Whatever that means… """
    sw: float
    
    def __init__(
        self, 
        ne: float,
        nw: float,
        se: float,
        sw: float,
    ):
        """
        A parsed Intensities response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param ne: Northeast intensity. Whatever that means…
        :type  ne: float
        
        :param nw: Northwest intensity. Whatever that means…
        :type  nw: float
        
        :param se: Southeast intensity. Whatever that means…
        :type  se: float
        
        :param sw: Southwest intensity. Whatever that means…
        :type  sw: float
        
        """
        self.ne = ne
        self.nw = nw
        self.se = se
        self.sw = sw
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Intensities], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Intensities constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['ne'] = data['ne']
        arguments['nw'] = data['nw']
        arguments['se'] = data['se']
        arguments['sw'] = data['sw']
        
        del data['ne']
        del data['nw']
        del data['se']
        del data['sw']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Intensities], data: Union[Dict, None, List[Dict]]) -> Union[Intensities, None]:
        """
        Deserialize a new Intensities from a given dictionary.

        :return: new Intensities instance.
        :rtype: Intensities|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Intensities = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(intensities_instance)`
        """
        return "{s.__class__.__name__}(ne={s.ne!r}, nw={s.nw!r}, se={s.se!r}, sw={s.sw!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(intensities_instance)`
        """
        
        return "{s.__class__.__name__}(ne={s.ne!r}, nw={s.nw!r}, se={s.se!r}, sw={s.sw!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `intensities_instance_a == intensities_instance_b`
        """
        if not (hasattr(other, 'ne') and hasattr(other, 'nw') and hasattr(other, 'se') and hasattr(other, 'sw')):
            return False
        # end if
        return self.ne == other.ne and self.nw == other.nw and self.se == other.se and self.sw == other.sw
    # end __eq__
# end class


class Comment(DerpiModel):
    """
    A parsed Comment response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param author: The comment's author.
    :type  author: str
    
    :param avatar: The comment's author's avatar. Normal URL or a base64 encoded inline svg with an appropriate header. Format like `data:image/svg+xml;base64,…`.
    :type  avatar: str
    
    :param body: The comment text.
    :type  body: str
    
    :param id: The comment's ID.
    :type  id: int
    
    :param created_at: The creation time, in UTC, of this comment.
    :type  created_at: datetime
    
    :param image_id: The ID of the image the comment belongs to.
    :type  image_id: int
    
    :param edit_reason: Optional. The user provided reason for an edit, if any.
    :type  edit_reason: str|None
    
    :param edited_at: Optional. The edit time, in UTC, of this comment.
    :type  edited_at: datetime|None
    
    :param updated_at: The time, in UTC, the comment was last updated.
    :type  updated_at: datetime
    
    :param user_id: The ID of the user the comment belongs to, if any.
    :type  user_id: int
    
    """

    
    """ The comment's author. """
    author: str
    
    """ The comment's author's avatar. Normal URL or a base64 encoded inline svg with an appropriate header. Format like `data:image/svg+xml;base64,…`. """
    avatar: str
    
    """ The comment text. """
    body: str
    
    """ The comment's ID. """
    id: int
    
    """ The creation time, in UTC, of this comment. """
    created_at: datetime
    
    """ The ID of the image the comment belongs to. """
    image_id: int
    
    """ Optional. The user provided reason for an edit, if any. """
    edit_reason: Union[str, None]
    
    """ Optional. The edit time, in UTC, of this comment. """
    edited_at: Union[datetime, None]
    
    """ The time, in UTC, the comment was last updated. """
    updated_at: datetime
    
    """ The ID of the user the comment belongs to, if any. """
    user_id: int
    
    def __init__(
        self, 
        author: str,
        avatar: str,
        body: str,
        id: int,
        created_at: datetime,
        image_id: int,
        updated_at: datetime,
        user_id: int,
        edit_reason: Union[str, None] = None,
        edited_at: Union[datetime, None] = None,
    ):
        """
        A parsed Comment response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param author: The comment's author.
        :type  author: str
        
        :param avatar: The comment's author's avatar. Normal URL or a base64 encoded inline svg with an appropriate header. Format like `data:image/svg+xml;base64,…`.
        :type  avatar: str
        
        :param body: The comment text.
        :type  body: str
        
        :param id: The comment's ID.
        :type  id: int
        
        :param created_at: The creation time, in UTC, of this comment.
        :type  created_at: datetime
        
        :param image_id: The ID of the image the comment belongs to.
        :type  image_id: int
        
        :param edit_reason: Optional. The user provided reason for an edit, if any.
        :type  edit_reason: str|None
        
        :param edited_at: Optional. The edit time, in UTC, of this comment.
        :type  edited_at: datetime|None
        
        :param updated_at: The time, in UTC, the comment was last updated.
        :type  updated_at: datetime
        
        :param user_id: The ID of the user the comment belongs to, if any.
        :type  user_id: int
        
        """
        self.author = author
        self.avatar = avatar
        self.body = body
        self.id = id
        self.created_at = created_at
        self.image_id = image_id
        self.edit_reason = edit_reason
        self.edited_at = edited_at
        self.updated_at = updated_at
        self.user_id = user_id
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Comment], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Comment constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['author'] = data['author']
        arguments['avatar'] = data['avatar']
        arguments['body'] = data['body']
        arguments['id'] = data['id']
        arguments['created_at'] = iso8601.parse_date(data['created_at'])
        arguments['image_id'] = data['image_id']
        arguments['edit_reason'] = data['edit_reason'] if data.get('edit_reason', None) is not None else None
        arguments['edited_at'] = iso8601.parse_date(data['edited_at']) if data.get('edited_at', None) is not None else None
        arguments['updated_at'] = iso8601.parse_date(data['updated_at'])
        arguments['user_id'] = data['user_id']
        
        del data['author']
        del data['avatar']
        del data['body']
        del data['id']
        del data['created_at']
        del data['image_id']
        if 'edit_reason' in data:
            del data['edit_reason']
        # end if
        if 'edited_at' in data:
            del data['edited_at']
        # end if
        del data['updated_at']
        del data['user_id']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Comment], data: Union[Dict, None, List[Dict]]) -> Union[Comment, None]:
        """
        Deserialize a new Comment from a given dictionary.

        :return: new Comment instance.
        :rtype: Comment|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Comment = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(comment_instance)`
        """
        return "{s.__class__.__name__}(author={s.author!r}, avatar={s.avatar!r}, body={s.body!r}, id={s.id!r}, created_at={s.created_at!r}, image_id={s.image_id!r}, edit_reason={s.edit_reason!r}, edited_at={s.edited_at!r}, updated_at={s.updated_at!r}, user_id={s.user_id!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(comment_instance)`
        """
        
        return "{s.__class__.__name__}(author={s.author!r}, avatar={s.avatar!r}, body={s.body!r}, id={s.id!r}, created_at={s.created_at!r}, image_id={s.image_id!r}, edit_reason={s.edit_reason!r}, edited_at={s.edited_at!r}, updated_at={s.updated_at!r}, user_id={s.user_id!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `comment_instance_a == comment_instance_b`
        """
        if not (hasattr(other, 'author') and hasattr(other, 'avatar') and hasattr(other, 'body') and hasattr(other, 'id') and hasattr(other, 'created_at') and hasattr(other, 'image_id') and hasattr(other, 'edit_reason') and hasattr(other, 'edited_at') and hasattr(other, 'updated_at') and hasattr(other, 'user_id')):
            return False
        # end if
        return self.author == other.author and self.avatar == other.avatar and self.body == other.body and self.id == other.id and self.created_at == other.created_at and self.image_id == other.image_id and self.edit_reason == other.edit_reason and self.edited_at == other.edited_at and self.updated_at == other.updated_at and self.user_id == other.user_id
    # end __eq__
# end class


class Forum(DerpiModel):
    """
    A parsed Forum response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param name: The forum's name.
    :type  name: str
    
    :param short_name: The forum's short name (used to identify it).
    :type  short_name: str
    
    :param description: The forum's description.
    :type  description: str
    
    :param topic_count: The amount of topics in the forum.
    :type  topic_count: int
    
    :param post_count: The amount of posts in the forum.
    :type  post_count: int
    
    """

    
    """ The forum's name. """
    name: str
    
    """ The forum's short name (used to identify it). """
    short_name: str
    
    """ The forum's description. """
    description: str
    
    """ The amount of topics in the forum. """
    topic_count: int
    
    """ The amount of posts in the forum. """
    post_count: int
    
    def __init__(
        self, 
        name: str,
        short_name: str,
        description: str,
        topic_count: int,
        post_count: int,
    ):
        """
        A parsed Forum response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param name: The forum's name.
        :type  name: str
        
        :param short_name: The forum's short name (used to identify it).
        :type  short_name: str
        
        :param description: The forum's description.
        :type  description: str
        
        :param topic_count: The amount of topics in the forum.
        :type  topic_count: int
        
        :param post_count: The amount of posts in the forum.
        :type  post_count: int
        
        """
        self.name = name
        self.short_name = short_name
        self.description = description
        self.topic_count = topic_count
        self.post_count = post_count
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Forum], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Forum constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['name'] = data['name']
        arguments['short_name'] = data['short_name']
        arguments['description'] = data['description']
        arguments['topic_count'] = data['topic_count']
        arguments['post_count'] = data['post_count']
        
        del data['name']
        del data['short_name']
        del data['description']
        del data['topic_count']
        del data['post_count']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Forum], data: Union[Dict, None, List[Dict]]) -> Union[Forum, None]:
        """
        Deserialize a new Forum from a given dictionary.

        :return: new Forum instance.
        :rtype: Forum|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Forum = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(forum_instance)`
        """
        return "{s.__class__.__name__}(name={s.name!r}, short_name={s.short_name!r}, description={s.description!r}, topic_count={s.topic_count!r}, post_count={s.post_count!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(forum_instance)`
        """
        
        return "{s.__class__.__name__}(name={s.name!r}, short_name={s.short_name!r}, description={s.description!r}, topic_count={s.topic_count!r}, post_count={s.post_count!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `forum_instance_a == forum_instance_b`
        """
        if not (hasattr(other, 'name') and hasattr(other, 'short_name') and hasattr(other, 'description') and hasattr(other, 'topic_count') and hasattr(other, 'post_count')):
            return False
        # end if
        return self.name == other.name and self.short_name == other.short_name and self.description == other.description and self.topic_count == other.topic_count and self.post_count == other.post_count
    # end __eq__
# end class


class Topic(DerpiModel):
    """
    A parsed Topic response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param slug: The topic's slug (used to identify it).
    :type  slug: str
    
    :param title: The topic's title.
    :type  title: str
    
    :param post_count: The amount of posts in the topic.
    :type  post_count: int
    
    :param view_count: The amount of views the topic has received.
    :type  view_count: int
    
    :param sticky: Whether the topic is sticky.
    :type  sticky: bool
    
    :param last_replied_to_at: The time, in UTC, when the last reply was made.
    :type  last_replied_to_at: datetime
    
    :param locked: Whether the topic is locked.
    :type  locked: bool
    
    :param user_id: The ID of the user who made the topic. `Null` if posted anonymously.
    :type  user_id: int
    
    :param author: The name of the user who made the topic.
    :type  author: str
    
    """

    
    """ The topic's slug (used to identify it). """
    slug: str
    
    """ The topic's title. """
    title: str
    
    """ The amount of posts in the topic. """
    post_count: int
    
    """ The amount of views the topic has received. """
    view_count: int
    
    """ Whether the topic is sticky. """
    sticky: bool
    
    """ The time, in UTC, when the last reply was made. """
    last_replied_to_at: datetime
    
    """ Whether the topic is locked. """
    locked: bool
    
    """ The ID of the user who made the topic. `Null` if posted anonymously. """
    user_id: int
    
    """ The name of the user who made the topic. """
    author: str
    
    def __init__(
        self, 
        slug: str,
        title: str,
        post_count: int,
        view_count: int,
        sticky: bool,
        last_replied_to_at: datetime,
        locked: bool,
        user_id: int,
        author: str,
    ):
        """
        A parsed Topic response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param slug: The topic's slug (used to identify it).
        :type  slug: str
        
        :param title: The topic's title.
        :type  title: str
        
        :param post_count: The amount of posts in the topic.
        :type  post_count: int
        
        :param view_count: The amount of views the topic has received.
        :type  view_count: int
        
        :param sticky: Whether the topic is sticky.
        :type  sticky: bool
        
        :param last_replied_to_at: The time, in UTC, when the last reply was made.
        :type  last_replied_to_at: datetime
        
        :param locked: Whether the topic is locked.
        :type  locked: bool
        
        :param user_id: The ID of the user who made the topic. `Null` if posted anonymously.
        :type  user_id: int
        
        :param author: The name of the user who made the topic.
        :type  author: str
        
        """
        self.slug = slug
        self.title = title
        self.post_count = post_count
        self.view_count = view_count
        self.sticky = sticky
        self.last_replied_to_at = last_replied_to_at
        self.locked = locked
        self.user_id = user_id
        self.author = author
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Topic], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Topic constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['slug'] = data['slug']
        arguments['title'] = data['title']
        arguments['post_count'] = data['post_count']
        arguments['view_count'] = data['view_count']
        arguments['sticky'] = data['sticky']
        arguments['last_replied_to_at'] = iso8601.parse_date(data['last_replied_to_at'])
        arguments['locked'] = data['locked']
        arguments['user_id'] = data['user_id']
        arguments['author'] = data['author']
        
        del data['slug']
        del data['title']
        del data['post_count']
        del data['view_count']
        del data['sticky']
        del data['last_replied_to_at']
        del data['locked']
        del data['user_id']
        del data['author']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Topic], data: Union[Dict, None, List[Dict]]) -> Union[Topic, None]:
        """
        Deserialize a new Topic from a given dictionary.

        :return: new Topic instance.
        :rtype: Topic|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Topic = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(topic_instance)`
        """
        return "{s.__class__.__name__}(slug={s.slug!r}, title={s.title!r}, post_count={s.post_count!r}, view_count={s.view_count!r}, sticky={s.sticky!r}, last_replied_to_at={s.last_replied_to_at!r}, locked={s.locked!r}, user_id={s.user_id!r}, author={s.author!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(topic_instance)`
        """
        
        return "{s.__class__.__name__}(slug={s.slug!r}, title={s.title!r}, post_count={s.post_count!r}, view_count={s.view_count!r}, sticky={s.sticky!r}, last_replied_to_at={s.last_replied_to_at!r}, locked={s.locked!r}, user_id={s.user_id!r}, author={s.author!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `topic_instance_a == topic_instance_b`
        """
        if not (hasattr(other, 'slug') and hasattr(other, 'title') and hasattr(other, 'post_count') and hasattr(other, 'view_count') and hasattr(other, 'sticky') and hasattr(other, 'last_replied_to_at') and hasattr(other, 'locked') and hasattr(other, 'user_id') and hasattr(other, 'author')):
            return False
        # end if
        return self.slug == other.slug and self.title == other.title and self.post_count == other.post_count and self.view_count == other.view_count and self.sticky == other.sticky and self.last_replied_to_at == other.last_replied_to_at and self.locked == other.locked and self.user_id == other.user_id and self.author == other.author
    # end __eq__
# end class


class Post(DerpiModel):
    """
    A parsed Post response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param author: The post's author.
    :type  author: str
    
    :param body: The post text.
    :type  body: str
    
    :param id: The post's ID (used to identify it).
    :type  id: int
    
    :param user_id: The ID of the user the comment belongs to, if any.
    :type  user_id: int
    
    :param avatar: The post's author's avatar. Normal URL or a base64 encoded inline svg with an appropriate header. Format like `data:image/svg+xml;base64,…`.
    :type  avatar: str
    
    :param created_at: The creation time, in UTC, of this post.
    :type  created_at: datetime
    
    :param edit_reason: Optional. The user provided reason for an edit, if given.
    :type  edit_reason: str|None
    
    :param edited_at: Optional. The edit time, in UTC, of this post. If it got edited.
    :type  edited_at: datetime|None
    
    :param updated_at: The time, in UTC, the post was last updated.
    :type  updated_at: datetime
    
    """

    
    """ The post's author. """
    author: str
    
    """ The post text. """
    body: str
    
    """ The post's ID (used to identify it). """
    id: int
    
    """ The ID of the user the comment belongs to, if any. """
    user_id: int
    
    """ The post's author's avatar. Normal URL or a base64 encoded inline svg with an appropriate header. Format like `data:image/svg+xml;base64,…`. """
    avatar: str
    
    """ The creation time, in UTC, of this post. """
    created_at: datetime
    
    """ Optional. The user provided reason for an edit, if given. """
    edit_reason: Union[str, None]
    
    """ Optional. The edit time, in UTC, of this post. If it got edited. """
    edited_at: Union[datetime, None]
    
    """ The time, in UTC, the post was last updated. """
    updated_at: datetime
    
    def __init__(
        self, 
        author: str,
        body: str,
        id: int,
        user_id: int,
        avatar: str,
        created_at: datetime,
        updated_at: datetime,
        edit_reason: Union[str, None] = None,
        edited_at: Union[datetime, None] = None,
    ):
        """
        A parsed Post response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param author: The post's author.
        :type  author: str
        
        :param body: The post text.
        :type  body: str
        
        :param id: The post's ID (used to identify it).
        :type  id: int
        
        :param user_id: The ID of the user the comment belongs to, if any.
        :type  user_id: int
        
        :param avatar: The post's author's avatar. Normal URL or a base64 encoded inline svg with an appropriate header. Format like `data:image/svg+xml;base64,…`.
        :type  avatar: str
        
        :param created_at: The creation time, in UTC, of this post.
        :type  created_at: datetime
        
        :param edit_reason: Optional. The user provided reason for an edit, if given.
        :type  edit_reason: str|None
        
        :param edited_at: Optional. The edit time, in UTC, of this post. If it got edited.
        :type  edited_at: datetime|None
        
        :param updated_at: The time, in UTC, the post was last updated.
        :type  updated_at: datetime
        
        """
        self.author = author
        self.body = body
        self.id = id
        self.user_id = user_id
        self.avatar = avatar
        self.created_at = created_at
        self.edit_reason = edit_reason
        self.edited_at = edited_at
        self.updated_at = updated_at
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Post], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Post constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['author'] = data['author']
        arguments['body'] = data['body']
        arguments['id'] = data['id']
        arguments['user_id'] = data['user_id']
        arguments['avatar'] = data['avatar']
        arguments['created_at'] = iso8601.parse_date(data['created_at'])
        arguments['edit_reason'] = data['edit_reason'] if data.get('edit_reason', None) is not None else None
        arguments['edited_at'] = iso8601.parse_date(data['edited_at']) if data.get('edited_at', None) is not None else None
        arguments['updated_at'] = iso8601.parse_date(data['updated_at'])
        
        del data['author']
        del data['body']
        del data['id']
        del data['user_id']
        del data['avatar']
        del data['created_at']
        if 'edit_reason' in data:
            del data['edit_reason']
        # end if
        if 'edited_at' in data:
            del data['edited_at']
        # end if
        del data['updated_at']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Post], data: Union[Dict, None, List[Dict]]) -> Union[Post, None]:
        """
        Deserialize a new Post from a given dictionary.

        :return: new Post instance.
        :rtype: Post|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Post = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(post_instance)`
        """
        return "{s.__class__.__name__}(author={s.author!r}, body={s.body!r}, id={s.id!r}, user_id={s.user_id!r}, avatar={s.avatar!r}, created_at={s.created_at!r}, edit_reason={s.edit_reason!r}, edited_at={s.edited_at!r}, updated_at={s.updated_at!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(post_instance)`
        """
        
        return "{s.__class__.__name__}(author={s.author!r}, body={s.body!r}, id={s.id!r}, user_id={s.user_id!r}, avatar={s.avatar!r}, created_at={s.created_at!r}, edit_reason={s.edit_reason!r}, edited_at={s.edited_at!r}, updated_at={s.updated_at!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `post_instance_a == post_instance_b`
        """
        if not (hasattr(other, 'author') and hasattr(other, 'body') and hasattr(other, 'id') and hasattr(other, 'user_id') and hasattr(other, 'avatar') and hasattr(other, 'created_at') and hasattr(other, 'edit_reason') and hasattr(other, 'edited_at') and hasattr(other, 'updated_at')):
            return False
        # end if
        return self.author == other.author and self.body == other.body and self.id == other.id and self.user_id == other.user_id and self.avatar == other.avatar and self.created_at == other.created_at and self.edit_reason == other.edit_reason and self.edited_at == other.edited_at and self.updated_at == other.updated_at
    # end __eq__
# end class


class Tag(DerpiModel):
    """
    A parsed Tag response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param aliased_tag: The slug of the tag this tag is aliased to, if any.
    :type  aliased_tag: str
    
    :param aliases: The slugs of the tags aliased to this tag.
    :type  aliases: list
    
    :param category: The category class of this tag. One of `"character", "content-fanmade", "content-official", "error", "oc", "origin", "rating", "species", "spoiler"`.
    :type  category: str
    
    :param description: The long description for the tag.
    :type  description: str
    
    :param dnp_entries: An array of objects containing DNP entries claimed on the tag.
    :type  dnp_entries: list
    
    :param id: The tag's ID.
    :type  id: int
    
    :param images: The image count of the tag.
    :type  images: int
    
    :param implied_by_tags: The slugs of the tags this tag is implied by.
    :type  implied_by_tags: list
    
    :param implied_tags: The slugs of the tags this tag implies.
    :type  implied_tags: list
    
    :param name: The name of the tag.
    :type  name: str
    
    :param name_in_namespace: The name of the tag in its namespace.
    :type  name_in_namespace: str
    
    :param namespace: The namespace of the tag.
    :type  namespace: str
    
    :param short_description: The short description for the tag.
    :type  short_description: str
    
    :param slug: The slug for the tag.
    :type  slug: str
    
    :param spoiler_image: Optional. The spoiler image URL for the tag.
    :type  spoiler_image: str|None
    
    :param spoiler_image_uri: Optional. The spoiler image URL for the tag.
    :type  spoiler_image_uri: str|None
    
    """

    
    """ The slug of the tag this tag is aliased to, if any. """
    aliased_tag: str
    
    """ The slugs of the tags aliased to this tag. """
    aliases: list
    
    """ The category class of this tag. One of `"character", "content-fanmade", "content-official", "error", "oc", "origin", "rating", "species", "spoiler"`. """
    category: str
    
    """ The long description for the tag. """
    description: str
    
    """ An array of objects containing DNP entries claimed on the tag. """
    dnp_entries: list
    
    """ The tag's ID. """
    id: int
    
    """ The image count of the tag. """
    images: int
    
    """ The slugs of the tags this tag is implied by. """
    implied_by_tags: list
    
    """ The slugs of the tags this tag implies. """
    implied_tags: list
    
    """ The name of the tag. """
    name: str
    
    """ The name of the tag in its namespace. """
    name_in_namespace: str
    
    """ The namespace of the tag. """
    namespace: str
    
    """ The short description for the tag. """
    short_description: str
    
    """ The slug for the tag. """
    slug: str
    
    """ Optional. The spoiler image URL for the tag. """
    spoiler_image: Union[str, None]
    
    """ Optional. The spoiler image URL for the tag. """
    spoiler_image_uri: Union[str, None]
    
    def __init__(
        self, 
        aliased_tag: str,
        aliases: list,
        category: str,
        description: str,
        dnp_entries: list,
        id: int,
        images: int,
        implied_by_tags: list,
        implied_tags: list,
        name: str,
        name_in_namespace: str,
        namespace: str,
        short_description: str,
        slug: str,
        spoiler_image: Union[str, None] = None,
        spoiler_image_uri: Union[str, None] = None,
    ):
        """
        A parsed Tag response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param aliased_tag: The slug of the tag this tag is aliased to, if any.
        :type  aliased_tag: str
        
        :param aliases: The slugs of the tags aliased to this tag.
        :type  aliases: list
        
        :param category: The category class of this tag. One of `"character", "content-fanmade", "content-official", "error", "oc", "origin", "rating", "species", "spoiler"`.
        :type  category: str
        
        :param description: The long description for the tag.
        :type  description: str
        
        :param dnp_entries: An array of objects containing DNP entries claimed on the tag.
        :type  dnp_entries: list
        
        :param id: The tag's ID.
        :type  id: int
        
        :param images: The image count of the tag.
        :type  images: int
        
        :param implied_by_tags: The slugs of the tags this tag is implied by.
        :type  implied_by_tags: list
        
        :param implied_tags: The slugs of the tags this tag implies.
        :type  implied_tags: list
        
        :param name: The name of the tag.
        :type  name: str
        
        :param name_in_namespace: The name of the tag in its namespace.
        :type  name_in_namespace: str
        
        :param namespace: The namespace of the tag.
        :type  namespace: str
        
        :param short_description: The short description for the tag.
        :type  short_description: str
        
        :param slug: The slug for the tag.
        :type  slug: str
        
        :param spoiler_image: Optional. The spoiler image URL for the tag.
        :type  spoiler_image: str|None
        
        :param spoiler_image_uri: Optional. The spoiler image URL for the tag.
        :type  spoiler_image_uri: str|None
        
        """
        self.aliased_tag = aliased_tag
        self.aliases = aliases
        self.category = category
        self.description = description
        self.dnp_entries = dnp_entries
        self.id = id
        self.images = images
        self.implied_by_tags = implied_by_tags
        self.implied_tags = implied_tags
        self.name = name
        self.name_in_namespace = name_in_namespace
        self.namespace = namespace
        self.short_description = short_description
        self.slug = slug
        self.spoiler_image = spoiler_image
        self.spoiler_image_uri = spoiler_image_uri
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Tag], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Tag constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['aliased_tag'] = data['aliased_tag']
        arguments['aliases'] = data['aliases']
        arguments['category'] = data['category']
        arguments['description'] = data['description']
        arguments['dnp_entries'] = data['dnp_entries']
        arguments['id'] = data['id']
        arguments['images'] = data['images']
        arguments['implied_by_tags'] = data['implied_by_tags']
        arguments['implied_tags'] = data['implied_tags']
        arguments['name'] = data['name']
        arguments['name_in_namespace'] = data['name_in_namespace']
        arguments['namespace'] = data['namespace']
        arguments['short_description'] = data['short_description']
        arguments['slug'] = data['slug']
        arguments['spoiler_image'] = data['spoiler_image'] if data.get('spoiler_image', None) is not None else None
        arguments['spoiler_image_uri'] = data['spoiler_image_uri'] if data.get('spoiler_image_uri', None) is not None else None
        
        del data['aliased_tag']
        del data['aliases']
        del data['category']
        del data['description']
        del data['dnp_entries']
        del data['id']
        del data['images']
        del data['implied_by_tags']
        del data['implied_tags']
        del data['name']
        del data['name_in_namespace']
        del data['namespace']
        del data['short_description']
        del data['slug']
        if 'spoiler_image' in data:
            del data['spoiler_image']
        # end if
        if 'spoiler_image_uri' in data:
            del data['spoiler_image_uri']
        # end if

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Tag], data: Union[Dict, None, List[Dict]]) -> Union[Tag, None]:
        """
        Deserialize a new Tag from a given dictionary.

        :return: new Tag instance.
        :rtype: Tag|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Tag = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(tag_instance)`
        """
        return "{s.__class__.__name__}(aliased_tag={s.aliased_tag!r}, aliases={s.aliases!r}, category={s.category!r}, description={s.description!r}, dnp_entries={s.dnp_entries!r}, id={s.id!r}, images={s.images!r}, implied_by_tags={s.implied_by_tags!r}, implied_tags={s.implied_tags!r}, name={s.name!r}, name_in_namespace={s.name_in_namespace!r}, namespace={s.namespace!r}, short_description={s.short_description!r}, slug={s.slug!r}, spoiler_image={s.spoiler_image!r}, spoiler_image_uri={s.spoiler_image_uri!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(tag_instance)`
        """
        
        return "{s.__class__.__name__}(aliased_tag={s.aliased_tag!r}, aliases={s.aliases!r}, category={s.category!r}, description={s.description!r}, dnp_entries={s.dnp_entries!r}, id={s.id!r}, images={s.images!r}, implied_by_tags={s.implied_by_tags!r}, implied_tags={s.implied_tags!r}, name={s.name!r}, name_in_namespace={s.name_in_namespace!r}, namespace={s.namespace!r}, short_description={s.short_description!r}, slug={s.slug!r}, spoiler_image={s.spoiler_image!r}, spoiler_image_uri={s.spoiler_image_uri!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `tag_instance_a == tag_instance_b`
        """
        if not (hasattr(other, 'aliased_tag') and hasattr(other, 'aliases') and hasattr(other, 'category') and hasattr(other, 'description') and hasattr(other, 'dnp_entries') and hasattr(other, 'id') and hasattr(other, 'images') and hasattr(other, 'implied_by_tags') and hasattr(other, 'implied_tags') and hasattr(other, 'name') and hasattr(other, 'name_in_namespace') and hasattr(other, 'namespace') and hasattr(other, 'short_description') and hasattr(other, 'slug') and hasattr(other, 'spoiler_image') and hasattr(other, 'spoiler_image_uri')):
            return False
        # end if
        return self.aliased_tag == other.aliased_tag and self.aliases == other.aliases and self.category == other.category and self.description == other.description and self.dnp_entries == other.dnp_entries and self.id == other.id and self.images == other.images and self.implied_by_tags == other.implied_by_tags and self.implied_tags == other.implied_tags and self.name == other.name and self.name_in_namespace == other.name_in_namespace and self.namespace == other.namespace and self.short_description == other.short_description and self.slug == other.slug and self.spoiler_image == other.spoiler_image and self.spoiler_image_uri == other.spoiler_image_uri
    # end __eq__
# end class


class User(DerpiModel):
    """
    A parsed User response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param id: The ID of the user.
    :type  id: int
    
    :param name: The name of the user.
    :type  name: str
    
    :param slug: The slug of the user.
    :type  slug: str
    
    :param role: The role of the user.
    :type  role: str
    
    :param description: The description (bio) of the user.
    :type  description: str
    
    :param avatar_url: The URL of the user's thumbnail. `Null` if they haven't set one.
    :type  avatar_url: str
    
    :param created_at: The creation time, in UTC, of the user.
    :type  created_at: datetime
    
    :param comments_count: The comment count of the user.
    :type  comments_count: int
    
    :param uploads_count: The upload count of the user.
    :type  uploads_count: int
    
    :param posts_count: The forum posts count of the user.
    :type  posts_count: int
    
    :param topics_count: The forum topics count of the user.
    :type  topics_count: int
    
    :param links: `Links`.
    :type  links: Links
    
    :param awards: `Awards`.
    :type  awards: Awards
    
    """

    
    """ The ID of the user. """
    id: int
    
    """ The name of the user. """
    name: str
    
    """ The slug of the user. """
    slug: str
    
    """ The role of the user. """
    role: str
    
    """ The description (bio) of the user. """
    description: str
    
    """ The URL of the user's thumbnail. `Null` if they haven't set one. """
    avatar_url: str
    
    """ The creation time, in UTC, of the user. """
    created_at: datetime
    
    """ The comment count of the user. """
    comments_count: int
    
    """ The upload count of the user. """
    uploads_count: int
    
    """ The forum posts count of the user. """
    posts_count: int
    
    """ The forum topics count of the user. """
    topics_count: int
    
    """ `Links`. """
    links: Links
    
    """ `Awards`. """
    awards: Awards
    
    def __init__(
        self, 
        id: int,
        name: str,
        slug: str,
        role: str,
        description: str,
        avatar_url: str,
        created_at: datetime,
        comments_count: int,
        uploads_count: int,
        posts_count: int,
        topics_count: int,
        links: Links,
        awards: Awards,
    ):
        """
        A parsed User response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param id: The ID of the user.
        :type  id: int
        
        :param name: The name of the user.
        :type  name: str
        
        :param slug: The slug of the user.
        :type  slug: str
        
        :param role: The role of the user.
        :type  role: str
        
        :param description: The description (bio) of the user.
        :type  description: str
        
        :param avatar_url: The URL of the user's thumbnail. `Null` if they haven't set one.
        :type  avatar_url: str
        
        :param created_at: The creation time, in UTC, of the user.
        :type  created_at: datetime
        
        :param comments_count: The comment count of the user.
        :type  comments_count: int
        
        :param uploads_count: The upload count of the user.
        :type  uploads_count: int
        
        :param posts_count: The forum posts count of the user.
        :type  posts_count: int
        
        :param topics_count: The forum topics count of the user.
        :type  topics_count: int
        
        :param links: `Links`.
        :type  links: Links
        
        :param awards: `Awards`.
        :type  awards: Awards
        
        """
        self.id = id
        self.name = name
        self.slug = slug
        self.role = role
        self.description = description
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.comments_count = comments_count
        self.uploads_count = uploads_count
        self.posts_count = posts_count
        self.topics_count = topics_count
        self.links = links
        self.awards = awards
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[User], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the User constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['id'] = data['id']
        arguments['name'] = data['name']
        arguments['slug'] = data['slug']
        arguments['role'] = data['role']
        arguments['description'] = data['description']
        arguments['avatar_url'] = data['avatar_url']
        arguments['created_at'] = iso8601.parse_date(data['created_at'])
        arguments['comments_count'] = data['comments_count']
        arguments['uploads_count'] = data['uploads_count']
        arguments['posts_count'] = data['posts_count']
        arguments['topics_count'] = data['topics_count']
        arguments['links'] = Links.from_dict(data['links'])
        arguments['awards'] = Awards.from_dict(data['awards'])
        
        del data['id']
        del data['name']
        del data['slug']
        del data['role']
        del data['description']
        del data['avatar_url']
        del data['created_at']
        del data['comments_count']
        del data['uploads_count']
        del data['posts_count']
        del data['topics_count']
        del data['links']
        del data['awards']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[User], data: Union[Dict, None, List[Dict]]) -> Union[User, None]:
        """
        Deserialize a new User from a given dictionary.

        :return: new User instance.
        :rtype: User|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: User = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(user_instance)`
        """
        return "{s.__class__.__name__}(id={s.id!r}, name={s.name!r}, slug={s.slug!r}, role={s.role!r}, description={s.description!r}, avatar_url={s.avatar_url!r}, created_at={s.created_at!r}, comments_count={s.comments_count!r}, uploads_count={s.uploads_count!r}, posts_count={s.posts_count!r}, topics_count={s.topics_count!r}, links={s.links!r}, awards={s.awards!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(user_instance)`
        """
        
        return "{s.__class__.__name__}(id={s.id!r}, name={s.name!r}, slug={s.slug!r}, role={s.role!r}, description={s.description!r}, avatar_url={s.avatar_url!r}, created_at={s.created_at!r}, comments_count={s.comments_count!r}, uploads_count={s.uploads_count!r}, posts_count={s.posts_count!r}, topics_count={s.topics_count!r}, links={s.links!r}, awards={s.awards!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `user_instance_a == user_instance_b`
        """
        if not (hasattr(other, 'id') and hasattr(other, 'name') and hasattr(other, 'slug') and hasattr(other, 'role') and hasattr(other, 'description') and hasattr(other, 'avatar_url') and hasattr(other, 'created_at') and hasattr(other, 'comments_count') and hasattr(other, 'uploads_count') and hasattr(other, 'posts_count') and hasattr(other, 'topics_count') and hasattr(other, 'links') and hasattr(other, 'awards')):
            return False
        # end if
        return self.id == other.id and self.name == other.name and self.slug == other.slug and self.role == other.role and self.description == other.description and self.avatar_url == other.avatar_url and self.created_at == other.created_at and self.comments_count == other.comments_count and self.uploads_count == other.uploads_count and self.posts_count == other.posts_count and self.topics_count == other.topics_count and self.links == other.links and self.awards == other.awards
    # end __eq__
# end class


class Filter(DerpiModel):
    """
    A parsed Filter response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param id: The id of the filter.
    :type  id: int
    
    :param name: The name of the filter.
    :type  name: str
    
    :param description: The description of the filter.
    :type  description: str
    
    :param user_id: The id of the user the filter belongs to. `Null` if it isn't assigned to a user (usually `system` filters only).
    :type  user_id: int
    
    :param user_count: The amount of users employing this filter.
    :type  user_count: int
    
    :param system: If `true`, is a system filter. System filters are usable by anyone and don't have a `user_id` set.
    :type  system: bool
    
    :param public: If `true`, is a public filter. Public filters are usable by anyone.
    :type  public: bool
    
    :param spoilered_tag_ids: A list of tag IDs (as integers) that this filter will spoil.
    :type  spoilered_tag_ids: list
    
    :param spoilered_complex: The complex spoiled filter.
    :type  spoilered_complex: str
    
    :param hidden_tag_ids: A list of tag IDs (as integers) that this filter will hide.
    :type  hidden_tag_ids: list
    
    :param hidden_complex: The complex hidden filter.
    :type  hidden_complex: str
    
    """

    
    """ The id of the filter. """
    id: int
    
    """ The name of the filter. """
    name: str
    
    """ The description of the filter. """
    description: str
    
    """ The id of the user the filter belongs to. `Null` if it isn't assigned to a user (usually `system` filters only). """
    user_id: int
    
    """ The amount of users employing this filter. """
    user_count: int
    
    """ If `true`, is a system filter. System filters are usable by anyone and don't have a `user_id` set. """
    system: bool
    
    """ If `true`, is a public filter. Public filters are usable by anyone. """
    public: bool
    
    """ A list of tag IDs (as integers) that this filter will spoil. """
    spoilered_tag_ids: list
    
    """ The complex spoiled filter. """
    spoilered_complex: str
    
    """ A list of tag IDs (as integers) that this filter will hide. """
    hidden_tag_ids: list
    
    """ The complex hidden filter. """
    hidden_complex: str
    
    def __init__(
        self, 
        id: int,
        name: str,
        description: str,
        user_id: int,
        user_count: int,
        system: bool,
        public: bool,
        spoilered_tag_ids: list,
        spoilered_complex: str,
        hidden_tag_ids: list,
        hidden_complex: str,
    ):
        """
        A parsed Filter response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param id: The id of the filter.
        :type  id: int
        
        :param name: The name of the filter.
        :type  name: str
        
        :param description: The description of the filter.
        :type  description: str
        
        :param user_id: The id of the user the filter belongs to. `Null` if it isn't assigned to a user (usually `system` filters only).
        :type  user_id: int
        
        :param user_count: The amount of users employing this filter.
        :type  user_count: int
        
        :param system: If `true`, is a system filter. System filters are usable by anyone and don't have a `user_id` set.
        :type  system: bool
        
        :param public: If `true`, is a public filter. Public filters are usable by anyone.
        :type  public: bool
        
        :param spoilered_tag_ids: A list of tag IDs (as integers) that this filter will spoil.
        :type  spoilered_tag_ids: list
        
        :param spoilered_complex: The complex spoiled filter.
        :type  spoilered_complex: str
        
        :param hidden_tag_ids: A list of tag IDs (as integers) that this filter will hide.
        :type  hidden_tag_ids: list
        
        :param hidden_complex: The complex hidden filter.
        :type  hidden_complex: str
        
        """
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.user_count = user_count
        self.system = system
        self.public = public
        self.spoilered_tag_ids = spoilered_tag_ids
        self.spoilered_complex = spoilered_complex
        self.hidden_tag_ids = hidden_tag_ids
        self.hidden_complex = hidden_complex
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Filter], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Filter constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['id'] = data['id']
        arguments['name'] = data['name']
        arguments['description'] = data['description']
        arguments['user_id'] = data['user_id']
        arguments['user_count'] = data['user_count']
        arguments['system'] = data['system']
        arguments['public'] = data['public']
        arguments['spoilered_tag_ids'] = data['spoilered_tag_ids']
        arguments['spoilered_complex'] = data['spoilered_complex']
        arguments['hidden_tag_ids'] = data['hidden_tag_ids']
        arguments['hidden_complex'] = data['hidden_complex']
        
        del data['id']
        del data['name']
        del data['description']
        del data['user_id']
        del data['user_count']
        del data['system']
        del data['public']
        del data['spoilered_tag_ids']
        del data['spoilered_complex']
        del data['hidden_tag_ids']
        del data['hidden_complex']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Filter], data: Union[Dict, None, List[Dict]]) -> Union[Filter, None]:
        """
        Deserialize a new Filter from a given dictionary.

        :return: new Filter instance.
        :rtype: Filter|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Filter = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(filter_instance)`
        """
        return "{s.__class__.__name__}(id={s.id!r}, name={s.name!r}, description={s.description!r}, user_id={s.user_id!r}, user_count={s.user_count!r}, system={s.system!r}, public={s.public!r}, spoilered_tag_ids={s.spoilered_tag_ids!r}, spoilered_complex={s.spoilered_complex!r}, hidden_tag_ids={s.hidden_tag_ids!r}, hidden_complex={s.hidden_complex!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(filter_instance)`
        """
        
        return "{s.__class__.__name__}(id={s.id!r}, name={s.name!r}, description={s.description!r}, user_id={s.user_id!r}, user_count={s.user_count!r}, system={s.system!r}, public={s.public!r}, spoilered_tag_ids={s.spoilered_tag_ids!r}, spoilered_complex={s.spoilered_complex!r}, hidden_tag_ids={s.hidden_tag_ids!r}, hidden_complex={s.hidden_complex!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `filter_instance_a == filter_instance_b`
        """
        if not (hasattr(other, 'id') and hasattr(other, 'name') and hasattr(other, 'description') and hasattr(other, 'user_id') and hasattr(other, 'user_count') and hasattr(other, 'system') and hasattr(other, 'public') and hasattr(other, 'spoilered_tag_ids') and hasattr(other, 'spoilered_complex') and hasattr(other, 'hidden_tag_ids') and hasattr(other, 'hidden_complex')):
            return False
        # end if
        return self.id == other.id and self.name == other.name and self.description == other.description and self.user_id == other.user_id and self.user_count == other.user_count and self.system == other.system and self.public == other.public and self.spoilered_tag_ids == other.spoilered_tag_ids and self.spoilered_complex == other.spoilered_complex and self.hidden_tag_ids == other.hidden_tag_ids and self.hidden_complex == other.hidden_complex
    # end __eq__
# end class


class Links(DerpiModel):
    """
    A parsed Links response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param user_id: The ID of the user who owns this link.
    :type  user_id: int
    
    :param created_at: The creation time, in UTC, of this link.
    :type  created_at: datetime
    
    :param state: The state of this link.
    :type  state: str
    
    :param tag_id: The ID of an associated tag for this link. `Null` if no tag linked.
    :type  tag_id: int
    
    """

    
    """ The ID of the user who owns this link. """
    user_id: int
    
    """ The creation time, in UTC, of this link. """
    created_at: datetime
    
    """ The state of this link. """
    state: str
    
    """ The ID of an associated tag for this link. `Null` if no tag linked. """
    tag_id: int
    
    def __init__(
        self, 
        user_id: int,
        created_at: datetime,
        state: str,
        tag_id: int,
    ):
        """
        A parsed Links response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param user_id: The ID of the user who owns this link.
        :type  user_id: int
        
        :param created_at: The creation time, in UTC, of this link.
        :type  created_at: datetime
        
        :param state: The state of this link.
        :type  state: str
        
        :param tag_id: The ID of an associated tag for this link. `Null` if no tag linked.
        :type  tag_id: int
        
        """
        self.user_id = user_id
        self.created_at = created_at
        self.state = state
        self.tag_id = tag_id
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Links], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Links constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['user_id'] = data['user_id']
        arguments['created_at'] = iso8601.parse_date(data['created_at'])
        arguments['state'] = data['state']
        arguments['tag_id'] = data['tag_id']
        
        del data['user_id']
        del data['created_at']
        del data['state']
        del data['tag_id']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Links], data: Union[Dict, None, List[Dict]]) -> Union[Links, None]:
        """
        Deserialize a new Links from a given dictionary.

        :return: new Links instance.
        :rtype: Links|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Links = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(links_instance)`
        """
        return "{s.__class__.__name__}(user_id={s.user_id!r}, created_at={s.created_at!r}, state={s.state!r}, tag_id={s.tag_id!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(links_instance)`
        """
        
        return "{s.__class__.__name__}(user_id={s.user_id!r}, created_at={s.created_at!r}, state={s.state!r}, tag_id={s.tag_id!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `links_instance_a == links_instance_b`
        """
        if not (hasattr(other, 'user_id') and hasattr(other, 'created_at') and hasattr(other, 'state') and hasattr(other, 'tag_id')):
            return False
        # end if
        return self.user_id == other.user_id and self.created_at == other.created_at and self.state == other.state and self.tag_id == other.tag_id
    # end __eq__
# end class


class Awards(DerpiModel):
    """
    A parsed Awards response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param image_url: The URL of this award.
    :type  image_url: str
    
    :param title: The title of this award.
    :type  title: str
    
    :param id: The ID of the badge this award is derived from.
    :type  id: int
    
    :param label: The label of this award.
    :type  label: str
    
    :param awarded_on: The time, in UTC, when this award was given.
    :type  awarded_on: datetime
    
    """

    
    """ The URL of this award. """
    image_url: str
    
    """ The title of this award. """
    title: str
    
    """ The ID of the badge this award is derived from. """
    id: int
    
    """ The label of this award. """
    label: str
    
    """ The time, in UTC, when this award was given. """
    awarded_on: datetime
    
    def __init__(
        self, 
        image_url: str,
        title: str,
        id: int,
        label: str,
        awarded_on: datetime,
    ):
        """
        A parsed Awards response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param image_url: The URL of this award.
        :type  image_url: str
        
        :param title: The title of this award.
        :type  title: str
        
        :param id: The ID of the badge this award is derived from.
        :type  id: int
        
        :param label: The label of this award.
        :type  label: str
        
        :param awarded_on: The time, in UTC, when this award was given.
        :type  awarded_on: datetime
        
        """
        self.image_url = image_url
        self.title = title
        self.id = id
        self.label = label
        self.awarded_on = awarded_on
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Awards], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Awards constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['image_url'] = data['image_url']
        arguments['title'] = data['title']
        arguments['id'] = data['id']
        arguments['label'] = data['label']
        arguments['awarded_on'] = iso8601.parse_date(data['awarded_on'])
        
        del data['image_url']
        del data['title']
        del data['id']
        del data['label']
        del data['awarded_on']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Awards], data: Union[Dict, None, List[Dict]]) -> Union[Awards, None]:
        """
        Deserialize a new Awards from a given dictionary.

        :return: new Awards instance.
        :rtype: Awards|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Awards = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(awards_instance)`
        """
        return "{s.__class__.__name__}(image_url={s.image_url!r}, title={s.title!r}, id={s.id!r}, label={s.label!r}, awarded_on={s.awarded_on!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(awards_instance)`
        """
        
        return "{s.__class__.__name__}(image_url={s.image_url!r}, title={s.title!r}, id={s.id!r}, label={s.label!r}, awarded_on={s.awarded_on!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `awards_instance_a == awards_instance_b`
        """
        if not (hasattr(other, 'image_url') and hasattr(other, 'title') and hasattr(other, 'id') and hasattr(other, 'label') and hasattr(other, 'awarded_on')):
            return False
        # end if
        return self.image_url == other.image_url and self.title == other.title and self.id == other.id and self.label == other.label and self.awarded_on == other.awarded_on
    # end __eq__
# end class


class Gallery(DerpiModel):
    """
    A parsed Gallery response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param description: The gallery's description.
    :type  description: str
    
    :param id: The gallery's ID.
    :type  id: int
    
    :param spoiler_warning: The gallery's spoiler warning.
    :type  spoiler_warning: str
    
    :param thumbnail_id: The ID of the cover image for the gallery.
    :type  thumbnail_id: int
    
    :param title: The gallery's title.
    :type  title: str
    
    :param user: The name of the gallery's creator.
    :type  user: str
    
    :param user_id: The ID of the gallery's creator.
    :type  user_id: int
    
    """

    
    """ The gallery's description. """
    description: str
    
    """ The gallery's ID. """
    id: int
    
    """ The gallery's spoiler warning. """
    spoiler_warning: str
    
    """ The ID of the cover image for the gallery. """
    thumbnail_id: int
    
    """ The gallery's title. """
    title: str
    
    """ The name of the gallery's creator. """
    user: str
    
    """ The ID of the gallery's creator. """
    user_id: int
    
    def __init__(
        self, 
        description: str,
        id: int,
        spoiler_warning: str,
        thumbnail_id: int,
        title: str,
        user: str,
        user_id: int,
    ):
        """
        A parsed Gallery response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param description: The gallery's description.
        :type  description: str
        
        :param id: The gallery's ID.
        :type  id: int
        
        :param spoiler_warning: The gallery's spoiler warning.
        :type  spoiler_warning: str
        
        :param thumbnail_id: The ID of the cover image for the gallery.
        :type  thumbnail_id: int
        
        :param title: The gallery's title.
        :type  title: str
        
        :param user: The name of the gallery's creator.
        :type  user: str
        
        :param user_id: The ID of the gallery's creator.
        :type  user_id: int
        
        """
        self.description = description
        self.id = id
        self.spoiler_warning = spoiler_warning
        self.thumbnail_id = thumbnail_id
        self.title = title
        self.user = user
        self.user_id = user_id
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Gallery], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Gallery constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['description'] = data['description']
        arguments['id'] = data['id']
        arguments['spoiler_warning'] = data['spoiler_warning']
        arguments['thumbnail_id'] = data['thumbnail_id']
        arguments['title'] = data['title']
        arguments['user'] = data['user']
        arguments['user_id'] = data['user_id']
        
        del data['description']
        del data['id']
        del data['spoiler_warning']
        del data['thumbnail_id']
        del data['title']
        del data['user']
        del data['user_id']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Gallery], data: Union[Dict, None, List[Dict]]) -> Union[Gallery, None]:
        """
        Deserialize a new Gallery from a given dictionary.

        :return: new Gallery instance.
        :rtype: Gallery|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Gallery = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(gallery_instance)`
        """
        return "{s.__class__.__name__}(description={s.description!r}, id={s.id!r}, spoiler_warning={s.spoiler_warning!r}, thumbnail_id={s.thumbnail_id!r}, title={s.title!r}, user={s.user!r}, user_id={s.user_id!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(gallery_instance)`
        """
        
        return "{s.__class__.__name__}(description={s.description!r}, id={s.id!r}, spoiler_warning={s.spoiler_warning!r}, thumbnail_id={s.thumbnail_id!r}, title={s.title!r}, user={s.user!r}, user_id={s.user_id!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `gallery_instance_a == gallery_instance_b`
        """
        if not (hasattr(other, 'description') and hasattr(other, 'id') and hasattr(other, 'spoiler_warning') and hasattr(other, 'thumbnail_id') and hasattr(other, 'title') and hasattr(other, 'user') and hasattr(other, 'user_id')):
            return False
        # end if
        return self.description == other.description and self.id == other.id and self.spoiler_warning == other.spoiler_warning and self.thumbnail_id == other.thumbnail_id and self.title == other.title and self.user == other.user and self.user_id == other.user_id
    # end __eq__
# end class


class Oembed(DerpiModel):
    """
    A parsed Oembed response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param author_name: The comma-delimited names of the image authors.
    :type  author_name: str
    
    :param author_url: The source URL of the image.
    :type  author_url: str
    
    :param cache_age: Always `7200`.
    :type  cache_age: int
    
    :param derpibooru_comments: The number of comments made on the image.
    :type  derpibooru_comments: int
    
    :param derpibooru_id: The image's ID.
    :type  derpibooru_id: int
    
    :param derpibooru_score: The image's number of upvotes minus the image's number of downvotes.
    :type  derpibooru_score: int
    
    :param derpibooru_tags: The names of the image's tags.
    :type  derpibooru_tags: list
    
    :param provider_name: Always `"Derpibooru"`.
    :type  provider_name: str
    
    :param provider_url: Always `"https://derpibooru.org"`.
    :type  provider_url: str
    
    :param title: The image's ID and associated tags, as would be given on the title of the image page.
    :type  title: str
    
    :param type: Always `"photo"`.
    :type  type: str
    
    :param version: Always `"1.0"`.
    :type  version: str
    
    """

    
    """ The comma-delimited names of the image authors. """
    author_name: str
    
    """ The source URL of the image. """
    author_url: str
    
    """ Always `7200`. """
    cache_age: int
    
    """ The number of comments made on the image. """
    derpibooru_comments: int
    
    """ The image's ID. """
    derpibooru_id: int
    
    """ The image's number of upvotes minus the image's number of downvotes. """
    derpibooru_score: int
    
    """ The names of the image's tags. """
    derpibooru_tags: list
    
    """ Always `"Derpibooru"`. """
    provider_name: str
    
    """ Always `"https://derpibooru.org"`. """
    provider_url: str
    
    """ The image's ID and associated tags, as would be given on the title of the image page. """
    title: str
    
    """ Always `"photo"`. """
    type: str
    
    """ Always `"1.0"`. """
    version: str
    
    def __init__(
        self, 
        author_name: str,
        author_url: str,
        cache_age: int,
        derpibooru_comments: int,
        derpibooru_id: int,
        derpibooru_score: int,
        derpibooru_tags: list,
        provider_name: str,
        provider_url: str,
        title: str,
        type: str,
        version: str,
    ):
        """
        A parsed Oembed response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param author_name: The comma-delimited names of the image authors.
        :type  author_name: str
        
        :param author_url: The source URL of the image.
        :type  author_url: str
        
        :param cache_age: Always `7200`.
        :type  cache_age: int
        
        :param derpibooru_comments: The number of comments made on the image.
        :type  derpibooru_comments: int
        
        :param derpibooru_id: The image's ID.
        :type  derpibooru_id: int
        
        :param derpibooru_score: The image's number of upvotes minus the image's number of downvotes.
        :type  derpibooru_score: int
        
        :param derpibooru_tags: The names of the image's tags.
        :type  derpibooru_tags: list
        
        :param provider_name: Always `"Derpibooru"`.
        :type  provider_name: str
        
        :param provider_url: Always `"https://derpibooru.org"`.
        :type  provider_url: str
        
        :param title: The image's ID and associated tags, as would be given on the title of the image page.
        :type  title: str
        
        :param type: Always `"photo"`.
        :type  type: str
        
        :param version: Always `"1.0"`.
        :type  version: str
        
        """
        self.author_name = author_name
        self.author_url = author_url
        self.cache_age = cache_age
        self.derpibooru_comments = derpibooru_comments
        self.derpibooru_id = derpibooru_id
        self.derpibooru_score = derpibooru_score
        self.derpibooru_tags = derpibooru_tags
        self.provider_name = provider_name
        self.provider_url = provider_url
        self.title = title
        self.type = type
        self.version = version
    # end def __init__

    @classmethod
    def prepare_dict(cls: Type[Oembed], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        """
        Builds a new dict with valid values for the Oembed constructor.

        :return: new dict with valid values
        :rtype: dict
        """
        assert_type_or_raise(data, dict, parameter_name="data")

        arguments = super().prepare_dict(data) 
        arguments['author_name'] = data['author_name']
        arguments['author_url'] = data['author_url']
        arguments['cache_age'] = data['cache_age']
        arguments['derpibooru_comments'] = data['derpibooru_comments']
        arguments['derpibooru_id'] = data['derpibooru_id']
        arguments['derpibooru_score'] = data['derpibooru_score']
        arguments['derpibooru_tags'] = data['derpibooru_tags']
        arguments['provider_name'] = data['provider_name']
        arguments['provider_url'] = data['provider_url']
        arguments['title'] = data['title']
        arguments['type'] = data['type']
        arguments['version'] = data['version']
        
        del data['author_name']
        del data['author_url']
        del data['cache_age']
        del data['derpibooru_comments']
        del data['derpibooru_id']
        del data['derpibooru_score']
        del data['derpibooru_tags']
        del data['provider_name']
        del data['provider_url']
        del data['title']
        del data['type']
        del data['version']

        if data:
            logger.warning(f'still got leftover data: {data!r}')
            if cls._assert_consuming_all_params:
                raise ValueError(
                    f'the dict should be consumed completely, but still has the following elements left: {list(data.keys())!r}'
                )
            # end if
        # end if
        return arguments
    # end def prepare_dict

    @classmethod
    def from_dict(cls: Type[Oembed], data: Union[Dict, None, List[Dict]]) -> Union[Oembed, None]:
        """
        Deserialize a new Oembed from a given dictionary.

        :return: new Oembed instance.
        :rtype: Oembed|None
        """
        if not data:  # None or {}
            return None
        # end if
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        # end if

        data: Dict = cls.prepare_dict(data)
        instance: Oembed = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(oembed_instance)`
        """
        return "{s.__class__.__name__}(author_name={s.author_name!r}, author_url={s.author_url!r}, cache_age={s.cache_age!r}, derpibooru_comments={s.derpibooru_comments!r}, derpibooru_id={s.derpibooru_id!r}, derpibooru_score={s.derpibooru_score!r}, derpibooru_tags={s.derpibooru_tags!r}, provider_name={s.provider_name!r}, provider_url={s.provider_url!r}, title={s.title!r}, type={s.type!r}, version={s.version!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(oembed_instance)`
        """
        
        return "{s.__class__.__name__}(author_name={s.author_name!r}, author_url={s.author_url!r}, cache_age={s.cache_age!r}, derpibooru_comments={s.derpibooru_comments!r}, derpibooru_id={s.derpibooru_id!r}, derpibooru_score={s.derpibooru_score!r}, derpibooru_tags={s.derpibooru_tags!r}, provider_name={s.provider_name!r}, provider_url={s.provider_url!r}, title={s.title!r}, type={s.type!r}, version={s.version!r})".format(s=self)
    # end def __repr__

    def __eq__(self, other):
        """
        Implements equality check, i.e. `oembed_instance_a == oembed_instance_b`
        """
        if not (hasattr(other, 'author_name') and hasattr(other, 'author_url') and hasattr(other, 'cache_age') and hasattr(other, 'derpibooru_comments') and hasattr(other, 'derpibooru_id') and hasattr(other, 'derpibooru_score') and hasattr(other, 'derpibooru_tags') and hasattr(other, 'provider_name') and hasattr(other, 'provider_url') and hasattr(other, 'title') and hasattr(other, 'type') and hasattr(other, 'version')):
            return False
        # end if
        return self.author_name == other.author_name and self.author_url == other.author_url and self.cache_age == other.cache_age and self.derpibooru_comments == other.derpibooru_comments and self.derpibooru_id == other.derpibooru_id and self.derpibooru_score == other.derpibooru_score and self.derpibooru_tags == other.derpibooru_tags and self.provider_name == other.provider_name and self.provider_url == other.provider_url and self.title == other.title and self.type == other.type and self.version == other.version
    # end __eq__
# end class

