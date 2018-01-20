from django.contrib.auth.models import Permission, User
from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=250)

    def __str__(self):
        return self.department_name


class Employee(models.Model):
    user = models.OneToOneField(User)
    employee_name = models.CharField(max_length=250)
    department = models.ForeignKey(Department, default=1, on_delete=models.CASCADE)
    manager = models.ForeignKey('self', null=True, related_name='employee')

    def __str__(self):
        return self.employee_name


class Asset(models.Model):
    asset_name = models.CharField(max_length=250)

    def __str__(self):
        return self.asset_name


class Ownership(models.Model):
    BOOKED = 'Booked asset'
    APPROVED = 'Approved'

    STATUS_TYPE = (
        (BOOKED, 'Booked asset'),
        (APPROVED, 'Approved')
    )

    owner = models.ForeignKey(Employee, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_TYPE)

    def __str__(self):
        return str(self.owner) + ' - ' + str(self.asset) + ' - ' + self.status
