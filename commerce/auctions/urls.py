from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("items/<int:item_id>", views.item, name="item"),
    path("watchlist/<int:watch_id>", views.watch_list, name="watchlist"),
    path("watch",views.watch, name="watch"),
    path("bid/<int:bid_id>",views.bid,name="bid"),
    path("remove/<int:item_id>",views.remove_bid,name="remove"),
    path("comment/<int:item_id>",views.comment,name="comment"),
    path("category",views.category_list,name="category_list"),
    path("category/<str:category_name>",views.category,name="category")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
