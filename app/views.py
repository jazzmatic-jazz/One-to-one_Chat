from concurrent.futures import thread
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Chat

User = get_user_model()

def index(request):
    users = User.objects.exclude(username=request.user.username)
    print(users)
    return render(request, 'app/index.html', {'users': users})

def chatPage(request, username):
    # try:
    #     user_obj = User.objects.get(username=username)
    #     print(user_obj)
    # except:
    #     user_obj = User.objects.create_user(username)
    #     users = User.objects.exclude(username=request.user.username)
    # return render(request, 'app/chat.html', {'users': users, 'user': user_obj})

    user_obj = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)
    print("Id:" ,request.user.id)
    

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'

    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    
    message_obj = Chat.objects.filter(thread_name=thread_name)
    return render(request, 'app/chat.html', {'users': users, 'user': user_obj, 'messages': message_obj})
