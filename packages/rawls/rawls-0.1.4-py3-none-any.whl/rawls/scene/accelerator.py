class Accelerator():
    """Accelerator class which store Accelerator information

    Attributes:
        name: {str} -- name of the accelerator
        params: {str} -- parameters of accelerator used
    """

    def __init__(self, name, params):
        """Construct accelerator with all information
        
        Arguments:
            name: {str} -- name of the accelerator
            params: {str} -- parameters of accelerator used
        """
        self.name = name
        self.params = params

    def __str__(self):
        """Display Accelerator information
        
        Returns:
            {str} -- accelerator information
        """
        if len(self.name) > 0:
            return "Accelerator: `{0}`, ({1})".format(self.name, self.params)
        else:
            return "Accelerator: default"

    def to_rawls(self):
        """Display Accelerator information for .rawls file
        
        Returns:
            {str} -- accelerator information for .rawls file
        """
        return "#Accelerator {0}\n\t#params {1}".format(self.name, self.params)
