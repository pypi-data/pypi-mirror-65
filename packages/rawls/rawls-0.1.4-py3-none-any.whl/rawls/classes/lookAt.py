class LookAt():
    """LookAt class information

    Attributes:
        eye: {Vector3f} -- eye coordinate
        point: {Vector3f} -- point to look at coordinate
        up: {Vector3f} -- up vector
    """

    def __init__(self, eye, point, up):
        """LookAt information storage
        
        Arguments:
            eye: {Vector3} -- 3D eye coordinate
            point: {Vector3} -- 3D point to look at coordinate
            up: {Vector3} -- 3D up vector
        """
        self.eye = eye
        self.point = point
        self.up = up

    def __str__(self):
        """Display LookAt object representation
        
        Returns:
            {str} -- LookAt information
        """
        return 'LookAt: (eye: {0}, point: {1}, up: {2})'.format(
            self.eye, self.point, self.up)

    def to_rawls(self):
        """Display LookAt information for .rawls file
        
        Returns:
            {str} -- LookAt information for .rawls file
        """
        return "#LookAt {0} {1} {2}  {3} {4} {5}  {6} {7} {8}".format(
            self.eye.x, self.eye.y, self.eye.z, self.point.x, self.point.y,
            self.point.z, self.up.x, self.up.y, self.up.z)
