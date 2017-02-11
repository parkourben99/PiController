from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, Http404, render_to_response
from django.template import RequestContext

from PiPool.models import Pin
from PiPool.models import Git
from PiPool.pin_controller import PinController
from .forms import PinForm

# Create the pin controller instance
controller = PinController()


@login_required(login_url="login/")
def dashboard(request):
    return render(request, "dashboard.html", controller.get_dashboard_data())


@login_required(login_url="login/")
def pins(request):
    return render(request, "pins/pins.html", controller.get_all_pins())


@login_required(login_url="login/")
def pin_create(request):
    return render(request, "pins/pin-create-edit.html", {'form': PinForm()})


@login_required(login_url="login/")
def pin_delete(request, id):
    try:
        pin = controller.my_pins.get(id=id)
    except Pin.DoesNotExist:
        raise Http404("Could not find that pin!")

    result = pin.delete()
    controller.set_all_pins()

    return JsonResponse({'success': result})


@login_required(login_url="login/")
def pin_post(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/pins")

    pin = Pin()
    form = PinForm(request.POST, instance=pin)

    if form.is_valid():
        form.save()
        controller.set_all_pins()

        return HttpResponseRedirect("/pins")

    return render(request, "pins/pin-create-edit.html", {'form': form})


@login_required(login_url="login/")
def pin_edit(request, id):
    try:
        pin = controller.my_pins.get(id=id)
    except Pin.DoesNotExist:
        raise Http404("Could not find that pin!")

    form = PinForm(instance=pin)

    return render(request, "pins/pin-create-edit.html", {"pin": form})


@login_required(login_url="login/")
def pin_set(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")

    pin_id = request.POST['pin']
    state = True if request.POST['state'] == '1' or request.POST['state'].lower() == 'true' else False
    result = False

    try:
        pin = controller.my_pins.get(id=pin_id)
    except Pin.DoesNotExist:
        return JsonResponse({'success': False, 'state': state, 'message': 'Can not find pin'})

    pin.set_state(state)
    new_state = pin.get_state()

    if new_state == state:
        result = True

    return JsonResponse({'success': result, 'state': new_state})


@login_required(login_url="login/")
def update(request):
    git = Git()
    status = git.check()

    if request.method == 'POST':
        result = False

        if status:
            result = git.update()

        return JsonResponse({'success': result})

    return render(request, "git/update.html", {"status": status})


@login_required(login_url="login/")
def handler404(request):
    response = render_to_response('errors/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


@login_required(login_url="login/")
def handler500(request):
    response = render_to_response('errors/500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response