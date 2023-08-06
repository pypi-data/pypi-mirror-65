#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peyutil.test import PathMapForTests

def get_test_path_mapper():
    return PathMapForTests(path_map_filepath=__file__)

