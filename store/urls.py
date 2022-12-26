from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
#from .views import CustomLoginView, RegisterView

#app_name = 'store'

urlpatterns =[
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.update_item,name='update_item'),
    path('process_order/',views.process_order,name='process_order'),
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page ='store'),name='logout'),
    #path('register/',views.RegisterPage.as_view(),name='register'),
    path('register/',views.register,name='register'),
    ]