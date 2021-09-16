from django.contrib.auth.models import User

User.objects.create_user(username="FirstUser",
                         email="firstuser@example.com",
                         password="HyPerPasS")
