from django.core.paginator import Paginator
from django.shortcuts import render

def paginate_and_render(request, queryset, template_name, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, template_name, {'page_obj': page_obj})