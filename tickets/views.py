
from django.contrib.auth.decorators import login_required

from .models import Ticket, Comment
from tickets.forms import TicketForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged in.")
            return redirect('ticket_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have been successfully registered and logged in.")
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)


    is_tech_support = request.user.groups.filter(name='Tech Support').exists()

    if not is_tech_support:
        messages.error(request, "You do not have permission to delete tickets.")
        return redirect('ticket_list')


    if ticket.status != 'closed':
        messages.error(request, "You can only delete tickets with a 'closed' status.")
        return redirect('ticket_list')


    ticket.delete()
    messages.success(request, "Ticket deleted successfully.")
    return redirect('ticket_list')


@login_required
def profile(request):

    is_tech_support = request.user.groups.filter(name='Tech Support').exists()

    if is_tech_support:

        user_tickets = Ticket.objects.filter(assigned_to=request.user)
        ticket_type = "assigned to you"
    else:

        user_tickets = Ticket.objects.filter(created_by=request.user)
        ticket_type = "created by you"

    paginator = Paginator(user_tickets, 10)
    page_number = request.GET.get('page')
    try:
        user_tickets = paginator.page(page_number)
    except PageNotAnInteger:

        user_tickets = paginator.page(1)
    except EmptyPage:

        user_tickets = paginator.page(paginator.num_pages)

    return render(request, 'registration/profile.html', {
        'user_tickets': user_tickets,
        'ticket_type': ticket_type,
        'is_tech_support': is_tech_support,
    })


from django.shortcuts import  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from tickets.forms import CommentForm, TicketStatusForm


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)



    is_creator = ticket.created_by == request.user
    is_tech_support = request.user.groups.filter(name='Tech Support').exists()


    if (is_creator or is_tech_support) and request.method == 'POST' and 'update_status' in request.POST:
        status_form = TicketStatusForm(request.POST, instance=ticket, user=request.user)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, "Ticket status updated successfully.")
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        status_form = TicketStatusForm(instance=ticket, user=request.user)

    comment_form = CommentForm()
    if request.method == 'POST' and 'add_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('ticket_detail', pk=ticket.pk)
    comments = ticket.comments.all().order_by('-created_at')
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:

        comments = paginator.page(1)
    except EmptyPage:

        comments = paginator.page(paginator.num_pages)

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'status_form': status_form,
        'comment_form': comment_form,
        'is_creator': is_creator,
        'is_tech_support': is_tech_support,
        'comments': comments,
    })

def custom_logout(request):
    logout(request)

    messages.success(request, "You have been successfully logged in.")
    return redirect('login')

@login_required
def ticket_create(request):

    is_tech_support = request.user.groups.filter(name='Tech Support').exists()

    if is_tech_support:

        return redirect('profile')


    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Ticket created successfully.")
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_create.html', {'form': form})


from django.shortcuts import render


