from .base import *



class BaseSVM(BaseModel):
    def __init__(self, kernel='linear', C=1, degree=3, gamma='auto', beta=1, theta=-1, n_iter=100, verbose=2):
        super(BaseSVM, self).__init__(n_iter)
        _kernel_map = {"linear": self.linear_kernel, 'poly': self.poly_kernel, 'rbf': self.gaussian_kernel, 'laplace': self.laplace_kernel, 'sigmoid': self.sigmoid_kernel}
        self.kernel = self._select_kernel(kernel, _kernel_map)
        self.degree = degree
        self.gamma = gamma
        self.beta = beta
        self.theta = theta
        self.C = C
        self.verbose = verbose
        self.acc = []
        self.loss = []




    def _select_kernel(self, kernel, kernel_map):
        if isinstance(kernel, str) and kernel in kernel_map:
            return kernel_map[kernel]
        elif callable(kernel):
            return kernel


    def linear_kernel(self, x1, x2):
        '''
        :param x1: (n_sample1, n_features)
        :param x2: (n_sample2, n_features)
        :return: (n_sample1, n_sample2)
        '''
        return x1.dot(x2.T)

    def poly_kernel(self, x1, x2):
        return np.power(self.linear_kernel(x1, x2), self.degree)


    def gaussian_kernel(self, x1, x2):
        '''
        :param x1: (n_sample1, n_features)
        :param x2: (n_sample2, n_features)
        :param degree:
        :param gamma:
        :param args:
        :return: (n_sample1, n_sample2)
        '''
        if x1.ndim == 1:
            x1 = x1[np.newaxis, ...]
        if x2.ndim == 1:
            x2 = x2[np.newaxis, ...]
        m = x1.shape[0]
        n = x2.shape[0]
        K = np.zeros((m, n))
        for i in range(m):
            K[i] = np.exp(- np.square(np.linalg.norm(x1[i] - x2)) / (2 * (self.gamma ** 2)))
        return K


    def laplace_kernel(self, x1, x2):
        '''
        :param x1: (n_sample1, n_features)
        :param x2: (n_sample2, n_features)
        :param degree:
        :param gamma:
        :param args:
        :return: (n_sample1, n_sample2)
        '''
        if x1.ndim == 1:
            x1 = x1[np.newaxis, ...]
        if x2.ndim == 1:
            x2 = x2[np.newaxis, ...]
        m = x1.shape[0]
        n = x2.shape[0]
        K = np.zeros((m, n))
        for i in range(m):
            K[i] = np.exp(- np.linalg.norm(x1[i] - x2) / self.gamma)
        return K


    def sigmoid_kernel(self, x1, x2):
        return np.tanh(self.beta * np.dot(x1, x2.T) + self.theta)



