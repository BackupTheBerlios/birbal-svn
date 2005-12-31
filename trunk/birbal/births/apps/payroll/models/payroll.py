from django.core import meta

# complete attendance and personal management


#######################################################
# define officials, persons, powers, ranks and statuses

class Power(meta.Model):
    """ Powers that officials have to take actions
        will be attached to officials with a check that
        if there is no power the action will not take place
        """
    name = meta.CharField(_("Power"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.name)

class Status(Power):
    """ A field describing what a person is doing - should be
        set by changes in the movement register
        """
    name = meta.CharField(_("Status"),maxlength=50,unique=True)

class Official(meta.Model):
    """ Types of officials with their powers
        """
    rank = meta.CharField(_("Rank"),maxlength=50,unique=True)
    powers = meta.ManyToManyField(Power)
    class META:
        admin = meta.Admin(
        list_display = ('rank',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.rank)

class Person(meta.Model):
    """ Persons working - rank and status. Once movement register is
        set up we could remove the status field
        """
    name = meta.CharField(_("Name"),maxlength=50,unique=True)
    rank = meta.ForeignKey(Official)
    status = meta.ForeignKey(Status)
    class META:
        ordering = ['rank','name'.lower()]
        admin = meta.Admin(
        list_display = ('name','rank','status',),
            search_fields = ['name','rank'],)
    def __repr__(self):
            return "%s %s %s"\
            %(self.name,self.get_rank(),self.get_status())

#############################################end of persons
