from django.shortcuts import render
from utils.pagination import paginate_and_render

from .models import State, Municipality, District

def state(request):
    states = State.objects.select_related('region').all().order_by('name')

    query = request.GET.get('filter', '')

    if query:
        states = states.filter(name__icontains=query).order_by('name')

    return paginate_and_render(request, states, 'state/index.html')


def municipalities(request):
    municipalities = (
        Municipality.objects
        .select_related('microregion')
        .select_related('immediate_region')
        .all()
        .order_by('name')
    )

    query = request.GET.get('filter', '')

    if query:
        municipalities = municipalities.filter(name__icontains=query).order_by('name')

    return paginate_and_render(request, municipalities, 'municipalities/index.html')


def districts(request):
    districts = (
        District.objects
        .select_related('municipality')
        .all()
        .order_by('name')
    )

    query = request.GET.get('filter', '')

    if query:
        districts = districts.filter(name__icontains=query).order_by('name')

    return paginate_and_render(request, districts, 'districts/index.html')
