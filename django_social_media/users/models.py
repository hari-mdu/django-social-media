from django.db import models

# Create your models here.
class Users(models.Model):
 
    userid = models.AutoField(primary_key=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    user_name = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to= 'image', null=True)
    created_on = models.DateField(blank=True, null=True)
    modified_on = models.DateField(blank=True, null=True)
    deleted_on = models.DateField(blank=True, null=True)
    created_by = models.IntegerField(null = True)

    class Meta:
        db_table = 'users'


