#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime
from typing import Union, List, Dict, Type

from luckydonaldUtils.logger import logging
from luckydonaldUtils.typing import JSONType

__author__ = 'luckydonald'
__all__ = ['DerpiModel', 'Intensities', 'Representations', 'Image', 'Comment', 'Forum', 'Topic', 'Post', 'Tag', 'User', 'Filter', 'Links', 'Awards', 'Gallery', 'Oembed']

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if





class DerpiModel(object):
    """ Base class for all models """
    pass
# end class DerpiModel




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
    def validate_dict(cls: Type[Intensities], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Intensities], data: Union[Dict, None]) -> Union[Intensities, None]:
        """
        Deserialize a new Intensities from a given dictionary.

        :return: new Intensities instance.
        :rtype: Intensities|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(ne={s.ne!r}, nw={s.nw!r}, se={s.se!r}, sw={s.sw!r})".format(s=self)
    # end def __repr__
# end class



class Representations(DerpiModel):
    """
    A parsed Representations response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param full: A mapping of the 'full' representation names to their respective URLs.
    :type  full: str
    
    :param large: A mapping of the 'large' representation names to their respective URLs.
    :type  large: str
    
    :param medium: A mapping of the 'medium' representation names to their respective URLs.
    :type  medium: str
    
    :param small: A mapping of the 'small' representation names to their respective URLs.
    :type  small: str
    
    :param tall: A mapping of the 'tall' representation names to their respective URLs.
    :type  tall: str
    
    :param thumb: A mapping of the 'thumb' representation names to their respective URLs.
    :type  thumb: str
    
    :param thumb_small: A mapping of the 'thumb_small' representation names to their respective URLs.
    :type  thumb_small: str
    
    :param thumb_tiny: A mapping of the 'thumb_tiny' representation names to their respective URLs.
    :type  thumb_tiny: str
    
    """

    
    """ A mapping of the 'full' representation names to their respective URLs. """
    full: str
    
    """ A mapping of the 'large' representation names to their respective URLs. """
    large: str
    
    """ A mapping of the 'medium' representation names to their respective URLs. """
    medium: str
    
    """ A mapping of the 'small' representation names to their respective URLs. """
    small: str
    
    """ A mapping of the 'tall' representation names to their respective URLs. """
    tall: str
    
    """ A mapping of the 'thumb' representation names to their respective URLs. """
    thumb: str
    
    """ A mapping of the 'thumb_small' representation names to their respective URLs. """
    thumb_small: str
    
    """ A mapping of the 'thumb_tiny' representation names to their respective URLs. """
    thumb_tiny: str
    

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
    ):
        """
        A parsed Representations response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param full: A mapping of the 'full' representation names to their respective URLs.
        :type  full: str
        
        :param large: A mapping of the 'large' representation names to their respective URLs.
        :type  large: str
        
        :param medium: A mapping of the 'medium' representation names to their respective URLs.
        :type  medium: str
        
        :param small: A mapping of the 'small' representation names to their respective URLs.
        :type  small: str
        
        :param tall: A mapping of the 'tall' representation names to their respective URLs.
        :type  tall: str
        
        :param thumb: A mapping of the 'thumb' representation names to their respective URLs.
        :type  thumb: str
        
        :param thumb_small: A mapping of the 'thumb_small' representation names to their respective URLs.
        :type  thumb_small: str
        
        :param thumb_tiny: A mapping of the 'thumb_tiny' representation names to their respective URLs.
        :type  thumb_tiny: str
        
        """
        self.full = full
        self.large = large
        self.medium = medium
        self.small = small
        self.tall = tall
        self.thumb = thumb
        self.thumb_small = thumb_small
        self.thumb_tiny = thumb_tiny
    # end def __init__

    @classmethod
    def validate_dict(cls: Type[Representations], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Representations], data: Union[Dict, None]) -> Union[Representations, None]:
        """
        Deserialize a new Representations from a given dictionary.

        :return: new Representations instance.
        :rtype: Representations|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
        instance: Representations = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(representations_instance)`
        """
        return "{s.__class__.__name__}(full={s.full!r}, large={s.large!r}, medium={s.medium!r}, small={s.small!r}, tall={s.tall!r}, thumb={s.thumb!r}, thumb_small={s.thumb_small!r}, thumb_tiny={s.thumb_tiny!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(representations_instance)`
        """
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(full={s.full!r}, large={s.large!r}, medium={s.medium!r}, small={s.small!r}, tall={s.tall!r}, thumb={s.thumb!r}, thumb_small={s.thumb_small!r}, thumb_tiny={s.thumb_tiny!r})".format(s=self)
    # end def __repr__
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
    
    :param deletion_reason: The hide reason for the image, or null if none provided. This will only have a value on images which are deleted for a rule violation.
    :type  deletion_reason: str
    
    :param description: The image's description.
    :type  description: str
    
    :param downvotes: The number of downvotes the image has.
    :type  downvotes: int
    
    :param duplicate_of: The ID of the target image, or null if none provided. This will only have a value on images which are merged into another image.
    :type  duplicate_of: int
    
    :param faves: The number of faves the image has.
    :type  faves: int
    
    :param first_seen_at: The time, in UTC, this image was first seen (before any duplicate merging).
    :type  first_seen_at: datetime
    
    :param format: The file extension of this image. One of "gif", "jpg", "jpeg", "png", "svg", "webm".
    :type  format: str
    
    :param height: The image's height, in pixels.
    :type  height: int
    
    :param hidden_from_users: Whether this image is hidden. An image is hidden if it is merged or deleted for a rule violation.
    :type  hidden_from_users: bool
    
    :param id: The image's ID.
    :type  id: int
    
    :param intensities: Optional object of internal image intensity data for deduplication purposes. May be null if intensities have not yet been generated.
    :type  intensities: Intensities
    
    :param mime_type: The MIME type of this image. One of "image/gif", "image/jpeg", "image/png", "image/svg+xml", "video/webm".
    :type  mime_type: str
    
    :param name: The filename that this image was uploaded with.
    :type  name: str
    
    :param orig_sha512_hash: The SHA512 hash of this image as it was originally uploaded.
    :type  orig_sha512_hash: str
    
    :param processed: Whether the image has finished optimization.
    :type  processed: bool
    
    :param representations: A mapping of representation names to their respective URLs. Contains the keys "full", "large", "medium", "small", "tall", "thumb", "thumb_small", "thumb_tiny".
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
    
    :param thumbnails_generated: Whether this image has finished thumbnail generation. Do not attempt to load images from view_url or representations if this is false.
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
    
    :param wilson_score: The lower bound of the Wilson score interval for the image, based on its upvotes and downvotes, given a z-score corresponding to a confidence of 99.5%.
    :type  wilson_score: float
    
    """

    
    """ The image's width divided by its height. """
    aspect_ratio: float
    
    """ The number of comments made on the image. """
    comment_count: int
    
    """ The creation time, in UTC, of the image. """
    created_at: datetime
    
    """ The hide reason for the image, or null if none provided. This will only have a value on images which are deleted for a rule violation. """
    deletion_reason: str
    
    """ The image's description. """
    description: str
    
    """ The number of downvotes the image has. """
    downvotes: int
    
    """ The ID of the target image, or null if none provided. This will only have a value on images which are merged into another image. """
    duplicate_of: int
    
    """ The number of faves the image has. """
    faves: int
    
    """ The time, in UTC, this image was first seen (before any duplicate merging). """
    first_seen_at: datetime
    
    """ The file extension of this image. One of "gif", "jpg", "jpeg", "png", "svg", "webm". """
    format: str
    
    """ The image's height, in pixels. """
    height: int
    
    """ Whether this image is hidden. An image is hidden if it is merged or deleted for a rule violation. """
    hidden_from_users: bool
    
    """ The image's ID. """
    id: int
    
    """ Optional object of internal image intensity data for deduplication purposes. May be null if intensities have not yet been generated. """
    intensities: Intensities
    
    """ The MIME type of this image. One of "image/gif", "image/jpeg", "image/png", "image/svg+xml", "video/webm". """
    mime_type: str
    
    """ The filename that this image was uploaded with. """
    name: str
    
    """ The SHA512 hash of this image as it was originally uploaded. """
    orig_sha512_hash: str
    
    """ Whether the image has finished optimization. """
    processed: bool
    
    """ A mapping of representation names to their respective URLs. Contains the keys "full", "large", "medium", "small", "tall", "thumb", "thumb_small", "thumb_tiny". """
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
    
    """ Whether this image has finished thumbnail generation. Do not attempt to load images from view_url or representations if this is false. """
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
    
    """ The lower bound of the Wilson score interval for the image, based on its upvotes and downvotes, given a z-score corresponding to a confidence of 99.5%. """
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
        intensities: Intensities,
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
        
        :param deletion_reason: The hide reason for the image, or null if none provided. This will only have a value on images which are deleted for a rule violation.
        :type  deletion_reason: str
        
        :param description: The image's description.
        :type  description: str
        
        :param downvotes: The number of downvotes the image has.
        :type  downvotes: int
        
        :param duplicate_of: The ID of the target image, or null if none provided. This will only have a value on images which are merged into another image.
        :type  duplicate_of: int
        
        :param faves: The number of faves the image has.
        :type  faves: int
        
        :param first_seen_at: The time, in UTC, this image was first seen (before any duplicate merging).
        :type  first_seen_at: datetime
        
        :param format: The file extension of this image. One of "gif", "jpg", "jpeg", "png", "svg", "webm".
        :type  format: str
        
        :param height: The image's height, in pixels.
        :type  height: int
        
        :param hidden_from_users: Whether this image is hidden. An image is hidden if it is merged or deleted for a rule violation.
        :type  hidden_from_users: bool
        
        :param id: The image's ID.
        :type  id: int
        
        :param intensities: Optional object of internal image intensity data for deduplication purposes. May be null if intensities have not yet been generated.
        :type  intensities: Intensities
        
        :param mime_type: The MIME type of this image. One of "image/gif", "image/jpeg", "image/png", "image/svg+xml", "video/webm".
        :type  mime_type: str
        
        :param name: The filename that this image was uploaded with.
        :type  name: str
        
        :param orig_sha512_hash: The SHA512 hash of this image as it was originally uploaded.
        :type  orig_sha512_hash: str
        
        :param processed: Whether the image has finished optimization.
        :type  processed: bool
        
        :param representations: A mapping of representation names to their respective URLs. Contains the keys "full", "large", "medium", "small", "tall", "thumb", "thumb_small", "thumb_tiny".
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
        
        :param thumbnails_generated: Whether this image has finished thumbnail generation. Do not attempt to load images from view_url or representations if this is false.
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
        
        :param wilson_score: The lower bound of the Wilson score interval for the image, based on its upvotes and downvotes, given a z-score corresponding to a confidence of 99.5%.
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
    def validate_dict(cls: Type[Image], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Image], data: Union[Dict, None]) -> Union[Image, None]:
        """
        Deserialize a new Image from a given dictionary.

        :return: new Image instance.
        :rtype: Image|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(aspect_ratio={s.aspect_ratio!r}, comment_count={s.comment_count!r}, created_at={s.created_at!r}, deletion_reason={s.deletion_reason!r}, description={s.description!r}, downvotes={s.downvotes!r}, duplicate_of={s.duplicate_of!r}, faves={s.faves!r}, first_seen_at={s.first_seen_at!r}, format={s.format!r}, height={s.height!r}, hidden_from_users={s.hidden_from_users!r}, id={s.id!r}, intensities={s.intensities!r}, mime_type={s.mime_type!r}, name={s.name!r}, orig_sha512_hash={s.orig_sha512_hash!r}, processed={s.processed!r}, representations={s.representations!r}, score={s.score!r}, sha512_hash={s.sha512_hash!r}, source_url={s.source_url!r}, spoilered={s.spoilered!r}, tag_count={s.tag_count!r}, tag_ids={s.tag_ids!r}, tags={s.tags!r}, thumbnails_generated={s.thumbnails_generated!r}, updated_at={s.updated_at!r}, uploader={s.uploader!r}, uploader_id={s.uploader_id!r}, upvotes={s.upvotes!r}, view_url={s.view_url!r}, width={s.width!r}, wilson_score={s.wilson_score!r})".format(s=self)
    # end def __repr__
# end class



class Comment(DerpiModel):
    """
    A parsed Comment response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param author: The comment's author.
    :type  author: str
    
    :param body: The comment text.
    :type  body: str
    
    :param id: The comment's ID.
    :type  id: int
    
    :param image_id: The ID of the image the comment belongs to.
    :type  image_id: int
    
    :param user_id: The ID of the user the comment belongs to, if any.
    :type  user_id: int
    
    """

    
    """ The comment's author. """
    author: str
    
    """ The comment text. """
    body: str
    
    """ The comment's ID. """
    id: int
    
    """ The ID of the image the comment belongs to. """
    image_id: int
    
    """ The ID of the user the comment belongs to, if any. """
    user_id: int
    

    def __init__(
        self, 
        author: str,
        body: str,
        id: int,
        image_id: int,
        user_id: int,
    ):
        """
        A parsed Comment response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param author: The comment's author.
        :type  author: str
        
        :param body: The comment text.
        :type  body: str
        
        :param id: The comment's ID.
        :type  id: int
        
        :param image_id: The ID of the image the comment belongs to.
        :type  image_id: int
        
        :param user_id: The ID of the user the comment belongs to, if any.
        :type  user_id: int
        
        """
        self.author = author
        self.body = body
        self.id = id
        self.image_id = image_id
        self.user_id = user_id
    # end def __init__

    @classmethod
    def validate_dict(cls: Type[Comment], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Comment], data: Union[Dict, None]) -> Union[Comment, None]:
        """
        Deserialize a new Comment from a given dictionary.

        :return: new Comment instance.
        :rtype: Comment|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
        instance: Comment = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(comment_instance)`
        """
        return "{s.__class__.__name__}(author={s.author!r}, body={s.body!r}, id={s.id!r}, image_id={s.image_id!r}, user_id={s.user_id!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(comment_instance)`
        """
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(author={s.author!r}, body={s.body!r}, id={s.id!r}, image_id={s.image_id!r}, user_id={s.user_id!r})".format(s=self)
    # end def __repr__
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
    def validate_dict(cls: Type[Forum], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Forum], data: Union[Dict, None]) -> Union[Forum, None]:
        """
        Deserialize a new Forum from a given dictionary.

        :return: new Forum instance.
        :rtype: Forum|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(name={s.name!r}, short_name={s.short_name!r}, description={s.description!r}, topic_count={s.topic_count!r}, post_count={s.post_count!r})".format(s=self)
    # end def __repr__
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
    
    :param user_id: The ID of the user who made the topic. Null if posted anonymously.
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
    
    """ The ID of the user who made the topic. Null if posted anonymously. """
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
        
        :param user_id: The ID of the user who made the topic. Null if posted anonymously.
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
    def validate_dict(cls: Type[Topic], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Topic], data: Union[Dict, None]) -> Union[Topic, None]:
        """
        Deserialize a new Topic from a given dictionary.

        :return: new Topic instance.
        :rtype: Topic|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(slug={s.slug!r}, title={s.title!r}, post_count={s.post_count!r}, view_count={s.view_count!r}, sticky={s.sticky!r}, last_replied_to_at={s.last_replied_to_at!r}, locked={s.locked!r}, user_id={s.user_id!r}, author={s.author!r})".format(s=self)
    # end def __repr__
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
    
    """

    
    """ The post's author. """
    author: str
    
    """ The post text. """
    body: str
    
    """ The post's ID (used to identify it). """
    id: int
    
    """ The ID of the user the comment belongs to, if any. """
    user_id: int
    

    def __init__(
        self, 
        author: str,
        body: str,
        id: int,
        user_id: int,
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
        
        """
        self.author = author
        self.body = body
        self.id = id
        self.user_id = user_id
    # end def __init__

    @classmethod
    def validate_dict(cls: Type[Post], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Post], data: Union[Dict, None]) -> Union[Post, None]:
        """
        Deserialize a new Post from a given dictionary.

        :return: new Post instance.
        :rtype: Post|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
        instance: Post = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(post_instance)`
        """
        return "{s.__class__.__name__}(author={s.author!r}, body={s.body!r}, id={s.id!r}, user_id={s.user_id!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(post_instance)`
        """
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(author={s.author!r}, body={s.body!r}, id={s.id!r}, user_id={s.user_id!r})".format(s=self)
    # end def __repr__
# end class



class Tag(DerpiModel):
    """
    A parsed Tag response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param aliased_tag: The slug of the tag this tag is aliased to, if any.
    :type  aliased_tag: str
    
    :param aliases: The slugs of the tags aliased to this tag.
    :type  aliases: list
    
    :param category: The category class of this tag. One of "character", "content-fanmade", "content-official", "error", "oc", "origin", "rating", "species", "spoiler".
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
    
    :param spoiler_image: The spoiler image URL for the tag.
    :type  spoiler_image: str
    
    """

    
    """ The slug of the tag this tag is aliased to, if any. """
    aliased_tag: str
    
    """ The slugs of the tags aliased to this tag. """
    aliases: list
    
    """ The category class of this tag. One of "character", "content-fanmade", "content-official", "error", "oc", "origin", "rating", "species", "spoiler". """
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
    
    """ The spoiler image URL for the tag. """
    spoiler_image: str
    

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
        spoiler_image: str,
    ):
        """
        A parsed Tag response of the Derpibooru API.
        Yes, a better description should be here.

        
        :param aliased_tag: The slug of the tag this tag is aliased to, if any.
        :type  aliased_tag: str
        
        :param aliases: The slugs of the tags aliased to this tag.
        :type  aliases: list
        
        :param category: The category class of this tag. One of "character", "content-fanmade", "content-official", "error", "oc", "origin", "rating", "species", "spoiler".
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
        
        :param spoiler_image: The spoiler image URL for the tag.
        :type  spoiler_image: str
        
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
    # end def __init__

    @classmethod
    def validate_dict(cls: Type[Tag], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Tag], data: Union[Dict, None]) -> Union[Tag, None]:
        """
        Deserialize a new Tag from a given dictionary.

        :return: new Tag instance.
        :rtype: Tag|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
        instance: Tag = cls(**data)
        instance._raw = data
        return instance
    # end def from_dict

    def __str__(self):
        """
        Implements `str(tag_instance)`
        """
        return "{s.__class__.__name__}(aliased_tag={s.aliased_tag!r}, aliases={s.aliases!r}, category={s.category!r}, description={s.description!r}, dnp_entries={s.dnp_entries!r}, id={s.id!r}, images={s.images!r}, implied_by_tags={s.implied_by_tags!r}, implied_tags={s.implied_tags!r}, name={s.name!r}, name_in_namespace={s.name_in_namespace!r}, namespace={s.namespace!r}, short_description={s.short_description!r}, slug={s.slug!r}, spoiler_image={s.spoiler_image!r})".format(s=self)
    # end def __str__

    def __repr__(self):
        """
        Implements `repr(tag_instance)`
        """
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(aliased_tag={s.aliased_tag!r}, aliases={s.aliases!r}, category={s.category!r}, description={s.description!r}, dnp_entries={s.dnp_entries!r}, id={s.id!r}, images={s.images!r}, implied_by_tags={s.implied_by_tags!r}, implied_tags={s.implied_tags!r}, name={s.name!r}, name_in_namespace={s.name_in_namespace!r}, namespace={s.namespace!r}, short_description={s.short_description!r}, slug={s.slug!r}, spoiler_image={s.spoiler_image!r})".format(s=self)
    # end def __repr__
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
    
    :param avatar_url: The URL of the user's thumbnail. Null if they haven't set one.
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
    
    :param links: The links the user has registered. See `Links`.
    :type  links: Links
    
    :param awards: The awards/badges of the user. See `Awards`.
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
    
    """ The URL of the user's thumbnail. Null if they haven't set one. """
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
    
    """ The links the user has registered. See `Links`. """
    links: Links
    
    """ The awards/badges of the user. See `Awards`. """
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
        
        :param avatar_url: The URL of the user's thumbnail. Null if they haven't set one.
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
        
        :param links: The links the user has registered. See `Links`.
        :type  links: Links
        
        :param awards: The awards/badges of the user. See `Awards`.
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
    def validate_dict(cls: Type[User], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[User], data: Union[Dict, None]) -> Union[User, None]:
        """
        Deserialize a new User from a given dictionary.

        :return: new User instance.
        :rtype: User|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(id={s.id!r}, name={s.name!r}, slug={s.slug!r}, role={s.role!r}, description={s.description!r}, avatar_url={s.avatar_url!r}, created_at={s.created_at!r}, comments_count={s.comments_count!r}, uploads_count={s.uploads_count!r}, posts_count={s.posts_count!r}, topics_count={s.topics_count!r}, links={s.links!r}, awards={s.awards!r})".format(s=self)
    # end def __repr__
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
    
    :param user_id: The id of the user the filter belongs to. Null if it isn't assigned to a user (usually system filters only).
    :type  user_id: int
    
    :param user_count: The amount of users employing this filter.
    :type  user_count: int
    
    :param system: If true, is a system filter. System filters are usable by anyone and don't have a user_id set.
    :type  system: bool
    
    :param public: If true, is a public filter. Public filters are usable by anyone.
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
    
    """ The id of the user the filter belongs to. Null if it isn't assigned to a user (usually system filters only). """
    user_id: int
    
    """ The amount of users employing this filter. """
    user_count: int
    
    """ If true, is a system filter. System filters are usable by anyone and don't have a user_id set. """
    system: bool
    
    """ If true, is a public filter. Public filters are usable by anyone. """
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
        
        :param user_id: The id of the user the filter belongs to. Null if it isn't assigned to a user (usually system filters only).
        :type  user_id: int
        
        :param user_count: The amount of users employing this filter.
        :type  user_count: int
        
        :param system: If true, is a system filter. System filters are usable by anyone and don't have a user_id set.
        :type  system: bool
        
        :param public: If true, is a public filter. Public filters are usable by anyone.
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
    def validate_dict(cls: Type[Filter], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Filter], data: Union[Dict, None]) -> Union[Filter, None]:
        """
        Deserialize a new Filter from a given dictionary.

        :return: new Filter instance.
        :rtype: Filter|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(id={s.id!r}, name={s.name!r}, description={s.description!r}, user_id={s.user_id!r}, user_count={s.user_count!r}, system={s.system!r}, public={s.public!r}, spoilered_tag_ids={s.spoilered_tag_ids!r}, spoilered_complex={s.spoilered_complex!r}, hidden_tag_ids={s.hidden_tag_ids!r}, hidden_complex={s.hidden_complex!r})".format(s=self)
    # end def __repr__
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
    
    :param tag_id: The ID of an associated tag for this link. Null if no tag linked.
    :type  tag_id: int
    
    """

    
    """ The ID of the user who owns this link. """
    user_id: int
    
    """ The creation time, in UTC, of this link. """
    created_at: datetime
    
    """ The state of this link. """
    state: str
    
    """ The ID of an associated tag for this link. Null if no tag linked. """
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
        
        :param tag_id: The ID of an associated tag for this link. Null if no tag linked.
        :type  tag_id: int
        
        """
        self.user_id = user_id
        self.created_at = created_at
        self.state = state
        self.tag_id = tag_id
    # end def __init__

    @classmethod
    def validate_dict(cls: Type[Links], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Links], data: Union[Dict, None]) -> Union[Links, None]:
        """
        Deserialize a new Links from a given dictionary.

        :return: new Links instance.
        :rtype: Links|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(user_id={s.user_id!r}, created_at={s.created_at!r}, state={s.state!r}, tag_id={s.tag_id!r})".format(s=self)
    # end def __repr__
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
    def validate_dict(cls: Type[Awards], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Awards], data: Union[Dict, None]) -> Union[Awards, None]:
        """
        Deserialize a new Awards from a given dictionary.

        :return: new Awards instance.
        :rtype: Awards|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(image_url={s.image_url!r}, title={s.title!r}, id={s.id!r}, label={s.label!r}, awarded_on={s.awarded_on!r})".format(s=self)
    # end def __repr__
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
    def validate_dict(cls: Type[Gallery], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Gallery], data: Union[Dict, None]) -> Union[Gallery, None]:
        """
        Deserialize a new Gallery from a given dictionary.

        :return: new Gallery instance.
        :rtype: Gallery|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(description={s.description!r}, id={s.id!r}, spoiler_warning={s.spoiler_warning!r}, thumbnail_id={s.thumbnail_id!r}, title={s.title!r}, user={s.user!r}, user_id={s.user_id!r})".format(s=self)
    # end def __repr__