class SVC(BaseSVM):
    def __init__(self, kernel='linear', C=1, tol=1e-3,  degree=3, gamma='auto', beta=1, theta=-1, n_iter=10, verbose=2):
        super(SVC, self).__init__(kernel, C, degree, gamma, beta, theta, n_iter, verbose)
        self.alphas = None
        self.tol = tol
        self.E = None
        self.g = None
        self.m = None
        self.b = None
        self.changed_pairs = []
        self.support_vector_idx = None
        self.X = None
        self.y = None



    def calc_E(self, X, y, index_list):
        for i in index_list:
            self.g[i] = self.predict(X[i], is_train=True)
            self.E[i] = self.g[i] - y[i]



    def initial_params(self, X, y):
        self.X = X
        self.y = y
        self.m = X.shape[0]
        self.gamma = 1 / X.shape[1] if self.gamma == 'auto' else self.gamma
        self.alphas = np.zeros((self.m, 1))
        self.g = np.zeros((self.m, 1))
        self.E = np.zeros((self.m, 1))
        self.b = 0
        self.calc_E(X, y, range(self.m))



    @count_time
    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        if y.ndim == 1:
            y = y[:, np.newaxis]
        self.initial_params(X, y)
        while self.n_iter == -1 or self.iteration < self.n_iter:
            t1 = time.time()
            changed_alpha_pairs = 0
            index_list = [i for i in range(self.m) if 0 < self.alphas[i] < self.C]
            unsatisfy_list = [i for i in range(self.m) if i not in index_list]
            index_list.extend(unsatisfy_list)
            for i in index_list:
                if self.select_I(y, i):
                    j = self.select_J(i)
                else:
                    continue
                if y[i] == y[j]:
                    L = max(0, self.alphas[i] + self.alphas[j] - self.C)
                    H = min(self.C, self.alphas[i] + self.alphas[j])
                else:
                    L = max(0, self.alphas[j] - self.alphas[i])
                    H = min(self.C, self.alphas[j] - self.alphas[i] + self.C)
                eta = self.kernel(X[i], X[i]) + self.kernel(X[j], X[j]) - 2 * self.kernel(X[i], X[j])
                if eta <= 0:
                    continue
                alpha2_new_unc = self.alphas[j] + y[j] * (self.E[i] - self.E[j]) / eta
                alpha2_new = np.clip(alpha2_new_unc, L, H)
                if abs(self.alphas[j] - alpha2_new) < self.tol:
                    j, alpha2_new, flag = self.reselect_J(i, index_list, X, y)
                    if not flag:
                        continue

                changed_alpha_pairs += 1
                alpha1_new = self.alphas[i] + y[i] * y[j] * (self.alphas[j] - alpha2_new)
                b1_new = - self.E[i] - y[i] * self.kernel(X[i], X[i]) * (alpha1_new - self.alphas[i]) - y[j] * self.kernel(X[j], X[i]) * (alpha2_new - self.alphas[j]) + self.b
                b2_new = - self.E[j] - y[i] * self.kernel(X[i], X[j]) * (alpha1_new - self.alphas[i]) - y[j] * self.kernel(X[j], X[j]) * (alpha2_new - self.alphas[j]) + self.b
                if 0 < alpha1_new < self.C and 0 < alpha2_new < self.C:
                    b_new = b1_new
                else:
                    b_new = (b1_new + b2_new) / 2

                self.alphas[i] = alpha1_new
                self.alphas[j] = alpha2_new
                self.b = b_new
                self.calc_E(X, y, [i, j])
            t2 = time.time()
            iter_time = t2 - t1
            self.changed_pairs.append(changed_alpha_pairs)
            loss = self.get_loss(X, y)
            acc = self.get_acc(y, self.predict(X))
            self.loss.append(loss)
            self.acc.append(acc)
            self.iteration += 1
            self.train_verbose(acc, loss, iter_time)
            if changed_alpha_pairs == 0:
                break
        if self.verbose == 2:
            print()
        support_vector_idx = np.nonzero(self.alphas > 0)[0]
        self.X = X[support_vector_idx]
        self.y = y[support_vector_idx]
        self.alphas = self.alphas[support_vector_idx]
        self.support_vector_idx = support_vector_idx


    def get_loss(self, X, y):
        w = np.sum(self.alphas * y * X, axis=0, keepdims=True) # (1, n)
        loss = np.linalg.norm(w) / 2 + np.maximum(0, np.sum(1 - X.dot(w.T) * y))
        return loss


    def select_I(self, y, i):
        if y[i] * self.g[i] == 1 and 0 < self.alphas[i] < self.C:
            return False
        elif y[i] * self.g[i] >= 1 and self.alphas[i] == 0:
            return False
        elif y[i] * self.g[i] <= 1 and self.alphas[i] == self.C:
            return False
        return True


    def select_J(self, i):
        E1 = self.E[i]
        if E1 >= 0:
            j = np.argmin(self.E)
        else:
            j = np.argmax(self.E)
        return j



    def reselect_J(self, i, index_list, X, y):
        flag = False
        j_index = -1
        alpha = 0
        for j in index_list:
            if j != i:
                if y[i] == y[j]:
                    L = max(0, self.alphas[j] + self.alphas[i] - self.C)
                    H = min(self.C, self.alphas[j] + self.alphas[i])
                else:
                    L = max(0, self.alphas[j] - self.alphas[i])
                    H = min(self.C, self.C + self.alphas[j] - self.alphas[i])
                eta = self.kernel(X[i], X[i]) + self.kernel(X[j], X[j]) - 2 * self.kernel(X[i], X[j])
                if eta <= 0:
                    continue
                alpha2_new_unc = self.alphas[j] + y[j] * (self.E[i] - self.E[j]) / eta
                alpha2_new = np.clip(alpha2_new_unc, L, H)
                if abs(self.alphas[j] - alpha2_new) < self.tol:
                    continue
                else:
                    j_index = j
                    flag = True
                    alpha = alpha2_new
                    break
        return j_index, alpha, flag



    def predict(self, X, is_train=False, *args):
        if X.ndim == 1:
            X = X[np.newaxis, ...]
        pred = np.multiply(self.alphas, self.y).T.dot(self.kernel(self.X, X)) + self.b
        return pred if is_train else np.sign(pred)


    def summary(self):
        plt.figure()
        plt.title('training')
        plt.subplot(1, 3, 1)
        plt.plot(self.acc)
        plt.xlabel('iteration')
        plt.ylabel('acc')
        plt.subplot(1, 3, 2)
        plt.plot(self.loss)
        plt.xlabel('iteration')
        plt.ylabel('loss')
        plt.subplot(1, 3, 3)
        plt.plot(self.changed_pairs)
        plt.xlabel('iteration')
        plt.ylabel('changed-pairs')
        plt.show()


