
Demonstration of Hopfield-Brody snychronization using artificial cells in NEURON+python.

The main file in this demonstration is net.py

To use:
 1. unzip the contents of the zip file
 2. nrnivmodl , to compile the mod files
 3. ./x86_64/special -python net.py

The third step will run the simulation for 500 ms of simulation time and display
the spikes of the cells as red dots. The vertical blue lines indicate the
synchronization between the cells. The third step also assumes your computer's
architecture is 64-bit. If not, then the special file will be created in a
different sub-directory.


This demo was originally written by Bill Lytton and then later translated to python
by Sam Neymotin. 

For questions/comments contact Sam Neymotin:
 samuel dot neymotin at yale dot edu
  or
 samn at neurosim dot downstate dot edu

