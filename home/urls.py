
from django.urls import path
from . views import RegisterView,LoginView,Userview,LogOutView

urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', Userview.as_view()),
    path('logout/', LogOutView.as_view()),


]