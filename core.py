import numpy as np
import scipy as sp

#---------------------------------------------------
#Compute an approximate basis for the nullspace of 
#A using the singular value decomposition of `A`.
#---------------------------------------------------
#def nullspace(A, atol=1e-13, rtol=0):
def nullspace(A, atol=1e-9):
	"""Compute an approximate basis for the nullspace of A using the singular value
	decomposition of `A`.

	Parameters
	----------
	'A' : ndarray;  A should be at most 2-D.  A 1-D array with length k will be treated
	as a 2-D with shape (1, k)
	'atol' : float; The absolute tolerance for a zero singular value.  Singular values
		smaller than `atol` are considered to be zero.
	'rtol' : float; The relative tolerance.  Singular values less than rtol*smax are
		considered to be zero, where smax is the largest singular value.

		If both `atol` and `rtol` are positive, the combined tolerance is the
		maximum of the two; that is::
		tol = max(atol, rtol * smax)
		Singular values smaller than `tol` are considered to be zero.

	Returns
	-------
	'ns' : ndarray; If `A` is an array with shape (m, k), then `ns` will be an array
		with shape (k, n), where n is the estimated dimension of the
		nullspace of `A`.  The columns of `ns` are a basis for the
		nullspace; each element in numpy.dot(A, ns) will be approximately
		zero.
	"""

	#A = np.atleast_2d(A)
	#u, s, vh = np.linalg.svd(A)
	#tol = max(atol, rtol * s[0])
	#nnz = (s >= tol).sum()
	#ns = vh[nnz:].conj().T
	#return ns
	
	u, s, vh = sp.linalg.svd(A)
	#print "u",u
	#print "s",s
	#print "vh",vh
	null_mask = (s <= atol)
	null_space = sp.compress(null_mask, vh, axis=0)
	return sp.transpose(null_space)

