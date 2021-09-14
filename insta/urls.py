from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns=[  
    url(r'^$',views.index,name='index'),
    url(r'register/',views.register, name='registration'),
    url('login/', auth_views.LoginView.as_view(), name='login'),
    url(r'profile/', views.profile, name='profile'),
    url(r'updateProfile/', views.update_profile,name = 'update_profile'),
    url(r'new/post/', views.post_image, name='post_image'),
    url(r'comment/<int:id>', views.comment, name='comment'),
    url('search/', views.searchprofile, name='search'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)




    