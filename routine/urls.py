from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('addexercise', views.add_exercise, name="add_exercise"),
    path('show_log/<str:exercise>',views.show_log,name="show_log"),
    path('logout',views.logout,name="logout")
]