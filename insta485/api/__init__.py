"""Insta485 REST API."""

from insta485.api.services import get_services
from insta485.api.posts import get_posts, get_post
from insta485.api.comments import get_comments, add_comment
from insta485.api.likes import get_likes, add_like, remove_like
