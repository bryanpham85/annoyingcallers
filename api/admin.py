from django.contrib import admin
from api.models import Caller, Category, Caller_Categories

admin.site.register(Caller)
admin.site.register(Category)
admin.site.register(Caller_Categories)
