from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, View
from django.utils.translation import gettext as _
from .tasks import hello, printer, complete_order
from datetime import datetime, timedelta, timezone
from .models import Order

class IndexView(TemplateView):
    # def get(self, request):
    #     # printer.delay(10)
    #     # printer.apply_async([10], countdown=5) #время в секундах до начала выполнения задачи
    #     printer.apply_async([10], eta=datetime.now(timezone.utc) + timedelta(seconds=5)) #конеретная дата-время начала выполнения задачи
    #     printer.apply_async([10], expires=600)) #конеретная дата-время или число(секунды), отмены задачи
    #     hello.delay()
    #     return HttpResponse('Hello!')

    template_name = "mc_donalds/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context

# форма нового заказа
class NewOrderView(CreateView):
    model = Order
    fields = ['products', 'staff']  # единственное поле
    template_name = 'mc_donalds/new.html'

    # после валидации формы, сохраняем объект,
    # считаем его общую стоимость
    # и вызываем задачу "завершить заказ" через минуту после вызова
    def form_valid(self, form):
        order = form.save()
        order.cost = sum([prod.price for prod in order.products.all()])
        order.save()
        complete_order.apply_async([order.pk], countdown=60)
        return redirect('/')

# представление для "кнопки", чтобы можно было забрать заказ
def take_order(request, oid):
    order = Order.objects.get(pk=oid)
    order.time_out = datetime.now()
    order.save()
    return redirect('/')


class Index(View):
    def get(self, request):
        string = _('Hello World')

        return HttpResponse(string)
