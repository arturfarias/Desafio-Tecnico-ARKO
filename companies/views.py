from utils.pagination import paginate_and_render
from django.contrib.auth.decorators import login_required

from .models import Company

@login_required
def companies(request):
    query = {
        'cnpj': request.GET.get('filter_cnpj', ''),
        'name': request.GET.get('filter_social', ''),
        'legal': request.GET.get('filter_natureza', ''),
        'size': request.GET.get('filter_porte', ''),
    }

    if not any(query.values()):
        companies = Company.objects.none()
    else:
        companies = Company.objects.filter(
            cnpj__icontains=query['cnpj'],
            name__icontains=query['name'],
            legal_nature__icontains=query['legal'],
            size__icontains=query['size'])


    return paginate_and_render(request, companies, 'companies/index.html')