# main imports
import numpy as np

# stats import
from scipy.stats import skew, kurtosis

# modules imports
from .rawls import Rawls
from .utils import check_file_paths


class RawlsStats():
    """RawlsStats class which enables statistics other multiples Rawls instance
    
    Attributes:
        data: {ndrray} -- merged buffer data numpy array with higher dimension of all Rawls instance
        nelements: {int} -- number Rawls instance used
        details: {Details} -- details instance information
        mean_samples_per_elements: {float} -- statistic which gives mean number of samples used (if Rawls images do not have same number of samples)
        expected_shape: {(int, int, int)} -- describe expected shape of an Rawls image element
    """

    def __init__(self, rawls_images):
        """Init RawlsStats instance using list of Rawls instances
        
        Arguments:
            rawls_images {[Rawls]} -- list of Rawls instances
        
        Raises:
            Exception: Input format expection, unvalid input shape
        """

        shapes = []

        for img in rawls_images:
            shapes.append(img.shape)

        if not shapes[1:] == shapes[:-1]:
            raise Exception('Input rawls images do not have same shapes')

        # create array with higher dimension
        merged_values = np.array([img.data for img in rawls_images])

        # get total number of samples used
        total_samples = sum([img.details.samples for img in rawls_images])

        # details based on first element
        merged_details = rawls_images[0].details
        merged_details.samples = total_samples

        # set instance attributes
        self.data = merged_values
        self.nelements = len(rawls_images)
        self.details = merged_details
        self.mean_samples_per_element = self.details.samples / self.nelements
        self.expected_shape = shapes[0]

    @classmethod
    def load(self, filepaths):
        """load data from rawls files
        
        Arguments:
            filepath: {[str]} -- list of paths of .rawls files

        Returns:
            {RawlsStats} : RawlsStats instance
        """

        # check if given paths are corrects
        check_file_paths(filepaths)

        # read rawls
        rawls_images = []

        for filepath in filepaths:
            rawls_images.append(Rawls.load(filepath))

        # build
        return RawlsStats(rawls_images)

    def add(self, rawls_img):

        # check if list and recursively add elements if needed
        if isinstance(rawls_img, list):
            for img in rawls_img:
                self.add(img)

        else:
            # check elements
            if rawls_img.shape != self.expected_shape:
                raise Exception(
                    'Invalid rawls shape, impossible to add this shape with others elements'
                )

            rawls_data = np.expand_dims(rawls_img.data, axis=0)

            # append data to current elements
            self.data = np.concatenate([self.data, rawls_data], axis=0)

            # update others data
            self.details.samples += rawls_img.details.samples
            self.nelements += 1
            self.mean_samples_per_element = self.details.samples / self.nelements

    def mean(self):
        """Compute mean on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with mean data of rawls files
        """

        mean_values = np.mean(self.data, axis=0)
        return Rawls(self.expected_shape, mean_values, self.details)

    def var(self):
        """Compute variance on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with variance data of rawls files
        """

        var_values = np.var(self.data, axis=0)
        return Rawls(self.expected_shape, var_values, self.details)

    def std(self):
        """Compute std on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with std data of rawls files
        """

        std_values = np.std(self.data, axis=0)
        return Rawls(self.expected_shape, std_values, self.details)

    def skew(self):
        """Compute skewness on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with skewness data of rawls files
        """

        skew_values = skew(self.data, axis=0, nan_policy='raise')
        return Rawls(self.expected_shape, skew_values, self.details)

    def kurtosis(self):
        """Compute kurtosis on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with kurtosis data of rawls files
        """

        kurtosis_values = kurtosis(self.data, axis=0, nan_policy='raise')
        return Rawls(self.expected_shape, kurtosis_values, self.details)

    def __str__(self):
        """Display RawlsStats information
        
        Returns:
            {str} RawlsStats information
        """
        return "--------------------------------------------------------\nnelements: \n\t{0}\nDetails: \n{1}\nMean samples per element: \n\t{2}\nExpected shape: \n\t{3}\n--------------------------------------------------------".format(
            self.nelements, self.details, self.mean_samples_per_element,
            self.expected_shape)
