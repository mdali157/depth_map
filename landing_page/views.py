import os
import subprocess
from subprocess import call

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from depth.settings import BASE_DIR
from .models import File
from django.contrib import messages
from datetime import datetime
from PIL import Image

# Create your views here.
def home_page(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file_input')
        current_date_time = datetime.now()
        year = str(current_date_time.strftime("%Y"))
        month = str(current_date_time.strftime("%m"))
        day = str(current_date_time.strftime("%d"))
        time = str(current_date_time.strftime("%H%M%S"))

        uploaded_file.name = year + "_" + month + "_" + day + "_" + time + ".png"

        file_object = File(name=uploaded_file)
        file_object.save()
        file = os.path.join(BASE_DIR, 'media') + "/" + uploaded_file.name
        resize_command = "mogrify -resize 50% " + file
        os.system(resize_command)
        messages.success(request, 'File submitted and saved successful')
        with open(file, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename=' + uploaded_file.name
        return response
    return render(request, 'landing_page/home.html')