#---------------------------------------------------
#Calculates the kz from the characteristic equation
#---------------------------------------------------
def kz_eigenvalues(k0,kx,ky,m_eps):
	'''Calculates the kz from the characteristic equation.

	Parameters
	----------
	'ko'= vacuum wavevector
	'kx,ky'= in plane wavevector components
	'm_eps'= 3x3 complex dielectric tensor

	Returns
	-------
	'v_kz'= kz wavevector components

	'''	

	#------output------
	v_kz=np.zeros(4,dtype=np.complex128)

	#------are we diagonal and isotropic?------
	diag_flag= (m_eps==np.diag(np.diagonal(m_eps))).all()
	iso_flag= (m_eps[0,0]==m_eps[1,1]==m_eps[2,2])

	#------diagonal isotropic material------
	if diag_flag and iso_flag:
		kz=np.sqrt((k0**2)*m_eps[0,0] - kx**2 - ky**2)
		v_kz[0:2]=-kz;v_kz[2:4]=kz;

	#------general material------
	else:
		
		#------coefficients for the quartic equation------
		A=(kx/k0)*((m_eps[0,2]+m_eps[2,0])/m_eps[2,2]) + (ky/k0)*((m_eps[1,2]+m_eps[2,1])/m_eps[2,2])

		B=(  ((kx/k0)**2)*(1.0+m_eps[0,0]/m_eps[2,2]) + ((ky/k0)**2)*(1.0+m_eps[1,1]/m_eps[2,2]) + 
		((kx*ky)/((k0)**2))*(m_eps[0,1]+m_eps[1,0])/m_eps[2,2] + 
		((m_eps[0,2]*m_eps[2,0]+m_eps[1,2]*m_eps[2,1])/m_eps[2,2]-m_eps[0,0]-m_eps[1,1])  )

		C1=(   ((kx**2+ky**2)/(k0**2))*((kx/k0)*(m_eps[0,2]+m_eps[2,0])/m_eps[2,2]+
		(ky/k0)*(m_eps[1,2]+m_eps[2,1])/m_eps[2,2]) +
		(kx/k0)*((m_eps[0,1]*m_eps[1,2]+m_eps[1,0]*m_eps[2,1])/m_eps[2,2]-
		(m_eps[1,1]/m_eps[2,2])*(m_eps[0,2]+m_eps[2,0])) + 
		(ky/k0)*((m_eps[0,1]*m_eps[2,0]+m_eps[1,0]*m_eps[0,2])/m_eps[2,2]-
		(m_eps[0,0]/m_eps[2,2])*(m_eps[1,2]+m_eps[2,1]))   )

		D1=(   ((kx**2+ky**2)/(k0**2))*(((kx/k0)**2)*m_eps[0,0]/m_eps[2,2]+((ky/k0)**2)*m_eps[1,1]/m_eps[2,2] +
			((kx*ky)/(k0**2))*(m_eps[0,1]+m_eps[1,0])/m_eps[2,2]-m_eps[0,0]*m_eps[1,1]/m_eps[2,2])   )
		D2=((kx/k0)**2)*((m_eps[0,1]*m_eps[1,0]+m_eps[0,2]*m_eps[2,0])/m_eps[2,2]-m_eps[0,0])
		D3=((ky/k0)**2)*((m_eps[0,1]*m_eps[1,0]+m_eps[1,2]*m_eps[2,1])/m_eps[2,2]-m_eps[1,1])
		D4=((kx*ky)/(k0**2))*((m_eps[0,2]*m_eps[2,1]+m_eps[2,0]*m_eps[1,2])/m_eps[2,2]-m_eps[0,1]-m_eps[1,0])
		D5=(   m_eps[0,0]*m_eps[1,1]+(m_eps[0,1]*m_eps[1,2]*m_eps[2,0]+
			m_eps[1,0]*m_eps[2,1]*m_eps[0,2])/m_eps[2,2]-m_eps[0,1]*m_eps[1,0] - 
			(m_eps[0,0]/m_eps[2,2])*m_eps[1,2]*m_eps[2,1]-(m_eps[1,1]/m_eps[2,2])*m_eps[0,2]*m_eps[2,0]   )
		D=D1+D2+D3+D4+D5
		
		#print "A",'%.15e    %.15e' % (A.real,A.imag)
		#print "B",'%.15e    %.15e' % (B.real,B.imag)
		#print "C1",'%.15e    %.15e' % (C1.real,C1.imag)
		#print "D",'%.15e    %.15e' % (D.real,D.imag)
		#print
		#print
		#print
		#print "m_eps", m_eps[0,0],m_eps[0,1],m_eps[0,2]
		#print "m_eps", m_eps[1,0],m_eps[1,1],m_eps[1,2]
		#print "m_eps", m_eps[2,0],m_eps[2,1],m_eps[2,2]
		
		#------companion matrix------
		m_comp=np.zeros((4,4),dtype=np.complex128)
		m_comp[1,0]=1.0;m_comp[2,1]=1.0;m_comp[3,2]=1.0
		m_comp[0,3]=-D;m_comp[1,3]=-C1;m_comp[2,3]=-B;m_comp[3,3]=-A;

		#-----eigenvalues------
		v_kz=k0*np.linalg.eigvals(m_comp)
		
		#for kz in v_kz[np.argsort(np.imag(v_kz))]:
			#print "kz",'%.15e    %.15e' % (kz.real,kz.imag)
		
	#------output sorted by imaginary part------
	return v_kz[np.argsort(np.imag(v_kz))]


