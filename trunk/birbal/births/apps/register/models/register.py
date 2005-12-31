from django.core import meta
from births.apps.payroll.models.payroll import *


#######################################################################

sexes = (
    ('M','Male'),
    ('F','Female'),
    )


# master tables for actual data

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

class Deathplace(Area):
    """ Type of death place - at home, hospital, on the street ...
        """
    name = meta.CharField(_("Area"),maxlength=50,unique=True)


class Birthplace(Area):
    """ Type of death place - at home, hospital, on the street,
        found abandoned, given up for adoption etc
        """
    name = meta.CharField(_("Area"),maxlength=50,unique=True)


class Reporttype(Area):
    """ By email, over the web, phone, in person: how did the
        report come?
        """
    name = meta.CharField(_("Area"),maxlength=50,unique=True)


##############################################end of actual data master


# detail tables for actual data

#birth reports, death reports, birth register death register
#should have just one big class and subclass the rest - but
#subclassing is borked. The fields get diplayed in reverse order
#in the admin. 

class Birthreport(meta.Model):
    """ Actual report of birth - not to be altered
        """
    fileno = meta.CharField(_("File Number"),maxlength=50,unique=True)
    dateopened = meta.DateTimeField(
        _("Date Opened"),default=meta.LazyDate(),editable=False)
    reporttype = meta.ForeignKey(Reporttype,
                    verbose_name=_("Report Type"))
    informant = meta.CharField(_("Informant"),maxlength=50)
    informantaddress = meta.TextField(_("Informants Address"))
    informantsarea = meta.ForeignKey(Area,
                    verbose_name=_("Informants Area"))
    informantstreet = meta.ForeignKey(Street,
                    verbose_name=_("Informants Street"))
    father = meta.CharField(_("Fathers Name"),maxlength=80)
    mother = meta.CharField(_("Mothers Name"),maxlength=80)
    address = meta.TextField(_("Childs Address"))
    area = meta.ForeignKey(Area,verbose_name=_("Childs Area"))
    street = meta.ForeignKey(Street,verbose_name=_("Childs Street"))
    dob = meta.DateField(_("Date of birth"))
    sex = meta.CharField('Sex',maxlength=2,choices=sexes)
    birthplace = meta.CharField(_("Place of birth"),maxlength=50)
    birthaddress = meta.TextField(_("Birth Place Address"))
    birtharea = meta.ForeignKey(Area,
                    verbose_name=_("Place of birth Area"))
    birthstreet = meta.ForeignKey(Street,
                    verbose_name=_("Place of birth Street"))
    birthplacetype = meta.ForeignKey(Birthplace)
    scrutinised = meta.BooleanField(_("Scrutinised"),default=False)
    verified = meta.BooleanField(_("Verified"),default=False)
    accepted = meta.BooleanField(_("Accepted"),default=False)
    open = meta.BooleanField(_("File Open"),default=True,editable=False)
    dateclosed = meta.DateField(_("Date Closed"),
                                blank=True,null=True,
                                editable=False)
    reportfile = meta.ImageField(_("Scanned Report"),
                                 upload_to='images/reports/',
                                 blank=True,null=True)
    comments = meta.TextField(_("Comments"),null=True,blank=True)
    addedby = meta.CharField(_("Added By"),maxlength=100,editable=False)
    class META:
        admin = meta.Admin(
        list_display = ('fileno',),
            search_fields = ['fileno'],
        fields =
            (
                (
                None,
                    {
                    'fields': ('fileno','reporttype','reportfile')
                    }
                ),
                (
                _("Informant Information"),
                    {
                    'classes': 'collapse',
                    'fields': ('informant','informantsarea',
                               'informantstreet','informantaddress')
                    }
                ),
                (
                _("Details of Birth"),
                    {
                    'classes': 'collapse',
                    'fields': ('father','mother',
                               'area','street',
                               'dob','sex','comments')
                    }
                ),
                (
                _("Place of Birth"),
                    {
                    'classes': 'collapse',
                    'fields': ('birthplacetype','birthplace',
                               'birtharea','birthstreet',
                               'birthaddress')
                    }
                ),
                (
                _("Official Use"),
                    {
                    'classes': 'collapse',
                    'fields': ('scrutinised','verified','accepted')
                    }
                ),
            ),
        )
    def __repr__(self):
            return "%s %s" %(self.fileno,self.reportfile)

# some details are repeated - but it is necessary for audit purposes


