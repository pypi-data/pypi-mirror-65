# utils functions
def check_file_paths(filepaths):
    """check filepaths input extension
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Raises:
        Exception: Need at least two .rawls image filepaths
        Exception: Invalid input filepaths extension
    """

    if len(filepaths) < 2:
        raise Exception('Need at least two rawls image filepaths as input')

    if not all(['.rawls' in p for p in filepaths]):
        raise Exception('Unvalid input filepath images, need .rawls image')