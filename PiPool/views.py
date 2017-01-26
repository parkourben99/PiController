from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from PiPool.controllers.pin_controller import PinController

# Create the pin controller instance
controller = PinController()


@login_required(login_url="login/")
def dashboard(request):
    return render(request, "dashboard.html", controller.get_dashboard_data())
