from django.contrib import admin
from .models import Framework, Language, Paradigm, Programmer


admin.site.register(Language)
admin.site.register(Paradigm)
admin.site.register(Programmer)
admin.site.register(Framework)
