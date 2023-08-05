from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class CustomModelAdmin(ModelAdmin):
    change_list_template = 'contextmenu/base.html'

    def get_changelist_instance(self, request):
        """
        Return a `ChangeList` instance based on `request`. May raise
        `IncorrectLookupParameters`.
        """
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        # Add the action checkboxes if any actions are available.
        if self.get_actions(request):
            list_display = ['action_checkbox', 'context_menu', *list_display]
        sortable_by = self.get_sortable_by(request)
        ChangeList = self.get_changelist(request)
        return ChangeList(
            request,
            self.model,
            list_display,
            list_display_links,
            self.get_list_filter(request),
            self.date_hierarchy,
            self.get_search_fields(request),
            self.get_list_select_related(request),
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
            sortable_by,
        )

    def context_menu(self, obj):
        items = self.get_contextmenu_items(obj)
        return render_to_string('contextmenu/dropdown.html', context={
            'items': items,
            'title': 'links',
        })
    context_menu.short_description = mark_safe('Links')

    def get_contextmenu_items(self, obj):
        items = []
