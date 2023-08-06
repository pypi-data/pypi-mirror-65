import matplotlib.pyplot as plt

def plot1D(PyDPFT,Vx,Vint,rho):
  plt.figure(dpi=200,figsize=(4,4))
  ax1 = plt.subplot(221); ax1.title.set_text('Vx')
  ax2 = plt.subplot(222); ax2.title.set_text('Vint')
  ax3 = plt.subplot(223); ax3.title.set_text('rho')
  ax1.plot(PyDPFT.x,Vx)
  ax2.plot(PyDPFT.x,Vint)
  ax3.plot(PyDPFT.x,rho)
  plt.tight_layout(); plt.show()

def plot2D(PyDPFT,Vx,Vint,rho):
  plt.figure(dpi=200,figsize=(4,4))
  ax1 = plt.subplot(221); ax1.title.set_text('Vx')
  ax2 = plt.subplot(222); ax2.title.set_text('Vint')
  ax3 = plt.subplot(223); ax3.title.set_text('rho')
  y0 = int(PyDPFT.config['space']['y'][2]/2)
  ax4 = plt.subplot(224)
  ax4.title.set_text('rho, y={y:.2f}'.format(y=PyDPFT.y[y0]))
  resolution = 30
  ax1.contourf(PyDPFT.x,PyDPFT.y,Vx,resolution) 
  ax2.contourf(PyDPFT.x,PyDPFT.y,Vint,resolution) 
  ax3.contourf(PyDPFT.x,PyDPFT.y,rho,resolution)
  ax4.plot(PyDPFT.x,rho[:][y0])
  plt.tight_layout(); plt.show()

def plot3D(PyDPFT,Vx,Vint,rho):
  plt.figure(dpi=200,figsize=(4,4))
  ax11=plt.subplot(331); ax11.title.set_text('Vx x=0')
  ax12=plt.subplot(332); ax12.title.set_text('Vx y=0')
  ax13=plt.subplot(333); ax13.title.set_text('Vx z=0')

  ax21=plt.subplot(334); ax21.title.set_text('Vint x=0')
  ax22=plt.subplot(335); ax22.title.set_text('Vint y=0')
  ax23=plt.subplot(336); ax23.title.set_text('Vint z=0')

  ax31=plt.subplot(337); ax31.title.set_text('rho x=0')
  ax32=plt.subplot(338); ax32.title.set_text('rho y=0')
  ax33=plt.subplot(339); ax33.title.set_text('rho z=0')

  x0 = int(PyDPFT.config['space']['x'][2]/2)
  y0 = int(PyDPFT.config['space']['y'][2]/2)
  z0 = int(PyDPFT.config['space']['z'][2]/2)
  
  resolution = 30
  ax11.contourf(PyDPFT.y,PyDPFT.z,Vx[x0,:,:],resolution) 
  ax12.contourf(PyDPFT.x,PyDPFT.z,Vx[:,y0,:],resolution) 
  ax13.contourf(PyDPFT.x,PyDPFT.y,Vx[:,:,z0],resolution) 

  ax21.contourf(PyDPFT.y,PyDPFT.z,Vint[x0,:,:],resolution) 
  ax22.contourf(PyDPFT.x,PyDPFT.z,Vint[:,y0,:],resolution) 
  ax23.contourf(PyDPFT.x,PyDPFT.y,Vint[:,:,z0],resolution) 

  ax31.contourf(PyDPFT.y,PyDPFT.z,rho[x0,:,:],resolution) 
  ax32.contourf(PyDPFT.x,PyDPFT.z,rho[:,y0,:],resolution) 
  ax33.contourf(PyDPFT.x,PyDPFT.y,rho[:,:,z0],resolution) 
  plt.tight_layout(); plt.show()

def plot(PyDPFT,Vx,Vint,rho):
  if PyDPFT.dim == 1:   plot1D(PyDPFT,Vx,Vint,rho)
  elif PyDPFT.dim == 2: plot2D(PyDPFT,Vx,Vint,rho)
  elif PyDPFT.dim == 3: plot3D(PyDPFT,Vx,Vint,rho)