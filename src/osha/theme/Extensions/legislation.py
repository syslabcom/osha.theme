import os.path
import time, Acquisition
from Acquisition import aq_inner, aq_parent, aq_base, aq_chain, aq_get
from Products.CMFCore.utils import getToolByName
from Testing.makerequest import makerequest
import transaction
from BeautifulSoup import BeautifulSoup

class LegislationMigration:

    def __init__(self, app=None, portal_id="", portal=None):
        self.folder_map = {"The OSH framework directive":
                  ["1"],
                  "Workplaces, equipment, signs, personal protective equipment/OSH directives":
                  ["21", "9", "4", "3", "2"],
                  "Workplaces, equipment, signs, personal protective equipment/OSH related aspects":                   
                   ["council-directive-2006-95",
                   "directive-2006-42-ec-of-the-european-parliament-and-of-the-council",
                   "53",
                   "directive-98-37-ec-of-the-european-parliament-and-of-the-council",
                   "42", "33", "35", "56", "34",
                   "council-directive-89-106-eec",
                   "41",
                   "council-directive-85-374-eec",
                   "39", "38", "37", "36", "40"],
                  "Exposure to chemical agents and chemical safety/OSH directives":
                  ["commission-directive-2006-15-ec",
                   "directive.2008-02-07.5735076588",
                   "directive.2008-05-22.7061217851",
                   "75", "28", "25"],
                   "Exposure to chemical agents and chemical safety/OSH related aspects":
                   ["directive-2008-68-ec",
                   "regulation-ec-no-1907-2006-of-the-european-parliament-and-of-the-council",
                   "59", "64", "66",
                   "council-directive-91-414-eec",
                   "58"
                   ],
                  "Exposure to physical hazards/OSH directives":
                  ["directive-2006-25-ec-of-the-european-parliament-and-of-the-council-of-5-april-2006",
                   "directive-2004-40-ec-of-the-european-parliament-and-of-the-council",
                   "82", "19", "73"],
                   "Exposure to physical hazards/OSH related aspects":
                   ["council-directive-2009-71-euratom",
                   "council-directive-2004-108-ec",
                   "council-directive-2003-122-euratom",
                   "directive-2000-14-ec",
                   ],
                  "Exposure to biological agents":
                  ["77"],
                  "Provisions on workload, ergonomical and psychosocial risks/OSH directives":
                  ["5", "6"],
                   "Provisions on workload, ergonomical and psychosocial risks/OSH related aspects":
                   ["directive-2003-88-ec",
                   "directive-2002-15-ec",
                   "council-directive-2000-79-ec"],
                  "Sector specific and worker related provisions/OSH directives":
                  ["18", "13", "12", "11", "10", "15", "17", "16"],
                  "Sector specific and worker related provisions/OSH related aspects":
                  ["council-directive-2006-54-ec",
                   "directive.2005-01-03.0697184648",
                   "council-directive-2000-78-ec"],
                  }
        # missing:
        # ['31', 'directive-2001-18-ec-of-the-european-parliament-and-of-the-council']
        if portal:
            self.portal_root = portal
            self.portal = portal
            self.portal_path  = "/" + portal.id + "/en"
        else:
            self.portal_root = app[portal_id]
            self.portal = makerequest(self.portal_root)
            self.portal_path  = "/" + portal_id + "/en"
        self.directives_path = self.portal_path + "/legislation/directives/"
        portal_catalog = getToolByName(self.portal_root, 'portal_catalog')
        self.pc = portal_catalog

    def generateShortName(self, title):
        return title.replace(" ", "-").replace(",","").lower()

    def createFolders(self):
        for folder in self.folder_map.keys():
            container = self.directives_path
            new_folder = self.generateShortName(folder)
            portal = makerequest(self.portal_root)
            container_ob = portal.restrictedTraverse(container)
            if "/" in new_folder:
                a_title, b_title = folder.split("/")
                a,b = new_folder.split("/")
                if a not in container_ob.objectIds():
                    container_ob.invokeFactory(
                        "Folder", a, title=a_title
                        )
                a_ob = container_ob[a]
                if b not in a_ob.objectIds():
                    a_ob.invokeFactory(
                        "Folder", b, title=b_title
                        )
                
            elif new_folder not in container_ob.objectIds():
                container_ob.invokeFactory(
                    "Folder", new_folder, title=folder
                    )

    def createNewDirectiveDocuments(self):
        """ section_map is a map of each Directive section to a list
        of brains of objects in that section.

        If the Directive section is correct we copy over the object to
        the new location.
        """
        for folder in self.folder_map.keys():
            for directive in self.folder_map[folder]:
                path = "/"+self.portal.id+"/data/legislation/"+str(directive)
                old_ob = self.portal.unrestrictedTraverse(path)
                old_id = old_ob.id
                new_folder_path = self.directives_path +\
                                  self.generateShortName(folder)
                new_folder = self.portal.unrestrictedTraverse(new_folder_path)
                body = old_ob.abstract.getRaw()
                soup = BeautifulSoup(body)
                styles = soup.findAll("style")
                # remove any style blocks
                for style in styles:
                    style.extract()
                #links = [i['href'] for i in soup.findAll("a")]
                links = [i for i in soup.findAll("a")]
                internal_links = []
                for link in links:
                    if link.has_key("href"):
                        href = link["href"]
                        if href.startswith("/data")\
                           or href.startswith("."):
                            #it must be an internal link to another directive
                            directive = href.split("/")[-1]
                            for val in self.folder_map.values():
                                if directive in val:
                                    target_folder = ""
                                    for key in self.folder_map.keys():
                                        if directive in self.folder_map[key]:
                                            target_folder = self.generateShortName(key)
                                            new_href = "../"+target_folder+"/"+directive
                                            link['href'] = new_href 
                text = str(soup)
                if old_id not in new_folder.objectIds():
                    new_folder.invokeFactory("Document", old_id,
                                         title = old_ob.title,
                                         description = old_ob.description,
                                         text = text,
                                         effective_date = old_ob.effective_date,
                                         expiration_date = old_ob.expiration_date,
                                         creation_date = old_ob.creation_date,
                                         modification_date = old_ob.modification_date,
                                         creators = old_ob.creators,
                                         contributors = old_ob.contributors)
                # else:
                #     print "Directive %s already exists. Skipping"\
                #           % new_folder[old_id].absolute_url()

    def migrateLegislation(self):
        self.createFolders()
        self.createNewDirectiveDocuments()

def run(self):
    migration = LegislationMigration(portal=self)
    migration.migrateLegislation()

if __name__ == "__main__":
    migration = LegislationMigration(app=app, portal_id="osha")
    migration.migrateLegislation()
    print "Done"
