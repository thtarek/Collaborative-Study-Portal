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
import wikipedia
import random



# Create your views here.


@login_required(login_url="user_login")
def to_do(request):
    todo_lists = Todo.objects.filter(user=request.user)
    context = {
        'todo_lists': todo_lists,
    }
    return render(request, 'portal/to_do.html', context)
    
@login_required(login_url='user_login')
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
@login_required(login_url='user_login')
def delete_todo(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('X-requested-with') == 'XMLHttpRequest':
            todo = get_object_or_404(Todo, id=pk)
            todo.delete()
            return JsonResponse({'status': 'success', 'id':pk})

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
def weather_update(request):
    weather =[]
    if request.method == "POST":
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

@login_required(login_url='user_login')
def search_book(request):
    book_list = []
    if request.method == "POST":
        book_search_url = "https://www.googleapis.com/books/v1/volumes"
        search_params = {
                'q': request.POST['search_book_name'],
                'key': settings.BOOK_API_KEY,
                'maxResults': 12,
            }
        r =requests.get(book_search_url, search_params)
        results = r.json()['items']
        for result in results:
            book_data = {
                'id':result['id'],
                'title':result['volumeInfo']['title'],
                'image': result['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in result['volumeInfo'] else "",
                'authors':result['volumeInfo']['authors'] if 'authors' in result['volumeInfo'] else "",
                'publishedDate':result['volumeInfo']['publishedDate'] if 'publishedDate' in result['volumeInfo'] else "",
                'description':result['volumeInfo']['description'] if 'description' in result['volumeInfo'] else "",
                
            }
            book_list.append(book_data)
    context = {
        'book_lists': book_list,
    }
    # print(book_list)
    return render(request, 'portal/search_book.html', context)

@login_required(login_url='user_login')
def book_detail(request, id):
    book_details = []
    if request.method == "GET":
        specific_book = "https://www.googleapis.com/books/v1/volumes/"+id+"?key="+settings.BOOK_API_KEY
        r =requests.get(specific_book)
        result = r.json()
        book_data = {
            'id':result['id'],
            'title':result['volumeInfo']['title'],
            'subtitle':result['volumeInfo']['subtitle'] if 'subtitle' in result['volumeInfo'] else "",
            'image': result['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in result['volumeInfo'] else "",
            'authors':", ".join(result['volumeInfo']['authors']) if 'authors' in result['volumeInfo'] else "",
            'publisher':result['volumeInfo']['publisher'] if 'publisher' in result['volumeInfo'] else "",
            'description':result['volumeInfo']['description'] if 'description' in result['volumeInfo'] else "",
            'pageCount':result['volumeInfo']['pageCount'] if 'pageCount' in result['volumeInfo'] else "",
            'publishedDate':result['volumeInfo']['publishedDate'] if 'publishedDate' in result['volumeInfo'] else "",
            'ratingsCount':result['volumeInfo']['ratingsCount'] if 'ratingsCount' in result['volumeInfo'] else "",
            'categories':result['volumeInfo']['categories'] if 'categories' in result['volumeInfo'] else "",
            'previewLink':result['volumeInfo']['previewLink'] if 'previewLink' in result['volumeInfo'] else "",
            
        }
        book_details.append(book_data)
        context = {
        'book_details': book_details,
        }
        return render(request, 'portal/book_detail.html', context)

def search_wiki(request):
    if request.method == 'POST':
        info = request.POST['search_wiki']
        try:
            text = wikipedia.page(info, auto_suggest = False)
        except wikipedia.exceptions.DisambiguationError as e:
            s = random.choice(e.options)
            text = wikipedia.page(s, auto_suggest = False)
        context = {
            'title': text.title,
            'details': text.summary,
            'link': text.url,
            'image': text.images[0],
        }
        return render(request, 'portal/search_wiki.html', context)
    
    else:
        return render(request, 'portal/search_wiki.html')


            
           
