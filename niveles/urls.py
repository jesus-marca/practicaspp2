from django.urls import path
from . import views

app_name='niveles'
urlpatterns = [
    path('', views.StandardListView.as_view(), name='standard_list'),
    path('<slug:slug>/', views.SubjectListView.as_view(), name='subject_list'), 
    path('<str:standard>/<slug:slug>/', views.LessonListView.as_view(), name='lesson_list'),
    path('<str:standard>/<str:slug>/create/', views.LessonCreateView.as_view(),name='lesson_create'),
    path('<str:standard>/<str:subject>/<slug:slug>/', views.LessonDetailView.as_view(),name='lesson_detail'),
    path('<str:standard>/<str:subject>/<slug:slug>/update/', views.LessonUpdateView.as_view(),name='lesson_update'),
    path('<str:standard>/<str:subject>/<slug:slug>/delete/', views.LessonDeleteView.as_view(),name='lesson_delete'),
    path('usuarios', views.UsersListView.as_view(), name='users_list'),
    path('horarios', views.SlotSubjectListView.as_view(), name='slots_list'),
    path('/hora/<str:standard>/<str:slug>', views.SlotSubjectCreateView.as_view(),name='slot_subject_create'),
    path('horarios/<str:standard>/<str:subject>/<slug:slug>/update', views.SlotUpdateView.as_view(),name='slot_subject_update'),
    
    path('user/<int:id>/page/update/user/',views.user_update,name='user_update'),
    path('list/users/edit/view/',views.edit_user),
    
    path('delete/page/user/del/<int:id>/',views.user_delete,name='user_delete'),
    path('list/users/delete/views/user/',views.delete_user),           
    
    path('slot/page/update/<int:id>/',views.slot_subject_update,name='slot_subject_update'),
    path('list/slots/edit/view/',views.edit_slot_subject),    
    
    path('delete/page/slot/del/<int:id>/',views.slot_subject_delete,name='slot_subject_delete'),
    path('list/slots/delete/views/slot/',views.delete_slot_subject),    
]
 