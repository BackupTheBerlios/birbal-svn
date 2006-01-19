from django.core import meta

# Create your models here

class Category(meta.Model):
    category_name = meta.CharField(maxlength=50)
    parent = meta.ForeignKey('self', blank=True, null=True,
                             related_name='child')

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.get_parent()
            p_list.append(p.category_name)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' :: '

    def _parents_repr(self):
        p_list = self._recurse_for_parents(self)
        return self.get_separator().join(p_list)
    _parents_repr.short_description = "Category parents"


    def _pre_save(self):
        p_list = self._recurse_for_parents(self)
        if self.category_name in p_list:
            raise "You must not save a category in itself!"

    def __repr__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.category_name)
        return self.get_separator().join(p_list)

    class META:
        admin = meta.Admin(
            list_display = ('category_name', '_parents_repr'),
            search_fields = ['category_name'],
        )
        module_name = 'categories'

