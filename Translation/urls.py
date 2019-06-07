from django.urls import path
from . import views

urlpatterns = [
    #POST Method : add key
    #GET Method : get key
    path('keys', views.Key_Get_Post_View.as_view(), name = 'key_post_get'),

    #PUT Method : modify key
    path('keys/<int:pk>', views.Key_Update_View.as_view(), name = 'key_detail'),

    #GET Method : check translation
    #PUT Method : modify specific language translation
    #POST Method : add translation
    path('keys/<int:key_id>/translations/<str:locale>', views.Translation_Get_Put_Post_View.as_view(), name = 'translate_post'),

    #GET Method : check all translation
    path('keys/<int:key_id>/translations', views.Translations_Get_View.as_view(), name = 'translate_list'),

    #GET Method : detect language
    path('language_detect', views.Language_Get_View.as_view()),
]
