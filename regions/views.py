from utils.pagination import paginate_and_render
from django.contrib.auth.decorators import login_required


from .models import State, Municipality, District

@login_required()
def state(request):
    states = State.objects.select_related('region').all().order_by('name')

    query = request.GET.get('filter', '')

    if query:
        states = states.filter(name__icontains=query).order_by('name')

    return paginate_and_render(request, states, 'state/index.html')

@login_required()
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

@login_required()
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
