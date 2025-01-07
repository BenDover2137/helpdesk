# Register your models here.
from django.contrib import admin
from .models import Ticket, Comment, ProblemType

admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(ProblemType)
