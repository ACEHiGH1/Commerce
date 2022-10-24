from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name="create"),
    path('listing/<int:id>', views.listing, name="listingDetails"),
    path('categories', views.categories, name="categories"),
    path('category/<str:userCategory>', views.category, name="category"),
    path('bid', views.bid, name="bid"),
    path('close', views.closeAuction, name='closeAuction'),
    path('closedListings', views.closedListings, name="closedListings"),
    path('closedListing/<int:id>', views.closedListing, name="closedListing"),
    path('comment', views.comment, name="comment"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('add/<int:id>', views.addToWatchlist, name="addToWatchlist"),
    path('remove/<int:id>', views.removeFromWatchlist, name="removeFromWatchlist")
]
