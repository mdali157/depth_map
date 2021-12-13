import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from depth.settings import BASE_DIR
from .models import File
from django.contrib import messages
from datetime import datetime
from PIL import Image


@login_required(login_url='/admin/login/')
def home_page(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file_input')
        choosen_algorithm = request.POST.get('select_input')

        if not choosen_algorithm:
            choosen_algorithm = "0"

        current_date_time = datetime.now()
        year = str(current_date_time.strftime("%Y"))
        month = str(current_date_time.strftime("%m"))
        day = str(current_date_time.strftime("%d"))
        time = str(current_date_time.strftime("%H%M%S"))

        uploaded_file_name = year + "_" + month + "_" + day + "_" + time
        existing_name = uploaded_file.name
        uploaded_file.name = uploaded_file_name + "." + existing_name.split(".")[-1]

        file_object = File(name=uploaded_file)
        file_object.save()

        media_dir_path = os.path.join(BASE_DIR, 'media/')
        image = os.path.join(BASE_DIR, 'media/') + uploaded_file.name
        command = "mkdir " + media_dir_path + uploaded_file_name + "&& mkdir " + media_dir_path + uploaded_file_name + "/input" + "&& mkdir " + media_dir_path + uploaded_file_name + "/output" + " && cp " + image + " " + media_dir_path + uploaded_file_name + "/input/" + " && cd /home/ubuntu/BoostingMonocularDepth/" + " && /home/ubuntu/anaconda3/envs/pytorch_p37/bin/python run.py --Final --data_dir " + media_dir_path + uploaded_file_name + "/input/" + " --output_dir " + media_dir_path + uploaded_file_name + "/output/" + " --depthNet " + choosen_algorithm
        os.system(command)

        image = os.path.join(BASE_DIR, 'media/' + uploaded_file_name + '/output/' + uploaded_file_name + '.png')

        with open(image, 'rb') as img:
            response = HttpResponse(img.read(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename=' + existing_name.split(".")[0] + "D.png"
        return response
    return render(request, 'landing_page/home.html')
