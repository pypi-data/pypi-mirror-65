#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "info@christopherhahne.de"
__license__ = """
    Copyright (c) 2019 Christopher Hahne <info@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from plenopticam.lfp_aligner.lfp_microlenses import LfpMicroLenses
from plenopticam.misc import isint

import numpy as np
import os


class LfpCropper(LfpMicroLenses):

    def __init__(self, *args, **kwargs):
        super(LfpCropper, self).__init__(*args, **kwargs)

        self._lfp_img_align = kwargs['lfp_img_align'] if 'lfp_img_align' in kwargs else None

        self.var_init()

        if self._lfp_img_align is not None:

            self._LENS_Y_MAX = int(self._lfp_img_align.shape[0] / self._M)
            self._LENS_X_MAX = int(self._lfp_img_align.shape[1] / self._M)
            p = self._lfp_img_align.shape[-1] if len(self._lfp_img_align.shape) == 3 else 1
            self.new_lfp_img = np.zeros([int(self._Mn * self._LENS_Y_MAX), int(self._Mn * self._LENS_X_MAX), p],
                                        dtype=self._lfp_img_align.dtype)

    def lfp_align_pitch_guess(self):

        # iterate through potential (uneven) micro image size candidates
        for d in np.arange(3,51,2):
            # take pitch where remainder of aligned image dimensions and candidate size is zero
            if (self._lfp_img_align.shape[0] / d) % 1 == 0 and (self._lfp_img_align.shape[1] / d) % 1 == 0:
                self._M = int(d)
                break

        return self._M

    def var_init(self):

        # get maximum (M) and desired (Mn) micro image pitches
        if hasattr(self, '_CENTROIDS'):
            # get micro image size from centroid analysis
            self._M = self.pitch_analyse(shape=self._lfp_img_align.shape)
        else:
            # guess micro image size based on aligned light field
            self._M = self.lfp_align_pitch_guess()
        self._Mn = self.pitch_eval(self._M, self.cfg.params[self.cfg.ptc_leng], self.sta)

        # validate micro image size in lfp is large enough
        if self._M < self._Mn:
            # remove existing pickle file
            fp = os.path.join(self.cfg.exp_path, 'lfp_img_align.pkl')
            os.remove(fp)
            # status update
            self.sta.status_msg('Angular resolution mismatch in previous alignment. Redo process')
            self.sta.error = True

        self.cfg.params[self.cfg.ptc_leng] = self._Mn

        # use _k as crop margin
        self._k = (self._M - self._Mn)//2

    def main(self):

        # reduce light field in angular domain (depending on settings)
        if self._Mn < self._M and isint(self._M):
            self.proc_lens_iter(self.crop_micro_image, msg='Render angular domain')
        elif self._Mn == self._M:
            self.new_lfp_img = self._lfp_img_align

    def crop_micro_image(self, ly, lx):

        self.new_lfp_img[ly*self._Mn:ly*self._Mn+self._Mn, lx*self._Mn:lx*self._Mn+self._Mn] = \
            self._lfp_img_align[self._k+ly*self._M:ly*self._M+self._M-self._k,
                                self._k+lx*self._M:lx*self._M+self._M-self._k]

    @property
    def lfp_img_align(self):
        return self.new_lfp_img.copy()
