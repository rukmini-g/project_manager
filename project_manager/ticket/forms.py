from django import forms
from .models import Ticket, MileStone


class TaskForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"
