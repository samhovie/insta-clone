"""Views, one for each Insta485 page."""
from insta485.views.static import show_upload
from insta485.views.index import show_index
from insta485.views.user import (
    show_profile,
    show_followers,
    show_following
)
from insta485.views.post import show_post
from insta485.views.explore import show_explore
from insta485.views.account import (
    show_login,
    show_logout,
    show_create,
    show_delete,
    show_edit,
    show_password
)
