import os
import errno


def initialize_dirs():
    """
    Initialize directories for project:
    /data/history
    :return:
    """
    # create directory for user = name
    try:
        os.makedirs('data/history')
        print("Created directory:  data/history")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
