from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from base.models import Todo

# Create your views here.
@login_required(login_url="user_login")
def to_do(request):
    todo_lists = Todo.objects.filter(user=request.user)
    context = {
        'todo_lists': todo_lists,
    }
    return render(request, 'portal/to_do.html', context)

def add_to_do(request):
      if request.user.is_authenticated:
        if request.headers.get('X-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            title = request.POST.get('title')
            # print(title)
            try:
                add_data = Todo.objects.create(user=request.user, title=title)
                if add_data:
                    todo = Todo.objects.get(id=add_data.id)
                    if todo:
                        response = {'status': 'success', 'id':todo.id, 'title':todo.title, 'is_finished':todo.is_finished, 'created_at':todo.created_at }

                return JsonResponse(response)
            except:
                response = {'status': 'failed', 'message':' todo does not add!'}
                return JsonResponse(response)

        # return HttpResponse('OK')

def delete_todo(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('X-requested-with') == 'XMLHttpRequest':
            todo = get_object_or_404(Todo, pk=pk)
            todo.delete()
            return JsonResponse({'status': 'success', 'id':pk})
