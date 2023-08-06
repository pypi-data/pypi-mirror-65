# -*- coding: utf-8 -*-
import traceback
from django.apps import apps
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.static import serve
from djangoplus.cache import CACHE
from djangoplus.utils import permissions
from django.http import HttpResponseRedirect
from djangoplus.utils.http import return_response
from djangoplus.utils.serialization import json_serialize
from djangoplus.utils.storage import dropbox
from jinja2 import Template
from django.views.defaults import page_not_found
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from djangoplus.ui.components.forms import factory
from django.views.decorators.csrf import csrf_exempt
from djangoplus.ui.components.panel import ModelDashboard
from django.http.response import HttpResponseForbidden
from djangoplus.ui.components import ComponentHasResponseException
from djangoplus.ui.components.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from djangoplus.db.models import QuerySet
from djangoplus.ui.components.navigation.breadcrumbs import httprr
from djangoplus.utils.metadata import list_related_objects, is_many_to_many, is_one_to_one, get_metadata, \
    check_condition, is_one_to_many, getattr2, is_one_to_many_reverse, get_parameters_names, count_parameters_names, \
    get_role_value_for_action, get_role_values_for_condition
from django.contrib import auth

def listt(request, app, cls, subset=None):

    if not request.user.is_authenticated:
        return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))

    try:
        _model = apps.get_model(app, cls)
    except LookupError as e:
        return page_not_found(request, e, 'error404.html')
    title = get_metadata(_model, 'verbose_name_plural')
    subsetp = None
    list_display = None
    list_filter = None
    search_fields = None
    if subset:
        subset_func = getattr(_model.objects.get_queryset(), subset)
        can_view = get_metadata(subset_func, 'can_view')
        list_display = get_metadata(subset_func, 'list_display')
        list_filter = get_metadata(subset_func, 'list_filter')
        search_fields = get_metadata(subset_func, 'search_fields')
        title = '{} - {}'.format(title, get_metadata(subset_func, 'verbose_name'))
    else:
        tid = request.GET.get('tid')
        subsetp = request.GET.get('tab{}'.format(tid))
        if tid and subsetp:
            subset_func = getattr(_model.objects.get_queryset(), subsetp)
            subset_title = get_metadata(subset_func, 'verbose_name')
            can_view = get_metadata(subset_func, 'can_view')
            title = '{} - {}'.format(title, get_metadata(subset_func, 'verbose_name'))
            if not permissions.check_group_or_permission(request, can_view):
                return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))
        else:
            permission = '{}.list_{}'.format(app, cls)
            if not request.user.has_perm(permission):
                return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))

    qs = _model.objects.all(request.user)
    if subset:
        subset_func = getattr(qs, subset)
        parameters = get_role_values_for_condition(subset_func, request.user)
        qs = subset_func(*parameters)
    list_subsets = subset and [subset] or None

    paginator = Paginator(request, qs, title, list_subsets=list_subsets, is_list_view=True,
                          list_display=list_display, list_filter=list_filter, search_fields=search_fields)
    paginator.process_request()

    paginator.load_actions()
    return render(request, 'default.html', locals())


