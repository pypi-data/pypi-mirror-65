class Filter():
    """Filter class which store Filter information

    Attributes:
        name: {str} -- name of the filter
        params: {str} -- parameters of filter used
    """

    def __init__(self, name, params):
        """Construct filter with all information
        
        Arguments:
            name: {str} -- name of the filter
            params: {str} -- parameters of filter used
        """
        self.name = name
        self.params = params

    def __str__(self):
        """Display Filter information
        
        Returns:
            {str} -- filter information
        """
        return "Filter: `{0}`, ({1})".format(self.name, self.params)

    def to_rawls(self):
        """Display Filter information for .rawls file
        
        Returns:
            {str} -- filter information for .rawls file
        """
        return "#Filter {0}\n\t#params {1}".format(self.name, self.params)