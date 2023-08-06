class Sampler():
    """Sampler class representation
        
    Attributes:
        name: {str} -- name of the sampler technique
        pixelsamples: {int} -- number of samples used
    """

    def __init__(self, name, pixelsamples):
        """Construct Sampler instance
        
        Arguments:
            name: {str} -- name of the sampler technique
            pixelsamples: {int} -- number of samples used
        """
        self.name = name
        self.pixelsamples = int(pixelsamples)

    def __str__(self):
        """Display Sampler information
        
        Returns:
            {str} Sampler information
        """
        return "Sampler: `{0}` \n\t\t- samples: {1}".format(
            self.name, self.pixelsamples)

    def to_rawls(self):
        """Display Sampler information for .rawls file
        
        Returns:
            {str} -- Sampler information for .rawls file
        """
        return "#Sampler {0}\n\t#params \"integer pixelsamples\" [{1}]".format(
            self.name, self.pixelsamples)