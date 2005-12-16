from django.core import meta


#######################################################################

# application specific stuff - website specific stuff at the end

#######################################################
# define officials, persons, powers, ranks and statuses

class Power(meta.Model):
    name = meta.CharField(_("Power"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(_(self.name))

class Status(meta.Model):
    name = meta.CharField(_("Status"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(_(self.name))

class Official(meta.Model):
    rank = meta.CharField(_("Rank"),maxlength=50,unique=True)
    powers = meta.ManyToManyField(Power)
    class META:
        admin = meta.Admin(
        list_display = ('rank',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s has %s powers" %(self.rank,self.get_power_list())

class Person(meta.Model):
    name = meta.CharField(_("Name"),maxlength=50,unique=True)
    rank = meta.ForeignKey(Official)
    status = meta.ForeignKey(Status)
    class META:
        admin = meta.Admin(
        list_display = ('name','rank','status',),
            search_fields = ['name','rank'],)
    def __repr__(self):
            return "%s  %s" %(self.name,self.get_rank())

#############################################end of persons

# master tables for actual data

##############################################end of actual data master


# detail tables for actual data

##############################################end of actual data details


########################################################################

# Website specific stuff

class Advertisement(meta.Model):
    title = meta.CharField(_("Title"),maxlength=250)
    date = meta.DateTimeField(_("Date"),default=meta.LazyDate())
    expires = meta.DateField(_("Expiry Date"),blank=True,null=True)
    lead = meta.CharField(_("Lead"),maxlength=250)
    photo = meta.ImageField(_("Photo"),upload_to='images/',blank=True,null=True)
    matter = meta.TextField(_("Matter"),blank=True,null=True)
    class META:
        admin = meta.Admin(
        js = ('js/tiny_mce/tiny_mce.js','js/tiny_mce/textareas.js'),)
        unique_together = (("title","date"),)
    def __repr__(self):
            return "%s, Date: %s" %(self.title.capitalize(),self.date)


facility_types =(
    ('HM', _("Home")),
    ('FQ', _("Faq")),
    ('DC', _("Documentation")),
    
    )

layout_types =(
    ('TB', _("TopBottom")),
    ('LR', _("LeftRight")),
    ('RL', _("RightLeft")),
    )

class Facility(meta.Model):
    title = meta.CharField(_("Title"),maxlength=250)
    type = meta.CharField(_("Entry Type"),maxlength=2,choices=facility_types)
    layout = meta.CharField(_("Layout"),maxlength=2,choices=layout_types)
    photo = meta.ImageField(_("Photo"),upload_to='images/',blank=True,null=True)
    blurb = meta.CharField(_("Blurb for photo"),maxlength=250,blank=True,null=True)
    matter = meta.TextField(_("Matter"),blank=True,null=True)
    priority = meta.IntegerField(_("Priority"),default=1)
    class META:
        unique_together = (("title","type"),)
        ordering = ['type','priority']
        admin = meta.Admin(
        list_display = ('title','type','layout','priority'),
            search_fields = ['type'],
        js = ('js/tiny_mce/tiny_mce.js','js/tiny_mce/textareas.js'),)
    def __repr__(self):
            return "%s, Type: %s, Priority: %d, layout: %s\
            " %(self.title.capitalize(),self.get_type_display(),self.priority,\
                self.get_layout_display())
