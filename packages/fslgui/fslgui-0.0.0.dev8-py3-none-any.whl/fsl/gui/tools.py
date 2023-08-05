"""
models store data and allow FSL tools to be called from other python scripts
"""
#!/usr/bin/env python
#
# bet_model.py
#
# Author: Taylor Hanayik <hanayik@gmail.com>
import os
import subprocess

from fsl.utils import idle



class Bet(object):
    """
    A BetModel contains the data and methods necessary to setup and run FSL's bet tool.
    The BetModel can be queried and properties can be set via a controller of a GUI view object
    """
    bet_type_choices = {
        'default': '',
        'robust': '-R',
        'eye and optic nerve cleanup': '-S',
        'bias field and neck cleanup': '-B',
        'small z field of view': '-Z',
        'apply 4D': '-F',
        'bet + betsurf': '-A',
        'bet + betsurf with additional T2w image': '-A2'
    }

    def __init__(self,
                 image_in="",
                 image_t2="",
                 image_out="",
                 bet_type="",
                 fval=0.5,
                 gval=0,
                 center_coord=(0, 0, 0),
                 discard_bet=False,
                 save_mask=False,
                 applythresh=False,
                 save_skull=False,
                 save_overlay=False,
                 verbose=False,
                 suffix="_brain",
                 prefix=""
                 ):
        self._image_in = image_in
        self._image_t2 = image_t2
        self._image_out = image_out
        self._bet_type = bet_type
        self._fval = fval
        self._gval = gval
        self._center_coord = center_coord
        self._discard_bet = discard_bet
        self._save_mask = save_mask
        self._applythresh = applythresh
        self._save_skull = save_skull
        self._save_overlay = save_overlay
        self._verbose = verbose
        self._suffix = suffix
        self._prefix = prefix

        self._bool_argmap = {
            '-o': self._save_overlay,
            '-m': self._save_mask,
            '-s': self._save_skull,
            '-n': self._discard_bet,
            '-t': self._applythresh
        }

    # the input image string
    @property
    def image_in(self):
        return self._image_in

    @image_in.setter
    def image_in(self, val):
        assert isinstance(val, str), "image_in must be a string"
        self._image_in = val

    # the optional T2w input image str
    @property
    def image_t2(self):
        return self._image_t2

    @image_t2.setter
    def image_t2(self, val):
        assert isinstance(val, str), "image_t2 must be a string"
        self._image_t2 = val

    # the output image string
    @property
    def image_out(self):
        return self._image_out

    @image_out.setter
    def image_out(self, val):
        assert isinstance(val, str), "image_out must be a string"
        self._image_out = val

    @property
    def bet_type(self):
        return self._bet_type

    @bet_type.setter
    def bet_type(self, val):
        assert isinstance(val, str), "bet type must be a string"
        self._bet_type = val

    @property
    def fval(self):
        return self._fval

    @fval.setter
    def fval(self, val):
        val = float(val)
        assert (val >= 0) & (val <= 1), "fval must be in the range 0 .. 1"
        self._fval = val

    @property
    def gval(self):
        return self._gval

    @gval.setter
    def gval(self, val):
        val = float(val)
        assert (val >= -1) & (val <= 1), "gval must be in the range -1 .. 1"
        self._gval = val

    @property
    def center_coord(self):
        return self._center_coord

    @center_coord.setter
    def center_coord(self, coord):
        assert (isinstance(coord, tuple)) & (len(coord) == 3)
        self._center_coord = coord

    @property
    def discard_bet(self):
        return self._discard_bet

    @discard_bet.setter
    def discard_bet(self, val):
        assert isinstance(val, bool), "discard_bet must be a bool"
        self._bool_argmap['-n'] = val
        self._discard_bet = val

    @property
    def save_mask(self):
        return self._save_mask

    @save_mask.setter
    def save_mask(self, val):
        assert isinstance(val, bool), "save_mask must be a bool"
        self._bool_argmap['-m'] = val
        self._save_mask = val

    @property
    def applythresh(self):
        return self._applythresh

    @applythresh.setter
    def applythresh(self, val):
        assert isinstance(val, bool), "applythresh must be a bool"
        self._bool_argmap['-t'] = val
        self._applythresh = val

    @property
    def save_skull(self):
        return self._save_skull

    @save_skull.setter
    def save_skull(self, val):
        assert isinstance(val, bool), "save_skull must be a bool"
        self._bool_argmap['-s'] = val
        self._save_skull = val

    @property
    def save_overlay(self):
        return self._save_overlay

    @save_overlay.setter
    def save_overlay(self, val):
        assert isinstance(val, bool), "save_overlay must be a bool"
        self._bool_argmap['-o'] = val
        self._save_overlay = val

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        assert isinstance(val, bool), "verbose must be a bool"
        self._verbose = val

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, val):
        assert isinstance(val, str), "suffix must be a string"
        self._suffix = val

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, val):
        assert isinstance(val, str), "prefix must be a string"
        self._prefix = val

    def run(self, cb=None):
        """

        :return:
        dictionary
        {
            bet_input: str,
            bet_output: str,
            bet_mask: str,
            bet_skull: str,
            bet_overlay: str
        }
        """
        idle.run(self._run, onFinish=cb)

    def _run(self):
        # submit(" ".join(self.command()))
        subprocess.run(self.command())


    def command(self):
        """
        make command line string to call program
        """
        FSLDIR = os.getenv("FSLDIR", None)
        if FSLDIR is None:
            return False
        if not os.path.isfile(self.image_in):
            return False
        if (len(self.image_t2) > 0) & (os.path.isfile(self.image_t2) is False):
            return False

        cmd = [
            os.path.join(FSLDIR, 'bin', 'bet'),
            self.image_in,
            self.image_out,
            '-f', str(self.fval),
            '-g', str(self.gval)
        ]

        if self._center_coord != (0, 0, 0):
            (x, y, z) = self._center_coord
            cmd.extend(['-c', str(x), str(y), str(z)])

        for key in self._bool_argmap:
            if self._bool_argmap[key]:
                cmd.append(key)
        if self.bet_type != "":
            if self.bet_type == "-A2":
                cmd.append(self.bet_type)
                cmd.append(self.image_t2)
            else:
                cmd.append(self.bet_type)
        print(" ".join(cmd))
        return cmd


class Flirt(object):
    flirt_type_choices = [
        "highres to standard",
        "lowres to highres to standard"
    ]
    def __init__(self, in_highres=""):
        pass