import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common


class NapoFriendsViewlet(common.ViewletBase):

    _template = ViewPageTemplateFile('templates/napo_friendsmenu.pt')

    def render(self):
        return self._template()

    def listobjects(self):
        context = Acquisition.aq_inner(self.context)
        container = Acquisition.aq_parent(context)
        objects = container.objectValues(['ATDocument', 'RichDocument'])
        ip = container.getDefaultPage()
        filtered_objects = [x for x in objects if x.getId()!=ip]
        return filtered_objects
