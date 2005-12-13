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
