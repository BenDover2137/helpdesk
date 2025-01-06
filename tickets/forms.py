from django import forms
from .models import Ticket, Comment, ProblemType
from django.contrib.auth.models import Group

from django.contrib.auth.models import Group
class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from the form kwargs
        super().__init__(*args, **kwargs)

        # Restrict status options based on the user's role
        if self.user and self.user == self.instance.created_by:
            # Ticket creator can only set status to 'open'
            self.fields['status'].choices = [
                ('open', 'Open'),
            ]
        elif self.user and self.user.groups.filter(name='Tech Support').exists():
            # Tech Support users can set status to 'in_progress' or 'closed'
            self.fields['status'].choices = [
                ('in_progress', 'In Progress'),
                ('closed', 'Closed'),
            ]

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'problem_type', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict assigned_to to users in the "Tech Support" group

        tech_support_group, created = Group.objects.get_or_create(name='Tech Support')
        # Restrict assigned_to to users in the Tech Support group

        self.fields['assigned_to'].queryset = tech_support_group.user_set.all()
        # Add a dropdown for problem types
        self.fields['problem_type'].queryset = ProblemType.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']