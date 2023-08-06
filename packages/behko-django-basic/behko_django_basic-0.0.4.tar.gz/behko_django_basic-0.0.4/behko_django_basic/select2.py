from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.views import View


class Select2(View):
    """
    کلاس اصلی select2 است

    این کلاس برای صرفه جویی در زمان برای فیلد های select که اطلاعاتشان
    را از پایگاه داده میخانند ایجاد شده است و از Ajax استفاده میکند و همچنین
    قابلیت جستجو به کاربر میدهد
    """
    model = None
    id = 'id'
    text = 'title'
    per_page = 20

    def get_model(self):
        if self.model is None:
            thing = get_user_model().objects.all()
            return thing
        else:
            if hasattr(self.model, 'objects'):
                self.model = self.model.objects
            return self.model

    def get(self, request):
        page = request.GET.get('page', 1)
        search = request.GET.get('search')

        thing = self.get_model()

        if search is not None and len(search.strip()) > 0:
            thing = self.searching(search, thing)

        if self.id != 'id':
            thing = thing.annotate(id=self.get_id(), text=self.get_text())
        else:
            thing = thing.annotate(text=self.get_text())

        thing = thing.values('id', 'text')
        paginator = Paginator(thing, self.per_page)
        results = paginator.page(int(page)).object_list
        results_bitten = list(results)
        return JsonResponse({
            'results': results_bitten,
            "pagination": {
                "more": paginator.page(page).has_next()
            }
        }, safe=False)

    def get_text(self):
        return F(self.text)

    def get_id(self):
        return F(self.id)

    def searching(self, search, thing):
        return thing.filter(**{self.text + '__contains': search})
