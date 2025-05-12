from django.urls import path
from act_technical import views
from .views import  export_act_pdf, upload_act_image, delete_act_image, toggle_comment_active

app_name = 'act_technical'

urlpatterns = [

    path('act_add/', views.ActAddView.as_view(), name='act_add'),
    path('act_change/<int:pk>', views.ActChangeView.as_view(), name='act_change'),
    path('act_edit/<int:pk>', views.ActEditView.as_view(), name='act_edit'),
    path('act_edit2/<int:pk>', views.ActEdit2View.as_view(), name='act_edit2'),
    path('act/<int:pk>/pdf/', export_act_pdf, name='act_pdf'),
    path('acts/<int:pk>/comment/', views.add_comment_to_act, name='add_comment_to_act'),
    path('comment/<int:comment_id>/toggle/', toggle_comment_active, name='toggle_comment_active'),
    path('act/<int:pk>/upload-image/', upload_act_image, name='upload_act_image'),
    path('act/image/<int:pk>/delete/', delete_act_image, name='delete_act_image'),
]