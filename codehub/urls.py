"""
URL configuration for codehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.SignUPView.as_view(),name='signup'),

    path('', views.LoginView.as_view(),name="login"),

    path('index', views.IndexView.as_view(),name="index"),

    path('profile/<int:pk>/change/', views.UserProfileUpdateView.as_view(),name="profile-update"),

    path('project/add/', views.ProjectCreatView.as_view(),name="project-add"),

    path('works/all/', views.MyProjectListView.as_view(),name="myworks"),

    path('works/<int:pk>/delete/', views.WorksDeleteView.as_view(),name="work-delete"),

    path('project/<int:pk>/', views.ProjectDetailView.as_view(),name="project-detail"),

    path('project/<int:pk>/whishlist/add', views.AddToWishListView.as_view(),name="add-wishlistitem"),

    path('wishlist/summary/', views.MyCartView.as_view(),name="whishlist-summary"),

    path('cart_item/<int:pk>/remove', views.WhishListItemRemoveView.as_view(),name="cartitem-delete"),

    path('checkout/', views.CheckOutView.as_view(),name="checkout"),

    path('payment/verification/', views.PaymentVerificationView.as_view(),name="payment-verify"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
