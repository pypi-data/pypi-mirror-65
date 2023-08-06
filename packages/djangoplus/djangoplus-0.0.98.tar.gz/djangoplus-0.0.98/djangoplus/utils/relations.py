# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.utils.text import slugify
from djangoplus.utils import permissions
from djangoplus.ui.components.panel import ModelPanel, RelationModelPanel
from djangoplus.ui.components.paginator import Paginator
from djangoplus.utils.metadata import get_fieldsets, get_metadata
from djangoplus.ui.components.forms import ModelForm, ValidationError


class Relation(object):
    def __init__(self, instance, relation_info):
        self.instance = instance
        self.model = type(self.instance)
        self.relation_name = None
        self.relation_verbose_name = None
        self.relation_model = None
        self.relation_value = None
        self.relation_type = None
        self.hidden_field_name = None
        self.subsets = OrderedDict()

        app_label = get_metadata(self.model, 'app_label')
        model_name = self.model.__name__.lower()

        self.add_label = None
        self.can_add = None
        self.add_url = None
        self.edit_url = None
        self.view_url = None
        self.delete_url = None

        self.is_one_to_one = False
        self.is_many_to_one = False
        self.is_one_to_many = False
        self.is_one_to_many_reverse = False
        self.is_many_to_many = False

        self.children_info = None

        if '__' in relation_info:
            relation_info, self.children_info = relation_info.split('__')

        if ':' in relation_info:
            # 'relation_name:all[action_a,action_b],subset[action_c]'
            tokens = relation_info.replace(' ', '').split(':')
            self.relation_name, subsets_info = tokens[0], tokens[1].split('],')
            for subset_info in subsets_info:
                tokens = subset_info.split('[')
                if len(tokens) > 1:
                    subset_name, subset_actions = tokens[0], tokens[1].replace(']', '').split(',')
                else:
                    subset_name, subset_actions = tokens[0], []
                self.subsets[subset_name] = subset_actions
        elif '[' in relation_info:
            # 'relation_name[action_a,action_b]'
            tokens = relation_info.replace(' ', '').split('[')
            self.relation_name, subset_actions = tokens[0], tokens[1].replace(']', '').split(',')
            self.subsets['all'] = subset_actions
        else:
            # 'relation_name'
            self.relation_name = relation_info

        attr = getattr(self.model, self.relation_name)
        descriptor_name = attr.__class__.__name__

        if hasattr(attr, 'related'):
            if descriptor_name == 'ReverseOneToOneDescriptor':
                self.is_one_to_one = True
                self.relation_type = 'OneToOne'
                self.relation_model = attr.related.remote_field.model
                self.relation_verbose_name = getattr(attr.related.target_field.model, '_meta').verbose_name

                self.relation_value = getattr(instance, self.relation_name)
                relation_app_label = get_metadata(self.model, 'app_label')
                relation_model_name = self.relation_model.__name__.lower()

                self.add_url = None
                self.view_url = '/view/{}/{}/{}/'.format(
                    relation_app_label, relation_model_name, self.relation_value.pk
                )

        elif hasattr(attr, 'field'):

            field_name = attr.field.__class__.__name__

            if descriptor_name == 'ForwardOneToOneDescriptor':
                self.is_one_to_one = True
                self.relation_type = 'OneToOne'
                self.relation_model = attr.field.remote_field.model
                self.relation_verbose_name = attr.field.verbose_name

                self.relation_value = getattr(instance, self.relation_name)
                relation_app_label = get_metadata(self.relation_model, 'app_label')
                relation_model_name = self.relation_model.__name__.lower()

                self.add_url = '/add/{}/{}/{}/{}/'.format(
                    app_label, model_name, self.instance.pk, self.relation_name
                )
                if self.relation_value:
                    self.add_url = '/add/{}/{}/{}/{}/{}/'.format(
                        app_label, model_name, self.instance.pk, self.relation_name, self.relation_value.pk
                    )
                    self.view_url = '/view/{}/{}/{}/'.format(
                        relation_app_label, relation_model_name, self.relation_value.pk
                    )
                    self.delete_url = '/delete/{}/{}/{}/'.format(
                        relation_app_label, relation_model_name, self.relation_value.pk
                    )

            elif descriptor_name == 'ForwardManyToOneDescriptor':
                self.is_many_to_one = True
                self.relation_type = 'ManyToOne'
                self.relation_model = attr.field.remote_field.model
                self.relation_verbose_name = attr.field.verbose_name

                self.relation_value = getattr(instance, self.relation_name)
                relation_app_label = get_metadata(self.relation_model, 'app_label')
                relation_model_name = self.relation_model.__name__.lower()
                if self.relation_value:
                    self.view_url = '/view/{}/{}/{}/'.format(
                        relation_app_label, relation_model_name, self.relation_value.pk
                    )

            elif descriptor_name == 'ManyToManyDescriptor' and field_name == 'OneToManyField':
                self.is_one_to_many = True
                self.relation_type = 'OneToMany'
                self.relation_model = attr.field.remote_field.model
                self.relation_verbose_name = attr.field.verbose_name
                self.add_label = attr.field.add_label

                self.relation_value = getattr(instance, self.relation_name).all()
                relation_app_label = get_metadata(self.relation_model, 'app_label')
                relation_model_name = self.relation_model.__name__.lower()

                self.view_url = '/view/{}/{}/{{}}/'.format(
                    relation_app_label, relation_model_name
                )
                self.add_url = '/add/{}/{}/{}/{}/'.format(
                    app_label, model_name, self.instance.pk, self.relation_name
                )
                self.delete_url = '/delete/{}/{}/{}/{}/{{}}/'.format(
                    app_label, model_name, self.instance.pk, self.relation_name
                )

            elif descriptor_name == 'ReverseManyToOneDescriptor':
                self.is_one_to_many_reverse = True
                self.relation_type = 'OneToManyReverse'
                self.relation_model = attr.field.model
                self.relation_verbose_name = getattr(attr.field.model, '_meta').verbose_name_plural

                self.hidden_field_name = attr.rel.field.name
                self.relation_value = getattr(instance, self.relation_name).all()
                relation_app_label = get_metadata(self.relation_model, 'app_label')
                relation_model_name = self.relation_model.__name__.lower()

                self.add_url = '/add/{}/{}/{}/{}/'.format(
                    app_label, model_name, self.instance.pk, self.relation_name
                )
                self.edit_url = '/add/{}/{}/{}/{}/{{}}/'.format(
                    app_label, model_name, self.instance.pk, self.relation_name
                )
                self.view_url = '/view/{}/{}/{{}}/'.format(
                    relation_app_label, relation_model_name
                )
                self.delete_url = '/delete/{}/{}/{{}}/'.format(
                    relation_app_label, relation_model_name
                )

            elif descriptor_name == 'ManyToManyDescriptor':
                self.is_many_to_many = True
                self.relation_type = 'ManyToMany'
                self.relation_model = attr.field.remote_field.model
                self.relation_verbose_name = attr.field.verbose_name
                self.add_label = attr.field.add_label
                self.can_add = attr.field.can_add

                self.relation_value = getattr(instance, self.relation_name).all()
                relation_app_label = get_metadata(self.relation_model, 'app_label')
                relation_model_name = self.relation_model.__name__.lower()

                self.view_url = '/view/{}/{}/{{}}/'.format(
                    relation_app_label, relation_model_name
                )
                self.add_url = '/add/{}/{}/{}/{}/'.format(
                    app_label, model_name, self.instance.pk, self.relation_name
                )
                self.delete_url = '/delete/{}/{}/{}/{}/{{}}/'.format(
                    app_label, model_name, self.instance.pk, self.relation_name
                )
            else:
                raise Exception()
        elif hasattr(attr, '_metadata'):
            self.relation_value = getattr(self.instance, self.relation_name)()
            if hasattr(self.relation_value, 'model'):
                self.relation_model = self.relation_value.model
            else:
                self.relation_model = type(self.relation_value)
            self.relation_verbose_name = get_metadata(attr, 'verbose_name')

            relation_app_label = get_metadata(self.relation_model, 'app_label')
            relation_model_name = self.relation_model.__name__.lower()
            self.view_url = '/view/{}/{}/{{}}/'.format(relation_app_label, relation_model_name)
        else:
            raise Exception()

    def get_component(self, request, as_pdf=False):
        verbose_name = getattr(self.relation_model, '_meta').verbose_name
        if self.is_one_to_one or self.is_many_to_one:
            panel_fieldsets = getattr(self.relation_model, 'fieldsets', None)
            if panel_fieldsets:
                panel_fieldsets = ((self.relation_verbose_name, panel_fieldsets[0][1]),)
            else:
                panel_fieldsets = get_fieldsets(self.relation_model, self.relation_verbose_name)
            component = ModelPanel(
                request, self.relation_value or self.relation_model(),
                fieldsets=panel_fieldsets, complete=False
            )
            if self.view_url and permissions.has_view_permission(request, self.relation_model):
                label = 'Detalhar {}'.format(verbose_name)
                component.drop_down.add_action(label, self.view_url, 'ajax', 'fa-eye', category=label)
            if self.add_url and permissions.has_edit_permission(request, self.model):
                label = 'Atualizar {}'.format(verbose_name)
                component.drop_down.add_action(label, self.add_url, 'popup', 'fa-edit', category=label)
            if self.delete_url and permissions.has_edit_permission(request, self.model):
                label = 'Excluir {}'.format(verbose_name)
                component.drop_down.add_action(label, self.delete_url, 'popup', 'fa-close', category=label)
        else:
            inlines = []
            fieldsets = getattr(self.model, 'fieldsets', ())
            title = self.relation_verbose_name
            for fieldset in fieldsets:
                fieldset_relations = fieldset[1].get('relations', ())
                fieldset_inlines = fieldset[1].get('inlines', ())
                fieldset_fields = fieldset[1].get('fields', ())
                for inline in fieldset_inlines:
                    inlines.append(inline)
                is_relation = self.relation_name in fieldset_relations
                is_inline = self.relation_name in fieldset_inlines
                is_field = self.relation_name in fieldset_fields
                if is_relation or is_inline or is_field:
                    if len(fieldset_relations) + len(fieldset_inlines) + len(fieldset_fields) == 1:
                        title = fieldset[0].split('::')[-1]

            if self.is_one_to_many or self.is_many_to_many:
                if self.can_add:
                    has_add_permission = permissions.check_group_or_permission(request, self.can_add)
                else:
                    has_add_permission = permissions.has_add_permission(request, self.model)
            else:
                has_add_permission = permissions.has_add_permission(request, self.relation_model)

            if self.children_info:
                component = RelationModelPanel(request, self.relation_value, title, self.children_info)
            else:
                list_subsets = list(self.subsets.keys())
                component = Paginator(
                    request, self.relation_value.all(request.user), title, relation=self,
                    list_subsets=list_subsets, readonly=False, uid=slugify(self.relation_name)
                )
                action_names = self.subsets.get(component.current_tab or 'all', [])
                component.load_actions(action_names)
            instance = self.relation_model()
            if self.hidden_field_name:
                setattr(instance, self.hidden_field_name, self.instance)
            can_add = not hasattr(instance, 'can_add') or instance.can_add()

            if self.add_url and has_add_permission and can_add:
                if self.relation_name in inlines:
                    form_name = get_metadata(self.relation_model, 'add_form')
                    relation_verbose_name = get_metadata(self.relation_model, 'verbose_name')
                    if form_name:
                        fromlist = list(map(str, [get_metadata(self.relation_model, 'app_label')]))
                        module = __import__('{}.forms'.format(fromlist[0]), fromlist=fromlist)
                        form_cls = getattr(module, form_name)
                    else:
                        class Form(ModelForm):
                            class Meta:
                                model = self.relation_model
                                fields = get_metadata(self.relation_model, 'form_fields', '__all__')
                                exclude = get_metadata(self.relation_model, 'exclude_fields', ())
                                submit_label = 'Adicionar'
                                title = 'Adicionar {}'.format(relation_verbose_name)

                        form_cls = Form
                    form = form_cls(request, instance=instance, inline=True)
                    if self.hidden_field_name in form.fields:
                        del (form.fields[self.hidden_field_name])
                    if not hasattr(form.instance, 'can_add') or form.instance.can_add():
                        component.form = form
                        if form.is_valid():
                            try:
                                form.save()
                                component.message = 'Ação realizada com sucesso'
                            except ValidationError as e:
                                form.add_error(None, str(e.message))
                else:
                    add_label = self.add_label or get_metadata(self.relation_model, 'add_label')
                    add_style = self.add_label or get_metadata(self.relation_model, 'add_style', 'popup')
                    label = add_label or 'Adicionar {}'.format(verbose_name)
                    component.add_action(label, self.add_url, add_style, 'fa-plus')

        component.as_pdf = as_pdf

        return component

    def debug(self):
        url = 'http://localhost:8000'
        print('Instance:', self.instance)
        print('Model:', self.model)
        print('Relation Name:', self.relation_name)
        print('Relation Verbose Name:', self.relation_verbose_name)
        print('Relation Model:', self.relation_model)
        print('Relation Value:', self.relation_value)
        print('Relation Type:', self.relation_type)
        if self.add_url:
            print('Add URL', '{}{}'.format(url, self.add_url))
        if self.edit_url:
            print('Edit URL', '{}{}'.format(url, self.edit_url))
        if self.view_url:
            print('View URL', '{}{}'.format(url, self.view_url))
        if self.delete_url:
            print('Delete URL', '{}{}'.format(url, self.delete_url))
        print('\n\n\n\n')
