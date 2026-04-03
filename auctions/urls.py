"""URL routing configuration for auctions app.

Defines URL patterns mapping paths to view functions. Use path() for simple routes,
re_path() for regex. Included in main settings.urls via app namespace. Follow
RESTful naming: /resource/ (list), /resource/<id>/ (detail), etc.
"""
from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # CREATE LISTINGS
    path("create", views.create, name="create"),
    path("listing", views.new_listing, name="listing"),
    path("view_listing/<int:listing_id>", views.view_listing, name="view_listing"),

    # WATCHLISTS
    path("watch/<int:listing_id>", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),

    # BIDDINGS
    path("newbid/<int:listing_id>", views.new_bid, name="new_bid"),

    # CATEGORY
    path("category", views.category, name="category"),
    path("category_search/<str:category_id>", views.category_search, name="category_search"),

    # COMMENTS
    path("comment/<str:listing_id>", views.add_comment, name="comment")
    
]