#---------------------------------------------------
#Calculates the kz field eigenvectors from the characteristic equation.
#---------------------------------------------------
def kz_eigenvectors(k0,kx,ky,v_kz,m_eps):
	'''Calculates the kz field eigenvectors from the characteristic equation.

	Parameters
	----------
	'ko'= vacuum wavevector
	'kx,ky'= in plane wavevector components
	'v_kz'= off plane wavevector components
	'm_eps'= 3x3 complex dielectric tensor

	Returns
	-------
	'v_e'= kz field eigenvectors
	'''	

	#------initializing vector and matrix------
	v_e=np.zeros((4,3),dtype=np.complex128);v_e_norm=np.zeros_like(v_e)
	m_k=np.zeros_like(m_eps);
	m_char=np.zeros_like(m_eps);

	#------are we diagonal and isotropic?------
	diag_flag= (m_eps==np.diag(np.diagonal(m_eps))).all()
	iso_flag= (m_eps[0,0]==m_eps[1,1]==m_eps[2,2])

	#------diagonal isotropic material------
	if diag_flag and iso_flag:

		v_e[0,:]=np.array([-v_kz[0],0.0,kx])
		v_e[1,:]=np.array([ ky,-kx,0.0])
		v_e[2,:]=np.array([-v_kz[3],0.0,kx])
		v_e[3,:]=np.array([ky,-kx,0.0])

	#------general material------
	else:

		for m in range(4):

			#------k matrix------
			m_k[0,0]=0.0;m_k[0,1]=-v_kz[m];m_k[0,2]=ky
			m_k[1,0]=v_kz[m];m_k[1,1]=0.0;m_k[1,2]=-kx
			m_k[2,0]=-ky;m_k[2,1]=kx;m_k[2,2]=0.0

			#print "m_k"
			#for i in range(3):
				#for j in range(3):
				#print '%.15e    %.15e' % (m_k[i,j].real,m_k[i,j].imag)
					
			#print "m_eps"
			#for i in range(3):
				#for j in range(3):
				#print '%.15e    %.15e' % (m_eps[i,j].real,m_eps[i,j].imag)
			
			#------Characteristic matrix------
			m_char=np.dot(m_k,m_k)/(k0**2)
			
			#if m==3:
				#print
				#print "m_k2"
				#for i in range(3):
					#print '%.14e    %.14e    %.14e    %.14e    %.14e    %.14e' % (m_char[i,0].real,m_char[i,0].imag,m_char[i,1].real,m_char[i,1].imag,m_char[i,2].real,m_char[i,2].imag)
				
				#print
				#print "m_eps"
				#for i in range(3):
					#print '%.14e    %.14e    %.14e    %.14e    %.14e    %.14e' % (m_eps[i,0].real,m_eps[i,0].imag,m_eps[i,1].real,m_eps[i,1].imag,m_eps[i,2].real,m_eps[i,2].imag)
			
			m_char=m_char+m_eps
			
			#if m==3:
				#print
				#print "m_char"
				#for i in range(3):
					#print '%.14e    %.14e    %.14e    %.14e    %.14e    %.14e' % (m_char[i,0].real,m_char[i,0].imag,m_char[i,1].real,m_char[i,1].imag,m_char[i,2].real,m_char[i,2].imag)
			
			#print
			#print "m_char"
			#for i in range(3):
				#for j in range(3):
				#print '%.15e    %.15e' % (m_char[i,j].real,m_char[i,j].imag)
			#print
			#print
			#print
			
			#------Calculating the null space------
			null_space=nullspace(m_char,atol=1e-9)
			v_e[m,:]=null_space[:,0]
			#v_e[m,:]=v_e[m,:]/np.abs(np.sqrt(np.dot(v_e[m,:],np.conj(v_e[m,:]))))
			
			#if m==3:
				#print "v_e"
				#print '%.14e    %.14e    %.14e    %.14e    %.14e    %.14e' % (v_e[m,0].real,v_e[m,0].imag,v_e[m,1].real,v_e[m,1].imag,v_e[m,2].real,v_e[m,2].imag)
		
			
		#------eigenvector swapping to get appropriate polarization states------
		if np.abs(v_e[0,0])==0.0:
			swap_e=v_e[0,:].copy();v_e[0,:]=v_e[1,:].copy();v_e[1,:]=swap_e.copy()
			swap_kz=v_kz[0].copy();v_kz[0]=v_kz[1].copy();v_kz[1]=swap_kz.copy()
		elif np.abs(v_e[2,0])==0.0:
			swap_e=v_e[2,:].copy();v_e[2,:]=v_e[3,:].copy();v_e[3,:]=swap_e.copy()
			swap_kz=v_kz[2].copy();v_kz[2]=v_kz[3].copy();v_kz[3]=swap_kz.copy()
	
	#------normalizing eigenvectors------
	for m in range(4):
		v_e[m,:]=v_e[m,:]/np.abs(np.sqrt(np.dot(v_e[m,:],np.conj(v_e[m,:]))))
	
	return v_e,v_kz


