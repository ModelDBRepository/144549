# from net import * 

from mysetup import *
import numpy
# Declarations
g = h.Graph()
# objref g,rdm[2],ind,XO,YO,animv[2],tmpobj,tvec,vec[10],scr[2],tmpvec,veclist,ind
# objref netcon
# objref sl,gx[2],drv
ncell=100
cells = [] # h.List()
nclist = h.List()
vec = []
rdm = []
scr=[]
animv=[]
for ii in xrange(0,2):  rdm.append(h.Random())
for ii in xrange(0,10): vec.append(h.Vector())
for ii in xrange(0,2): scr.append(h.Vector())
for ii in xrange(0,2): animv.append(h.Vector())
tvec=h.Vector()
ind=h.Vector()
veclist=h.List()
sl=h.SectionList() # empty list
drv=h.Vector() # drawing vector
Gshp=0
tveclen=0

# Cell template
class Cell:
  def __init__ (self,_id,_x,_y,_z):
      self.pp = h.IntervalFire()
      self.pp.tau = 10
      self.pp.invl = 20
      self.id = _id
      self.x = _x
      self.y = _y
      self.z = _z
  def is_art ():
      return 1
  def connect2target (targ,nc):
      nc=h.NetCon(pp, targ)
      return nc
  def M ():
      return pp.M()

# Network specification
# createnet()
def createnet ():
  global cells,nclist,netcon
  netcon = h.nil
  cells = []
  for i in xrange(0,ncell): cells.append(Cell(i,i,0,0))
  wire()

# wire():: full non-self connectivity
# artificial cell templates have obj.pp
# params: ncell
# creates nclist: list of NetCons
def wire ():
  nclist.remove_all()
  for pre in cells: 
    for post in cells: 
      if pre!=post: nclist.append(h.NetCon(pre.pp,post.pp))

# ranwire()
def ranwire ():
  nclist.remove_all()
  rdm[0].discunif(0,ncell-1)
  for i in xrange(0,ncell):
    proj=rdm[0].repick()
    if proj<ncell/2:
      beg=proj
      end=proj+int(ncell/2.0)-1 
    else:
      beg=proj-int(ncell/2.0)+1
      end=proj
    for j in xrange(beg,end+1):
      if i!=j:
        netcon = h.NetCon(cells[i].pp,cells[j].pp)
        nclist.append(netcon)

# parameters
h.tstop = 500

ncell = 10
ta=10
w=-0.01
delay=4
low=10
high=11

# routines: weight(),delay(),tau(),interval()
def weight (w=-0.3): 
  vv=h.Vector()
  if w == -1: # a bad choice of code value
    for i in xrange(0,int(nclist.count())):
      vv.append(nclist.o(i).weight[0])
      print vv.min,vv.max,vv.mean,vv.stdev
  else:
    for n in nclist: n.weight[0] = w

# weight2(WT,EXCLUDE_VEC) :: set weight to WT 
# unless in EXCLUDE_VEC then set wt. to 0
def weight2 (w,ecv):
  for i,nc in zip(range(len(nclist)),nclist):
    if ecv.contains(i): 
      nc.weight[0]=0
    else:               
      nc.weight[0]=w

def setdelay (delay):
  for n in nclist: n.delay = delay

def settau (tau): 
  for c in cells: c.pp.tau = tau

# //** interval(low,high) randomly sets cells to have periods between low and high
def interval (low,high):
  rdm[0].uniform(low,high)
  vec[0].resize(ncell)
  vec[0].setrand(rdm[0])
  for i in xrange(0,len(cells)):
    cells[i].pp.invl = vec[0][i]

# //** setparams() sets weight, delay, tau and intervals
def setparams (w=-0.2,delay=2,ta=10,low=10,high=12):
  weight(w)
  setdelay(delay)
  settau(ta)  
  interval(low, high)

# //* Run code
# //** savspks() -- save to a vector
def savspks ():
  for ii in xrange(0,2): animv[ii].resize(0)
  for c in cells:
    if h.cvode.netconlist(c, '', '').count()==0:
      tmpobj=h.NetCon(c.pp, None)
    else:
      tmpobj=cvode.netconlist(c, '', '').object(0)
    tmpobj.record(tvec,ind)
    animv[0].append(h.objnum(tmpobj))
    animv[1].append(h.objnum(tmpobj.pre)) # in this case are all in a row anyway

# //** showspks() -- show spikes on graph g
def markspks ():
  g.erase()
  ind.mark(g,tvec,"O",4,2,1)
  g.flush()
  g.exec_menu("View = plot")

def showspks ():
  # ind.mark(g,tvec,"O",8,2,1)
  for x in tvec:
    g.beginline(3,1)
    g.line(x,ind.min())
    g.line(x,ind.max()) 
  g.flush()
  g.exec_menu("View = plot")

# //** syncer() :: returns sync measure 0 to <1
# // measures how well spikes "fill up" the time
# // assumes spike times in tvec, tstop
# // param: width
# // syncer doesn't take account of prob of overlaps 
# // due to too many spikes stuffed into too little time
def syncer (vec=tvec,width=1):
  t0=-1; cnt=0
  for tt in vec:
    if tt>=t0+width: t0=tt; cnt+=1
  return 1.0-cnt/(h.tstop/width)

