from django.db import models

# Patient Model
class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    file = models.FileField(upload_to='patients/')

    def __str__(self):
        return self.name

# Doctor Model
class Doctor(models.Model):
    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    ]
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()  # Years of experience
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    file = models.FileField(upload_to='doctors/')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Available')

    def __str__(self):
        return self.name

# Appointment Model
class Appointment(models.Model):
    DEPARTMENTS = [
        ('Neuro', 'Neuro'),
        ('Gynae', 'Gynae'),

        # Add other departments as needed
    ]
    TIME_SLOTS = [
        ('10AM-11AM', '10AM-11AM'),
        ('10PM-11PM', '10PM-11PM'),
        ('06AM-07AM', '06AM-07AM'),
        # Add other time slots as needed
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, choices=DEPARTMENTS)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    token_number = models.CharField(max_length=40, unique=True)  # Auto-generated
    problem = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')


    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} on {self.appointment_date}"

#Services
class Service(models.Model):
    name = models.CharField(max_length=100)
    cost_of_treatment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    
# Payment Model
class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    services = models.ManyToManyField(Service)
    discount = models.PositiveIntegerField()  # Discount percentage
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50, choices=[('Check', 'Check'), ('Card', 'Card'),('Cash', 'Cash')])
    card_check_number = models.CharField(max_length=50, blank=True, null=True)  # Optional

    def __str__(self):
        return f"Payment for {self.patient.name}"

# Room Allotment Model
class RoomAllotment(models.Model):
    ROOM_TYPES = [
        ('ICU', 'ICU'),
        ('General','General'),
        ('AC Room','AC Room'),
        # Add other room types as needed
    ]
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allotment_date = models.DateField()
    discharge_date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room {self.room_number} allotted to {self.patient.name}"
