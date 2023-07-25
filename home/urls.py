
from django.urls import path
from . views import RegisterView,LoginView,Userview,LogOutView,UserDeleteView,DocterRegisterview,DocterDetail,DocterEdit,Doctorblock,DocterDelete

urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', Userview.as_view()),
    path('logout/', LogOutView.as_view()),
    path('delete/<str:username>/', UserDeleteView.as_view()),

    path('docterRegistration/', DocterRegisterview.as_view()),
    path('docterdetials/<int:id>/', DocterDetail.as_view()),
    path('docteredit/<int:id>/', DocterEdit.as_view()),
    path('docterblocking/<int:id>/',Doctorblock.as_view()),
    path('docterdelete/<int:id>/',DocterDelete.as_view()),





    # path('docteredit/<str:email>/', DocterRegisterview.as_view()),
    # path('docterdelete/<str:email>/', DocterRegisterview.as_view()),
    # path('doctersblocking/<str:email>/', DocterRegisterview.as_view(), name='doctors-block'),
    

]