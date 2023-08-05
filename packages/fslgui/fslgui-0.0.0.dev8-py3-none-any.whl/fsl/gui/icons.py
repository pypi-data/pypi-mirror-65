#  Copyright (c) 2019.
#  Taylor Hanayik University of Oxford
#  Last modified: 02/08/2019, 12:45

"""
This module provides easy to import resources to be used throughout the FSL guis.

These are mainly various icons and logo files.
"""

from os.path import dirname, join, abspath

ICON_PATH = join(abspath(dirname(__file__)), 'icons')

icon_add = join(ICON_PATH, "add.png")
icon_clear = join(ICON_PATH, "clear.png")
icon_code = join(ICON_PATH, "code.png")
icon_detach = join(ICON_PATH, "detach.png")
icon_download = join(ICON_PATH, "download.png")
icon_explore = join(ICON_PATH, "explore.png")
icon_help = join(ICON_PATH, "help.png")
icon_open_folder = join(ICON_PATH, "open_folder.png")
icon_pause = join(ICON_PATH, "pause.png")
icon_play = join(ICON_PATH, "play.png")
icon_play_all = join(ICON_PATH, "play_all.png")
icon_save = join(ICON_PATH, "save.png")
icon_settings = join(ICON_PATH, "settings.png")
icon_upload = join(ICON_PATH, "upload.png")

logo_fsl_x2 = join(ICON_PATH, "fsl-logo-x2.png")











