from django.core import meta


#######################################################################

sexes = (
    ('M','Male'),
    ('F','Female'),
    )

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
            return "%s" %(self.name)

class Status(meta.Model):
    name = meta.CharField(_("Status"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.name)

class Official(meta.Model):
    rank = meta.CharField(_("Rank"),maxlength=50,unique=True)
    powers = meta.ManyToManyField(Power)
    class META:
        admin = meta.Admin(
        list_display = ('rank',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.rank)

class Person(meta.Model):
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

# master tables for actual data

class Area(meta.Model):
    name = meta.CharField(_("Area"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.name)

        

class Street(meta.Model):
    name = meta.CharField(_("Street"),maxlength=50)
    area = meta.ForeignKey(Area)
    class META:
        unique_together = (("name","area"),)
        admin = meta.Admin(
        list_display = ('name','area',),
            search_fields = ['name'],)
    def __repr__(self):
            return _("Street: %s Area %s") %(self.name,self.get_area)

class Deathplace(meta.Model):
    name = meta.CharField(_("Area"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.name)

class Birthplace(meta.Model):
    name = meta.CharField(_("Area"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.name)

class Reporttype(meta.Model):
    name = meta.CharField(_("Area"),maxlength=50,unique=True)

    class META:
        admin = meta.Admin(
        list_display = ('name',),
            search_fields = ['name'],)
    def __repr__(self):
            return "%s" %(self.name)

##############################################end of actual data master


# detail tables for actual data

#birth reports, death reports, birth register death register
#should have just one big class and subclass the rest - but
#subclassing is borked. The fields get diplayed in reverse order
#in the admin. 

class Birthreport(meta.Model):
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
