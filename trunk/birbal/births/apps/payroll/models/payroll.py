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
    rank = meta.ForeignKey(Official,
                           verbose_name=_("Rank"))
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

#############################################transactions
# basically the attendance/movement register. Will have to define
# holidays, earned leave, causal leave, medical leave etc

class Leave(Power):
    """Types of leave available
       """
    name = meta.CharField(_("Leave Type"),maxlength=50,unique=True)

class Leaveallotment(meta.Model):
    """This gives the amount of leave available for each
       type of leave for each type of official
       """
    year = meta.IntegerField(_("Year"))
    leave = meta.ForeignKey(Leave,
                            verbose_name=_("Type of leave"))
    rank =  meta.ForeignKey(Official,
                           verbose_name=_("Rank"))
    monthly = meta.IntegerField(_("Monthly quota"))
    yearly = meta.IntegerField(_("Yearly quota"))
    carriedforward = meta.BooleanField(_("Can be carried forward"),
                                       default=True)
    encashed = meta.BooleanField(_("Can be encashed"),
                                       default=True)

    class META:
        
        admin = meta.Admin(
        list_display = ('year','leave','rank',),
            search_fields = ['leave','rank'],)
        unique_together = (("year","leave","rank"),)
    def __repr__(self):
            return "%s %s %s"\
            %(self.year,self.get_rank(),self.get_leave())

class Holiday(meta.Model):
    """This gives the holidays announced for each year
       """
    name = meta.CharField(_("Holiday Name"),maxlength=50,unique=True)
    year = meta.IntegerField(_("Year"))
    date = meta.DateField(_("Date"))
    general = meta.BooleanField(_("General or Restricted"),
                                       default=True)

    class META:
        ordering = ['-date','name'.lower()]
        admin = meta.Admin(
        list_display = ('year','name','date',),
            search_fields = ['leave','rank'],)
    def __repr__(self):
            return "%s %s %s"\
            %(self.year,self.date,self.name)
    
    
    
    
