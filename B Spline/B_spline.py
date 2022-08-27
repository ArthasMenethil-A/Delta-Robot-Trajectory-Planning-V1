# B-Spline

# =================================================================================================
# -- IMPORTS --------------------------------------------------------------------------------------
# =================================================================================================

import numpy as np 
import math 
import matplotlib.pyplot as plt 

# =================================================================================================
# -- B SPLINE --------------------------------------------------------------------------------------
# =================================================================================================

# this function only works for p=4 

class BSpline: 
	def __init__(self, q, t, T=0.1, vi=0, vf=0, ai=0, af=0): 
		self.q = np.array(q)	# the points coordinates 
		self.t = np.array(t)	# the time instants array 
		self.n = self.q.shape[0] - 1

	def get_u_vector(self, t, p):
		t = np.array(t)
		n = t.shape[0] - 1

		if p%2 == 0: # p even
			n_knot = n + 2*p + 1
			u = np.zeros((n_knot+1))
			u[0:p+1] = t[0]
			u[p+1:n+p+1] = (t[0:n] + t[1:n+1])/2
			u[n+p+1:n+2*p+2] = t[n]
		elif p%2 != 0: # p odd 
			n_knot = n + 2*p
			u = np.zeros((n_knot+1))
			u[0:p+1] = t[0]
			u[p+1:n+p] = t[1:n]
			u[n+p:n+2*p+1] = t[n]
		else:
			print("p needs to be a positive integer")

		return u

	def which_span(self, u, u_instant, p=4):
		u = np.array(u)
		n_knot = u.shape[0] - 1
		high = n_knot - p
		low = p

		if u_instant == u[high]:
			mid = high
		else: 
			mid = (high+low)/2
			mid = int(mid)
			check = (u_instant < u[mid]) or (u_instant >= u[mid+1])
			while(check):

				if u_instant == u[int(mid+1)]:
					mid = mid+1
				else:
					if u_instant > u[int(mid)]:
						low = mid
					else:
						high = mid
					mid = (high+low)/2

		return mid

	def get_basis_function(self, i, u, u_instant, p=4): 
		u = np.array(u)
		n_knot = u.shape[0] - 1
		B = np.array((p+1))
		DL = np.array((p+1))
		DR = np.array((p+1))

		B[0] = 1
		for j in range(1, p+1):
			DL[j] = u_instant - u[i+1-j]
			DR[j] = u[i+j] - u_instant
			acc = 0 
			for r in range(j):
				temp = B[r]/(DR[r+1] + DL[j-r])
				B[r] = acc + DR[r+1]*temp
				acc = DL[j-r]*temp
			B[j] = acc

		return B
	def get_basis_function_derivative(self, u, B, p=4):
		B = np.array(B)
		u = np.array(u)
		n_knot = u.shape[0] - 1
		B_derive = np.zeros((B.shape[0], 3))
		a = np.zeros((3, 3))

		B_derive[:, 0] = B
		for k in [1, 2]:
			for j, u_j in enumerate(u):
				SUM = 0
				for m in range(k+1):
					SUM += a[k, m]*B_derive[p-k, j+m]
				B_derive[k, j] = math.factorial(p)/math.factorial(p-k)*SUM

		return B_derive

	def get_A_matrix(self, u, p=4):

		u = np.array(u)
		n_knot = u.shape[0]-1
		n = self.n
		m = n_knot-p-1
		temp_A = np.zeros((n+1, m+1))
		for i, t_i in enumerate(t):
			B = self.get_B_P(u, t_i)[0:m+1]
			temp_A[i, :] = B

		A = np.zeros((n+5, m+1))

		return A

	def get_c_matrix(self): 
		c = 0 

		return c 

	def get_P(self):
		pass 

# =================================================================================================
# -- MAIN --------------------------------------------------------------------------------------
# =================================================================================================
u = [0, 0, 0, 0, 1, 2, 4, 7, 7, 7, 7]
u_instant = 1.5

traj = BSpline([0], [0])
i = traj.which_span(u, u_instant, p=3)
print(i)
