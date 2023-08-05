#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

###############################################################################
# @package xenon2
#
###############################################################################

import logging
import sys

from .version import __version_info__
from .version import __release_date__

__module_name__ = "pygenash"
__version__ = '.'.join(str(c) for c in __version_info__)
__author__ = "Florent Tournois"
__copyright__ = "Copyright 2018, Guichet Entreprises"

__credits__ = ["Arnaud Boidard"]
__license__ = "MIT"
__maintainer__ = "Arnaud Boidard"
__email__ = "florent.tournois@gmail.fr"
__status__ = "Production"
__url__ = 'https://gitlab.com/guichet-entreprises.fr/tools/pygenash'

__gitlab_url__ = "https://gitlab.com/"
__gitlab_project_id__ = "15347134"

__all__ = []


###############################################################################
# Main script call only if this script is runned directly
###############################################################################
def __main():
    # ------------------------------------
    logging.info('Started %s', __file__)
    logging.info('The Python version is %s.%s.%s',
                 sys.version_info[0], sys.version_info[1], sys.version_info[2])

    print("version=%s" % __version__)

    logging.info('Finished')

    # ------------------------------------


###############################################################################
# Call main function if the script is main
# Exec only if this script is runned directly
###############################################################################
if __name__ == '__main__':
    __main()
