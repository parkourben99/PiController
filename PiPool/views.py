from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from PiPool.pin_controller import PinController

# Create the pin controller instance
controller = PinController()


@login_required(login_url="login/")
def dashboard(request):
    return render(request, "dashboard.html", controller.get_dashboard_data())


def setup(request):
    return render(request, "dashboard.html", controller.get_all_pins())


def pin_set(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")

    pin = request.POST['pin']
    state = request.POST['state']

    result = controller.set_pin_state(pin, state)
    return JsonResponse({'success': result})
