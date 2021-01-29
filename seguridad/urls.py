from django.urls import path
from seguridad.views import login_session,logout_user

urlpatterns = [
path('login/' ,login_session ,name='login'),
path('logout/', logout_user ,name='logout'),
]