from django.core import meta

# All address related data here. There should be a clickable map
# to populate the Area and Street tables/fields

class Area(meta.Model):
    """ Each jurisdiction is divided into areas. Areas can be wards,
        mohallas, sectors etc
        """
    name = meta.CharField(_("Area"),maxlength=50,unique=True)
    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.name)


class Street(meta.Model):
    """ Streets may be streets or colonies or slums or whatever
        they have to be unique in an area
        """
    name = meta.CharField(_("Street"),maxlength=50)
    area = meta.ForeignKey(Area)
    class META:
        unique_together = (("name","area"),)
        admin = meta.Admin(
        list_display = ('name','area',),
            search_fields = ['name'],)
    def __repr__(self):
            return _("Street: %s Area %s") %(self.name,self.get_area)
