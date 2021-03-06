from django.contrib.auth.models import User
from django.shortcuts import render,redirect

from predictor.models import Query
# from django.http import reponse
from .forms import RegisterForm,LoginForm
from django.views.generic import View
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
# Create your views here.
# Importing essential libraries
import pickle
import numpy as np
from django.contrib import messages
# from .models import User
from django.contrib.auth.hashers import make_password

# Load the Random Forest CLassifier model

filename = r'C:\Users\Asus\Desktop\AIML project\AIML-mini_project\pkl files\first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))



filename_rf = r'C:\Users\Asus\Desktop\AIML project\AIML-mini_project\pkl files\randomForest_jr.pkl'

rf = pickle.load(open(filename_rf, 'rb'))

filename_knc = r'C:\Users\Asus\Desktop\AIML project\AIML-mini_project\pkl files\knc_jr.pkl'

knc = pickle.load(open(filename_knc, 'rb'))

def home(request):
    print(request.user)
    if(request.user.is_authenticated):
        return render(request, 'index.html',{'user': True,'username':request.user.username})
    return render(request, 'index.html',{'user': False})
    

def predict(request):
    temp_array = list()
    
    if request.method == 'POST':
        
        batting_team = request.POST['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        bowling_team = request.POST['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        overs = float(request.POST['overs'])
        runs = int(request.POST['runs'])
        wickets = int(request.POST['wickets'])
        runs_in_prev_5 = int(request.POST['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.POST['wickets_in_prev_5'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        data = np.array([temp_array])
        result = int(regressor.predict(data)[0])

        result_rf = int(rf.predict(data)[0])
        result_knc = int(knc.predict(data)[0])

        q= Query.objects.create(user= request.user.username,
                                bat_team= batting_team,
                                bowl_team= bowling_team,
                                overs = overs,
                                runs =runs,
                                wickets = wickets,
                                runs_in_prev_5 = runs_in_prev_5,
                                wickets_in_prev_5 = wickets_in_prev_5,
                                logistic_result = result,
                                random_forest_result =result_rf ,
                                knn_result =result_knc )
        q.save()
        res = {'result':result, 'result_knc' : result_knc,'result_rf':result_rf,"username":request.user.username}

        return render(request, 'result.html', res)

@login_required
def history(request):
    user=request.user.username
    data=Query.objects.filter(user=user)
    for i in data:
        print(i.user)
    return render(request, 'history.html',{'user': True,'username':request.user.username,'data':data})
 

class register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("11")
            data=request.POST
            print(type(data['password']))
            c=User.objects.create_user(username=data['username'],email=data['email'],password=data["password"])
            c.save()
            # messages.success(request,f'Your account has been created ! You are now able to login')
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form,'errors':form.errors})

class loginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        print(request.POST['username'])
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
            # messages.error(request,f'Wrong credentials!Unable to login')
            
        return render(request, 'login.html', {'form': form,'error':"Username or password incorrect."})


