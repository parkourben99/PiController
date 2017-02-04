from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, Http404, render_to_response
from django.template import RequestContext

from PiPool.models import Pin
from PiPool.pin_controller import PinController

# Create the pin controller instance
controller = PinController()


@login_required(login_url="login/")
def dashboard(request):
    return render(request, "dashboard.html", controller.get_dashboard_data())


def pins(request):
    return render(request, "pins.html", controller.get_all_pins())


def pin_create(request):
    return render(request, "pin-create.html", {})


def pin_delete(request, id):
    try:
        pin = controller.my_pins.get(id=id)
    except Pin.DoesNotExist:
        raise Http404("Could not find that pin!")

    result = pin.delete()
    controller.set_all_pins()

    return JsonResponse({'success': result})


def pin_create_post(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")

    name = request.POST.get('name')
    pin_number = request.POST.get('pin_number')
    description = request.POST.get('description')
    is_thermometer = request.POST.get('is_thermometer', False)

    try:
        pin = Pin()
        pin.pin_number = pin_number
        pin.description = description
        pin.is_thermometer = is_thermometer
        pin.name = name
        pin.save()

        controller.set_all_pins()

        return HttpResponseRedirect("/pins")
    except:
        # todo send them back and try again
        return HttpResponseRedirect("/")


def pin_edit(request, id):
    try:
        pin = controller.my_pins.get(id=id)
    except Pin.DoesNotExist:
        raise Http404("Could not find that pin!")

    return render(request, "pin-create.html", {"pin": pin})


def pin_set(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")

    pin_id = request.POST['pin']
    state = request.POST['state']
    result = False

    try:
        pin = controller.my_pins.get(id=pin_id)
    except Pin.DoesNotExist:
        return JsonResponse({'success': False, 'state': state})

    pin.set_state(state)
    new_state = pin.get_state()

    if new_state == state:
        result = True

    return JsonResponse({'success': result, 'state': new_state})


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response