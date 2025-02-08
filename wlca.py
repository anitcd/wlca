import numpy as np
import scipy.stats as stats
from datetime import datetime


class WLCA:
    def __init__(self, n_components=2, tol=1e-3, max_iter=100, random_state=None):
        self.n_components = n_components
        self.random_state = random_state
        self.tol = tol
        self.max_iter = max_iter

        # flag to indicate if converged
        self.converged_ = False

        # model parameters
        self.ll_ = [-np.inf]
        self.weight = None
        self.theta = None
        self.responsibility = None

        # bic estimation
        self.bic = None

        # verbose level
        self.verbose = 0

    def _calculate_responsibility(self, data, weights):

        n_rows, n_cols = np.shape(data)
        r_numerator = np.zeros(shape=(n_rows, self.n_components))
        for k in range(self.n_components):
            r_numerator[:, k] = self.weight[k] * np.prod(stats.bernoulli.pmf(data, p=self.theta[k]), axis=1)
            #r_numerator[:, k] = self.weight[k] * np.prod(stats.bernoulli.pmf(data, p=self.theta[k])# ^weights
            #, axis=1)# * weights
        r_denominator = np.sum(r_numerator, axis=1)
        return r_numerator / np.tile(r_denominator, (self.n_components, 1)).T

    def _do_e_step(self, data, weights):

        self.responsibility = self._calculate_responsibility(data, weights)

    def _do_m_step(self, data, weights):

        n_rows, n_cols = np.shape(data)

        # pi
        for k in range(self.n_components):
            #self.weight[k] = np.sum(self.responsibility[:, k]) / float(n_rows)
            self.weight[k] = np.sum(self.responsibility[:, k] * weights) / np.sum(weights)
            #self.weight[k] = np.sum(self.responsibility[:, k] # * weights) / float(n_rows) # * \sum{weights}

        # theta
        for k in range(self.n_components):
            numerator = np.zeros((n_rows, n_cols))
            for n in range(n_rows):
                #numerator[n, :] = self.responsibility[n, k] * data[n, :]
                numerator[n, :] = self.responsibility[n, k] * data[n, :] * weights[n]
            numerator = np.sum(numerator, axis=0)
            #denominator = np.sum(self.responsibility[:, k] * weights[n]) # ??
            #denominator = np.sum(self.responsibility[:, k]) * np.sum(weights)
            denominator = np.sum(self.responsibility[:, k] * weights)
            self.theta[k] = numerator / denominator

        # correct numerical issues
        mask = self.theta > 1.0
        self.theta[mask] = 1.0
        mask = self.theta < 0.0
        self.theta[mask] = 0.0

    def fit(self, data, weights):

        # initialization step
        n_rows, n_cols = np.shape(data)
        if n_rows < self.n_components:
            raise ValueError(
                '''
                LCA estimation with {n_components} components, but got only
                {n_rows} samples
                '''.format(n_components=self.n_components, n_rows=n_rows))

        if self.verbose > 0:
            print('EM algorithm started')

        self.weight = stats.dirichlet.rvs(np.ones(shape=self.n_components) / 2, random_state=self.random_state)[0]
        self.theta = stats.dirichlet.rvs(alpha=np.ones(shape=n_cols) / 2,
                                         size=self.n_components,
                                         random_state=self.random_state)

        for i in range(self.max_iter):
            if self.verbose > 0:
                print('\tEM iteration {n_iter}'.format(n_iter=i))

            # E-step
            self._do_e_step(data, weights)

            # M-step
            self._do_m_step(data, weights)
            
            # Print the 'theta' matrix after each iteration
            #print(f'Theta matrix after iteration {i}:\n{self.theta}\n')

            # Check for convergence
            aux = np.zeros(shape=(n_rows, self.n_components))
            for k in range(self.n_components):
                normal_prob = np.prod(stats.bernoulli.pmf(data, p=self.theta[k]), axis=1)
                aux[:, k] = self.weight[k] * normal_prob
                #aux[:, k] = self.weight[k] * normal_prob * weights
            #ll_val = np.sum(np.log(np.sum(aux, axis=1)))
            ll_val = np.sum(np.log(np.sum(aux, axis=1)) * weights)
            
            # Adjust for sample weights in the convergence check
            #weighted_ll_diff = np.abs(ll_val - self.ll_[-1]) / np.mean(weights)
            
            # Scale tolerance by the mean of sample weights
            #weighted_tol = self.tol * np.mean(weights)
            
            # Compute the relative change in log-likelihood
            #ll_diff_ratio = np.abs(ll_val - self.ll_[-1]) / np.abs(self.ll_[-1])
    
            if np.abs(ll_val - self.ll_[-1]) < self.tol:
            #if len(self.ll_) > 1 and np.abs((ll_val - self.ll_[-1]) / self.ll_[-1]) < self.tol: # Check for convergence based on relative change
            #if weighted_ll_diff < self.tol:
            #if np.abs(ll_val - self.ll_[-1]) < weighted_tol:
            #if ll_diff_ratio < self.tol:
            # Get the current date and time
                current_time = datetime.now()
                with open("./output/convergence.txt", "a") as file:
                    file.write(f"[{current_time}] Converged.")

                break
            else:
                self.ll_.append(ll_val)

        # calculate bic
        self.bic = np.log(n_rows)*(sum(self.theta.shape)+len(self.weight)) - 2.0*self.ll_[-1]

    def predict(self, data, weights):
        return np.argmax(self.predict_proba(data, weights), axis=1)

    def predict_proba(self, data, weights):
        return self._calculate_responsibility(data, weights)
