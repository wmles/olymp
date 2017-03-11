from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from guardian.admin import GuardedModelAdmin
from userena.models import UserenaSignup
from userena import settings as userena_settings
from django.contrib.auth.models import Group

from .models import *


# von userena.admin kopiert und angepasst


