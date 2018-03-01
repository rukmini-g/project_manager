from django.contrib import admin

from .models import Ticket, MileStone

class MileStoneInline(admin.TabularInline):
    model = MileStone
    extra = 3


class TicketAdmin(admin.ModelAdmin):

    inlines = [MileStoneInline]
    list_display = ('title', 'ticket_type', 'created_at', 'updated_at')
    list_filter = ('created_at',)


admin.site.register(Ticket, TicketAdmin)