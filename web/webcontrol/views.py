from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from web.settings import DOWNLOAD_FILES_PATH
from webcontrol.tasks import controller, curr_id
import os, json

class Index(View):

    def get(self, request, *args, **kwargs):
        template = 'index.html'
        return render(request, template)

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()

        print(post_data)

        for ele in post_data.keys():
            controller.control_params[ele] = int(post_data[ele])

        if(controller.control_params['emergency_stop']):
            controller.emergency_shutdown()

        if(controller.control_params['soft_stop']):
            controller.soft_shutdown()

        if(controller.control_params['manual_mode']):
            controller.control_loop()

        if(controller.control_params['temp_setpoint']):
            controller.pid.setpoint = controller.control_params['temp_setpoint']

        if(controller.control_params['save']
            and not controller.data_save_started):
            controller.start_data_save()

        if(not controller.control_params['save']
            and controller.data_save_started):
            controller.stop_data_save()

        controller.control_loop()

        template = 'index.html'
        return render(request, template)

class UpdateData(View):
    def get(self, request, *args, **kwargs):
        res = controller.output

        return JsonResponse(res)

    def post(self, request):
        return HttpResponseBadRequest()

class DownloadFileView(View):
    def get(self, request):
        return HttpResponseBadRequest()

    def post(self, request):
        file_data = controller.get_data_from_db()

        return JsonResponse(file_data)
