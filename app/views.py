# analytics/views.py
from rest_framework import viewsets
from .models import Patient, Doctor, Appointment, Payment, RoomAllotment,Service
from .serializers import ServiceSerializer,PatientSerializer, DoctorSerializer, AppointmentSerializer,AppointmentCreateSerializer,AppointmentUpdateSerializer, PaymentSerializer, RoomAllotmentSerializer

class ServiceViewset(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializer

class PatientUpdateView(UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response


class DoctorUpdateView(UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


from rest_framework import viewsets

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        elif self.request.method == 'PUT':
            return AppointmentUpdateSerializer
        return AppointmentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class RoomAllotmentViewSet(viewsets.ModelViewSet):
    queryset = RoomAllotment.objects.all()
    serializer_class = RoomAllotmentSerializer


















from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Patient, Doctor, Appointment, Payment, RoomAllotment
from django.db.models import Count, Sum


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Query data for charts
    patient_count = Patient.objects.count()
    doctor_count = Doctor.objects.count()
    appointment_count = Appointment.objects.count()
    appointments = Appointment.objects.all()
    doctors  = Doctor.objects.all()

    # Example: Total payments and the number of payments
    total_payments = Payment.objects.aggregate(total_amount=Sum('paid'))['total_amount']

    payment_count = Payment.objects.count()
    
    # Example: Count of appointments by department
    department_counts = Appointment.objects.values('department').annotate(count=Count('id'))

    # Example: Room allotments
    room_allotments = RoomAllotment.objects.values('room_type').annotate(count=Count('id'))
    context = {
        'doctors' : doctors,
        'patient_count': patient_count,
        'doctor_count': doctor_count,
        'appointment_count': appointment_count,
        'appointments' : appointments,
        'total_payments': total_payments,
        'payment_count': payment_count,
        'department_counts': department_counts,
        'room_allotments': room_allotments,
        'active_page': 'dashboard',
    }

    return render(request, 'index.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
@login_required
def add_patient(request):
    return render(request,'add-patient.html',{'active_page': 'patients'})


@login_required
def all_patients(request):
    patients = Patient.objects.all()
    return render(request, 'patients.html', {'patients': patients,'active_page': 'patients'})

@login_required
def add_doctor(request):
    return render(request,'add-doctor.html',{'active_page': 'doctors'})
@login_required
def all_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors,'active_page': 'doctors'})


from django.http import JsonResponse
@login_required
def patient_autocomplete(request):
    term = request.GET.get('term', '')
    patients = Patient.objects.filter(name__icontains=term)
    results = [{'id': patient.id, 'name': patient.name} for patient in patients]
    return JsonResponse(results, safe=False)
@login_required
def add_appointment(request):
    time_slots = Appointment.TIME_SLOTS
    departments = Appointment.DEPARTMENTS
    doctors = Doctor.objects.filter(availability='Available')
    doctor_list = list(doctors.values('id', 'name'))  # Include only necessary fields
    return render(request, 'add-appointment.html', {'active_page': 'appointments','time_slots':time_slots,'departments':departments,'doctor_list':doctor_list})

@login_required
def all_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments.html', {'active_page': 'appointments','appointments':appointments})

@login_required
def add_payment(request):
    services = Service.objects.all()
    departments = Appointment.DEPARTMENTS
    doctors = Doctor.objects.all()
    doctor_list = list(doctors.values('id', 'name'))  # Include only necessary fields
 
    return render(request, 'add-payment.html', {'services':services,'active_page': 'payments','departments':departments,'doctor_list':doctor_list})

@login_required
def all_payments(request):
    patients = Patient.objects.all()
    services = Service.objects.all()
    payments = Payment.objects.all()
    departments = Appointment.DEPARTMENTS
    doctors = Doctor.objects.all()
    doctor_list = list(doctors.values('id', 'name'))  # Include only necessary fields
 
    return render(request, 'payments.html', {'patients':patients,'active_page': 'payments','payments': payments,'services':services,'departments':departments,'doctor_list':doctor_list})

@login_required
def add_room(request):
    types = RoomAllotment.ROOM_TYPES
    doctors = Doctor.objects.filter(availability='Available')
    doctor_list = list(doctors.values('id', 'name'))  # Include only necessary fields
    return render(request, 'add-room.html', {'active_page': 'rooms','types':types,"doctor_list":doctor_list})

@login_required
def all_rooms(request):
    room_allotments = RoomAllotment.objects.all()
    print(room_allotments)
    return render(request, 'rooms.html', {'active_page': 'rooms','room_allotments':room_allotments})

