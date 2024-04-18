from django.urls import path
# from Etsy.views.customer import *
# from api.apps.accounts.views.ua_uc import *
from Etsy.views.customer import *

urlpatterns = [
    path("users/all/", CustomUserList.as_view(), name="user_list"),
    path("users/", CustomUserCreate.as_view(), name="create_user"),
    # path('login/', CustomerLoginView.as_view(), name="login"),  #
    # path('signup/', SignupView.as_view(), name="signup"),
    # path('logout/', logout, name='logout'),
    
]
