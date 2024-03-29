from django.shortcuts import render

from django.shortcuts import render
from django.template import RequestContext


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию;
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, 'core/404.html', {'path': request.path}, status=404)

def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')

def server_error(request, *args, **argv):
    return render(request, 'core/500.html', status=500)