#------------------------------------------------------------
#Calculates layer by layer boundary and propagation matrixes
#to solve the transfer matrix problem
#------------------------------------------------------------
def m_abc(k0,kx,ky,v_kz,v_e,d):
	'''Calculates layer by layer boundary and propagation matrixes
	   to solve the transfer matrix problem

	Parameters
	----------
	'ko'= vacuum wavevector
	'kx,ky'= in plane wavevector components
	'v_kz'= off plane wavevector components
	'v_e'= kz field eigenvectors
	'd'= layer thickness in nm

	Returns
	-------
	'm_a12,m_a34,m_b12,m_b34,m_c12,m_c34'= boundary condition and propagation matrixes
	'''

	#------matrix allocation------
	m_a12=np.identity(2,dtype=np.complex128);m_a34=np.identity(2,dtype=np.complex128);
	m_b12=np.zeros((2,2),dtype=np.complex128);m_b34=np.zeros_like(m_b12);
	m_c12=np.zeros((2,2),dtype=np.complex128);m_c34=np.zeros_like(m_c12);


	#------a12 matrix------
	a1=v_e[0,1]/v_e[0,0];a2=v_e[1,0]/v_e[1,1];
	m_a12[0,1]=a2;m_a12[1,0]=a1;

	#------a34 matrix------
	a3=v_e[2,1]/v_e[2,0];a4=v_e[3,0]/v_e[3,1]
	m_a34[0,1]=a4;m_a34[1,0]=a3;


	#------b12 matrix------
	b1=v_e[0,2]/v_e[0,0];b2=v_e[1,2]/v_e[1,1]
	m_b12[0,0]=-v_kz[0]*a1+ky*b1;m_b12[0,1]=-v_kz[1]+ky*b2;m_b12[1,0]=v_kz[0]-kx*b1;m_b12[1,1]=v_kz[1]*a2-kx*b2;

	#------b34 matrix------
	b3=v_e[2,2]/v_e[2,0];b4=v_e[3,2]/v_e[3,1]
	m_b34[0,0]=-v_kz[2]*a3+ky*b3;m_b34[0,1]=-v_kz[3]+ky*b4;m_b34[1,0]=v_kz[2]-kx*b3;m_b34[1,1]=v_kz[3]*a4-kx*b4;


	#------c12 matrix------
	m_c12[0,0]=np.exp(1j*v_kz[0]*d);m_c12[1,1]=np.exp(1j*v_kz[1]*d);

	#------c34 matrix------
	m_c34[0,0]=np.exp(1j*v_kz[2]*d);m_c34[1,1]=np.exp(1j*v_kz[3]*d);

	return m_a12,m_a34,m_b12,m_b34,m_c12,m_c34



