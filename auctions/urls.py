from os import name
from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # my paths

    # general
    path("create_listing/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("watchlist/", views.watchlist_view, name='watchlist'),
    path("categories/", views.categories_view, name='categories'),
    path("categories/<int:category_id>", views.category_view, name='category'),

    # forms
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("categories/add_category", views.add_category, name="add_category"),

    # misc (i don't know of a better name) / REST API
    # I'm trying the REST API impementation (without knowing what it is, never looked into it)
    # Please don't laugh if this doesn't make sense, in the future i want to see how close 
    # i was to the concept, when i actually learn it
    path("listing/<int:listing_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("listing/<int:listing_id>/remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("listing/<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("listing/<int:listing_id>/reopen_auction", views.reopen_auction, name="reopen_auction"),
]
