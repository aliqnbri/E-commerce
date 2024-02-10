from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))

        if not password:
            raise ValueError (_("The Password must be set"))    

        if extra_fields.get("is_staff") is True:
            raise ValueError(_("Superuser must have is_staff=False."))
       
        if extra_fields.get("is_superuser") is True:
            raise ValueError(_("Superuser must have is_superuser=False."))  

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # change user passwoed
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 'admin')

        # if not username:
        #     raise ValueError (_("The username must be set"))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
       
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        # if User.objects.filter(is_superuser=True ,role='admin').exists():
        #     raise ValueError('Only one Admin user Can Exists.')    
        return self.create_user(email, password, **extra_fields)


    def create_staffuser(self, email ,password ):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 'staff')

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
        