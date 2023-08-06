class Vector3f():
    """3D vector representation
    
    Attributes:
        x: {float} -- x axis value
        y: {float} -- y axis value
        z: {float} -- z axis value
    """

    def __init__(self, x, y, z):
        """3D vector represention constructor
        
        Arguments:
            x: {float} -- x axis value
            y: {float} -- y axis value
            z: {float} -- z axis value
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """Display Vector3f object representation
        
        Returns:
            {str} -- Vector3f information
        """
        return '({0}, {1}, {2})'.format(self.x, self.y, self.z)
