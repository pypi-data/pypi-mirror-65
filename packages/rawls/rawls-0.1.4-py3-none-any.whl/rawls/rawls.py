# main imports
import math
import numpy as np
import struct
import copy
import os

# image processing imports
from PIL import Image

# package imports
from .scene.details import Details

extensions = ['png', 'rawls']


class Rawls():
    """Rawls class used to open `.rawls` path image

    Attributes:
        shape: {(int, int, int)} -- describe shape of the image
        data: {ndrray} -- buffer data numpy array
        details: {Details} -- details instance information
        gamma_converted: {Details} -- specify if Rawls instance is gamma converted or not
    """

    def __init__(self, shape, data, details, gamma_converted=False):
        self.shape = shape
        self.data = data
        self.details = details
        self.gamma_converted = gamma_converted

    @classmethod
    def load(self, filepath):
        """Open data of rawls file
        
        Arguments:
            filepath: {str} -- path of the .rawls file to open

        Returns:
            {Rawls} : Rawls instance
        """

        if '.rawls' not in filepath:
            raise Exception('filepath used is not valid')

        f = open(filepath, "rb")

        # finding data into files
        ihdr_line = 'IHDR'
        ihdr_found = False

        comments_line = 'COMMENTS'
        comments_found = False

        data_line = 'DATA'
        data_found = False

        # prepare rawls object data
        img_chanels = None
        img_width = None
        img_height = None

        comments = ""
        data = None

        # read first line
        line = f.readline()
        line = line.decode('utf-8')

        while not ihdr_found:

            if ihdr_line in line:
                ihdr_found = True

                # read info line
                f.readline()

                values = f.readline().strip().replace(b' ', b'')
                img_width, img_height, img_chanels = struct.unpack(
                    'III', values)

                data = np.empty((img_height, img_width, img_chanels))

        line = f.readline()
        line = line.decode('utf-8')

        while not comments_found:

            if comments_line in line:
                comments_found = True

        # get comments information
        while not data_found:

            line = f.readline()
            line = line.decode('utf-8')

            if data_line in line:
                data_found = True
            else:
                comments += line

        # default read data size
        line = f.readline()

        # read buffer image data (here samples)
        for y in range(img_height):
            for x in range(img_width):

                # read the float bytes
                line = f.read(4 * img_chanels)
                values = struct.unpack('f' * img_chanels, line)

                for c in range(img_chanels):
                    data[y][x][c] = values[c]

                # skip new line
                f.read(1)

        f.close()

        details = Details.fromcomments(comments)

        return Rawls(data.shape, data, details)

    @classmethod
    def fusion(self, rawls_image_1, rawls_image_2):
        """Fusion two rawls images together based on their number of samples
        
        Arguments:
            rawls: {Rawls} -- first Rawls image to merge
            rawls: {Rawls} -- second Rawls image to merge

        Returns:
            {Rawls} -- Rawls instance
        """

        if not isinstance(rawls_image_1, Rawls):
            raise Exception("`rawls_image_1` parameter is not of Rawls type")

        if not isinstance(rawls_image_2, Rawls):
            raise Exception("`rawls_image_2` parameter is not of Rawls type")

        # compute merge between two `Rawls` instances
        total_samples = float(rawls_image_1.details.samples +
                              rawls_image_2.details.samples)

        image_1_percent = rawls_image_1.details.samples / total_samples
        image_2_percent = rawls_image_2.details.samples / total_samples

        buffer_image_1 = rawls_image_1.data * image_1_percent
        buffer_image_2 = rawls_image_2.data * image_2_percent

        output_buffer = np.add(buffer_image_1, buffer_image_2)

        # update details informations (here samples used)
        details = copy.deepcopy(rawls_image_1.details)
        details.samples = int(total_samples)

        return Rawls(output_buffer.shape, output_buffer, details)

    def save(self, outfile, gamma_convert=True):
        """Save rawls image into new file
        
        Arguments:
            outfile: {str} -- output filename (rawls or png)
            gamma_convert: {bool} -- necessary or not to convert using gamma (default: True)
        """

        # check if expected extension can be managed
        extension = outfile.split('.')[-1]

        if extension not in extensions:
            raise Exception("Can't save image using `" + extension +
                            "` extension..")

        # check if necessary to construct output folder
        folder_path = outfile.split('/')

        if len(folder_path) > 1:
            del folder_path[-1]

            output_path = ''
            for folder in folder_path:
                output_path = os.path.join(output_path, folder)

            if not os.path.exists(output_path):
                os.makedirs(output_path)

        # save image using specific extension
        if extension == 'rawls':
            h, w, c = self.shape
            f = open(outfile, 'wb')

            f.write(b'IHDR\n')
            f.write(bytes(str(self.data.ndim * 4), 'utf-8') + b'\n')
            f.write(
                struct.pack('i', w) + b' ' + struct.pack('i', h) + b' ' +
                struct.pack('i', c) + b'\n')

            f.write(b'COMMENTS\n')
            f.write(bytes(self.details.to_rawls() + '\n', 'utf-8'))

            f.write(b'DATA\n')
            # integer is based on 4 bytes
            f.write(struct.pack('i', h * w * c * 4) + b'\n')

            for i in range(h):
                for j in range(w):

                    for k in range(c):
                        f.write(struct.pack('f', self.data[i][j][k]))
                    f.write(b'\n')

            f.close()

        elif extension == 'png':
            self.to_png(outfile, gamma_convert)

    def __clamp(self, n, smallest, largest):
        """Clamp number using two numbers
        
        Arguments:
            n: {float} -- the number to clamp
            smallest: {float} -- the smallest number interval
            largest: {float} -- the larget number interval
        
        Returns:
            {float} -- the clamped value
        """
        return max(smallest, min(n, largest))

    def __gamma_correct(self, value):
        """Correct gamma of luminance value
        
        Arguments:
            value: {float} -- luminance value to correct
        
        Returns:
            {float} -- correct value with specific gamma
        """
        if value <= 0.0031308:
            return 12.92 * value
        else:
            return 1.055 * math.pow(value, float(1. / 2.4)) - 0.055

    def __gamma_convert(self, value):
        """Correct gamma value and clamp it
        
        Arguments:
            value: {float} -- luminance value to correct and clamp
        
        Returns:
            {float} -- final chanel value
        """
        return self.__clamp(255. * self.__gamma_correct(value) + 0., 0., 255.)

    def gammaConvert(self):
        """Convert gamma of luminance chanel values of rawls image
        
        Returns:
            {ndarray} -- image buffer with converted gamma values
        """

        if not self.gamma_converted:
            height, width, chanels = self.shape

            for y in range(height):
                for x in range(width):
                    for c in range(chanels):
                        self.data[y][x][c] = self.__gamma_convert(
                            self.data[y][x][c])

            self.gamma_converted = True

    def to_pil(self, gamma_convert=True):
        """Convert current rawls image into PIL RGB Image
        
        Arguments:
            gamma_convert: {bool} -- necessary or not to convert using gamma (default: True)

        Returns:
            {PIL} -- RGB image converted
        
        Example:

        >>> import numpy as np
        >>> from rawls.rawls import Rawls
        >>> path = 'images/example_1.rawls'
        >>> rawls_img = Rawls.load(path)
        >>> rawls_pil_img = rawls_img.to_pil()
        >>> np.array(rawls_pil_img).shape
        (100, 100, 3)
        """
        if gamma_convert:
            self.gammaConvert()  # convert image to gamma if necessary

        # prepare input data
        input_data = np.array(self.data, 'uint8')

        # check if only one channel
        if self.data.ndim == 3:
            h, w, c = self.shape

            if c == 1:
                input_data = input_data.reshape(h, w)

        return Image.fromarray(input_data)

    def to_png(self, outfile, gamma_convert=True):
        """Save rawls image into PNG
        
        Arguments:
            outfile: {str} -- PNG output filename
            gamma_convert: {bool} -- necessary or not to convert using gamma (default: True)
        """

        if '/' in outfile:
            folders = outfile.split('/')
            del folders[-1]

            output_path = ''
            for folder in folders:
                output_path = os.path.join(output_path, folder)

            if not os.path.exists(output_path):
                os.makedirs(output_path)

        if '.png' not in outfile:
            raise Exception('output filename is not `.png` format')

        self.to_pil(gamma_convert).save(outfile)

    def h_flip(self):
        """Flip horizontally current Rawls instance 
        """
        self.data = np.flip(self.data, axis=1)

    def v_flip(self):
        """Flip vectically current Rawls instance 
        """
        self.data = np.flip(self.data, axis=0)

    def copy(self):
        """Copy current Rawls instance
        
        Returns:
            {Rawls} -- Rawls copy of current instance
        """
        return copy.deepcopy(self)

    def normalize(self, max_value=None):
        """Give new Rawls instance with normalized data
        
        Arguments:
            max_value {float} -- max expected value for normalization (default: {max data value})
        
        Returns:
            {Rawls} -- Rawls instance with normalized data
        """
        min_value = np.min(self.data)

        normalized_data = self.data
        # check negative values
        if min_value < 0:
            normalized_data = self.data + abs(min_value)

        # default max value
        if max_value is None:
            max_value = np.max(normalized_data)

        normalized_data /= max_value

        return Rawls(normalized_data.shape, normalized_data, self.details,
                     self.gamma_converted)

    def __str__(self):
        """Display Rawls information
        
        Returns:
            {str} Rawls information
        """
        return "--------------------------------------------------------\nShape: \n\t{0}\nDetails: \n{1}\nGamma converted: \n\t{2}\n--------------------------------------------------------".format(
            self.shape, self.details, self.gamma_converted)
