from django.core import meta

# Create your models here.

class Advertisement(meta.Model):
    title = meta.CharField('Title',maxlength=250)
    date = meta.DateTimeField('Date',default=meta.LazyDate())
    expires = meta.DateField('Expiry Date',blank=True,null=True)
    lead = meta.CharField('Lead',maxlength=250)
    photo = meta.ImageField('Photo',upload_to='images/',blank=True,null=True)
    matter = meta.TextField('Matter',blank=True,null=True)
    class META:
        admin = meta.Admin(
        js = ('js/tiny_mce/tiny_mce.js','js/tiny_mce/textareas.js'),)
        unique_together = (("title","date"),)
    def __repr__(self):
            return "%s, Date: %s" %(self.title.capitalize(),self.date)


facility_types =(
    ('HM', 'Home'),
    ('FQ', 'Faq'),
    ('DC', 'Documentation'),
    
    )

layout_types =(
    ('TB', 'TopBottom'),
    ('LR', 'LeftRight'),
    ('RL', 'RightLeft'),
    )

class Facility(meta.Model):
    title = meta.CharField('Title',maxlength=250)
    type = meta.CharField('Entry Type',maxlength=2,choices=facility_types)
    layout = meta.CharField('Layout',maxlength=2,choices=layout_types)
    photo = meta.ImageField('Photo',upload_to='images/',blank=True,null=True)
    blurb = meta.CharField('Blurb for photo',maxlength=250,blank=True,null=True)
    matter = meta.TextField('Matter',blank=True,null=True)
    priority = meta.IntegerField('Priority',default=1)
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
