#############################################################################################
# setup
# handler for printing out time during simulation run
def fi():
 for i in range(0,int(h.tstop),100):
  h.cvode.event(i, "print " + str(i))

import sys
import os
import string
import types

from neuron import *
# simctrl stuff
h("strdef simname, allfiles, simfiles, output_file, datestr, uname, osname, comment")
h.simname=simname = "mtlhpc"
h.allfiles=allfiles = "geom.hoc pyinit.py geom.py onepyr.py"
h.simfiles=simfiles = "pyinit.py geom.py onepyr.py"
h("runnum=1")
runnum = 1.0
h.datestr=datestr = "11may20"
h.output_file=output_file = "data/11may20.05"
h.uname=uname = "x86_64"
h.osname=osname="linux"
h("templates_loaded=0")
templates_loaded=0
h("xwindows=1.0")
xwindows = 1.0

h.xopen("nrnoc.hoc")
h.xopen("init.hoc")

from pyinit import *
# from geom import *

fih = h.FInitializeHandler(1, fi)

#############################################################################################