# end class



class Oembed(DerpiModel):
    """
    A parsed Oembed response of the Derpibooru API.
    Yes, a better description should be here.

    
    :param author_name: The comma-delimited names of the image authors.
    :type  author_name: str
    
    :param author_url: The source URL of the image.
    :type  author_url: str
    
    :param cache_age: Always 7200.
    :type  cache_age: int
    
    :param derpibooru_comments: The number of comments made on the image.
    :type  derpibooru_comments: int
    
    :param derpibooru_id: The image's ID.
    :type  derpibooru_id: int
    
    :param derpibooru_score: The image's number of upvotes minus the image's number of downvotes.
    :type  derpibooru_score: int
    
    :param derpibooru_tags: The names of the image's tags.
    :type  derpibooru_tags: list
    
    :param provider_name: Always "Derpibooru".
    :type  provider_name: str
    
    :param provider_url: Always "https://derpibooru.org".
    :type  provider_url: str
    
    :param title: The image's ID and associated tags, as would be given on the title of the image page.
    :type  title: str
    
    :param type: Always "photo".
    :type  type: str
    
    :param version: Always "1.0".
    :type  version: str
    
    """

    
    """ The comma-delimited names of the image authors. """
    author_name: str
    
    """ The source URL of the image. """
    author_url: str
    
    """ Always 7200. """
    cache_age: int
    
    """ The number of comments made on the image. """
    derpibooru_comments: int
    
    """ The image's ID. """
    derpibooru_id: int
    
    """ The image's number of upvotes minus the image's number of downvotes. """
    derpibooru_score: int
    
    """ The names of the image's tags. """
    derpibooru_tags: list
    
    """ Always "Derpibooru". """
    provider_name: str
    
    """ Always "https://derpibooru.org". """
    provider_url: str
    
    """ The image's ID and associated tags, as would be given on the title of the image page. """
    title: str
    
    """ Always "photo". """
    type: str
    
    """ Always "1.0". """
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
        
        :param cache_age: Always 7200.
        :type  cache_age: int
        
        :param derpibooru_comments: The number of comments made on the image.
        :type  derpibooru_comments: int
        
        :param derpibooru_id: The image's ID.
        :type  derpibooru_id: int
        
        :param derpibooru_score: The image's number of upvotes minus the image's number of downvotes.
        :type  derpibooru_score: int
        
        :param derpibooru_tags: The names of the image's tags.
        :type  derpibooru_tags: list
        
        :param provider_name: Always "Derpibooru".
        :type  provider_name: str
        
        :param provider_url: Always "https://derpibooru.org".
        :type  provider_url: str
        
        :param title: The image's ID and associated tags, as would be given on the title of the image page.
        :type  title: str
        
        :param type: Always "photo".
        :type  type: str
        
        :param version: Always "1.0".
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
    def validate_dict(cls: Type[Oembed], data: Union[Dict[str, JSONType]]) -> Dict[str, JSONType]:
        return data
    # end def validate_dict

    @classmethod
    def from_dict(cls: Type[Oembed], data: Union[Dict, None]) -> Union[Oembed, None]:
        """
        Deserialize a new Oembed from a given dictionary.

        :return: new Oembed instance.
        :rtype: Oembed|None
        """
        if not data:  # None or {}
            return None
        # end if

        data: Dict = cls.validate_dict(data)
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
        if self._raw:
            return "{s.__class__.__name__}.from_dict({s._raw})".format(s=self)
        # end if
        return "{s.__class__.__name__}(author_name={s.author_name!r}, author_url={s.author_url!r}, cache_age={s.cache_age!r}, derpibooru_comments={s.derpibooru_comments!r}, derpibooru_id={s.derpibooru_id!r}, derpibooru_score={s.derpibooru_score!r}, derpibooru_tags={s.derpibooru_tags!r}, provider_name={s.provider_name!r}, provider_url={s.provider_url!r}, title={s.title!r}, type={s.type!r}, version={s.version!r})".format(s=self)
    # end def __repr__
# end class

