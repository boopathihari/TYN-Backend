from django.db import models


class Startup(models.Model):
    startup_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    average_response_time = models.DecimalField(max_digits=5, decimal_places=2)
    query_count = models.IntegerField()
    poc_accepted = models.IntegerField(default=0) 
    poc_delivered = models.IntegerField(default=0) 
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'startup'
    
    def __str__(self):
        return self.name
    
class EnterpriseUser(models.Model):
    enterprise_user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    industry = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)
    invited = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'enterpriseuser'
    
    def __str__(self):
        return self.name


class UserPersona(models.Model):
    user_persona_id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50)  # Enterprise, Startup, Consultant, etc.
    count = models.IntegerField()  # Total count for each user type

    class Meta:
        db_table = 'userpersona'
    
    def __str__(self):
        return f"{self.user_type}: {self.count}"


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    enterpriseuser = models.ForeignKey(EnterpriseUser, null=True, blank=True, on_delete=models.SET_NULL)
    startup = models.ForeignKey(Startup, null=True, blank=True, on_delete=models.SET_NULL)
    session_date = models.DateTimeField()
    duration = models.IntegerField()  # Assuming duration is in minutes or seconds

    class Meta:
        db_table = 'session'
    
    def __str__(self):
        return f"Session {self.session_id} - {self.session_date}"