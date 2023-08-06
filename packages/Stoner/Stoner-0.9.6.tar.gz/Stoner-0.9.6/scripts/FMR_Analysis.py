#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 21:47:27 2019

@author: phygbu
"""
# pylint: disable=invalid-name
import os
import numpy as np

from Stoner import DataFolder
from Stoner.analysis.fitting.models.magnetism import FMR_Power


directory = r"/sshfs/phygbu@stonerlab/storage/data/Projects/Organics/FMR/Satam/20191003/Second Time"
pattern = "*.txt"
x = "Field"
y = "FMR_Signal"


def sign(r):
    return np.sign(r.x)


os.chdir(directory)

fldr = DataFolder(directory, pattern=pattern, setas={"x": x, "y": y})
for d in fldr:
    fldr += d.split(sign, final="groups")
