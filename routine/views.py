from django.shortcuts import render, redirect
from utils import get_client
from django.http import HttpResponse
import hashlib
from datetime import datetime
from youtubeapi import get_videos
# Create your views here.
db_client = None
db_handle = None
users_collection = None
rides_collection = None
def init_db():
    global client, users_collection, exercises_collection, db_handle
    client=get_client()
    db_handle = client.main
    users_collection = db_handle.users
    exercises_collection=db_handle.exercises
    print(users_collection)
    print("in")

def index(request):
    print('yes')
    if 'user' not in request.session:
        return redirect('login')
    if request.method=='POST':
        print('init')
        exercise_name=request.POST['exercise']
        print('exercise',exercise_name)
        return redirect('show_log/'+exercise_name)
    return render(request, 'index.html',{'log':None, 'exercise':None, 'videos':None})

def signup(request):
    init_db()
    print(users_collection,"ok")
    if request.method=='POST':
        print("in1")
        email=request.POST['email']
        name=request.POST["name"]
        password=request.POST['password']
        age=request.POST['age']
        height=request.POST['height']
        weight=request.POST['weight']
        # user=users_collection.find_one({"email":email})
        user_obj={
                "email":email,
                "name":name,
                "password":hashlib.sha256(password.encode()).hexdigest(),
                "age":age,
                "height":height,
                "weight":weight
            }
        print(users_collection,user_obj)
        users_collection.insert_one(user_obj)
        request.session['email']=email
        return redirect('login')
    else:
        return render(request,"signup.html",{"alert":""})
def login(request):
    init_db()
    print(users_collection,"ok")
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=users_collection.find_one({'email':email})
        if user and hashlib.sha256(password.encode()).hexdigest()==user['password']:
            request.session['user']=email
            return redirect('index')
        else:
            return render(request,'login.html',{'alert':"Invalid Credentials"})
    else:
        return render(request,'login.html',{'alert':''})
def add_exercise(request):
    init_db()
    if request.method=='POST':
        total_sets=request.POST['number_of_sets']
        exercise_name=request.POST['exercise'].lower()
        notes=request.POST['notes']
        set_count=1
        all_sets=[]
        for i in range(1,int(total_sets)+1):
            reps=request.POST['set'+str(i)+'reps']
            weight=request.POST['set'+str(i)+'weight']
            all_sets.append({'set':i,'reps':reps,'weight':weight})

        exercise_object={
                'user':request.session['user'],
                'exercise_name':exercise_name,
                'date':datetime.now(),
                'all_sets':all_sets,
                'notes':notes
            }
        exercises_collection.insert_one(exercise_object)
        return redirect('/addexercise')



    return render(request,'add_exercise.html')

def show_log(request,exercise):
    if request.method=='POST':
        print('init')
        exercise_name=request.POST['exercise']
        print('exercise',exercise_name)
        return redirect('/show_log/'+exercise_name)
    print("nice",exercise)
    init_db()
    exercise_name=exercise.lower()
    all_log=list(exercises_collection.find({"user": request.session['user'],"exercise_name": exercise_name}).sort('date',-1))
    if all_log==None:
        all_log=True
    print("leggo",all_log)
    results=[]
    items=get_videos(exercise_name)
    print(items)
    j=0
    for i in items:
        if j>4:
            break
        if j==0:
            classes="active"
        else:
            classes="carousel-item"
        title=i['snippet']['title']
        v_id=i['id']['videoId']
        thumbnail=i['snippet']['thumbnails']['medium']['url']
        results.append({'title':title, 'url':'https://www.youtube.com/embed/'+v_id+'?enablejsapi=1','thumbnail':thumbnail,'active':classes,'id':j})
        j+=1
    print(results,len(results))
    return render(request,'index.html',{'log':all_log,'exercise':exercise_name.upper(),'videos':results,range:[0,1,2,3,4]})

def logout(request):
    request.session.clear()
    return redirect('login')
 

