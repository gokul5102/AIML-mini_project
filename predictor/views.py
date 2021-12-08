from django.shortcuts import render
# from django.http import reponse

# Create your views here.
# Importing essential libraries
import pickle
import numpy as np

# Load the Random Forest CLassifier model

filename = r'C:\Users\Gokul\Desktop\match-predictor\first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))



filename_rf = r'C:\Users\Gokul\Desktop\match-predictor\randomForest_jr.pkl'

rf = pickle.load(open(filename_rf, 'rb'))

filename_knc = r'C:\Users\Gokul\Desktop\match-predictor\knc_jr.pkl'

knc = pickle.load(open(filename_knc, 'rb'))

def home(request):
	return render(request, 'index.html')

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

        
        res = {'result':result, 'result_knc' : result_knc,'result_rf':result_rf}

        return render(request, 'result.html', res)

