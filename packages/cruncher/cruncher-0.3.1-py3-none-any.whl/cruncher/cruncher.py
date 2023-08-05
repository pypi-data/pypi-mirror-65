"""
:Project: Cruncher
:Contents: cruncher.py
:copyright: © 2019 Daniel Morell
:license: GPL-3.0, see LICENSE for more details.
:Author: DanielCMorell
"""
# Standard Library Imports
import os

# Package Imports
from PIL import Image, ImageCms
import click

# Local Imports


class CruncherBase:

    def __init__(self, mode, path, output, image_path, version, file_format, settings):
        self.skip_image = False
        self.image = None
        self.mode = mode
        self.path = path
        self.output = output
        self.image_path = image_path
        self.version = version
        self.format = file_format
        self.settings = settings
        self.filename = self.generate_filename(os.path.split(image_path)[1], version)
        self.new_path = self.image_output_path(image_path)
        self.exif = b''
        self.output_bytes = 0
        self.messages = []

        # Open Image
        self.open_image()  # Step 1

        if self.skip_image:
            return

        # Run conversions and resizing
        self.convert_icc_profile()
        self.resize()

        if self.skip_image:
            return

        # Crunch the image
        self.crunch_image()  # needs o call self._save()

        self.get_output_kb()

    def image_output_path(self, image_path):
        """
        Calculate the output path for the image.

        :param image_path: Image input path.
        :return: Image output path.
        """
        if self.mode == 'img':
            return os.path.join(self.output, self.filename)
        relative_path = os.path.relpath(image_path, self.path)
        relative_path = os.path.join(os.path.split(relative_path)[0], self.filename)
        return os.path.join(self.output, relative_path)

    def crunch_image(self):
        pass

    def generate_filename(self, filename, version):
        if not version['append']:
            version['append'] = ''
        filename = filename.split('.')
        del (filename[-1])
        filename = '.'.join(filename)
        return f"{filename}{version['append']}.{self.format}"

    def resize(self):
        """
        The `resize()` function changes the size of an image without squashing or stretching
        as the PIL.Image.resize() function does.
        """

        image = self.image
        size = (self.version['width'], self.version['height'])
        version = self.version

        if size == (None, None):
            return image

        old_orientation = image.width / image.height
        new_orientation = size[0] / size[1]

        if (version['orientation']
                and (old_orientation <= 1 < new_orientation or old_orientation >= 1 > new_orientation)):
            # if one is horizontal and the other vertical flip the orientation
            size = (size[1], size[0])
            new_orientation = size[0] / size[1]

        if size == (image.width, image.height):
            self.image = image
            return

        if version['aspect']:
            image.thumbnail(size, Image.LANCZOS)
            self.image = image
            return

        if new_orientation < old_orientation:
            v_width = image.width - (image.height / size[1] * size[0])
            v_height = image.height
            left = v_width / 2
            top = 0
            right = image.width - left
            bottom = v_height

        else:
            v_width = image.width
            v_height = image.height - (image.width / size[0] * size[1])
            left = 0
            top = v_height / 2
            right = v_width
            bottom = image.height - top

        box = (left, top, right, bottom)
        try:
            resized = image.resize(size, Image.LANCZOS, box)
        except ValueError:
            self.messages.append(f'\n Image: {self.image_path} skipped because of resize error')
            self.skip_image = True
            return

        self.image = resized

    def calculate_sampling(self, options, base):
        if self.version['subsampling']:
            return self.version['subsampling']
        divisor = (100 - base) / len(options)
        raw_sampling = ((self.version['quality'] - base) / divisor) - 1
        if raw_sampling < 0:
            return 0
        return round(raw_sampling)

    def convert_icc_profile(self):
        """
        Converts image colors based on the input and output ICC profiles.

        :since: v0.2
        :return:
        """
        try:
            if (self.version.get('icc_conversion')
                    and self.settings.get('icc_conversions').get(self.version['icc_conversion'])):
                icc = self.settings['icc_conversions'][self.version['icc_conversion']]
                self.image = ImageCms.profileToProfile(
                    self.image,
                    inputProfile=icc.get('input_icc'),
                    outputProfile=icc.get('output_icc'),
                    renderingIntent=0,
                    outputMode=icc.get('mode')
                )
        except ImageCms.PyCMSError as e:
            self.messages.append(f'Image ICC profile conversion failed: {self.image_path}')
            self.skip_image = True

    def get_transparency(self, default=None):
        transparency = default
        if self.image.info.get('transparency'):
            transparency = self.image.info.get('transparency')
        return transparency

    def get_output_kb(self):
        """
        Get the output file size, and save to `self.output_bytes`.
        """
        self.output_bytes = os.stat(self.new_path).st_size

    def open_image(self):
        try:
            self.image = Image.open(self.image_path)
        except Image.DecompressionBombError as e:
            if click.confirm(f'\n{e}\nPath: {self.image_path}\nDo you want to try to crunch this image? '):
                Image.MAX_IMAGE_PIXELS = None
            else:
                self.skip_image = True
                self.messages.append(f'Image: {self.image_path} skipped because of decompression bomb error')
                return
        self.image = Image.open(self.image_path)
        if self.version['metadata'] and self.image.info.get('exif'):
            self.exif = self.image.info.get('exif')

    def _save(self, *args, **kwargs):
        self.image.save(*args, **kwargs)


