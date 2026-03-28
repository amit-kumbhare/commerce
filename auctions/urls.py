from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing", views.new_listing, name="listing"),
    path("view_listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("newbid/<int:listing_id>", views.new_bid, name="new_bid"),
    path("category", views.category, name="category"),
    path("category/<str:category_id>", views.category_search, name="category_search"),
    path("watch/<int:listing_id>", views.watch, name="watch")
]