def add(request, app, cls, pk=None, related_field_name=None, related_pk=None):

    if not request.user.is_authenticated:
        return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))

    try:
        _model = apps.get_model(app, cls)
    except LookupError as e:
        return page_not_found(request, e, 'error404.html')

    obj = pk and _model.objects.all(request.user).filter(pk=pk).first() or _model()
    obj.request = request
    obj._user = request.user

    title = pk and str(obj) or get_metadata(_model, 'verbose_name')

    if related_field_name is None:

        if obj.pk:
            if not permissions.has_edit_permission(request, _model) or not permissions.can_edit(request, obj):
                return HttpResponseForbidden()
        else:
            if not permissions.has_add_permission(request, _model) or not permissions.can_add(request, obj):
                return HttpResponseForbidden()

        form = factory.get_register_form(request, obj)
        title = form.title

    elif is_one_to_many(_model, related_field_name):
        if not permissions.can_add(request, obj) and not permissions.can_edit(request, obj):
            return HttpResponseForbidden()
        form = factory.get_one_to_many_form(request, obj, related_field_name)

    elif is_many_to_many(_model, related_field_name):
        if not permissions.can_edit_field(request, obj, related_field_name):
            return HttpResponseForbidden()
        form = factory.get_many_to_many_form(request, obj, related_field_name, related_pk)

    elif is_one_to_many_reverse(_model, related_field_name):
        form = factory.get_many_to_many_reverse_form(request, obj, related_field_name)

    elif is_one_to_one(_model, related_field_name):
        if not permissions.can_add(request, obj) and not permissions.can_edit(request, obj):
            return HttpResponseForbidden()
        form = factory.get_one_to_one_form(request, obj, related_field_name, related_pk)
    else:
        # many to one
        for rel in list_related_objects(_model):
            if hasattr(rel, 'get_accessor_name'):
                if rel.get_accessor_name() in ('{}_set'.format(related_field_name), related_field_name):
                    related_queryset = rel.related_model.objects.all(request.user)
                    related_obj = related_pk and related_queryset.get(pk=related_pk) or rel.related_model()
                    related_obj.request = request
                    setattr(related_obj, rel.field.name, obj)
                    setattr(related_obj, '{}_id'.format(rel.field.name), obj.pk)
                    if related_pk:
                        if not permissions.has_edit_permission(
                                request, rel.related_model) or not permissions.can_edit(request, related_obj):
                            return HttpResponseForbidden()
                    else:
                        if not permissions.has_add_permission(
                                request, rel.related_model) or not permissions.can_add(request, related_obj):
                            return HttpResponseForbidden()
                    form = factory.get_many_to_one_form(request, obj, rel.get_accessor_name(), related_obj)
                    title = form.title

    if form.is_valid():
        is_editing = form.instance.pk is not None
        try:
            form.save()
            obj = form.instance
            if 'select' in request.GET:
                return HttpResponse('{}|{}|{}'.format(obj.pk, obj, request.GET['select']));
            elif related_field_name:
                message = _('Action successfully performed.')
                url = '..'
            else:
                message = get_metadata(form.instance.__class__, 'add_message')
                if message and not is_editing:
                    if hasattr(obj, 'get_absolute_url'):
                        url = obj.get_absolute_url()
                    else:
                        url = '/view/{}/{}/{}/'.format(
                            get_metadata(obj.__class__, 'app_label'), obj.__class__.__name__.lower(), obj.pk)
                else:
                    url = '..'
                if is_editing:
                    message = message or _('Action successfully performed.')
                else:
                    message = message or _('Registration successfully performed.')
            return httprr(request, url, message)
        except ValidationError as e:
            form.add_error(None, str(e.message))
    return render(request, 'default.html', locals())


def view(request, app, cls, pk, tab=None):

    if not request.user.is_authenticated:
        return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))

    try:
        _model = apps.get_model(app, cls)
    except LookupError as e:
        return page_not_found(request, e, 'error404.html')

    obj = _model.objects.all(request.user).filter(pk=pk).first()
    obj.request = request
    obj._user = request.user

    if 'one_to_many_count' in request.GET:
        # TODO create a specific view for this purpose
        return HttpResponse(getattr2(obj, request.GET['one_to_many_count']))

    if not permissions.can_view(request, obj):
        return HttpResponseForbidden()

    title = str(obj)
    parent = request.GET.get('parent', None)
    printable = get_metadata(_model, 'pdf', False)
    widget_panel = ModelDashboard(request, obj, tab, parent, printable=printable)
    widget_panel.process_request()

    if widget_panel.model_panel.message:
        return httprr(request, request.get_full_path(), widget_panel.model_panel.message)

    log_data = get_metadata(obj.__class__, 'log', False)
    if log_data and request.user.is_superuser and request.user.has_perm('admin.list_log'):
        url = '/log/{}/{}/'.format(app, cls)
        widget_panel.model_panel.drop_down.add_action('{} {}'.format(_('View'), _('Log')), url, 'ajax', 'fa fa-history')

    return render(request, 'default.html', locals())


