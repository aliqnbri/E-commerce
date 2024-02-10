from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


class UsersManagersTests(TestCase):

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email="admin@admin.com", password="foo")
        self.assertEqual(user.email, "admin@admin.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser, False)
        self.assertTrue(user.role, 'ad')
        # try:
        #     # username is None for the AbstractUser option
        #     # username does not exist for the AbstractBaseUser option
        #     self.assertIsNone(user.username)
        # except AttributeError:
        #     pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@admin.com', password='admin', is_superuser=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@admin.com', password='admin', is_staff=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="", password="foo", role='customer')
        with self.assertRaises(TypeError):
            User.objects.create_superuser()
        with self.assertRaises(TypeError):
            User.objects.create_superuser(email="")

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, 'cu')
        with self.assertRaises(TypeError):
            User.objects.create_user(password="foo")
        with self.assertRaises(TypeError):
            User.objects.create_user(
                email="super@user.com")
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="super@user.com", password="foo", is_staff=True)
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="super@user.com", password="foo", is_superuser=True)

    # def test_staffuser(self):
    #     User = get_user_model()
    #     email = "staff@example.com"
    #     password = "password123"
    #     # is_staff=True, is_superuser=False, is_active=True, role="op"
    #     user = User.objects.create_staffuser(
    #         email=email, password=password)

    #     self.assertEqual(user.email, email)
    #     self.assertTrue(user.check_password(password))
    #     self.assertTrue(user.is_staff)
    #     self.assertFalse(user.is_superuser)
    #     self.assertTrue(user.is_active)
    #     self.assertEqual(user.role, "staff")

    # def test_create_staffuser_invalid_superuser(self):
    #     User = get_user_model()
    #     email = "staff@example.com"
    #     password = "password123"
    #     extra_fields = {
    #         "is_staff": True,
    #         "is_superuser": True,  # Invalid superuser flag
    #         "is_active": True,
    #         "role": "staff"
    #     }

    #     # Check if ValueError is raised when is_superuser is set to True
    #     with self.assertRaises(ValueError):
    #         User.objects.create_staffuser(
    #             email=email, password=password, **extra_fields)

    # def test_create_staffuser_invalid_staff(self):
    #     User = get_user_model()
    #     email = "staff@example.com"
    #     password = "password123"
    #     extra_fields = {
    #         "is_staff": False,  # Invalid staff flag
    #         "is_superuser": False,
    #         "is_active": True,
    #         "role": "staff"
    #     }

    #     # Check if ValueError is raised when is_staff is set to False
    #     with self.assertRaises(ValueError):
    #         User.objects.create_staffuser(
    #             email=email, password=password, **extra_fields)
