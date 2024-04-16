from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



class FoundationalModelManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class FoundationalModel(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(
        verbose_name="Name",
        max_length=50, 
        blank=False,
        help_text=("Please put your full name here"),
        validators=[MinLengthValidator(limit_value=5, message="Please enter name of good length.")])
    email = models.EmailField(verbose_name="Email", max_length=254, blank=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    class Types(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
    
    type = models.CharField(verbose_name="UserType", 
                            max_length=40, 
                            choices=Types.choices, 
                            default=Types.STUDENT)
    
    default_type = Types.STUDENT
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = FoundationalModelManager()
    
    # Here I am mentioning verbose_name that is used to denote the single instance of the model.
    class Meta:
        db_table_comment = "Base model for Student and Teacher"
        verbose_name = "Foundational Model"
        verbose_name_plural = "Foundation Users"
        
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.default_type
        return super().save(*args, **kwargs)
    
        

class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = FoundationalModel.Types.STUDENT)

class StudentExtended(models.Model):
    user = models.OneToOneField(FoundationalModel, on_delete=models.CASCADE)
    standard = models.IntegerField()
    
    
    class Meta:
        verbose_name = "Student Extended"
        verbose_name_plural = "Students Extended"
        
        
class Student(FoundationalModel):
    default_type = FoundationalModel.Types.STUDENT
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = "Baccha"
        verbose_name_plural = "Students"
    
    @property
    def extended(self):
        return self.studentextended
    
class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = FoundationalModel.Types.TEACHER)

class TeacherExtended(models.Model):
    user = models.OneToOneField(FoundationalModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Teacher Extended"
        verbose_name_plural = "Teachers Extended"


class Teacher(FoundationalModel):
    default_type = FoundationalModel.Types.TEACHER
    objects = TeacherManager()
    
    class Meta:
        proxy = True
        verbose_name = "Guruji"
        verbose_name_plural = "Teachers"
    
    @property
    def extended(self):
        return self.teacherextended

# Create your models here.
