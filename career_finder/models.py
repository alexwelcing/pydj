from django.db import models

# Company model
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=512)

    def __str__(self):
        return self.name

# Role model
class Role(models.Model):  # Using singular 'Role' instead of 'Roles' for consistency
    role_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Linking to the Company model
    role_title = models.CharField(max_length=255, null=False)
    role_link = models.CharField(max_length=512, null=True)
    salary = models.CharField(max_length=255, null=True)
    score = models.IntegerField(null=True)

    def __str__(self):
        return self.role_title