class Birthregister(meta.Model):
    """ Final entry in the birth register
        """
    report = meta.ForeignKey(Birthreport,
                             verbose_name=_("Original Report"))
    dateopened = meta.DateTimeField(
        _("Date Opened"),default=meta.LazyDate(),editable=False)
    father = meta.CharField(_("Fathers Name"),maxlength=80)
    mother = meta.CharField(_("Mothers Name"),maxlength=80)
    address = meta.TextField(_("Childs Address"))
    area = meta.ForeignKey(Area,verbose_name=_("Childs Area"))
    street = meta.ForeignKey(Street,verbose_name=_("Childs Street"))
    childname = meta.CharField(_("Name of Child"),maxlength=100,
                               blank=True,null=True)
    dob = meta.DateField(_("Date of birth"))
    sex = meta.CharField('Sex',maxlength=2,choices=sexes)
    birthplace = meta.CharField(_("Place of birth"),maxlength=50)
    birthaddress = meta.TextField(_("Birth Place Address"))
    birtharea = meta.ForeignKey(Area,
                    verbose_name=_("Place of birth Area"))
    birthstreet = meta.ForeignKey(Street,
                    verbose_name=_("Place of birth Street"))
    birthplacetype = meta.ForeignKey(Birthplace)
    dateclosed = meta.DateField(_("Date Closed"),
                                blank=True,null=True,
                                editable=False)
    comments = meta.TextField(_("Comments"),null=True,blank=True)
    addedby = meta.CharField(_("Added By"),maxlength=100,editable=False)
    class META:
        admin = meta.Admin(
        list_display = ('report',),
            search_fields = ['report'],
        fields =
            (
                (
                None,
                    {
                    'fields': ('report',)
                    }
                ),
                
                (
                _("Details of Birth"),
                    {
                    'classes': 'collapse',
                    'fields': ('father','mother',
                               'area','street',
                               'dob','sex',
                               'childname','comments')
                    }
                ),
                (
                _("Place of Birth"),
                    {
                    'classes': 'collapse',
                    'fields': ('birthplacetype','birthplace',
                               'birtharea','birthstreet',
                               'birthaddress')
                    }
                ),
                
            ),
        )
    def __repr__(self):
            return "%s" %(self.report)


# all repeated for deaths

class Deathreport(meta.Model):
    """ Actual report of death - not to be altered
        """
    fileno = meta.CharField(_("File Number"),maxlength=50,unique=True)
    dateopened = meta.DateTimeField(
        _("Date Opened"),default=meta.LazyDate(),editable=False)
    reporttype = meta.ForeignKey(Reporttype,
                    verbose_name=_("Report Type"))
    informant = meta.CharField(_("Informant"),maxlength=50)
    informantaddress = meta.TextField(_("Informants Address"))
    informantsarea = meta.ForeignKey(Area,
                    verbose_name=_("Informants Area"))
    informantstreet = meta.ForeignKey(Street,
                    verbose_name=_("Informants Street"))
    name = meta.CharField(_("Deceased Name"),maxlength=80)
    fathername = meta.CharField(_("Father/Husband Name"),maxlength=80)
    address = meta.TextField(_("Deceased Address"))
    area = meta.ForeignKey(Area,verbose_name=_("Deceased Area"))
    street = meta.ForeignKey(Street,verbose_name=_("Deceased Street"))
    dob = meta.DateField(_("Date of death"))
    sex = meta.CharField('Sex',maxlength=2,choices=sexes)
    causeofdeath = meta.CharField(_("Cause Of Death"),maxlength=150)
    deathplace = meta.CharField(_("Place of death"),maxlength=50)
    deathaddress = meta.TextField(_("death Place Address"))
    deatharea = meta.ForeignKey(Area,
                    verbose_name=_("Place of death Area"))
    deathstreet = meta.ForeignKey(Street,
                    verbose_name=_("Place of death Street"))
    deathplacetype = meta.ForeignKey(Deathplace)
    scrutinised = meta.BooleanField(_("Scrutinised"),default=False)
    verified = meta.BooleanField(_("Verified"),default=False)
    accepted = meta.BooleanField(_("Accepted"),default=False)
    open = meta.BooleanField(_("File Open"),default=True,editable=False)
    dateclosed = meta.DateField(_("Date Closed"),
                                blank=True,null=True,
                                editable=False)
    reportfile = meta.ImageField(_("Scanned Report"),
                                 upload_to='images/reports/',
                                 blank=True,null=True)
    comments = meta.TextField(_("Comments"),null=True,blank=True)
    addedby = meta.CharField(_("Added By"),maxlength=100,editable=False)
    class META:
        admin = meta.Admin(
        list_display = ('fileno',),
            search_fields = ['fileno'],
        fields =
            (
                (
                None,
                    {
                    'fields': ('fileno','reporttype','reportfile')
                    }
                ),
                (
                _("Informant Information"),
                    {
                    'classes': 'collapse',
                    'fields': ('informant','informantsarea',
                               'informantstreet','informantaddress')
                    }
                ),
                (
                _("Details of death"),
                    {
                    'classes': 'collapse',
                    'fields': ('name','fathersname',
                               'area','street',
                               'dob','sex',
                               'causeofdeath','comments')
                    }
                ),
                (
                _("Place of death"),
                    {
                    'classes': 'collapse',
                    'fields': ('deathplacetype','deathplace',
                               'deatharea','deathstreet',
                               'deathaddress')
                    }
                ),
                (
                _("Official Use"),
                    {
                    'classes': 'collapse',
                    'fields': ('scrutinised','verified','accepted')
                    }
                ),
            ),
        )
    def __repr__(self):
            return "%s %s" %(self.fileno,self.reportfile)

