
from django.contrib import admin
from django.urls import path, include


from CloudOnSite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('home/storage/', views.storage_view, name='storage'),
    path('home/storage/final', views.storage_view_final, name='storage_view_final'),
    path('home/profile/', views.profile_view, name='profile')


]
