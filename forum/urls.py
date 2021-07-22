from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView, name='detail'),
    path('making', views.MakingView.as_view(), name='making'),
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='forum:index'), name="logout"),
    path('<int:pk>/comment/', views.MakeComment.as_view(), name='comment'),
    path('profile/<int:up>', views.ProfileView, name="profile"),
    path('search/', views.SearchView.as_view(), name="search"),
    path('<int:pk>/rating', views.vote, name="rating"),
]