class GIFCruncher(CruncherBase):

    def __init__(self, mode, path, output, image_path, version, settings):
        super().__init__(mode, path, output, image_path, version, "gif", settings)

    def crunch_image(self):
        transparency = self.get_transparency()
        args = [self.new_path, "GIF"]
        kwargs = {'optimize': True, 'transparency': transparency}
        self._save(self.image, *args, **kwargs)


class JPEGCruncher(CruncherBase):
    """
    Quality Based Sampling
        0 - 70: 4:2:0
        71 - 89: 4:2:2
        90 - 100: 4:4:4
    """

    def __init__(self, mode, path, output, image_path, version, settings):
        super().__init__(mode, path, output, image_path, version, "jpg", settings)

    def crunch_image(self):
        sampling = self.calculate_sampling([0, 1, 2], 40)
        args = [self.new_path, "JPEG"]
        kwargs = {
            'quality': self.version['quality'],
            'sampling': sampling,
            'optimize': True,
            'progressive': True,
            'exif': self.exif,
            'icc_profile': self.image.info.get('icc_profile')
        }
        try:
            self._save(*args, **kwargs)
        except IOError:
            self.image = self.image.convert('RGB')
            self._save(*args, **kwargs)


class JPEG2000Cruncher(CruncherBase):

    def __init__(self, mode, path, output, image_path, version, settings):
        super().__init__(mode, path, output, image_path, version, "jp2", settings)

    def crunch_image(self):
        image = Image.open(self.image_path)
        args = [self.new_path, "JPEG2000"]
        kwargs = {
            'quality_mode': 'dB',
            'quality_layers': self.version['quality'],
            'progressive': True
        }
        self._save(image, *args, **kwargs)


class PNGCruncher(CruncherBase):

    def __init__(self, mode, path, output, image_path, version, settings):
        super().__init__(mode, path, output, image_path, version, "png", settings)

    def crunch_image(self):
        image = Image.open(self.image_path)
        transparency = self.get_transparency()
        args = [self.new_path, "PNG"]
        kwargs = {
            'optimize': True,
            'exif': self.exif,
            'transparency': transparency
        }
        try:
            self._save(image, *args, **kwargs)
        except IOError:
            image = image.convert('RGB')
            self._save(image, *args, **kwargs)


class WebPCruncher(CruncherBase):

    def __init__(self, mode, path, output, image_path, version, settings):
        super().__init__(mode, path, output, image_path, version, "webp", settings)

    def crunch_image(self):
        image = Image.open(self.image_path)
        args = [self.new_path, "WEBP"]
        kwargs = {
            'quality': (100 - self.version['quality']),
            'method': 0,
            'exif': self.exif
        }
        self._save(image, *args, **kwargs)
