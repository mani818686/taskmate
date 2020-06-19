from django.contrib import admin
from todolist_app.models import tasklist


@admin.register(tasklist)
class tasklistAdmin(admin.ModelAdmin):
    list_display=['task','done','manage','id']

#admin.site.register(tasklist)


# Register your models here.
