import pyvips
from pathlib import Path
from .error import SlideLoadError


class Slide:

    def __init__(self, path):
        self.path = path
        if not Path(path).exists():
            raise SlideLoadError("Slide File {} Not Found".format(path))
        self.slide = pyvips.Image.new_from_file(path)

        self.filestem = Path(path).stem
        self.wsi_width = self.slide.width
        self.wsi_height = self.slide.height
        self.set_properties()

    def export_thumbnail(self, save_to=".", size=500):
        thumb = self.get_thumbnail(size)
        thumb.pngsave("{}/thumb.png".format(save_to))

    def get_thumbnail(self, size=500):
        return pyvips.Image.thumbnail(self.path, size)

    def set_properties(self):
        for field in self.slide.get_fields():
            setattr(self, field, self.slide.get(field))
        if "openslide.objective-power" in self.slide.get_fields():
            self.magnification = self.slide.get("openslide.objective-power")
        else:
            self.magnification = None
