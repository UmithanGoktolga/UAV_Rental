from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    #path('list/', views.uav_list)
    path('register/', views.register_page, name='register_user'), # pageChecked - register da oldum
    path('login/', views.login_page, name='login_user'), # pageChecked - login de oldum

    path('logout/', views.logout_page, name='logout_user'),

    path('add/', views.uav_form), # pageChecked - drop down da sorun var (category) - Cozuldu :)
    path('<int:id>/', views.uav_form, name="uav_update"), #update calisiyor
    path('delete/<int:id>/', views.uav_delete, name="uav_delete"), #delete OK


        # URLs for rentals
    path('rentals/', views.rentals_list, name='rentals_list'), #tabloda rental detaylarini gorebiliyorum OK
    path('rental/add/', views.rental_form, name='add_rental'), # UAV yi rent ledim OK
    path('rental/<int:id>/', views.rental_form, name='update_rental'), # OK, saati update ledim OK

    path('rental/delete/<int:id>/', views.rental_delete, name='delete_rental') # OK

]