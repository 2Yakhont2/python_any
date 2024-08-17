from django.urls import path
from store.views import index
from accounts.views import delete_account, login_user, signup, logout_user

urlpatterns = [
    # path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('profile/', delete_account, name='profile'),
]
