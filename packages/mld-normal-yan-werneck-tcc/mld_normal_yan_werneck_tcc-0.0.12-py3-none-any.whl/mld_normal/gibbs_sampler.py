from .dinamic_linear_model import DinamicLinearModel
import numpy as np
from scipy import stats
from tqdm import tqdm

class GibbsSampler:

    def __init__(self, y, F, G, m0, C0, max_iterations = 1000):
          
        self.y = y
        self.F = F
        self.G = G
        self.m0 = m0
        self.C0 = C0
        self.max_iterations = max_iterations
        
        # size of the observations
        self.N = y.shape[0]

        # priori's hyperparameters that generates large variance and small mean (V)
        self.v_a_priori = 0.01
        self.v_b_priori = 0.01

        # priori's hyperparameters that generates large variance and small mean (W)
        self.w_a_priori = 0.01
        self.w_b_priori = 0.01

        # array of the states samples 
        self.states_samples = np.zeros(shape = (max_iterations, self.N))

        # array of the observation variance samples
        self.vt = np.zeros(shape = max_iterations + 1)
        
        # array of the states variance samples
        self.wt = np.zeros(shape = max_iterations + 1)

        # array of the state in time 0 samples
        self.u0t = np.zeros(shape = max_iterations + 1)
        

        # initial values
        self.vt[0] = 0.1
        self.wt[0] = 0.1
        self.u0t[0] = 1

    def __ffbs_normal_mld(self, m, C, R):
        states_size = m.shape[0]
        last_state_mean = m[-1]
        last_state_var = C[-1]
        
        states = np.zeros(shape = m.shape[0])
        h = np.zeros(shape = m.shape[0] - 1)
        H = np.zeros(shape = C.shape[0] - 1)
        
        states[-1] = stats.norm.rvs(loc = last_state_mean, scale = np.sqrt(last_state_var))
        
        for iteration in reversed( range(states_size - 1) ):
            h[iteration] = m[iteration] + C[iteration] * (states[iteration+1] - m[iteration]) / R[iteration]
            H[iteration] = C[iteration] - (C[iteration]**2) / R[iteration]
            states[iteration] = stats.norm.rvs(loc = h[iteration], scale = np.sqrt(H[iteration]))
        
        return states

    def __v_inverse_gamma(self, a_priori, b_priori, y, u):
        a_posteriori = a_priori + y.shape[0]/2
        sum_errors = 0
        for iteration in range(y.shape[0]):
            sum_errors += (y[iteration] - u[iteration])**2
        b_posteriori = b_priori + sum_errors/2
        
        return stats.invgamma.rvs(a_posteriori, scale = b_posteriori, size = 1)


    def __w_inverse_gamma(self, a_priori, b_priori, u, u0):
        a_posteriori = a_priori + u.shape[0]/2
        sum_errors = u[0] - u0
        for iteration in range(1, u.shape[0]):
            sum_errors += (u[iteration] - u[iteration-1])**2
        b_posteriori = b_priori + sum_errors/2

        return stats.invgamma.rvs(a_posteriori, scale = b_posteriori, size = 1)


    def __u0_normal(self, m0, u1, C0, W):
        mean = (C0*u1 + W*m0)/(C0 + W)
        variance = (C0*W)/(C0 + W)
        
        return stats.norm.rvs(loc = mean, scale = np.sqrt(variance))


    def run_sampling(self):
        with tqdm(total = self.max_iterations, desc="Sampling", 
            bar_format="{l_bar}{bar}| [ time left: {remaining} ] | [ elapsed time: {elapsed}]") as pbar:

            for i in range(self.max_iterations):
                mld = DinamicLinearModel(self.F, self.G, self.m0, 
                    self.C0, V = self.vt[i], W = self.wt[i])
                mld.fit(self.y)
                
                m = mld.get_m()
                C = mld.get_C()
                R = mld.get_R()
                
                self.states_samples[i] = self.__ffbs_normal_mld(m, C, R)
                
                self.vt[i + 1] = self.__v_inverse_gamma(self.v_a_priori, self.v_b_priori, 
                                 self.y, self.states_samples[i])
                
                self.wt[i + 1] = self.__w_inverse_gamma(self.w_a_priori, self.w_b_priori, 
                                 self.states_samples[i], self.u0t[i])
                
                self.u0t[i + 1] = self.__u0_normal(self.m0, self.states_samples[i][0], self.C0, 
                                 self.wt[i+1])
                pbar.update(1)

    
    def get_states_sample(self):
        return self.states_samples
    
    def get_mean_states_sample(self, offset = 0):
        self.smoothed_states = np.zeros(shape = self.N)

        for i in range(self.N):
            tmp_states = np.zeros(shape = self.max_iterations-offset)
            
            for j in range(offset, self.max_iterations):
                tmp_states[j-offset] = self.states_samples[j-offset][i]
            
            self.smoothed_states[i] = np.mean(tmp_states)

        return self.smoothed_states


    def get_V_sample(self):
        return self.vt

    def get_W_sample(self):
        return self.wt

    def get_u0_sample(self):
        return self.u0t





