from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return str(self.username)


class Bid(models.Model):
    bidderUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bidder', null=True, blank=True)
    bidAmount = models.FloatField(default=0)

    def __str__(self):
        return str(self.bidAmount)


class Category(models.Model):
    category = models.CharField(max_length=35, null=True, blank=True)

    def __str__(self):
        return self.category


class AuctionListing(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField(max_length=500)
    starting_bid = models.ForeignKey(
        Bid, on_delete=models.CASCADE, related_name='listingStartingBid')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='listingCategory')
    image_url = models.URLField(max_length=5000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='listingOwner')

    def __str__(self):
        return self.title


class Comment(models.Model):
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="listing", null=True, blank=True)
    commenterUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commenter', null=True, blank=True)
    comment = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.comment) + " by " + str(self.commenterUser) + " on " + str(self.listing)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='userWatchlist')
    favorites = models.ManyToManyField(
        AuctionListing, null=True, blank=True, related_name='userWatchlistListings')

    def __str__(self):
        return str(self.user) + " Watchlist"
