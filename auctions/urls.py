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
    path("create_listing/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("watchlist/", views.watchlist_view, name='watchlist'),
    path("categories/", views.categories_view, name='categories'),
    path("categories/<int:category_id>", views.category_view, name='category'),

    # forms
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),

    # misc (i don't know of a better name)
    path("listing/<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
]