#----------------------------------------------------------------
#Calculates reflection and transmission matrix for a multilayer
#----------------------------------------------------------------
def RT(wl,theta0,phi0,e_list,d_list):
	'''Calculates reflection and transmission matrix for a multilayer

	Parameters
	----------
	'wl'= vacuum incident wavelength in nm
	'theta0,phi0'= polar and azimuth angles as defined in Mansuripur JAP 67(10)
	'e_list'= [n_layer+2,3,3] numpy array: it contains n_layers+2 3x3 dielectric tensors:
			e_list[0]=3x3 incident medium dielectric tensor: must be real,diagonal and isotropic,
			e_list[n_layers+1]=3x3 substrate dielectric tensor: must be real,diagonal and isotropic,
			e_list[n]=3x3 dielectric tensor of the n_th layers: arbitrary
	'd_list'= n_layers+2 numpy array: contains layer thinknesses:
			d_list[0]=d_list[n_layers+1]=0: for the incident medium and substrate
			d_list[n]=d_n n_th layer thickness in nm

	Returns
	-------
	'm_R,m_T'= reflection and transmission matrix
	'''
	
	#------incident medium check------
	diag_flag = (e_list[0]==np.diag(np.diagonal(e_list[0]))).all()
	iso_flag = (e_list[0,0,0]==e_list[0,1,1]==e_list[0,2,2])
	real_flag =np.abs(e_list[0,0,0])==np.real(e_list[0,0,0])
	if not (diag_flag and iso_flag and real_flag):
		print "Incident medium must be real, diagonal and isotropic"
		return
	n0=np.sqrt(e_list[0,0,0])
	
	#------substrate check------
	diag_flag = (e_list[-1]==np.diag(np.diagonal(e_list[-1]))).all()
	iso_flag = (e_list[-1,0,0]==e_list[-1,1,1]==e_list[-1,2,2])
	real_flag =np.abs(e_list[-1,0,0])==np.real(e_list[-1,0,0])
	if not (diag_flag and iso_flag and real_flag):
		print "Substrate must be real, diagonal and isotropic"
		return
	ns=np.sqrt(e_list[-1,0,0])
	
	#------wavevector modulus and in plane components------
	k0=2.0*np.pi/wl;
	kx=-k0*n0*np.sin(theta0)*np.cos(phi0);
	ky=-k0*n0*np.sin(theta0)*np.sin(phi0);
	
	#print "lambda",'%.14e' % wl
	#print "1 div lambda",'%.14e' % (1.0/wl)
	#print "eps0",'%.14e    %.14e' % (e_list[0,0,0].real,e_list[0,0,0].imag)
	#print "n0",'%.14e    %.14e' % (n0.real,n0.imag)
	#print "k0",'%.14e' % k0
	#print "k0*n0",'%.14e    %.14e' % (k0*n0.real,k0*n0.imag)
	#print "kx",'%.14e    %.14e' % (kx.real,kx.imag)
	#print "ky",'%.14e    %.14e' % (ky.real,ky.imag)

	#------kz,v_e and boundary and propagation matrix for R and T------
	m_a12=np.zeros((len(e_list),2,2),dtype=np.complex128);m_a34=np.zeros_like(m_a12);
	m_b12=np.zeros_like(m_a12);m_b34=np.zeros_like(m_a12);
	m_c12=np.zeros_like(m_a12);m_c34=np.zeros_like(m_a12);
	for n in range(len(e_list)):
		v_kz=kz_eigenvalues(k0,kx,ky,e_list[n]);
		v_e,v_kz=kz_eigenvectors(k0,kx,ky,v_kz,e_list[n])
		
		#if n==3:
			
			#m_eps=e_list[n]
			
			#print
			#print "m_eps"
			#for i in range(3):
				#print '%.14e    %.14e    %.14e    %.14e    %.14e    %.14e' % (m_eps[i,0].real,m_eps[i,0].imag,m_eps[i,1].real,m_eps[i,1].imag,m_eps[i,2].real,m_eps[i,2].imag)
			
			
			#print "v_kz"
			#for kz in v_kz:
				#print '%.14e    %.14e' % (kz.real,kz.imag)
			#print
			
			#print "v_e"
			#for e in v_e:
				#print '%.14e    %.14e    %.14e    %.14e    %.14e    %.14e' % (e[0].real,e[0].imag,e[1].real,e[1].imag,e[2].real,e[2].imag)
			#print
			#print
			#print
		
		m_a12[n],m_a34[n],m_b12[n],m_b34[n],m_c12[n],m_c34[n]=m_abc(k0,kx,ky,v_kz,v_e,d_list[n])

	#------looping for R over the layers------
	m_R=np.zeros_like(m_c12)
	for n in range(len(e_list)-2,-1,-1):
	
		#------building the first factor for the F_n+1 matrix-----
		f1 = np.dot(m_b12[n+1],m_c12[n+1])+np.dot(np.dot(m_b34[n+1],m_c34[n+1]),m_R[n+1]) 
		
		#------building the second factor for the F_n+1 matrix-----
		f2_inv=np.dot(m_a12[n+1],m_c12[n+1])+np.dot(np.dot(m_a34[n+1],m_c34[n+1]),m_R[n+1]) #---inverse---
		f2=np.linalg.inv(f2_inv)
		
		#------F_n+1 matrix-----
		f_np1=np.dot(f1,f2)
		
		#------R_n------
		r1_inv=np.dot(f_np1,m_a34[n])-m_b34[n];r1=np.linalg.inv(r1_inv);
		r2=m_b12[n]-np.dot(f_np1,m_a12[n])
		m_R[n]=np.dot(r1,r2)
		
	#------rotating m_R to the s,p states------
	p_inc=np.zeros((2,2));
	p_inc[0,0]=np.cos(theta0)*np.cos(phi0);p_inc[0,1]=-np.sin(phi0);
	p_inc[1,0]=np.cos(theta0)*np.sin(phi0);p_inc[1,1]=np.cos(phi0);
	p_inc_inv=np.linalg.inv(p_inc)
	m_Rsp=np.dot(np.dot(p_inc_inv,m_R[0]),p_inc) #Finally the  R matrix output


	#------looping for T over the layers------
	m_Tn=np.zeros_like(m_c12);
	m_T=np.identity(2,dtype=np.complex128);
	for n in range(len(e_list)-1):
	
		#------building the first factor for the T_n-----
		f1_inv = np.dot(m_a12[n+1],m_c12[n+1])+np.dot(np.dot(m_a34[n+1],m_c34[n+1]),m_R[n+1])
		f1=np.linalg.inv(f1_inv)
		
		#------building the second factor for the T_n-----
		f2=m_a12[n]+np.dot(m_a34[n],m_R[n])
			
		#------T_n------
		m_Tn[n]=np.dot(f1,f2)
		
		#------T------
		m_T=np.dot(m_T,m_Tn[n])
	
	#------rotating m_R to the s,p states------
	theta_s=np.arcsin(np.sin(theta0)*n0/ns);
	p_sub=np.zeros((2,2),dtype=np.complex128);
	p_sub[0,0]=np.cos(theta_s)*np.cos(phi0);p_sub[0,1]=-np.sin(phi0);
	p_sub[1,0]=np.cos(theta_s)*np.sin(phi0);p_sub[1,1]=np.cos(phi0);
	p_sub_inv=np.linalg.inv(p_sub)
	m_Tsp=np.dot(np.dot(p_sub_inv,m_T),p_inc)
		
	#-------R,T-------
	return m_Rsp,m_Tsp