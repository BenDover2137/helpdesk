from django import forms
from .models import Ticket, Comment, ProblemType


from django.contrib.auth.models import Group
class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        if self.user and self.user == self.instance.created_by:
            self.fields['status'].choices = [
                ('open', 'Open'),
            ]
        elif self.user and self.user.groups.filter(name='Tech Support').exists():
            self.fields['status'].choices = [
                ('in_progress', 'In Progress'),
                ('closed', 'Closed'),
            ]
        else:
            self.fields['status'].disabled = True

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'problem_type', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        tech_support_group, created = Group.objects.get_or_create(name='Tech Support')


        self.fields['assigned_to'].queryset = tech_support_group.user_set.all()

        self.fields['problem_type'].queryset = ProblemType.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']