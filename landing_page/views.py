import os
from django.http import HttpResponse
from django.shortcuts import render
from depth.settings import BASE_DIR
from .models import File
from django.contrib import messages
from datetime import datetime


def home_page(request):
    """
    this function will get the file uploaded by the user, alter it's name to current date and time.
    the name of file will look like this "2021_11_27_134724.png"
    file will be saved and resized to 50% and the compressed file will be send as a response
    """
    if request.method == "POST":
        uploaded_file = request.FILES.get('file_input')
        # getting current date and time
        current_date_time = datetime.now()
        # separating year,month,date and time to individual varibale
        year = str(current_date_time.strftime("%Y"))
        month = str(current_date_time.strftime("%m"))
        day = str(current_date_time.strftime("%d"))
        time = str(current_date_time.strftime("%H%M%S"))

        # renaming the uploaded file to time stamp
        uploaded_file.name = year + "_" + month + "_" + day + "_" + time + ".png"

        file_object = File(name=uploaded_file)
        file_object.save()

        image = os.path.join(BASE_DIR, 'media/') + uploaded_file.name
        # command that will resize the image
        resize_command = "mogrify -resize 50% " + image
        os.system(resize_command)
        messages.success(request, 'File submitted and saved successful')
        #  sending modified file as a response
        with open(image, 'rb') as img:
            response = HttpResponse(img.read(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename=' + uploaded_file.name
        return response
    return render(request, 'landing_page/home.html')
