from plone.fieldsets.fieldsets import FormFieldsets
from types import * 

from zope.app.component.hooks import getSite
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import Choice
from zope.schema import Tuple
from zope.schema import List
from zope.schema import TextLine
from zope.schema import Bool
from zope.schema import Object

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from osha.theme import OSHAMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from slc.subsite.interfaces import ISubsiteEnhanced

from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from plone.app.controlpanel.form import ControlPanelForm

from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import ListSequenceWidget


from persistent import Persistent
from zope.annotation.interfaces import IAnnotations

from Products.Five import BrowserView
from zope.interface import Interface, Attribute

SETTING_KEY="osha.settings"



# BrowserView to read the settings
class ISettingsView(Interface):
    """ """
    settings = Attribute("The subsite portal settings")
    
class SettingsView(BrowserView):

    def __init__(self, context, request):
        super(SettingsView, self).__init__(context, request)
        site = getSite()
        self.settings = PropertiesControlPanelAdapter(site).settings


        
        
class Settings(Persistent):
    """Settings for a site/subsite
    """
    logo_url = ''
    support_email = ''
    crosschecker_email = ''
    pm_email = ''
    listserv_email = ''
    site_slogan = []    
    oshmail_subscribers = ''
    default_language = ''
    

### Language vocabulary

class AvailableLanguagesVocabulary(object):
    """Vocabulary factory returning available languages for the portal.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        # need to get the context of the adapter
        site = getSite()
        ltool = getToolByName(site, 'portal_languages')
        available = ltool.getAvailableLanguages()
        supported = ltool.getSupportedLanguages()
        
        items = []
        for lang in supported:
            ulang = unicode(lang, 'utf-8')
            desc = u"%s (%s)" % (
                available[lang]['native'],
                ulang
                )
            items.append(SimpleTerm(ulang, ulang, desc))

        return SimpleVocabulary(items)

AvailableLanguagesVocabularyFactory = AvailableLanguagesVocabulary()


class ITitleLanguagePair(Interface):
    language = Choice(title=_(u"Language"), vocabulary="osha.vocabularies.AvailableLanguages")
    text = TextLine(title=_(u"Title"))

class TitleLanguagePair:
    implements(ITitleLanguagePair)
    
    def __init__(self, language='', text=''):
        self.language = language
        self.text = text
    
#
# Combined schemata and fieldsets
#

# Properties for Logo
class ILogoSchema(Interface):
    logo_url = TextLine(title=_(u"Link to the site logo (on the right)"),
                        description=_(u"Place here the path to your logo. Make sure it has the proper dimensions (104pxx92px)."),
                        default=u'topbanner2.jpg',
                        required=False
    )

# Properties for Email
#    support_email = ''
#    crosschecker_email = ''
#    pm_email = ''
#    listserv_email = ''

class IEmailSchema(Interface):
    support_email = TextLine(title=_(u"Support email address"),
                        description=_(u"This email address is used for sending the support form and the broken link form. If no email address is specified, the site administrators email address is used."),
                        required=False
    )
    crosschecker_email = TextLine(title=_(u"TC Cross Checker email address"),
                        description=_(u"The email address for the workflow group cross checker. If no email address is specified, the site administrators email address is used."),
                        required=False
    )    
    pm_email = TextLine(title=_(u"Agency Project Manager email address"),
                        description=_(u"The email address for the workflow group project manager. If no email address is specified, the site administrators email address is used."),
                        required=False
    )    
    listserv_email = TextLine(title=_(u"Listserv Address"),
                        description=_(u"The email address for the listserv server. If no email address is specified, the site administrators email address is used. "),
                        required=False
    )    

# Properties for Site Slogan
class ISloganSchema(Interface):
    site_slogan = List(title=_(u"Site Slogan"),
                        description=_(u"Displayed in the portal header. "),
                        default=[],
                        value_type=Object(ITitleLanguagePair, title=u"Slogan by Language"),
                        required=False
    )

# Properties for Parameters
class IParametersSchema(Interface):
    oshmail_subscribers = TextLine(title=_(u"Number of OSHMail Subscribers"),
                        description=_(u"Number of subscribers of the OSHMail newsletter."),
                        required=False
    )

class IPropertiesSchema(ILogoSchema, IEmailSchema, ISloganSchema, IParametersSchema):
    """Combined schema for the adapter lookup.
    """

class PropertiesControlPanelAdapter(SchemaAdapterBase):

    #adapts(IPloneSiteRoot)
    implements(IPropertiesSchema)

    def __init__(self, context):
        super(PropertiesControlPanelAdapter, self).__init__(context)
        self.context = context

    def get_logo_url(self):
        return self.settings.logo_url
    def set_logo_url(self, value):
        self.settings.logo_url = value
    logo_url = property(get_logo_url, set_logo_url)
    
    def get_support_email(self):
        return self.settings.support_email
    def set_support_email(self, value):
        self.settings.support_email = value
    support_email = property(get_support_email, set_support_email)

    def get_crosschecker_email(self):
        return self.settings.crosschecker_email
    def set_crosschecker_email(self, value):
        self.settings.crosschecker_email = value
    crosschecker_email = property(get_crosschecker_email, set_crosschecker_email)
   
    def get_pm_email(self):
        return self.settings.pm_email
    def set_pm_email(self, value):
        self.settings.pm_email = value
    pm_email = property(get_pm_email, set_pm_email)

    def get_listserv_email(self):
        return self.settings.listserv_email
    def set_listserv_email(self, value):
        self.settings.listserv_email = value
    listserv_email = property(get_listserv_email, set_listserv_email)        

    def get_default_language(self):
        return self.settings.default_language
    def set_default_language(self, value):
        self.settings.default_language = value
    default_language = property(get_default_language, set_default_language)

    @apply
    def site_slogan():
        def get(self):
            return [TitleLanguagePair(l,t) for (l,t) in self.settings.site_slogan]
        def set(self, value):
            pairs = []
            for ta in value:
                language = ta.language
                text = ta.text
                pairs.append((language,text))

            self.settings.site_slogan = pairs
        return property(get, set)
        


    def get_oshmail_subscribers(self):
        return self.settings.oshmail_subscribers
    def set_oshmail_subscribers(self, value):
        self.settings.oshmail_subscribers = value
    oshmail_subscribers = property(get_oshmail_subscribers, set_oshmail_subscribers)
    
    @property
    def settings(self):
        ann = IAnnotations(self.context)
        return ann.setdefault(SETTING_KEY, Settings())

 
logoset = FormFieldsets(ILogoSchema)
logoset.id = 'logo'
logoset.label = _(u'Logo')

emailset = FormFieldsets(IEmailSchema)
emailset.id = 'email'
emailset.label = _(u'Email')

sloganset = FormFieldsets(ISloganSchema)
sloganset.id = 'slogan'
sloganset.label = _(u'Slogan')

parametersset = FormFieldsets(IParametersSchema)
parametersset.id = 'parameters'
parametersset.label = _(u'Parameters')


title_widget = CustomWidgetFactory(ObjectWidget, TitleLanguagePair)
slogan_widget = CustomWidgetFactory(ListSequenceWidget,
                                           subwidget=title_widget)
               
                                         
class PropertiesControlPanel(ControlPanelForm):

    form_fields = FormFieldsets(logoset, emailset, sloganset, parametersset)
    form_fields['site_slogan'].custom_widget = slogan_widget
        
    label = _("Site Properties")
    description = _("Configuration of site specific settings")
    form_name = _("Site Properties")



