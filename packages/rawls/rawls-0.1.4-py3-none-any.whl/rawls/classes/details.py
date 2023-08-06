# main imports
import re

# class imports
from .sampler import Sampler
from .integrator import Integrator
from .camera import Camera
from .resolution import Resolution
from .lookAt import LookAt
from .vector import Vector3f
from .filter import Filter
from .accelerator import Accelerator


class Details():
    """Rawls details information

    Attributes:
            resolution: {Resolution} -- x and y resolution of image
            samples: {int} -- number of samples used for generate image
            pixelfilter: {Filter} -- pixelfilter instance with information
            sampler: {Sampler} -- sampler instance with information
            accelerator: {Accelerator} -- accelerator instance with information
            integrator: {Integrator} -- integrator instance with information
            camera: {Camera} -- camera instance with information
            lookAt: {LookAt} -- look at instance with eye, point and up vector
    """

    def __init__(self, resolution, samples, pixelfilter, sampler, accelerator,
                 integrator, camera, lookAt):
        """Details information used to rendering current image
        
        Arguments:
            resolution: {Resolution} -- x and y resolution of image
            samples: {int} -- number of samples used for generate image
            pixelfilter: {Filter} -- pixelfilter instance with information
            sampler: {Sampler} -- sampler instance with information
            accelerator: {Accelerator} -- accelerator instance with information
            integrator: {Integrator} -- integrator instance with information
            camera {Camera} -- camera instance with information
            lookAt {LookAt} -- look at instance with eye, point and up information
        """
        self.samples = samples
        self.pixelfilter = pixelfilter
        self.resolution = resolution
        self.accelerator = accelerator
        self.integrator = integrator
        self.sampler = sampler
        self.camera = camera
        self.lookAt = lookAt

    @classmethod
    def fromcomments(self, comments):
        """Instanciate Details object with all comments information
        
        Arguments:
            comments: {str} -- extracted comments data

        Returns:
            {Details} -- details information instance
        """
        comments_line = comments.split('\n')

        samples = None
        for index, line in enumerate(comments_line):

            if 'Film' in line:
                res = re.findall(r'\[\d*', comments_line[index + 1])

                # only if output filename information is present
                if len(res) > 2:
                    del res[-1]  # remove name of outfile

                resolution = [int(r.replace('[', '')) for r in res]
                resolution = Resolution(resolution[0], resolution[1])

            if 'Samples' in line:
                samples = int(line.split(' ')[-1])

            if 'Filter' in line:
                if len(line.split(' ')) < 2:
                    filter_name = line.split(' ')[-1]
                    filter_params = comments_line[index + 1].split(' ')[-1]
                    pixelfilter = Filter(filter_name, filter_params)
                else:
                    pixelfilter = Filter('', '')

            if 'Sampler' in line:
                sampler_name = line.split(' ')[-1]

                res = re.findall(r'\[\d*', comments_line[index + 1])
                pixelsamples = int(res[0].replace('[', ''))
                sampler = Sampler(sampler_name, pixelsamples)

            if 'Accelerator' in line:
                if len(line.split(' ')) < 2:
                    accelerator_name = line.split(' ')[-1]
                    accelerator_params = comments_line[index +
                                                       1].split(' ')[-1]
                    accelerator = Accelerator(accelerator_name,
                                              accelerator_params)
                else:
                    accelerator = Accelerator('', '')

            if 'Integrator' in line:
                integrator_name = line.split(' ')[-1]
                res = re.findall(r'\[\d*', comments_line[index + 1])
                maxdepth = int(res[0].replace('[', ''))
                integrator = Integrator(integrator_name, maxdepth)

            if 'Camera' in line:
                camera_name = line.split(' ')[-1]
                res = re.findall(r'\[\d*', comments_line[index + 1])
                parsed_res = [float(r.replace('[', '')) for r in res]

                # check default value
                if len(parsed_res) > 2:
                    camera = Camera(camera_name, parsed_res[0], parsed_res[1],
                                    parsed_res[2])
                else:
                    camera = Camera(camera_name, parsed_res[0])

            if 'LookAt' in line:
                info = line.split()
                del info[0]
                info = [float(i) for i in info]

                eye = Vector3f(info[0], info[1], info[2])
                point = Vector3f(info[3], info[4], info[5])
                up = Vector3f(info[6], info[7], info[8])

                lookAt = LookAt(eye, point, up)

        return Details(resolution, samples, pixelfilter, sampler, accelerator,
                       integrator, camera, lookAt)

    def __str__(self):
        """Display Details object representation
        
        Returns:
            {str} -- details information
        """
        return 'Samples {0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}'.format(
            self.samples, self.pixelfilter, self.resolution, self.sampler,
            self.accelerator, self.integrator, self.camera, self.lookAt)

    def to_rawls(self):
        """Display Details information for .rawls file
        
        Returns:
            {str} -- details information for .rawls file
        """
        return '#Samples {0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}'.format(
            self.samples, self.pixelfilter.to_rawls(),
            self.resolution.to_rawls(), self.sampler.to_rawls(),
            self.accelerator.to_rawls(), self.integrator.to_rawls(),
            self.camera.to_rawls(), self.lookAt.to_rawls())
