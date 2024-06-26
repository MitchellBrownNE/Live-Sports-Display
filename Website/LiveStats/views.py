from django.shortcuts import render
from .forms import UploadFileForm
from PIL import Image
import pytesseract
from django.conf import settings
import os
import TextParsing
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .SSH import run_stacked_display
from api_calls import SportsAPI
import time

@csrf_exempt
def run_ssh(request):
    if request.method == "POST":
        data = request.json
        action = data.get("action")
        
        if action == "stackedDisplay":
            response_message = run_stacked_display()
            return JsonResponse({"message": response_message})
    
    return JsonResponse({"message": "Invalid request"}, status=400)
    
#pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe" #requires local path
def handle_uploaded_file(f, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#2/19-Jordan
def home_view(request):
    return render(request, 'home.html')

#jordan testing git
#yuh

def upload_and_ocr(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Use TextParsing to process the image and extract player names
            arrayOfPlayerNames = TextParsing.imageToPlayerNames(file_path)
            # For demonstration, join names into a string to display. Adjust as necessary.
            playerNamesText = ', '.join(arrayOfPlayerNames)
            return render(request, 'result.html', {'text': playerNamesText})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

""" #old function 
def upload_and_ocr(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            text = OCR_Image(file_path)
            return render(request, 'result.html', {'text': text})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
"""

def OCR_Image(path):
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return text


## API calls ##
def Get_League_Standings(request):
    API = SportsAPI()
    standings = API.get_league_standings()

    return render(request, 'league_standings.html', {'standings': standings})

def Get_Game_Schedule(request):
    API = SportsAPI()
    schedule = API.get_current_schedule()

    return render(request, 'game_schedule.html', {'schedule': schedule})

def Get_Live_Team_Stats(request):
    inputted_team_name = request.GET.get('inputted_team_name', '')
    API = SportsAPI()
    stats = API.get_live_team_stats(inputted_team_name)

    context = {
        'stats': stats,
        'inputted_team_name': inputted_team_name
    }
    return render(request, 'live_team_stats.html', context)

def Get_Live_Game_Stats(request):
    inputted_team_name = request.GET.get('inputted_team_name', '')
    API = SportsAPI()
    stats = API.get_live_game_stats(inputted_team_name)

    context = {
        'stats': stats,
        'inputted_team_name': inputted_team_name
    }
    return render(request, 'live_game_stats.html', context)

def Get_Live_Player_Stats(request):
    inputted_player_name = request.GET.get('inputted_player_name', '')
    API = SportsAPI()
    stats = API.get_live_player_stats(inputted_player_name)

    context = {
        'stats': stats,
        'inputted_player_name': inputted_player_name
    }
    return render(request, 'live_player_stats.html', context)

def Get_Live_OCR_Roster_Stats(request):
    OCR_Names = request.POST.getlist('players[]')
    API = SportsAPI()
    StatsArray = []
    
    for name in OCR_Names:
        stat = API.get_live_player_stats(name)
        StatsArray.append(stat)
        time.sleep(2)
        
    context = {
        'NamesArray': OCR_Names,
        'StatsArray': StatsArray
        }
    return render(request, 'OCRStats.html',context)

def stats_page(request):
    return render(request, 'stats_page.html')
