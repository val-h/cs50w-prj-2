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
]
