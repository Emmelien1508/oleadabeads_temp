from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views.logout_view, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete'),
    path("producten/<str:soort>", views.allproducts, name="allproducts"),
    path("product/<str:naam>", views.product, name="product"),
    path("DIY", views.diy, name="diy"),
    path("overons", views.about, name="about"),
    path("winkelwagen", views.cart, name="cart"),
    path("continue", views.cont, name="cont"),
    path("checkout", views.checkout, name="checkout"),
    path("contact", views.contact, name="contact"),
    path("mijnaccount", views.profile, name="profile"),
    path("bestelinformatie", views.info, name="info"),
    path("favorieten/<str:naam>", views.fav, name="fav"),
    path("verwijderen/<str:naam>", views.deletefromprofile, name="deletefromprofile"),
    path("toevoegenwinkelwagen/<str:naam>", views.addtocart, name="addtocart"),
    path("verwijderenwinkelwagen/<str:naam>", views.deletefromcart, name="deletefromcart"),
    path("bestelling/<int:ordernummer>", views.order, name="order"),
    path("kortingscodetoevoegen", views.discount, name="discount")
]