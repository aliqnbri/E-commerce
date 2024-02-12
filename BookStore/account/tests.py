from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


class UsersManagersTests(TestCase):

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email="admin@admin.com", password="foo" ,username='admin')
        self.assertEqual(user.email, "admin@admin.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser, False)
        self.assertTrue(user.role, 'ad')
        self.assertTrue(user.username, 'admin')
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

    