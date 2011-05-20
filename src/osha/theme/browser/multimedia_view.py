from ordereddict import OrderedDict

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MultimediaImageFoldersView(BrowserView):
    """
    Photo gallery style folder listing
    """
    template = ViewPageTemplateFile(
        'templates/multimedia_image_folders_view.pt')
    template.id = "multimedia-image-folders-view"

    def __call__(self):
        return self.template()

    def get_image_folders(self):
        """Get an ordered dict of folders and details of their images

        OrderedDict(
            "folder_id1": {
                "title": "Folder 1"
                "images":
                    OrderedDict(
                    "image_1":"Image 1",
                    )
                }
            )
        """
        max_image_folders = 6
        image_folders = OrderedDict()
        for folder in self.context.objectValues():
            if max_image_folders < 1:
                return image_folders
            if folder.portal_type == "Folder":
                images = OrderedDict()
                for image in folder.objectValues():
                    if image.portal_type == "Image":
                        images[image.id] = {"title" : image.title}
                if images:
                    image_folders[folder.id] = {"title" : folder.title,
                                           "images" : images}
                    max_image_folders = max_image_folders - 1
        return image_folders

class MultimediaImageDetailsView(BrowserView):
    template = ViewPageTemplateFile(
        'templates/multimedia_image_details_view.pt')
    template.id = "multimedia-image-details-view"

    def __call__(self):
        return self.template()

    def get_images_in_folder(self):
        """Get an ordered dict of images and titles

        OrderedDict("image_1": "Image 1",)
        """
        images = OrderedDict()
        for image in folder.objectValues():
            if image.portal_type == "Image":
                images[image.id] = image.title
        return images