def action(request, app, cls, action_name, pk=None):

    if not request.user.is_authenticated:
        return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))

    try:
        _model = apps.get_model(app, cls)
    except LookupError as e:
        return page_not_found(request, e, 'error404.html')

    for group in CACHE['INSTANCE_ACTIONS'][_model]:
        if action_name in CACHE['INSTANCE_ACTIONS'][_model][group]:
            break

    form_action = CACHE['INSTANCE_ACTIONS'][_model][group][action_name]
    action_verbose_name = form_action['verbose_name']
    action_can_execute = form_action['can_execute']
    action_condition = form_action['condition']
    action_function = form_action['function']
    action_message = 'message' in form_action and form_action['message'] or None
    action_permission = '{}.{}'.format(_model._meta.app_label, action_function.__name__)
    action_input = form_action['input']
    action_display = form_action['display']
    action_style = form_action['style']
    action_redirect = form_action['redirect_to']

    obj = pk and _model.objects.all(request.user).distinct().get(pk=pk) or _model()
    obj.request = request
    obj._user = request.user
    title = action_verbose_name
    redirect_to = None

    if check_condition(request.user, action_condition, obj) and (
            not action_can_execute or permissions.check_group_or_permission(request, action_permission)):
        f_return = None
        func = getattr(_model, action_function.__name__, action_function)
        form = factory.get_action_form(request, obj, form_action)

        if form.fields and form.is_valid() or not form.fields:
            if 'instance' in form.fields:
                obj = form.cleaned_data['instance']
            func = getattr(obj, action_function.__name__, action_function)
            params = []
            for param in get_parameters_names(func, include_annotated=True):
                if param in form.cleaned_data:
                    params.append(form.cleaned_data[param])
                else:
                    params.append(get_role_value_for_action(func, request.user, param))
            try:
                f_return = func(*params)
                if not action_redirect:
                    if count_parameters_names(func) > 0 or action_display:
                        redirect_to = '..'
                    else:
                        redirect_to = '.'
                else:
                    redirect_to = Template(action_redirect).render(obj=obj)
            except ValidationError as e:
                if form.fields:
                    form.add_error(None, e.message)
                    redirect_to = None
                else:
                    return httprr(request, '.', e.message, error=True)

        if f_return and type(f_return) != str:
            template_name = '{}.html'.format(action_function.__name__)
            return return_response(f_return, request, title, action_style, template_name)

        elif redirect_to:
            return httprr(request, redirect_to, f_return or action_message)

        if form.title == _('Form'):
            form.title = action_verbose_name
        if form.submit_label == _('Send'):
            form.submit_label = action_verbose_name
        return render(request, 'default.html', locals())
    else:
        return HttpResponseForbidden()


def delete(request, app, cls, pk, related_field_name=None, related_pk=None):

    if not request.user.is_authenticated:
        return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))

    try:
        _model = apps.get_model(app, cls)
    except LookupError as e:
        return page_not_found(request, e, 'error404.html')

    obj = _model.objects.all(request.user).get(pk=pk)
    obj._request = request
    obj._user = request.user

    if permissions.can_delete(request, obj):
        if related_field_name:
            getattr(obj, related_field_name).remove(related_pk)
            return httprr(request, '..', _('Deletion successfully performed.'))
        else:
            title = '{} {}'.format(_('Delete'), str(obj))
            form = factory.get_delete_form(request, obj)
            if form.is_valid():
                obj.delete()
                return httprr(request, '..', _('Action successfully performed.'))
            return render(request, 'delete.html', locals())
    else:
        return HttpResponseForbidden()


def log(request, app, cls, pk=None):

    if not request.user.is_authenticated:
        return httprr(request, '/admin/login/?next={}'.format(request.get_full_path()))

    try:
        _model = apps.get_model(app, cls)
    except LookupError as e:
        return page_not_found(request, e, 'error404.html')

    if pk:
        obj = _model.objects.get(pk=pk)
        qs = obj.get_logs()
        title = 'Log - {}'.format(obj)
    else:
        content_type = ContentType.objects.get_for_model(_model)
        qs = content_type.log_set.all()
        title = 'Logs - {}'.format(get_metadata(_model, 'verbose_name_plural'))

    paginator = Paginator(request, qs, 'Log')
    return render(request, 'default.html', locals())


