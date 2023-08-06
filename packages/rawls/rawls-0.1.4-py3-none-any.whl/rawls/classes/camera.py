class Camera():
    """Camera class which store camera information

    Attributes:
        name: {str} -- name of the camera
        fov: {float} -- field of view information
        focaldistance: {float} -- focal distance of camera
        lensradius: {float} -- lens radius of camera
    """

    def __init__(self, name, fov, focaldistance=None, lensradius=None):
        """Construct camera with all information
        
        Arguments:
            name: {str} -- name of the camera
            fov: {float} -- field of view information
            focaldistance: {float} -- focal distance information
            lensradius: {float} -- lens radius information
        """
        self.name = name
        self.fov = float(fov)

        if focaldistance is not None:
            self.focaldistance = float(focaldistance)
        else:
            self.focaldistance = None

        if lensradius is not None:
            self.lensradius = float(lensradius)
        else:
            self.lensradius = None

    def __str__(self):
        """Display Camera information
        
        Returns:
            {str} -- camera information
        """
        return "Camera: `{0}`, (fov: {1}, focaldistance: {2}, lensradius: {3})".format(
            self.name, self.fov, self.focaldistance, self.lensradius)

    def to_rawls(self):
        """Display Accelerator information for .rawls file
        
        Returns:
            {str} -- accelerator information for .rawls file
        """
        return "#Camera {0}\n\t#params \"float fov\" [{1}] \"float focaldistance\" [{2}] \"float lensradius\" [{3}]".format(
            self.name, self.fov, self.focaldistance, self.lensradius)
