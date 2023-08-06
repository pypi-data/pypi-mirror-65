import numpy as np
import torch as tc
import time

GPU = tc.device('cuda:0' if tc.cuda.is_available() else 'cpu')

def initVariables(o):
  print('PyDPFT: Written by Ding Ruiqi from NUS for his bachelor thesis')
  s = o.config['space']; c = o.config['const']
  x = np.linspace(*s['x']); dx = x[1] - x[0]
  dim = 1; o.dV = dx 
  if 'y' in s: 
    y = np.linspace(*s['y']); dy = y[1] - y[0]
    dim = 2; o.dV = dx * dy 
  if 'z' in s:
    z = np.linspace(*s['z']); dz = z[1] - z[0]
    dim = 3; o.dV = dx * dy * dz
  o.dim = dim
  if dim == 1: 
    o.x = x; o.xx = x
    r = ((x[None,:]-x[:,None])**2)**0.5
  elif dim == 2:
    xx, yy = np.meshgrid(x,y,sparse=True,indexing='ij')
    o.x, o.y = x, y; o.xx, o.yy = xx, yy
    r = ( (xx[None,None,:,:]-xx[:,:,None,None])**2 
        + (yy[None,None,:,:]-yy[:,:,None,None])**2 )**0.5
  elif dim == 3:
    xx, yy, zz = np.meshgrid(x,y,z,sparse=True,indexing='ij')
    o.x, o.y, o.z = x, y, z; o.xx, o.yy, o.zz = xx, yy, zz
    r = ( (xx[None,None,None,:,:,:]-xx[:,:,:,None,None,None])**2 
        + (yy[None,None,None,:,:,:]-yy[:,:,:,None,None,None])**2 
        + (zz[None,None,None,:,:,:]-zz[:,:,:,None,None,None])**2 )**0.5 
  
  if 'Hartree' in o.config['Vint']['name']:
    VhKernel = o.dV / (r + c['epsilon'])
    o.VhKernel = tc.from_numpy(VhKernel).to(GPU)
  elif 'Dipole' in o.config['Vint']['name']:
    if dim == 2:
      mu2 = c['mu'][0]**2 + c['mu'][1]**2 
      muDotR = c['mu'][0] * (xx[None,None,:,:]-xx[:,:,None,None]) +\
               c['mu'][1] * (yy[None,None,:,:]-yy[:,:,None,None]) 
    elif dim == 3:
      mu2 = c['mu'][0]**2 + c['mu'][1]**2 + c['mu'][2]**2
      muDotR = c['mu'][0] * (xx[None,None,None,:,:,:]-xx[:,:,:,None,None,None]) +\
               c['mu'][1] * (yy[None,None,None,:,:,:]-yy[:,:,:,None,None,None]) +\
               c['mu'][2] * (zz[None,None,None,:,:,:]-zz[:,:,:,None,None,None]) 
    if dim != 1:
      Vdd_p_Kernel = o.dV * (muDotR**2/(r**2 + c['epsilon']) - mu2/3)
      o.Vdd_p_Kernel = tc.from_numpy(Vdd_p_Kernel).to(GPU)
      Vdd_x_Kernel = - o.dV * (muDotR**2/(r**5 + c['epsilon']) - mu2/3/(r**3 + c['epsilon']))
      o.Vdd_x_Kernel = tc.from_numpy(Vdd_x_Kernel).to(GPU)
  print('PyDPFT: Detected dim = {}'.format(dim))

def getVint(o,rho):
  v = o.config['Vint']
  Vx = - rho**(1/3)
  if v['name'] == 'Hartree':
    if o.dim == 1:   Vint = rho[None,:] * o.VhKernel
    elif o.dim == 2: Vint = rho[None,None,:,:] * o.VhKernel
    elif o.dim == 3: Vint = rho[None,None,None,:,:,:] * o.VhKernel
  elif v['name'] == 'Dipole-x':
    assert o.dim != 1,'Dipole interaction makes no sense in 1D !'
    if o.dim == 2:   Vint = rho[None,None,:,:] * o.Vdd_x_Kernel
    elif o.dim == 3: Vint = rho[None,None,None,:,:,:] * o.Vdd_x_Kernel
  elif v['name'] == 'Dipole-p': 
    assert o.dim != 1,'Dipole interaction makes no sense in 1D !'
    if o.dim == 2:   rhoDiff = rho[None,None,:,:]-rho[:,:,None,None]
    elif o.dim == 3: rhoDiff = rho[None,None,None,:,:,:]-rho[:,:,:,None,None,None]
    rhoDiff[rhoDiff<0] = 0; rhoDiff[rhoDiff>0] = 1
    Vint = rhoDiff * o.Vdd_p_Kernel
  if o.dim == 1:   return Vx,v['coef'] * Vint.sum(-1)
  elif o.dim == 2: return Vx,v['coef'] * Vint.sum(-1).sum(-1)
  elif o.dim == 3: return Vx,v['coef'] * Vint.sum(-1).sum(-1).sum(-1)

def getRhoDPFT(o,V):
  def getRhoN(mu,V):
      muMinusV = mu - V; muMinusV[muMinusV<0] =0
      rho = muMinusV**(o.dim/2)
      N = tc.sum(rho) * o.dV
      return rho,N
  muMax = 1; muMin = tc.min(V); trueN = o.config['rho']['N']
  while getRhoN(muMax,V)[1] < trueN: muMax = muMax*2
  for i in range(o.config['loop']['Imax']): 
    muMid = (muMax+muMin)/2
    rho,N = getRhoN(muMid,V)
    if(N > trueN): muMax = muMid
    else: muMin = muMid
    if 1-muMin/muMax < o.config['loop']['precision']: break
  return rho,N

class PyDPFTclass(tc.nn.Module):
  def __init__(self,config):
    super(PyDPFTclass,self).__init__()
    self.config = config
    initVariables(self)
  
  def forward(self,Vext): # self consistent loop
    l = self.config['loop']
    rho = tc.zeros(self.xx.shape).to(GPU)
    Vext = tc.from_numpy(Vext).to(GPU)
    converged = False
    print('PyDPFT: Starting the self consistent loop')
    start = time.time()
    for i in range(l['Imax']):
      Vx,Vint = getVint(self,rho)
      oldRho = rho
      rho,N = getRhoDPFT(self,Vx+Vint+Vext)
      rho = (1-l['mix']) * oldRho + l['mix'] * rho
      if tc.mean(tc.abs(oldRho-rho)) < l['precision']: 
        timeTaken = time.time()- start
        converged = True; break
      if i == l['Imax']-1: timeTaken = time.time()- start
      tc.cuda.empty_cache()
    if converged: print('PyDPFT: Converged after {} iterations in {} seconds!'.format(i,timeTaken))
    else: print('PyDPFT: NOT Converged after {} seconds!'.format(timeTaken))
    return Vx.cpu().numpy(),Vint.cpu().numpy(),rho.cpu().numpy(),N.cpu().numpy()

def PyDPFT(config):
  PyDPFT = PyDPFTclass(config)
  if tc.cuda.device_count() > 1: PyDPFT = tc.nn.DataParallel(PyDPFT)
  PyDPFT.to(GPU)
  print('PyDPFT: Using {} GPUs !'.format(tc.cuda.device_count()))
  return PyDPFT
