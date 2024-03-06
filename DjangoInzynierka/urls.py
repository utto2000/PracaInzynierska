
from django.contrib import admin
from django.urls import path, include


from CloudOnSite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
   # path('login/', views.login, name='login'),

]
