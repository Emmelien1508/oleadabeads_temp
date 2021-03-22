from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views.logout_view, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "webshop/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "webshop/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "webshop/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "webshop/password_reset_done.html"), name ='password_reset_complete'),
    path("producten/<str:soort>", views.allproducts, name="allproducts"),
    path("product/<str:naam>", views.product, name="product"),
    path("DIY", views.diy, name="diy"),
    path("over-ons", views.about, name="about"),
    path("winkelwagen", views.cart, name="cart"),
    path("doorgaan-als-klant", views.cont, name="cont"),
    path("checkout", views.checkout, name="checkout"),
    path("contact", views.contact, name="contact"),
    path("profiel", views.profile, name="profile"),
    path("verzenden-retourneren", views.info, name="info"),
    path("garantie", views.guarantee, name="guarantee"),
    path("DIY/<str:idnr>", views.diyproduct, name="diyproduct"),
    path("favorieten/<str:naam>", views.fav, name="fav"),
    path("verwijderen/<str:naam>", views.deletefromprofile, name="deletefromprofile"),
    path("toevoegen-aan-winkelwagen/<str:naam>", views.addtocart, name="addtocart"),
    path("verwijderen-van-winkelwagen/<str:naam>", views.deletefromcart, name="deletefromcart"),
    path("bestelling/<int:ordernummer>", views.order, name="order"),
    path("kortingscode-toevoegen", views.discount, name="discount"),
    path("gegevens-wijzigen", views.changeprofile, name="change"),
    path("gegevens-wijzigen", views.changeprofile, name="changeinfo"),
    path("statusveranderen/<int:ordernummer>", views.changestatus, name="changestatus"),
    path("algemene-voorwaarden", views.terms_conditions, name="termsconditions"),
    path("privacy-verklaring", views.privacypolicy, name="privacypolicy"),
    path("disclaimer", views.disclaimer, name="disclaimer"),
    path("materialen", views.material, name="material")
]