# some details are repeated - but it is necessary for audit purposes


class Deathregister(meta.Model):
    """ Final entry in the death register
        """
    report = meta.ForeignKey(Deathreport,
                             verbose_name=_("Original Report"))
    dateopened = meta.DateTimeField(
        _("Date Opened"),default=meta.LazyDate(),editable=False)
    name = meta.CharField(_("Name"),maxlength=80)
    fathersname = meta.CharField(_("Father/Husband Name"),maxlength=80)
    address = meta.TextField(_("deceaseds Address"))
    area = meta.ForeignKey(Area,verbose_name=_("deceaseds Area"))
    street = meta.ForeignKey(Street,verbose_name=_("deceaseds Street"))
    dob = meta.DateField(_("Date of death"))
    sex = meta.CharField('Sex',maxlength=2,choices=sexes)
    causeofdeath = meta.CharField(_("Cause Of Death"),maxlength=150)
    deathplace = meta.CharField(_("Place of death"),maxlength=50)
    deathaddress = meta.TextField(_("death Place Address"))
    deatharea = meta.ForeignKey(Area,
                    verbose_name=_("Place of death Area"))
    deathstreet = meta.ForeignKey(Street,
                    verbose_name=_("Place of death Street"))
    deathplacetype = meta.ForeignKey(Deathplace)
    dateclosed = meta.DateField(_("Date Closed"),
                                blank=True,null=True,
                                editable=False)
    comments = meta.TextField(_("Comments"),null=True,blank=True)
    addedby = meta.CharField(_("Added By"),maxlength=100,editable=False)
    class META:
        admin = meta.Admin(
        list_display = ('report',),
            search_fields = ['report'],
        fields =
            (
                (
                None,
                    {
                    'fields': ('report',)
                    }
                ),
                
                (
                _("Details of death"),
                    {
                    'classes': 'collapse',
                    'fields': ('name','fathersname',
                               'area','street',
                               'dob','sex',
                               'causeofdeath','comments')
                    }
                ),
                (
                _("Place of death"),
                    {
                    'classes': 'collapse',
                    'fields': ('deathplacetype','deathplace',
                               'deatharea','deathstreet',
                               'deathaddress')
                    }
                ),
                
            ),
        )
    def __repr__(self):
            return "%s" %(self.report)



##############################################end of actual data details

# transaction tables

# report, register and certificate handling - basically file noting
# one generic noting thingie that does everything - cant have that
# foreign key problem - so subclass 

class Notingdeathreport(meta.Model):
    """ Processing the death report
        """
    report = meta.ForeignKey(Deathreport,
                             verbose_name=_("Death Report File"))
    date = meta.DateTimeField(
        _("Date Opened"),default=meta.LazyDate(),editable=False)
    action = meta.ForeignKey(Power,
                             verbose_name=_("Action Taken"))
    person = meta.ForeignKey(Person,
                             verbose_name=_("Person making the note"))
    note = meta.TextField(_("Note"))
    addedby = meta.CharField(_("Added By"),maxlength=100,editable=False)

    class META:
        admin = meta.Admin(
        list_display = ('report','date'),
            search_fields = ['report'],
        fields =
            (
                (
                None,
                    {
                    'fields': ('report',
                               'action',
                               'person',
                               'note')
                    }
                ),
                
                
                
            ),
        )
    def __repr__(self):
            return "%s %s" %(self.report,self.date)

class Notingbirthreport(Notingdeathreport):
    """ Processing the birth report
        """
    report = meta.ForeignKey(Birthreport,
                             verbose_name=_("Birth Report File"))

class Notingdeathregister(Notingdeathreport):
    """ Processing the death register
        """
    report = meta.ForeignKey(Birthregister,
                             verbose_name=_("Death Register Entry"))

class Notingbirthregister(Notingdeathreport):
    """ Processing the birth register
        """
    report = meta.ForeignKey(Birthregister,
                             verbose_name=_("Birth Register Entry"))



    

##############################################end of actual data details