# ** autorun() changes weights
def autorun ():
  veclist.remove_all()
  rvc() # clear the storage vectors
  for w in [-0.5,-0.3,-0.1,-0.01,-0.001]:
    weight(w)
    run()
    savevec([ind,tvec])
    vec[1].append(w)
    s = syncer()
    vec[2].append(s)
    print w,s
  g.erase()
  vec[2].plot(g,vec[1])
  vec[2].mark(g,vec[1],"O",8,2,1)
  g.exec_menu("View = plot")

# //** autorun1() changes connections density
def autorun1 ():
  veclist.remove_all()
  rvc()
  maxx=-0.1
  pij_inc=0.1
  S=ncell*ncell
  vec[3].resize(0)
  for ii in xrange(0,10):
    C = (1-ii*pij_inc) # // percent convergence
    w=maxx/C  # // scale weight up as convergence goes down
    setparams()
    weight2(w,vec[3])
    run()
    savevec([ind,tvec])
    print S-vec[3].size(),syncer()
    vec[1].append((S-vec[3].size())/S)
    vec[2].append(syncer())
    rdm[0].discunif(0,S-1)
    rdmunq(vec[3],0.1*S,rdm[0]) # increase those set to 0
  g.erase()
  vec[2].plot(g,vec[1])
  vec[2].mark(g,vec[1],"O",8,2,1)
  g.exec_menu("View = plot")

# //* Utility functions
# //** savevec(list of vectors) add vectors onto veclist
def savevec (vecs):
  for vec in vecs:
    tmpvec = h.Vector(vec.size())
    tmpvec.copy(vec)
    veclist.append(tmpvec)
    tmpvec = h.nil

# //** rvc() clears vec[0..9]
def rvc ():
  for ii in xrange(0,10):
    vec[ii].resize(0)

# //** setdensity(pij) sets connection density to 0<pij<1
def setdensity (pij):
  maxx=-0.1
  S=nclist.count()
  rdm[0].discunif(0,S-1)
  vec[3].resize(0)
  rdmunq(vec[3],(1-pij)*S,rdm[0]) # // number to set to 0
  C = (1-pij) # // percent convergence
  w=maxx/C  # // scale weight up as convergence goes down
  setparams()
  weight2(w,vec[3])

# //** rdmunq(vec,n,rdm) -- augment vec1 by n unique vals from rdm
def rdmunq (vec,n,rm):
  num=0
  flag=1
  loop=0
  scr[0].resize(n*4) # // hopefully will get what we want
  while flag:
    scr[0].setrand(rm)
    for ii in xrange(0,int(scr[0].size())):
      xx=scr[0].x[ii]
      if not vec.contains(xx):
        vec.append(xx)
        num+=1
      if num==n:
        flag=0
        break 
    loop+=1
    if loop==10:
      print "rdmunq ERR; inf loop"
      flag=0
      break

# //** rdmord (vec,n) randomly ordered numbers 0->n-1 in vec
def rdmord (vec,n):
  rdm[0].uniform(0,100)
  scr[0].resize(n)
  scr[0].setrand(rdm[0])
  scr[0].sortindex(vec)

# // vcount (num,vec)
def vcount (num,vec):
  scr[0].where(vec,"==",num)
  return scr[0].size()

# //* Mapping functions
# //** getcnum(CELL_OBJ) return index given cell object
def getcnum (cell):
  return cell.id
#  h.sprint(h.tstr,"%s",cell)
#  h("sscanf("
#  if h.sscanf(h.tstr,"IntervalFire[%d]",&x) != 1:
#    x=-1
#  return x 

# //** fconn(PREVEC,POSTVEC) places values of 
# // pre- and post-syn cells in parallel vectors
# // only lists pairs with non-zero connections
# // getcnum() returns index of cell obj
def fconn (prev,post):
  prev.resize(0)
  postv.resize(0)
  for ii in xrange(0,nclist.count()):
    XO=nclist.o(ii)
    if XO.weight[0]!=0:
      prev.append(getcnum(XO.pre))
      postv.append(getcnum(XO.syn))

# //** showconns() -- show all the connections as line segments
def showconns ():
  g.erase()
  fconn(scr[0],scr[1])
  for ii in xrange(0,scr[0].size()):
    pr=scr[0].x[ii]
    po=scr[1].x[ii]
    drawline(pr,po,10)
  g.flush()

# //** showconv1(ID,color) -- show convergence to one cell as line seg
def showconv1 (ID,colr=2):
  fconn(scr[0],scr[1])
  for ii in xrange(0,scr[0].size()):
    pr=scr[0].x[ii]
    po=scr[1].x[ii]
    if po==ID:
      drawline(pr,po,10,colr,3)
      print pr
  print ''
  g.flush()

# //** showdiv1() -- show divergence from one cell as line seg
def showdiv1 (id,colr=2):
  fconn(scr[0],scr[1])
  for ii in xrange(0,scr[0].size()):
    pr=scr[0].x[ii]
    po=scr[1].x[ii]
    if pr==id:
      drawline(pr,po,10,colr,8)
      print po
  print ''
  g.flush()

