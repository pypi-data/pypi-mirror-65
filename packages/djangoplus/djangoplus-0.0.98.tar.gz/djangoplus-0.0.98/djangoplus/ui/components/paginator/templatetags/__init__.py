# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from djangoplus.utils import permissions
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from djangoplus.utils.metadata import get_metadata
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from djangoplus.cache import CACHE


from django_jinja import library as register


@register.global_function
def tree_info(obj, queryset):
    if hasattr(obj, 'get_parent_field'):
        parent_field = obj.get_parent_field()
        if parent_field:
            parent = getattr(obj, parent_field.name)
            if not hasattr(queryset, '__pks'):
                queryset.__pks = queryset.values_list('pk', flat=True)
            if parent and parent.pk in queryset.__pks:
                return 'treegrid-{}  treegrid-parent-{}'.format(obj.pk, parent.pk)
            else:
                return 'treegrid-{}'.format(obj.pk)
    else:
        return ''


@register.global_function
def paginator_checkboxes(paginator, obj, as_row=False):
    l = []
    if paginator.display_checkboxes:
        if as_row:
            l.append('<td style="vertical-align: middle" width="5px">')
        if obj:
            l.append('<input type="checkbox" name="pk" value="{}" onclick="check{}();"><span class="custom-checkbox"></span>'.format(obj.pk, paginator.id))
        else:
            l.append("""<input name="pk" type="checkbox" value="0" onclick="$('input[name=\\\'pk\\\']').prop('checked', this.checked);check{}();"><span class="custom-checkbox"></span>""".format(paginator.id))
        if as_row:
            l.append('</td>')
    return mark_safe(''.join(l))


@register.global_function
def paginator_icons(paginator, obj, as_button=False):
    relation = paginator.relation
    edit = not paginator.readonly
    delete = not paginator.readonly
    return obj_icons(paginator.request, obj, relation=relation, edit=edit, delete=delete, as_button=as_button)


@register.global_function
def obj_icons(request, obj, relation=None, edit=True, delete=True, css=None, as_button=False):
    outuput = []

    if as_button:
        css = 'btn btn-default {}'.format(css or '{}')
    else:
        css = 'hide-label {}'.format(css or '{}')

    if relation:
        if type(obj) not in CACHE['SIMPLE_MODELS']:
            view_url = relation.view_url.format(obj.pk)
            btn = '<a id="{}" class="{}" href="{}" title="{}"><i class="fa fa-search fa-lg"></i><span>  {}</span></a>'
            outuput.append(btn.format(slugify(view_url), css.format('ajax'), view_url, _('View'), _('View')))

        if relation.edit_url:
            if relation.is_one_to_many or relation.is_many_to_many:
                has_edit_permission = permissions.has_edit_permission(request, relation.model)
            else:
                has_edit_permission = permissions.has_edit_permission(request, relation.relation_model)
            if has_edit_permission and (not hasattr(obj, 'can_edit') or obj.can_edit()):
                edit_url = relation.edit_url.format(obj.pk)
                btn = ' <a id="{}" class="{}" href="{}" title="{}"><i class="fa fa-edit fa-lg"></i><span> {}</span></a>'
                outuput.append(btn.format(slugify(edit_url), css.format(get_metadata(relation.relation_model, 'add_style', 'popup')), edit_url, _('Edit'), _('Edit')))

        if relation.delete_url:
            if relation.is_one_to_many or relation.is_many_to_many:
                has_delete_permission = delete
            else:
                has_delete_permission = permissions.has_delete_permission(request, relation.relation_model)
            if has_delete_permission and (not hasattr(obj, 'can_delete') or obj.can_delete()):
                delete_url = relation.delete_url.format(obj.pk)
                btn = ' <a id="{}" class="{}" href="{}" title="{}"><i class="fa fa-close fa-lg"></i><span> {}</span></a>'
                outuput.append(btn.format(slugify(delete_url), css.format('popup'), delete_url, _('Delete'), _('Delete')))
    else:
        model = type(obj)
        cls = model.__name__.lower()
        app = get_metadata(model, 'app_label')

        tree_index_field = None
        if hasattr(obj, 'get_tree_index_field'):
            tree_index_field = obj.get_tree_index_field()

        view_url = hasattr(obj, 'get_absolute_url') and obj.get_absolute_url() or '/view/{}/{}/{}/'.format(app, cls, obj.pk)
        btn = '<a id="{}" class="{}" href="{}" title="{}"><i class="fa fa-search fa-lg"></i><span> {}</span></a>'
        outuput.append(btn.format(slugify(view_url), css.format('ajax'), view_url, _('View'), _('View')))

        if edit and permissions.has_edit_permission(request, model) and (not hasattr(obj, 'can_edit') or obj.can_edit()):
            edit_url = '/add/{}/{}/{}/'.format(app, cls, obj.pk)
            btn = ' <a id="{}" class="{}" href="{}" title="{}"><i class="fa fa-edit fa-lg"></i><span> {}</span></a>'
            outuput.append(btn.format(slugify(edit_url), css.format('ajax'), edit_url, _('Edit'), _('Edit')))

        if delete and permissions.has_delete_permission(request, model) and (not hasattr(obj, 'can_delete') or obj.can_delete()):
            delete_url = '/delete/{}/{}/{}/'.format(app, cls, obj.pk)
            btn = ' <a id="{}" class="{}" href="{}" title="{}"><i class="fa fa-close fa-lg"></i><span> {}</span></a>'
            outuput.append(btn.format(slugify(delete_url), css.format('popup'), delete_url, _('Delete'), _('Delete')))

        if tree_index_field:
            add_url = '/add/{}/{}/{}/{}/'.format(app, cls, obj.pk, cls)
            btn = ' <a id="{}" class="{}" href="{}" title="{}"><i class="fa fa-plus fa-lg"><span> {}</span></i></a>'
            outuput.append(btn.format(slugify(view_url), css.format('popup'), add_url, _('Add'), _('Add')))

    return mark_safe(''.join(outuput))


@register.filter()
def align(value):
    position ='left'
    if isinstance(value, bool) or isinstance(value, datetime.date):
        position='center'
    elif isinstance(value, Decimal) or isinstance(value, int):
        position='right'
    elif isinstance(value, tuple):
        return align(value[0])
    return position


@register.filter
def column_name(paginator, i):
    return paginator.column_names[i][0]


@register.filter
def paginate(paginator):
    return render_to_string(paginator.template, {'component': paginator})


@register.global_function
def add_grouped_actions(paginator, obj):
    return add_actions(paginator, obj, category=_('Actions'))


@register.global_function
def add_actions(paginator, obj, category=None):
    paginator.drop_down.add_actions(
        obj, subset_name=paginator.get_current_tab_name() or None, category=category,
        action_names=paginator.action_names
    )
    return ''
