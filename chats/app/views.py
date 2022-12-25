import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .models import Message


@login_required(login_url="/login/")
def users(request):
    all_users = User.objects.exclude(id=request.user.id).values('username', 'id')
    context = {
        'users': all_users,
    }
    return render(request, 'chat/users.html', context)


@login_required(login_url="/login/")
def chat(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = None

    if messages:
        directs = Message.objects.filter(user=user, recipient__username=username)
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    context = {
        'directs':directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'chat/index.html', context)



def send_direct(request):
    data = json.loads(request.body)
    print(data)
    from_user = request.user
    to_user_username = data.get('to_user')
    body = data.get('body')

    to_user = User.objects.get(username=to_user_username)
    Message.sender_message(from_user, to_user, body)
    return JsonResponse('done', safe=False)



def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}

    return render(request, 'register/registration.html', context)