def xpos (x,cols):
  return x%cols

def ypos (co1s,y):
  return int(co1s/y)

# //*** func distn () calc distance
def distn (c1,c2,cols):
  from math import sqrt
  xd=xpos(c1,cols)-xpos(c2,cols)
  yd=ypos(c1,cols)-ypos(c2,cols)
  return sqrt(xd*xd+yd*yd)

# //*** distwire(pij)
def distwire (pij):
  allsyns = nclist.count()
  total=pij*allsyns # how many syns to set
  rdm[1].uniform(0,1) # for flipping coin
  # // maxdist==12.728 for 10x10; mindist=1 (neighbors)
  maxdist=0.33*distn(0,ncell-1,sqrt(ncell)) # the full dist from lower left to upper right
  maxwt=-0.9/pij  # norm wt by convergence
  loop=cnt=0 # counters
  for i in xrange(0,allsyns): nclist.o(i).weight[0] = 0 # # clear weights
  while cnt<total and loop<4:
    rdmord(vec[3],allsyns)  # # test each synapse in random order
    for ii in xrange(0,vec[3].size()):
      XO=nclist.object(vec[3].x[ii]) # # pick a synapse
      # max prob of connection is 0.8*(1-mindist/maxdist)~74% for 10x10
      # zero prob of diag connection from corner to corner
      prob = 1.0*(1-(distn(getcnum(XO.pre),getcnum(XO.syn),sqrt(ncell))/maxdist))
      if rdm[1].repick<prob:
        XO.weight=maxwt
        cnt+=1
      if cnt>=total:
        break # finished
  print cnt,total
  if cnt<total:
    print "distwire ERR: target ", total, "set ", cnt
    
# //*** drawline(beg,end,columns[,color,line_width]) 
def drawline (beg,end,cols,clr=4,lwid=1): 
  # local beg,end,cols,clr,lwid
  g.beginline(clr,lwid)
  g.line(xpos(beg,cols),ypos(beg,cols))
  g.line(xpos(end,cols),ypos(end,cols))

# //* Animation
# //** animplot() put up the shape plot for hinton diagram
def animplot ():
  gx[Gshp] = h.PlotShape(sl,0)
  h.flush_list.append(gx[Gshp])
  ctern(gx[Gshp],0,2)
  gx[Gshp].view(1,0,1.1,1.1,500,200,100,100)
  drawcells()

# //* Ternary color map
def ctern (cm,minc,maxc):
  cm.colormap(3)
  cm.colormap(0, 255, 0, 0)
  cm.colormap(1, 255, 255, 0)
  cm.colormap(2, 0, 0, 255)
  cm.scale(minc, maxc)

# //** drawcells() draw squares of hinton diagram
def drawcells ():
  if ncell!=100:
    print "ERROR: drawcells() currently written for ncell=100"
    return 
  gx[Gshp].erase_all()
  drv.resize(ncell)
  xoff=1.1
  yoff=0.1
  wdt=0.1
  nx=ny=10
  for i in xrange(0,nx):
    for j in xrange(0,ny):
      #gx[Gshp].hinton(&drv.x[j*nx+i],(i+.5)*wdt+xoff,(j+.5)*wdt+yoff,wdt)
      gx[Gshp].hinton(drv.x[j*nx+i],(i+.5)*wdt+xoff,(j+.5)*wdt+yoff,wdt)
  gx[Gshp].size(1, 2.2, 0, 1.2)
  gx[Gshp].exec_menu("Shape Plot")

# //** chkhint(cell#) light up a location for a single cell
def chkhint (cellid):
  drv.fill(0)
  drv.x[cellid]=2
  gx.flush()

# //** anim() animates sim stored in tvec,ind
def anim ():
  tstep=0.1
  sz = ind.size()-1
  gx[Gshp].exec_menu("Shape Plot")
  scr[0].copy(tvec)
  scr[0].add(500*tstep)  # how many steps to keep it illuminated
  drv.fill(0)
  ii=jj=0 
  for tt in numpy.linspace(0,h.tstop,h.tstop/tstep+1):
    while ii < sz and tt > tvec.x[ii]:
      drv.x[animv.indwhere("==",ind.x[ii])]=2
      ii = ii + 1
    while jj < sz and tt > scr[0].x[jj]:
      drv.x[animv.indwhere("==",ind.x[jj])]=0
      jj = jj + 1
    gx[Gshp].flush()
    doEvents()

# //* Run sequences
h.cvode_active(1)
def run ():h.run()
def runseq ():
  createnet()
  setparams()
  savspks()
  run()

# from net import *
# ncell=10
# w=-1e-6
# runseq()
# g=new Graph()
# g.erase_all
# markspks()
# showspks()
# w=-0.3 # and repeat
# setparams()
# run() # then erase graph and show

createnet()
savspks()
setparams(w=-0.1)
# don't repeat runseq() unless want to change # of cells
run();g.erase_all();markspks();showspks()
# animplot()
# anim()
