from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from base.forms import TodoForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from base.models import Todo
from django.http import HttpResponse
import requests
from django.conf import settings
from isodate import parse_duration


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
            todo = get_object_or_404(Todo, id=pk)
            todo.delete()
            return JsonResponse({'status': 'success', 'id':pk})

def complete_todo(request, pk=None):
    # return HttpResponse(pk)
    if request.user.is_authenticated:
        if request.headers.get('X-requested-with') == 'XMLHttpRequest':
            todo_item = Todo.objects.get(user=request.user, id=pk)
            
            if todo_item.is_finished == False:
                todo_item.is_finished = True
                todo_item.save()
                return JsonResponse({'status': 'success','is_finished':True, 'id':pk})
            else:
                  return JsonResponse({'status': 'Failed'})

def edit_todo(request, pk=None):
    todo_list = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo_list)
        if form.is_valid():
            print('Okkkk')
            title = form.cleaned_data['title']
            form.save()
            return redirect('to_do')
    else: 
        form = TodoForm(instance=todo_list)
    context ={
        'form': form
    }
    return render(request, 'portal/edit_todo.html', context)

def youtube_search(request):
    videos = []
    if request.method == "POST":
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_API_KEY,
            'maxResults': 18,
            'type': 'video',
        }

        video_ids = []
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_API_KEY,
            'id': ','.join(video_ids),
            'maxResults': 18,
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnail': result['snippet']["thumbnails"]['high']['url'],
                'duration': int(parse_duration(result['contentDetails']["duration"]).total_seconds()//60),
            }
            videos.append(video_data)
    context = {
        'videos': videos
    }
    return  render(request, 'portal/youtube.html', context)


def weather_update(request):
    weather =[]
    if request.method == "POST":
        # key = "cb5bd540aa71df72d1e7986a40bff392"
        weather_search_url = "https://api.openweathermap.org/data/2.5/weather"
        search_params = {
            'q': request.POST['city_name'],
            'appid': settings.WEATHER_API_KEY,
            'units': 'metric',
        }
        r =requests.get(weather_search_url, search_params)
        results = r.json()
        weather_data = {
            'des': results['weather'][0]['description'],
            'wet': results['weather'][0]['main'],
            'icon': results['weather'][0]['icon'],
            'temp': results['main']['temp'],
            'feels_like': results['main']['feels_like'],
            'humidity': results['main']['humidity'],
            'wind': results['wind']['speed'],
            'visibility': round(int(results['visibility'])/1000, 1),
            'city': results['name'],
            'country': results['sys']['country'],
        }
        weather.append(weather_data)
    context = {
        'weathers': weather
    }
        
    return render(request, 'portal/weather_update.html', context)

            
           
