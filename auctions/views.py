from email.mime import image
from msilib.schema import BindImage
from turtle import update
from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import AuctionListing, User, Category, Bid, Comment, Watchlist


def index(request):
    activeListings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        'activeListings': activeListings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        return render(request, "auctions/create.html", {
            'categories': categories
        })
    elif request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        imageURL = request.POST['image_url']
        startingBid = request.POST['starting_bid']
        category = request.POST['category']

        bid = Bid(bidderUser=request.user, bidAmount=startingBid)
        bid.save()
        listing = AuctionListing(title=title, description=description, image_url=imageURL, category=Category.objects.get(
            category=category), starting_bid=bid, owner=request.user)
        listing.save()

        return HttpResponseRedirect(reverse("index"))


def listing(request, id):
    specificListing = AuctionListing.objects.get(pk=id)
    comments = Comment.objects.filter(listing=specificListing)
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        watchlistListings = watchlist.favorites.all()

    except Watchlist.DoesNotExist:
        watchlist = None
        watchlistListings = []
    if specificListing in watchlistListings:
        isWatchlisted = True
    else:
        isWatchlisted = False

    return render(request, "auctions/listing.html", {
        'listing': specificListing,
        'comments': comments,
        'isWatchlisted': isWatchlisted
    })


def categories(request):
    allCategories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': allCategories
    })


def category(request, userCategory):
    categoryObject = Category.objects.get(category=userCategory)
    Listings = AuctionListing.objects.filter(
        is_active=True, category=categoryObject)
    return render(request, "auctions/categoryListings.html", {
        "categoryListing": Listings
    })


def bid(request):
    if request.method == "POST":
        bid = request.POST['bid']
        listingId = request.POST['listingId']
        newBid = Bid(bidderUser=request.user, bidAmount=bid)
        listing = AuctionListing.objects.get(pk=listingId)
        if float(bid) > listing.starting_bid.bidAmount:
            listing.starting_bid = newBid
            listing.starting_bid.save()
            listing.save(update_fields=['starting_bid'])
            return render(request, "auctions/listing.html", {
                'listing': listing,
                'messageB': "Successfull bid"
            })
        else:
            return render(request, "auctions/listing.html", {
                'listing': listing,
                'messageB': "Unable to bid"
            })


def closeAuction(request):
    if request.method == "POST":
        listingId = request.POST['listingId']
        listing = AuctionListing.objects.get(pk=listingId)
        listing.is_active = False
        listing.save(update_fields=['is_active'])
        return render(request, "auctions/closedListing.html", {
            'listing': listing
        })


def closedListings(request):
    closedListings = AuctionListing.objects.filter(is_active=False)
    return render(request, "auctions/closedListings.html", {
        'closedListings': closedListings
    })


def closedListing(request, id):
    specificListing = AuctionListing.objects.get(pk=id)
    return render(request, "auctions/closedListing.html", {
        'listing': specificListing
    })


def comment(request):
    if request.method == "POST":
        listingID = request.POST['listingId']
        commentLeft = request.POST['comment']
        listing = AuctionListing.objects.get(pk=listingID)
        newComment = Comment(
            listing=listing, commenterUser=request.user, comment=commentLeft)
        newComment.save()
        return HttpResponseRedirect(reverse("listingDetails", args=(listingID,)))


def watchlist(request):
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        watchlistListings = watchlist.favorites.all()
    except Watchlist.DoesNotExist:
        watchlist = None
        watchlistListings = []
    return render(request, "auctions/watchlist.html", {
        "watchlistListings": watchlistListings
    })


def addToWatchlist(request, id):
    listing = AuctionListing.objects.get(pk=id)
    Watchlist.objects.get_or_create(user=request.user)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.favorites.add(listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("listingDetails", args=(id,)))


def removeFromWatchlist(request, id):
    listing = AuctionListing.objects.get(pk=id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.favorites.remove(listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("listingDetails", args=(id,)))