def dispatcher(request, app, view_name, params):

    params = params.split('/')[0:-1]

    full_app_name = settings.APP_MAPPING.get(app, app)
    fromlist = full_app_name.split('.')

    try:
        views = __import__('{}.views'.format(full_app_name), fromlist=list(map(str, fromlist)))
        func = getattr(views, view_name)
    except ComponentHasResponseException as e:
        raise e
    except (ImportError, TypeError, AttributeError) as e:
        traceback.print_exc()
        return page_not_found(request, e, 'error404.html')

    try:
        return func(request, *params)
    except ComponentHasResponseException as e:
        raise e
    except Exception as e:
        print(e)
        traceback.print_exc()
        #return server_error(request, 'error500.html')
        raise e


def cloud(request, path, document_root=None, show_indexes=False):
    storage = dropbox.DropboxStorage()
    if storage.exists_locally(path):
        return serve(request, path, document_root=document_root, show_indexes=show_indexes)
    else:
        return HttpResponseRedirect(storage.remote_url('/{}'.format(path)))


@csrf_exempt
def api(request, app_label, model_name, arg1=None, arg2=None):
    from djangoplus.admin.models import User

    obj = None
    form = None
    result = None
    errors = None
    func_name = None
    message = None
    args = {}

    http_authorization = request.META.get('HTTP_AUTHORIZATION')
    if http_authorization and 'Token' in http_authorization:
            page= int(request.GET.get('page', '') or 0)
            token = http_authorization[5:].strip()
            user = User.objects.get(token=token)
            request.user = user
            if app_label and model_name:
                model = apps.get_model(app_label, model_name)
                if model == User and str(user.pk) == arg1:
                    data = dict(name=user.name, username=user.username, photo=user.photo.url, email=user.email)
                    return HttpResponse(
                        json_serialize(result, request.GET, errors=[], message=_('Action successfully performed.'), exception=None, result=data)
                    )
                # model @action or @meta | manager @subset [@action or @meta]
                elif arg1 and arg2:
                    # model
                    if arg1.isdigit():
                        obj = model.objects.all(user).get(pk=arg1)
                        if arg2:
                            # @action
                            group = None
                            for group in CACHE['INSTANCE_ACTIONS'][model]:
                                if arg2 in CACHE['INSTANCE_ACTIONS'][model][group]:
                                    action_dict = CACHE['INSTANCE_ACTIONS'][model][group][arg2]
                                    message = action_dict.get('message')
                                    func_name = arg2
                                    break
                            if func_name:
                                func = getattr(obj, func_name)
                                form_action = CACHE['INSTANCE_ACTIONS'][model][group][arg2]
                                # with input
                                if count_parameters_names(func) > 0:
                                    form = factory.get_action_form(request, obj, form_action)
                            # it is not @action
                            else:
                                # @meta
                                for method in CACHE['INSTANCE_METHODS'].get(model, []):
                                    if method['function'] == arg2:
                                        func_name = arg2
                                        func = getattr(obj, func_name)
                                        break
                    # manager @subset
                    else:
                        obj = model.objects.all(user)
                        pks = request.GET.get('ids', [])
                        if pks:
                            obj = obj.filter(pk__in=pks)
                        group = None
                        # @action
                        for group in CACHE['QUERYSET_ACTIONS'][model]:
                            if arg2 in CACHE['QUERYSET_ACTIONS'][model][group]:
                                action_dict = CACHE['QUERYSET_ACTIONS'][model][group][arg2]
                                message = action_dict.get('message')
                                func_name = arg2
                                break
                        if func_name:
                            func = getattr(obj, func_name)
                            form_action = CACHE['QUERYSET_ACTIONS'][model][group][arg2]
                            # with input
                            if count_parameters_names(func) > 0:
                                form = factory.get_class_action_form(request, obj.model, form_action, func)
                        # it is not @action
                        else:
                            # @meta
                            for method in CACHE['MANAGER_METHODS'].get(model, []):
                                if method['function'] == arg1:
                                    func_name = arg2
                                    func = getattr(obj, func_name)
                                    break
                # model | manager @subset or @action or @meta
                elif arg1:
                    if arg1.isdigit():
                        # model
                        obj = model.objects.all(user).get(pk=arg1)
                        if request.method.lower() == 'get':
                            result = obj
                        elif request.method.lower() == 'delete':
                            result = None
                            obj.delete()
                            message = _('Deletion successfully performed.')
                        else:
                            form = factory.get_register_form(request, obj)
                    else:
                        # manager @subset or @action or @meta
                        obj = model.objects.all(user)
                        pks = request.GET.get('ids', [])
                        if pks:
                            obj = obj.filter(pk__in=pks)
                        group = None

                        # @action
                        func = None
                        action_dict = None
                        for group in CACHE['QUERYSET_ACTIONS'][model]:
                            if arg1 in CACHE['QUERYSET_ACTIONS'][model][group]:
                                action_dict = CACHE['QUERYSET_ACTIONS'][model][group][arg1]
                                message = action_dict.get('message')
                                func = getattr(obj, arg1)
                                func_name = arg1
                                break
                        if not func_name:
                            for group in CACHE['CLASS_ACTIONS'][model]:
                                if arg1 in CACHE['CLASS_ACTIONS'][model][group]:
                                    action_dict = CACHE['CLASS_ACTIONS'][model][group][arg1]
                                    message = action_dict.get('message')
                                    func = getattr(obj, arg1)
                                    func_name = arg1
                                    break
                        if func_name:
                            # with input
                            if count_parameters_names(func) > 0:
                                form = factory.get_class_action_form(request, obj.model, action_dict, func)
                        # it is not @action
                        else:
                            # @subset or @meta
                            for subset in CACHE['SUBSETS'][model]:
                                if arg1 == subset['name']:
                                    func_name = arg1
                                    break
                            if func_name:
                                func = getattr(obj, func_name)
                            # it is not @subset
                            else:
                                # @meta
                                for method in CACHE['MANAGER_METHODS'].get(model, []):
                                    if method['function'] == arg1:
                                        func_name = arg1
                                        func = getattr(obj, func_name)
                                        break
                # list or save
                else:
                    if request.method.lower() == 'get':
                        obj = model.objects.all(user)
                        func_name = 'all'
                    else:
                        form = factory.get_register_form(request, model())

            # list or action
            if func_name:
                if form:
                    if form.is_valid():
                        params = []
                        func = getattr(obj, func_name)
                        for param in get_parameters_names(func, include_annotated=True):
                            if param in form.cleaned_data:
                                params.append(form.cleaned_data[param])
                            else:
                                params.append(get_role_value_for_action(func, request.user, param))
                        try:
                            result = func(*params)
                            if hasattr(result, 'all'):
                                result = result[page*10:(page*10)+10]
                            
                        except ValidationError as e:
                            message = None
                            form.add_error(None, e.message)
                    else:
                        errors = form.errors
                elif obj:
                    try:
                        func = getattr(obj, func_name)
                        args = get_role_values_for_condition(func, request.user)
                        result = func(*args)
                        if hasattr(result, 'all'):
                            result = result[page*10:(page*10)+10]
                    except ValidationError as e:
                        errors = {'__all__': e.message}
                        message = None
                return HttpResponse(
                    json_serialize(result, request.GET, errors=errors, message=message, exception=None)
                )
            # add or edit
            elif form:
                if form.is_valid():
                    result = form.save()
                    message = _('Action successfully performed.')
                else:
                    errors = form.errors
                return HttpResponse(
                    json_serialize(result, request.GET, errors=errors, message=message, exception=None)
                )
            # get or delete
            else:
                return HttpResponse(
                    json_serialize(result, request.GET, errors=errors, message=message, exception=None)
                )
    else:
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            return HttpResponse(
                json_serialize(result, request.GET, errors=[], message=_('Action successfully performed.'), exception=None, result=dict(token=user.token, id=user.id))
            )
        else:
            return HttpResponseForbidden()
