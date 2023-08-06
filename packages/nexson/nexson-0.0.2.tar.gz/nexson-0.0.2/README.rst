nexson
======


`nexson` is a package for handling the "NexSON" format used by the
`Open Tree of Life project`_ to store information about externally produced phylognetic trees.
The package was refactored from `peyotl`, which is a more general purpose package.

Instructions
------------

::

    python3 -mvenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop
    python setup.py test

performs the basic installation and test.

Thanks
------

Thanks to NSF_ and HITS_ for funding support.

nexson is primarily written by Mark Holder, Emily Jane McTavish, and Jim Allman,
but see the CONTRIBUTORS_ file for a more complete list
of people who have contributed code.

Jim Allman, Karen Cranston, Cody Hinchliff, Mark Holder, Peter Midford, and Jonathon Rees
all participated in the discussions that led to the NexSON mapping.

The peyotl/test/data/nexson/phenoscape/nexml test file is from
    https://raw.github.com/phenoscape/phenoscape-data/master/Curation%20Files/completed-phenex-files/Characiformes/Buckup_1998.xml
    Phenoscape file (download), NESCent_ [Feb 16, 2014] The citation for the data is in the nexml doc itself.

****************

.. _Open Tree of Life project: http://blog.opentreeoflife.org/
.. _CONTRIBUTORS: https://raw.githubusercontent.com/OpenTreeOfLife/nexson/master/CONTRIBUTORS.txt
.. _NSF: http://www.nsf.gov
.. _HITS: http://www.h-its.org/english
.. _NESCent: http://kb.phenoscape.org
