from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
import csv
from django.core.files.storage import FileSystemStorage
from .models import User, List, WatchList, Bid, Comment


def index(request):
    listings = List.objects.all()


    return render(request, "auctions/index.html", {
            "listings" : listings
        })


def first(request):
    return render(request, 'auctions/index.html', {
        'listings': List.objects.all()
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
    if request.method == 'POST':
        myimage = request.FILES['my-image']
        fs = FileSystemStorage()
        filename = fs.save(myimage.name, myimage)
        uploaded_file_url = fs.url(filename)
        title = request.POST['title']
        description = request.POST['a_description']
        category = request.POST['category']
        bid = request.POST['bid']
        user = request.user.username
        
        
        a = List(title=title, description=description, starting_bid = bid, category = category, user=user, image=myimage)
        a.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, 'auctions/create.html')

def item(request, item_id):
    
    check = List.objects.get(id=item_id)
    current = Bid.objects.filter(bid_item = check)
    coms = Comment.objects.filter(comment_item = check)

    
    if current.exists() == True:
        if check.available == False and check.final_buyer == request.user.username:
            #messages.success(request, 'You have won this bid.')
            return render(request,"auctions/items.html",{
                "items": List.objects.filter(id=item_id),
                "a_user" : request.user.username,
                "current_bid": Bid.objects.get(bid_item = check).starting_bid,
                "comments": coms,
                "message":"You have won this bid"
                })
        else:
            return render(request, "auctions/items.html", {
                "items": List.objects.filter(id=item_id),
                "a_user": request.user.username,
                "current_bid": Bid.objects.get(bid_item=check).starting_bid,
                "comments": coms
            })
    else:
        return render(request,"auctions/items.html",{
            "items": List.objects.filter(id=item_id),
            "a_user" : request.user.username,
            "current_bid": "No current bids",
            "comments": coms
            })


def watch_list(request, watch_id):
    
    item = List.objects.filter(id=watch_id)
    watch = List.objects.get(id=watch_id)
    check = WatchList.objects.all()
    new = WatchList.objects.filter(list=watch, buyer=request.user.username)
        
    if check.exists() == False:
        b = WatchList(list=watch, buyer=request.user.username)
        b.save()
        
    elif new.exists() == True:    
        return render(request, "auctions/layout.html",{
        "message":"This item already exists in your watch list."
        })
    else:
        a = WatchList(list=watch, buyer=request.user.username)
        a.save()
            
    
    show = WatchList.objects.all()
    return render(request, "auctions/watchlist.html",{
        "items":show
    })
    
def watch(request):
    new = WatchList.objects.filter(buyer=request.user.username)
    return render(request, "auctions/watch.html",{
        "items":new
    })

def bid(request, bid_id):
    
    item = List.objects.get(id=bid_id)
    f_check = Bid.objects.all()
    check = Bid.objects.filter(bid_item=item, bidder = request.user.username)
    
    if request.method == "POST":
        bid = request.POST['bid']
        if f_check.exists() != True or check.exists() is False:
        

            if int(bid) < item.starting_bid:
                return render(request, "auctions/layout.html",{
            "message":"Your price is lower than the current bid."
            })
            else:
                a = Bid(bid_item=item, starting_bid=bid,bidder=request.user.username, current_bid=bid)
                a.save()
                return render(request, "auctions/layout.html",{
            "message":f"{item.title} successfully bidded for."
            })
        elif check.exists() is True:
            there = Bid.objects.filter(bid_item=item, bidder = request.user.username).first()
            if int(bid) > there.starting_bid:
                there.starting_bid = bid
                there.save()
                return render(request, "auctions/layout.html",{
                            "message":"You have changed your bid"
                            })
            else:
                return render(request, "auctions/layout.html",{
                            "message":"Your bid is lower than the current"
                            })


    return render(request, "auctions/index.html")

def remove_bid(request, item_id):

    item = List.objects.get(id=item_id)

    
    f_check = Bid.objects.all()
    check = Bid.objects.filter(bid_item=item).first()
    final = check.bidder
    item.available = False
    item.final_buyer = final
    item.save()
    return render(request, "auctions/index.html")

def category_list(request):
    new = []
    here = List.objects.values_list('category')


    for i in here:
        if i not in new:
            new.append(i)
    this = new
    there = [i[0] for i in this]
    
    return render(request, "auctions/category.html",{
        'items': there
    })

def category(request, category_name):
    item = List.objects.filter(category=category_name)

    return render(request, "auctions/category_view.html",{
        'categories': item,
        'name': category_name
    })

def comment(request, item_id):
    item = List.objects.get(id=item_id)

    if request.method == 'POST':
        comment = request.POST['the_comment']
        c = Comment(comment_item=item, the_comment=comment, author=request.user.username)
        c.save()
    return HttpResponseRedirect(reverse("item", args=(item.id,)))
