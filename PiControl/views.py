from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, Http404, render_to_response
from django.template import RequestContext

from PiControl.models import Pin
from PiControl.models import Git
from PiControl.pin_controller import PinController
from .forms import PinForm

# Create the pin controller instance
pin_controller = PinController()


@login_required()
def dashboard(request):
    return render(request, "dashboard.html", pin_controller.get_dashboard_data())


@login_required(login_url="/login/")
def pins(request):
    return render(request, "pins/pins.html", pin_controller.get_all_pins())


@login_required(login_url="/login/")
def pin_create(request):
    return render(request, "pins/pin-create-edit.html", {'form': PinForm()})


@login_required(login_url="/login/")
def pin_delete(request, id):
    try:
        pin = pin_controller.my_pins.get(id=id)
    except Pin.DoesNotExist:
        raise Http404("Could not find that pin!")

    result = pin.delete()
    pin_controller.set_all_pins()

    # todo return bool not {object:bool}
    return JsonResponse({'success': result})


@login_required(login_url="/login/")
def pin_post(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/pins")

    id = request.POST.get('id')

    if id.isdigit():
        pin = pin_controller.my_pins.get(id=id)
    else:
        pin = Pin()

    form = PinForm(request.POST, instance=pin)

    if form.is_valid():
        form.save()
        pin_controller.set_all_pins()

        return HttpResponseRedirect("/pins")

    return render(request, "pins/pin-create-edit.html", {'form': form})


@login_required(login_url="/login/")
def pin_edit(request, id):
    try:
        pin = pin_controller.my_pins.get(id=id)
    except Pin.DoesNotExist:
        raise Http404("Could not find that pin!")

    form = PinForm(instance=pin)
    return render(request, "pins/pin-create-edit.html", {"form": form})


@login_required(login_url="/login/")
def pin_set(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/")

    pin_id = request.POST['pin']
    state = True if request.POST['state'] == '1' or request.POST['state'].lower() == 'true' else False
    result = False

    try:
        pin = pin_controller.my_pins.get(id=pin_id)
    except Pin.DoesNotExist:
        return JsonResponse({'success': False, 'state': state, 'message': 'Can not find pin'})

    pin.set_state(state)
    new_state = pin.get_state()

    if new_state == state:
        result = True

    return JsonResponse({'success': result, 'state': new_state})


@login_required(login_url="/login/")
def update(request):
    git = Git()

    if request.method == 'POST':
        result = git.update()

        return JsonResponse({'success': result})

    status = git.check()

    return render(request, "git/update.html", {"status": status})


@login_required(login_url="/login/")
def handler404(request):
    response = render_to_response('errors/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


@login_required(login_url="/login/")
def handler500(request):
    response = render_to_response('errors/500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response