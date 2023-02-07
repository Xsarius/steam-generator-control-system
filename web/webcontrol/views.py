from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, FileResponse, HttpResponseBadRequest
from web.settings import DEBUG, DOWNLOAD_FILES_PATH
from webcontrol.tasks import controller
import os

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
        res = controller.get_output()
        return JsonResponse(res)

class DownloadFileView(View):
    def post(self, request):
        file_name = request.POST.get('file_name')
        file_data = controller.get_data_from_db()
        file_path = os.path.join(DOWNLOAD_FILES_PATH, file_name)

        with open(file_path, "w") as file:
            file.write(file_data)
            response = FileResponse(file)
            response['content_type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.file_name)

        return response

    def get(self, request):
        return HttpResponseBadRequest()