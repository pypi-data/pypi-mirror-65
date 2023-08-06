import inspect

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView


class BasicDatatableView(BaseDatatableView):
    search_columns = []

    def search_qs(self, qs, search):
        filters = []
        for search_column in self.search_columns:
            filters.append(Q(**{f'{search_column}__icontains': search}))
        if len(filters) > 0:
            f = filters[0]
            for _filter in filters[1:]:
                f |= _filter
            qs = qs.filter(f)
        return qs

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = self.search_qs(qs, search)
        return qs


class BasicDeleteView(DeleteView):

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return JsonResponse({"success": "success"})


class AllInOne:
    namespace = None
    all_model = None
    include_template_name = 'shared/main.html'
    errors_template = 'shared/form-errors.html'
    shared_messages = 'shared/messages.html'

    create_model = None
    create_template = 'behko_django_basic/all_in_one.html'
    create_form_title = None
    create_form_class = None
    create_success_message = None
    create_failure_message = None

    update_model = None
    update_form_title = None
    update_form_class = None
    update_success_message = None
    update_failure_message = None
    update_template = 'behko_django_basic/all_in_one_update.html'

    delete_model = None

    datatable_title = None
    datatable_model = None
    datatable_name = None
    datatable_column_names = None
    datatable_columns = None
    datatable_order = None
    search_columns = []
    extra_context_data = {}
    _os = []

    def get_os(self, pattern):
        os = []
        if len(self._os) > 0:
            os = self._os
        else:
            os = inspect.getmembers(self, inspect.ismethod)
            self._os = os
        return list(filter(lambda x: pattern in x[0], os))

    def override(self, klass, pattern):
        for o in self.get_os(pattern):
            generated_name = o[0].replace(pattern, '')

            def rp(s):
                return getattr(super(klass, s), generated_name)

            setattr(klass, generated_name, o[1](klass, rp))

    def get_create_class(self):
        if hasattr(self.__class__, 'Create'):
            return getattr(self.__class__, 'Create')

        oo = self

        class Create(CreateView):
            model = self.all_model if self.all_model else self.create_model
            form_class = self.create_form_class
            template_name = self.create_template
            success_url = reverse_lazy(self.namespace + ':create')

            def form_valid(self, form):
                response = super().form_valid(form)
                messages.success(self.request, oo.create_success_message)
                return response

            def form_invalid(self, form):
                response = super().form_invalid(form)
                messages.error(self.request, oo.create_failure_message)
                return response

            def get_context_data(self, **kwargs):
                context = super(Create, self).get_context_data(**kwargs)
                context.update({
                    'namespace': oo.namespace,
                    'include_template_name': oo.include_template_name,
                    'errors_template': oo.errors_template,
                    'shared_messages': oo.shared_messages,
                    'create_form_title': oo.create_form_title,
                    'datatable_title': oo.datatable_title,
                    'datatable_column_names': oo.datatable_column_names,
                    'datatable_name': oo.datatable_name,
                })
                return context

        self.override(Create, 'o_c_')
        return Create

    def get_update_class(self):
        if hasattr(self.__class__, 'Update'):
            return getattr(self.__class__, 'Update')
        oo = self

        class Update(UpdateView):
            model = self.all_model if self.all_model else self.update_model
            template_name = self.update_template
            form_class = self.update_form_class
            success_url = reverse_lazy(self.namespace + ':create')

            def form_valid(self, form):
                response = super().form_valid(form)
                messages.success(self.request, oo.update_success_message)
                return response

            def form_invalid(self, form):
                response = super().form_invalid(form)
                messages.error(self.request, oo.update_success_message)
                return response

            def get_context_data(self, **kwargs):
                context = super(Update, self).get_context_data(**kwargs)
                context.update({
                    'namespace': oo.namespace,
                    'success_url': reverse_lazy(oo.namespace + ':create'),
                    'include_template_name': oo.include_template_name,
                    'errors_template': oo.errors_template,
                    'shared_messages': oo.shared_messages,
                    'update_form_title': oo.update_form_title
                })
                return context

        self.override(Update, 'o_u_')
        return Update

    def get_datatable_class(self):
        if hasattr(self.__class__, 'Datatable'):
            return getattr(self.__class__, 'Datatable')

        class Datatable(BasicDatatableView):
            model = self.all_model if self.all_model else self.datatable_model
            columns = self.datatable_columns
            search_columns = self.search_columns
            if self.datatable_order is None:
                order_columns = self.datatable_columns
            else:
                order_columns = self.datatable_order

        self.override(Datatable, 'o_d_')
        return Datatable

    def get_delete_class(self):
        if hasattr(self.__class__, 'Delete'):
            return getattr(self.__class__, 'Delete')

        class Delete(BasicDeleteView):
            model = self.all_model if self.all_model else self.delete_model

        self.override(Delete, 'o_del_')
        return Delete
