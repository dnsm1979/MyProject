from django.urls import path
from act_technical import views
from .views import ActUpdateView, export_act_pdf

app_name = 'act_technical'

urlpatterns = [

    path('act_add/', views.ActAddView.as_view(), name='act_add'),
    path('act_change/<int:pk>', views.ActChangeView.as_view(), name='act_change'),
    path('act_edit/<int:pk>', views.ActEditView.as_view(), name='act_edit'),
    path('act_edit2/<int:pk>', views.ActEdit2View.as_view(), name='act_edit2'),
    path('act/<int:pk>/pdf/', export_act_pdf, name='act_pdf'),
    path('acts/<int:pk>/comment/', views.add_comment_to_act, name='add_comment_to_act'),
    path('act/<int:pk>/update/', ActUpdateView.as_view(), name='act_update'),
]