from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-patient/',views.add_patient,name='add-patient'),
    path('all-patients/',views.all_patients,name='all-patients'),

    path('add-doctor/',views.add_doctor,name='add-doctor'),
    path('all-doctors/',views.all_doctors,name='all-doctors'),
    path('patient-autocomplete/', views.patient_autocomplete, name='patient_autocomplete'),

    path('add-appointment/', views.add_appointment, name='add-appointment'),
    path('all-appointments/', views.all_appointments, name='all-appointments'),
    path('add-payment/', views.add_payment, name='add-payment'),
    path('all-payments/', views.all_payments, name='all-payments'),
    path('add-room/', views.add_room, name='add-room'),
    path('all-rooms/', views.all_rooms, name='all-rooms'),
]
# analytics/urls.py
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, AppointmentViewSet, PaymentViewSet, RoomAllotmentViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'room-allotments', RoomAllotmentViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
]
