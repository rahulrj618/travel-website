from django.urls import path
from .import views


urlpatterns = [
    path('',views.index),
    path('accounts/login/',views.login_view,name="login"),
    path('accounts/sign_up/',views.signup,name='Signup'),
    path('userdashboard/',views.user_dashboard,name='user_dashboard'),
    path('logout/',views.logout_view,name='logout'),
    path('trips/', views.trip_list, name='trip_list'),
    path('aboutus/', views.aboutus_view,name="aboutus"),
    path('contactus/', views.contactus_view,name="contactus"),
    path('destinations/', views.destination_list, name='destination_list'),    
    path('spots/<int:destination_id>/', views.spot_list, name='spot_list'),  
    path('spot_detail/<int:spot_id>/', views.spot_detail, name='spot_detail'),
    path('stays/', views.stay_list, name='stay-list'),
    path('stay/<int:stay_id>/', views.stay_detail, name='stay-detail'),
    path('restaurants/', views.restaurant_list, name='restaurant-list'),
    path('restaurants/destination/<int:destination_id>/', views.restaurant_list, name='restaurant-list-by-destination'),
    path('restaurants/stay/<int:stay_id>/', views.restaurant_list, name='restaurant-list-by-stay'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant-detail'),
    path('payment/', views.homepage, name='index'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('paymentsuccess/', views.paymentsuccess, name='payment_success'),
    path('paymentfail/', views.paymentfail, name='payment_fail'),
]