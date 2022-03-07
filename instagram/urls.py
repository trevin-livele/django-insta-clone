from django.urls import path
from  .import views


urlpatterns = [
    path('createpost/', views.createpost, name='createpost'),
    path('<int:pk>/', views.comment, name='comment'),



 
]