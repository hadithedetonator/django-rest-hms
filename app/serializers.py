# app/serializers.py
from rest_framework import serializers
from .models import Patient, Doctor, Appointment, Payment, RoomAllotment,Service

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'date_of_birth', 'age', 'phone', 'email', 'gender', 'address', 'file']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'  # Or explicitly list all fields


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'cost_of_treatment']

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'id',
            'patient',
            'department',
            'doctor',
            'admission_date',
            'discharge_date',
            'services',
            'discount',
            'paid',
            'payment_type',
            'card_check_number'
        ]

    
class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'appointment_date','department' ,'time_slot', 'token_number', 'status', 'problem', 'doctor', 'doctor_name', 'patient', 'patient_name']
class AppointmentUpdateSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'appointment_date', 'time_slot', 'status', 'problem', 'doctor', 'doctor_name', 'patient', 'patient_name']
class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'appointment_date', 'time_slot', 'token_number', 'status', 'problem', 'doctor', 'doctor_name', 'patient', 'patient_name']

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'PUT':
            # Remove token_number if the request method is PUT
            data.pop('token_number', None)
        return super().validate(data)
    
class RoomAllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAllotment
        fields = ['id', 'room_number', 'room_type', 'patient', 'allotment_date', 'discharge_date', 'doctor']
