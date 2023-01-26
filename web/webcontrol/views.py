from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from web.settings import DEBUG
from webcontrol.tasks import controller

post_request_commands = {
    'emergency_stop': 0,
    'soft_stop': 0,
    'save': 0,
    'heater_w1': 0,
    'heater_w2': 0,
    'heater_w3': 0,
    'heater_st': 0,
    'valve': 0,
}

class Index(View):

    def get(self, request, *args, **kwargs):
        template = 'index.html'
        return render(request, template)

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()

        if(DEBUG):
            print(post_data)

        for ele in post_data.keys():
            if(ele in post_request_commands.keys()):
                post_request_commands[ele] = int(post_data[ele])

        if(post_request_commands['emergency_stop']):
            controller.emergency_shutdown()

        if(post_request_commands['soft_stop']):
            controller.soft_shutdown()

        controller.set_commands({
            'heater_1_power': post_request_commands['heater_w1'],
            'heater_2_power': post_request_commands['heater_w2'],
            'heater_3_power': post_request_commands['heater_w3'],
            'heater_steam_power': post_request_commands['heater_st'],
            'valve': post_request_commands['valve'],
        })

        controller.control_loop()

        if(post_request_commands['save']
            and not controller.data_save_started):
            controller.start_data_save()

        if(not post_request_commands['save']):
            controller.stop_data_save()

        template = 'index.html'
        return render(request, template)

class UpdateData(View):
    def get(self, request, *args, **kwargs):
        res = controller.get_output()
        return JsonResponse(res)

