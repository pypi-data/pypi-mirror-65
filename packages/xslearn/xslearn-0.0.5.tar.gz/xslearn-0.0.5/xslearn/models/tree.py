from .base import *
from pylab import *


class TreeNode():
    def __init__(self, label=None, feature_index=None,feature_name=None, parent_node=None, leaf=False, c_val=0.):
        self.label = label
        self.leaf = leaf
        self.feature_index = feature_index
        self.feature_name = feature_name
        self.parent_node = parent_node
        self.child_node_dict = {}
        self.sample_lists = []
        self.prune_visited = False
        self.entropy = 0.
        self.gini = 0.
        self.c = c_val



    def predict(self, node, X, is_classify=True, c_val=0.):
        if node.leaf:
            if is_classify:
                return node.label
            else:
                return node.c + c_val
        feature_index = node.feature_index
        feature_val = X[:, feature_index]
        if str(feature_val[0]).isalnum() or str(feature_val[0]).isalpha():
            # discrete feature
            feature_val = str(feature_val[0])
            try:
                return self.predict(node.child_node_dict[feature_val], X, is_classify, c_val + node.c)
            except KeyError:
                return self.predict(node.child_node_dict['others'], X, is_classify, c_val + node.c)
        else:
            T = -1

            feature_val = float(feature_val)

            for val in node.child_node_dict.keys():
                if val[0] == '>':
                    T = float(val[1:])
                else:
                    T = float(val[2:])
                break
            if feature_val > T:
                child_name = '>' + str(T)
            else:
                child_name = '<=' + str(T)
            return self.predict(node.child_node_dict[child_name], X, is_classify, c_val + node.c)



class BaseDecisionTree(BaseModel):
    def __init__(self, max_depth=None, max_features=None, max_leaf_nodes=None, criterion='gini', attr_sets=None, *args, **kwargs):
        super(BaseDecisionTree, self).__init__()
        self.root = None
        self.X = None
        self.y = None
        self.attr_sets = attr_sets
        self.tree_dict = None
        self.max_depth = max_depth
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.criterion = criterion
        self.depth = 0
        self.features = 0
        self.leaf_nums = 0


    def fit(self, X, y, *args, **kwargs):
        self.feature_mask = kwargs.pop('feature_mask', None)
        self.root = TreeNode(parent_node='root')
        self.X = np.array(X)
        self.y = np.array(y)
        if self.attr_sets is None:
            self.attr_sets = ['attr%d' % i for i in range(X.shape[1])]
        if self.y.ndim > 1:
            self.y = self.y.flatten()



    def isSameClass(self, y):
        C = y[0]
        for label in y:
            if label != C:
                return False
        return True


    def majorityClass(self, y):
        class_dict = self.class_count(y)
        sortted_class_dict = sorted(class_dict.items(), key=operator.itemgetter(1), reverse=True)
        return sortted_class_dict[0][0]


    def class_count(self, y):
        class_dict = {}
        for label in y:
            if label not in class_dict:
                class_dict[label] = 1
            else:
                class_dict[label] += 1
        return class_dict


    def predict(self, X, is_train=False, *args):
        if X.shape[0] > 1:
            pred = np.zeros((X.shape[0], 1))
            for i, x in enumerate(X):
                pred[i] = self.root.predict(self.root, x)
            return pred
        return self.root.predict(self.root, X)


    def score(self, X, y, use_batch=1, reduction='mean', *args, **kwargs):
        super(BaseDecisionTree, self).score(X, y, use_batch, reduction, *args, **kwargs)


    def visualize(self):
        # 绘图
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False

        decisionNode = dict(boxstyle="sawtooth", fc="0.8")
        leafNode = dict(boxstyle="round4", fc="0.8")
        arrow_args = dict(arrowstyle="<-")

        def plotNode(nodeTxt, centerPt, parentPt, nodeType):
            createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                                    textcoords='axes fraction', va='center', ha='center', bbox=nodeType,
                                    arrowprops=arrow_args)

        def getNumLeafs(myTree):
            numLeafs = 0
            firstStr = list(myTree.keys())[0]
            secondDict = myTree[firstStr]
            for key in secondDict.keys():
                if type(secondDict[key]).__name__ == 'dict':
                    numLeafs += getNumLeafs(secondDict[key])
                else:
                    numLeafs += 1
            return numLeafs

        def getTreeDepth(myTree):
            maxDepth = 0
            firstStr = list(myTree.keys())[0]
            secondDict = myTree[firstStr]
            for key in secondDict.keys():
                if type(secondDict[key]).__name__ == 'dict':
                    thisDepth = 1 + getTreeDepth(secondDict[key])
                else:
                    thisDepth = 1
                if thisDepth > maxDepth:
                    maxDepth = thisDepth
            return maxDepth

        def plotMidText(cntrPt, parentPt, txtString):
            xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0] + 0.02
            yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
            createPlot.ax1.text(xMid, yMid, txtString)

        def plotTree(tree_dict, node, criterion, parentPt, nodeTxt):
            numLeafs = getNumLeafs(tree_dict)
            # depth = getTreeDepth(myTree)
            firstStr = list(tree_dict.keys())[0]
            text = firstStr + '\n'

            if criterion == 'gini':
                text += 'gini = ' + str(round(node.gini, 2))
            else:
                text += 'entropy = ' + str(round(node.entropy, 2))
            text += '\nsamples = ' + str(len(node.sample_lists))
            text += '\nclass = ' + str(node.label)

            cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)

            plotMidText(cntrPt, parentPt, nodeTxt)
            plotNode(text, cntrPt, parentPt, decisionNode)
            secondDict = tree_dict[firstStr]
            plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
            for key in secondDict.keys():
                if type(secondDict[key]).__name__ == 'dict':
                    plotTree(secondDict[key], node.child_node_dict[key], criterion, (cntrPt[0], cntrPt[1] - 0.03), str(key))
                else:

                    plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
                    sub_node = node.child_node_dict[key]
                    if criterion == 'gini':
                        text = 'gini = ' + str(round(sub_node.gini, 2))
                    else:
                        text = 'entropy = ' + str(round(sub_node.entropy, 2))
                    text += '\nsamples = ' + str(len(sub_node.sample_lists))
                    text += '\nclass = ' + str(sub_node.label)

                    plotNode(text, (plotTree.xOff, plotTree.yOff), (cntrPt[0], cntrPt[1] - 0.03), leafNode)
                    plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
            plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD


        def createPlot(tree_dict, tree_root, criterion):
            fig = plt.figure(1, facecolor='white')
            fig.clf()
            axprops = dict(xticks=[], yticks=[])
            createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
            plotTree.totalW = float(getNumLeafs(tree_dict))
            plotTree.totalD = float(getTreeDepth(tree_dict))
            plotTree.xOff = - 0.5 / plotTree.totalW
            plotTree.yOff = 1.0
            plotTree(tree_dict, tree_root, criterion, (0.5, 1.0), '')
            plt.show()

        createPlot(self.tree_dict, self.root, self.criterion)




class ID3Tree(BaseDecisionTree):
    def __init__(self, max_depth=None, max_features=None, max_leaf_nodes=None, criterion='entropy',*args, **kwargs):
        super(ID3Tree, self).__init__(max_depth, max_features, max_leaf_nodes, criterion, *args, **kwargs)



    @count_time
    def fit(self, *args, **kwargs):
        super(ID3Tree, self).fit(*args, **kwargs)
        self.tree_dict = self.__recusive(self.X, self.y, self.attr_sets, self.root, self.max_depth)



    def calc_entropy(self, y):
        Ent = 0
        m = len(y)
        class_dict = self.class_count(y)
        for k, v in class_dict.items():
            prob = v / m
            if prob == 0.0:
                Ent = 0.0
            else:
                Ent += prob * math.log(prob, 2)
        return -Ent


    def __recusive(self, X, y, attr_sets, node, depth):
        if (self.max_leaf_nodes is not None and self.leaf_nums >= self.max_leaf_nodes) or (self.max_features is not None and self.features >= self.max_features) or (depth is not None and depth <= 1) or len(attr_sets) == 0:
            node.label = self.majorityClass(y)
            node.leaf = True
            node.entropy = self.calc_entropy(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label

        if self.isSameClass(y):
            node.label = y[0]
            node.leaf = True
            node.entropy = self.calc_entropy(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label
        if len(attr_sets) == 0:
            node.label = self.majorityClass(y)
            node.leaf = True
            node.entropy = self.calc_entropy(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label

        split_feature_index, split_T = self.chooseBestFeaturToSplit(X, y, attr_sets)
        node.feature_index = split_feature_index
        node.feature_name = self.attr_sets[split_feature_index]
        node.entropy = self.calc_entropy(y)
        node.sample_lists = X
        self.features += 1


        my_dict = {node.feature_name: {}}
        split_data = self.X[:, split_feature_index]

        if split_T is None:
            # discrete feature
            unique_split_data = set(split_data)
            for feat in unique_split_data:
                sub_node = TreeNode(parent_node=node)
                node.child_node_dict[feat] = sub_node
                sub_dataset, sub_dataset_label = self.split_data(X, split_feature_index, feat, y)
                if len(sub_dataset_label) == 0:
                    sub_node.label = self.majorityClass(y)
                    sub_node.leaf = True
                    sub_node.entropy = self.calc_entropy(y)
                    sub_node.sample_lists = X
                    self.leaf_nums += 1
                    return sub_node.label
                else:
                    sub_attr_sets = attr_sets.copy()
                    sub_attr_sets.remove(self.attr_sets[split_feature_index])
                    if depth is None:
                        my_dict[node.feature_name][feat] = self.__recusive(sub_dataset, sub_dataset_label, sub_attr_sets, sub_node, depth)
                    else:
                        my_dict[node.feature_name][feat] = self.__recusive(sub_dataset, sub_dataset_label,sub_attr_sets, sub_node, depth - 1)
        else:
            # continuous feature
            pos_X_sub, neg_X_sub, pos_y_sub, neg_y_sub = self.split_data_by_T(X, split_feature_index, split_T, y)
            sub_dataset = [neg_X_sub, pos_X_sub]
            sub_dataset_label = [neg_y_sub, pos_y_sub]
            for i in range(2):
                sub_node = TreeNode(parent_node=node)
                if i == 0:
                    val = '<=' + str(split_T)
                else:
                    val = '>' + str(split_T)
                node.child_node_dict[val] = sub_node
                if len(sub_dataset[i]) == 0:
                    sub_node.label = self.majorityClass(y)
                    sub_node.leaf = True
                    sub_node.entropy = self.calc_entropy(y)
                    sub_node.sample_lists = X
                    self.leaf_nums += 1
                    return sub_node.label
                else:
                    if depth is None:
                        my_dict[node.feature_name][val] = self.__recusive(sub_dataset[i], sub_dataset_label[i], attr_sets, sub_node, depth)
                    else:
                        my_dict[node.feature_name][val] = self.__recusive(sub_dataset[i], sub_dataset_label[i], attr_sets, sub_node, depth - 1)

        return my_dict



    def chooseBestFeaturToSplit(self, X, y, attr_sets):
        base_ent = self.calc_entropy(y)
        m = X.shape[0]
        best_gain = -1
        best_feature_index = 0
        best_T = None
        for attr in attr_sets:
            j = self.attr_sets.index(attr)
            if self.feature_mask is not None and j not in self.feature_mask:
                continue
            feature_list = [x[j] for x in X]
            if str(feature_list[0]).isalnum():
                # discrete feature
                unique_feature_val = set(feature_list)
                ent = 0
                for feat in unique_feature_val:
                    sub_X, sub_y = self.split_data(X, j, feat, y)
                    prob = len(sub_y) / m
                    ent += prob * self.calc_entropy(sub_y)
                gain = base_ent - ent
                if gain > best_gain:
                    best_gain = gain
                    best_feature_index = j
            else:
                # continuous feature
                feature_list = list(map(float, feature_list))
                sorted_feature_list = sorted(feature_list)
                for f in range(len(sorted_feature_list) - 1):
                    T = 0.5 * (sorted_feature_list[f] + sorted_feature_list[f + 1])
                    pos_X, neg_X, pos_y, neg_y = self.split_data_by_T(X, j, T, y)
                    pos_prob = len(pos_y) / m
                    neg_prob = len(neg_y) / m
                    ent = pos_prob * self.calc_entropy(pos_y) + neg_prob * self.calc_entropy(neg_y)
                    gain = base_ent - ent
                    if gain > best_gain:
                        best_gain = gain
                        best_feature_index = j
                        best_T = T

        return best_feature_index, best_T




    def split_data(self, X, feature_index, split_val, y=None):
        split_index = X[:, feature_index] == split_val
        X_sub = X[split_index]
        if y is not None:
            y_sub = y[split_index]
            return X_sub, y_sub
        return X_sub


    def split_data_by_T(self, X, feature_index, T, y=None):
        pos_index = X[:, feature_index] > T
        neg_index = X[:, feature_index] <= T
        pos_X_sub = X[pos_index]
        neg_X_sub = X[neg_index]
        if y is not None:
            pos_y_sub = y[pos_index]
            neg_y_sub = y[neg_index]
            return pos_X_sub, neg_X_sub, pos_y_sub, neg_y_sub
        return pos_X_sub, neg_X_sub




class C45Tree(BaseDecisionTree):
    def __init__(self, max_depth=None, max_features=None, max_leaf_nodes=None, criterion='entropy_ratio', *args, **kwargs):
        super(C45Tree, self).__init__(max_depth, max_features, max_leaf_nodes, criterion, *args, **kwargs)


    @count_time
    def fit(self, *args, **kwargs):
        super(C45Tree, self).fit(*args, **kwargs)
        self.tree_dict = self.__recusive(self.X, self.y, self.attr_sets, self.root, self.max_depth)



    def calc_entropy(self, y):
        Ent = 0
        m = len(y)
        class_dict = self.class_count(y)
        for k, v in class_dict.items():
            prob = v / m
            if prob == 0.0:
                Ent = 0.0
            else:
                Ent += prob * math.log(prob, 2)
        return -Ent


    def __recusive(self, X, y, attr_sets, node, depth):
        if (self.max_leaf_nodes is not None and self.leaf_nums >= self.max_leaf_nodes) or (self.max_features is not None and self.features >= self.max_features) or (depth is not None and depth <= 1) or len(attr_sets) == 0:
            node.label = self.majorityClass(y)
            node.leaf = True
            node.entropy = self.calc_entropy(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label
        if self.isSameClass(y):
            node.label = y[0]
            node.leaf = True
            node.entropy = self.calc_entropy(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label



        split_feature_index, split_T = self.chooseBestFeaturToSplit(X, y, attr_sets)
        node.feature_index = split_feature_index
        node.feature_name = self.attr_sets[split_feature_index]
        node.entropy = self.calc_entropy(y)
        node.sample_lists = X
        self.features += 1

        my_dict = {node.feature_name: {}}
        split_data = self.X[:, split_feature_index]

        if split_T is None:
            # discrete feature
            unique_split_data = set(split_data)
            for feat in unique_split_data:
                sub_node = TreeNode(parent_node=node)
                node.child_node_dict[feat] = sub_node
                sub_dataset, sub_dataset_label = self.split_data(X, split_feature_index, feat, y)
                if len(sub_dataset_label) == 0:
                    sub_node.label = self.majorityClass(y)
                    sub_node.leaf = True
                    sub_node.entropy = self.calc_entropy(y)
                    sub_node.sample_lists = X
                    self.leaf_nums += 1
                    return sub_node.label
                else:
                    sub_attr_sets = attr_sets.copy()
                    sub_attr_sets.remove(self.attr_sets[split_feature_index])
                    if depth is None:
                        my_dict[node.feature_name][feat] = self.__recusive(sub_dataset, sub_dataset_label, sub_attr_sets, sub_node, depth)
                    else:
                        my_dict[node.feature_name][feat] = self.__recusive(sub_dataset, sub_dataset_label, sub_attr_sets, sub_node, depth - 1)

        else:
            # continuous feature
            pos_X_sub, neg_X_sub, pos_y_sub, neg_y_sub = self.split_data_by_T(X, split_feature_index, split_T, y)
            sub_dataset = [neg_X_sub, pos_X_sub]
            sub_dataset_label = [neg_y_sub, pos_y_sub]
            for i in range(2):
                sub_node = TreeNode(parent_node=node)
                if i == 0:
                    val = '<=' + str(split_T)
                else:
                    val = '>' + str(split_T)
                node.child_node_dict[val] = sub_node
                if len(sub_dataset[i]) == 0:
                    sub_node.label = self.majorityClass(y)
                    sub_node.leaf = True
                    sub_node.entropy = self.calc_entropy(y)
                    sub_node.sample_lists = X
                    self.leaf_nums += 1
                    return sub_node.label
                else:
                    if depth is None:
                        my_dict[node.feature_name][val] = self.__recusive(sub_dataset[i], sub_dataset_label[i], attr_sets, sub_node, depth)
                    else:
                        my_dict[node.feature_name][val] = self.__recusive(sub_dataset[i], sub_dataset_label[i], attr_sets, sub_node, depth - 1)

        return my_dict



    def chooseBestFeaturToSplit(self, X, y, attr_sets):
        base_ent = self.calc_entropy(y)
        m = X.shape[0]
        best_gain_ratio = -1
        best_feature_index = 0
        best_T = None
        for attr in attr_sets:
            j = self.attr_sets.index(attr)
            if self.feature_mask is not None and j not in self.feature_mask:
                continue
            feature_list = [x[j] for x in X]
            if str(feature_list[0]).isalnum():
                # discrete feature
                unique_feature_val = set(feature_list)
                ent = 0
                IV = 0
                for feat in unique_feature_val:
                    sub_X, sub_y = self.split_data(X, j, feat, y)
                    prob = len(sub_y) / m
                    ent += prob * self.calc_entropy(sub_y)
                    IV -= (prob * math.log(prob, 2))
                gain = base_ent - ent
                if IV == 0:
                    gain_ratio = 0
                else:
                    gain_ratio = gain / IV
                if gain_ratio >= best_gain_ratio:
                    best_gain_ratio = gain_ratio
                    best_feature_index = j
            else:
                # continuous feature
                feature_list = list(map(float, feature_list))

                sorted_feature_list = sorted(feature_list)
                for f in range(len(sorted_feature_list) - 1):
                    T = 0.5 * (sorted_feature_list[f] + sorted_feature_list[f + 1])
                    pos_X, neg_X, pos_y, neg_y = self.split_data_by_T(X, j, T, y)
                    pos_prob = len(pos_y) / m
                    neg_prob = len(neg_y) / m
                    ent = pos_prob * self.calc_entropy(pos_y) + neg_prob * self.calc_entropy(neg_y)
                    IV = -(pos_prob * math.log(pos_prob, 2)) - (neg_prob * math.log(neg_prob, 2))
                    gain = base_ent - ent
                    if IV == 0:
                        gain_ratio = 0
                    else:
                        gain_ratio = gain / IV
                    if gain_ratio > best_gain_ratio:
                        best_gain_ratio = gain_ratio
                        best_feature_index = j
                        best_T = T

        return best_feature_index, best_T




    def split_data(self, X, feature_index, split_val, y=None):
        split_index = X[:, feature_index] == split_val
        X_sub = X[split_index]
        if y is not None:
            y_sub = y[split_index]
            return X_sub, y_sub
        return X_sub


    def split_data_by_T(self, X, feature_index, T, y=None):
        pos_index = X[:, feature_index] > T
        neg_index = X[:, feature_index] <= T
        pos_X_sub = X[pos_index]
        neg_X_sub = X[neg_index]
        if y is not None:
            pos_y_sub = y[pos_index]
            neg_y_sub = y[neg_index]
            return pos_X_sub, neg_X_sub, pos_y_sub, neg_y_sub
        return pos_X_sub, neg_X_sub




class CartTree(BaseDecisionTree):
    def __init__(self, is_classify=True, max_depth=None, max_features=None, max_leaf_nodes=None, criterion='gini', *args, **kwargs):
        super(CartTree, self).__init__(max_depth, max_features, max_leaf_nodes, criterion, *args, **kwargs)
        self.is_classify = is_classify



    @count_time
    def fit(self, *args, **kwargs):
        super(CartTree, self).fit(*args, **kwargs)
        self.tree_dict = self.__recusive(self.X, self.y, self.attr_sets, self.root, self.max_depth)



    def calc_gini_index(self, y):
        gini = 1
        m = len(y)
        class_dict = self.class_count(y)
        for k, v in class_dict.items():
            p = v / m
            gini -= (p ** 2)
        return gini


    def __recusive(self, X, y, attr_sets, node, depth):
        if (self.max_leaf_nodes is not None and self.leaf_nums >= self.max_leaf_nodes) or (self.max_features is not None and self.features >= self.max_features) or (depth is not None and depth <= 1):
            node.label = self.majorityClass(y)
            node.leaf = True
            node.gini = self.calc_gini_index(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label

        if self.isSameClass(y):
            node.label = y[0]
            node.leaf = True
            node.gini = self.calc_gini_index(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label
        if len(attr_sets) == 0:
            node.label = self.majorityClass(y)
            node.leaf = True
            node.gini = self.calc_gini_index(y)
            node.sample_lists = X
            self.leaf_nums += 1
            return node.label

        self.features += 1
        split_feature_index, split_feature_val, c1, c2 = self.chooseBestFeaturToSplit(X, y, attr_sets)
        node.feature_index = split_feature_index
        node.feature_name = self.attr_sets[split_feature_index]
        node.gini = self.calc_gini_index(y)
        node.sample_lists = X


        my_dict = {node.feature_name: {}}

        if type(split_feature_val) == str:
            # discrete feature
            X_equal, X_unequal, y_equal, y_unequal = self.split_data(X, split_feature_index, split_feature_val, y)
            sub_X = [X_equal, X_unequal]
            sub_y = [y_equal, y_unequal]
            c = [c2, c1]
            for i in range(2):
                sub_node = TreeNode(parent_node=node, c_val=c[i])
                if i == 0:
                    val = split_feature_val
                else:
                    val = 'others'

                node.child_node_dict[val] = sub_node

                if len(sub_y[i]) == 0:
                    sub_node.label = self.majorityClass(y)
                    sub_node.leaf = True
                    sub_node.gini = self.calc_gini_index(sub_y[i])
                    sub_node.sample_lists = sub_X[i]
                    self.leaf_nums += 1
                    return sub_node.label
                else:
                    sub_attr_sets = attr_sets.copy()
                    sub_attr_sets.remove(self.attr_sets[split_feature_index])
                    if depth is None:
                        my_dict[node.feature_name][val] = self.__recusive(sub_X[i], sub_y[i], sub_attr_sets, sub_node, depth)
                    else:
                        my_dict[node.feature_name][val] = self.__recusive(sub_X[i], sub_y[i], sub_attr_sets, sub_node, depth - 1)
        else:
            # continuous feature
            X_pos, X_neg, y_pos, y_neg = self.split_data_by_T(X, split_feature_index, split_feature_val, y)
            sub_X = [X_neg, X_pos]
            sub_y = [y_neg, y_pos]
            c = [c1, c2]
            for i in range(2):
                sub_node = TreeNode(parent_node=node, c_val=c[i])
                if i == 0:
                    val = '<=' + str(split_feature_val)
                else:
                    val = '>' + str(split_feature_val)
                node.child_node_dict[val] = sub_node
                if len(sub_y[i]) == 0:
                    sub_node.label = self.majorityClass(y)
                    sub_node.leaf = True
                    sub_node.gini = self.calc_gini_index(sub_y[i])
                    sub_node.sample_lists = sub_X[i]
                    self.leaf_nums += 1
                    return sub_node.label
                else:
                    if depth is None:
                        my_dict[node.feature_name][val] = self.__recusive(sub_X[i], sub_y[i], attr_sets, sub_node, depth)
                    else:
                        my_dict[node.feature_name][val] = self.__recusive(sub_X[i], sub_y[i], attr_sets, sub_node, depth - 1)

        return my_dict



    def chooseBestFeaturToSplit(self, X, y, attr_sets):
        m = X.shape[0]
        best_split_val = math.inf
        best_feature_index = 0
        best_feature_val = None
        c1 = 0
        c2 = 0
        for attr in attr_sets:
            j = self.attr_sets.index(attr)
            if self.feature_mask is not None and j not in self.feature_mask:
                continue
            feature_list = [x[j] for x in X]
            if str(feature_list[0]).isalnum():
                # discrete feature
                unique_feature_val = set(feature_list)
                for feat in unique_feature_val:
                    X_equal, X_unequal, y_equal, y_unequal = self.split_data(X, j, feat, y)
                    if self.is_classify:
                        # classify tree
                        equal_prob = len(y_equal) / m
                        unequal_prob = len(y_unequal) / m
                        split_val = equal_prob * self.calc_gini_index(y_equal) + unequal_prob * self.calc_gini_index(y_unequal)
                    else:
                        # regression tree
                        c2 = np.mean(y_equal)
                        c1 = np.mean(y_unequal)
                        split_val = np.sum((y_equal - c1) ** 2 + (y_unequal - c2) ** 2)


                    if split_val <= best_split_val:
                        best_split_val = split_val
                        best_feature_index = j
                        best_feature_val = str(feat)
            else:
                # continuous feature
                feature_list = list(map(float, feature_list))
                sorted_feature_list = sorted(feature_list)
                for f in range(len(sorted_feature_list) - 1):
                    T = 0.5 * (sorted_feature_list[f] + sorted_feature_list[f + 1])
                    X_pos, X_neg, y_pos, y_neg = self.split_data_by_T(X, j, T, y)
                    if self.is_classify:
                        equal_prob = len(y_pos) / m
                        unequal_prob = len(y_neg) / m
                        split_val = equal_prob * self.calc_gini_index(y_pos) + unequal_prob * self.calc_gini_index(y_neg)
                    else:
                        if len(y_pos) == 0:
                            c1 = np.mean(y_neg)
                            c2 = 0
                            split_val = np.sum((y_neg - c1) ** 2)

                        elif len(y_neg) == 0:
                            c1 = 0
                            c2 = np.mean(y_pos)
                            split_val = np.sum((y_pos - c2) ** 2)
                        else:
                            c1 = np.mean(y_neg)
                            c2 = np.mean(y_pos)
                            split_val = np.sum((y_neg - c1) ** 2) + np.sum((y_pos - c2) ** 2)

                    if split_val <= best_split_val:
                        best_split_val = split_val
                        best_feature_index = j
                        best_feature_val = T

        return best_feature_index, best_feature_val, c1, c2


    def split_data(self, X, feature_index, split_val, y=None):
        equal_index = X[:, feature_index] == split_val
        unequal_index = X[:, feature_index] != split_val
        X_equal = X[equal_index]
        X_unequal = X[unequal_index]
        if y is not None:
            y_equal = y[equal_index]
            y_unequal = y[unequal_index]
            return X_equal, X_unequal, y_equal, y_unequal
        return X_equal, X_unequal


    def split_data_by_T(self, X, feature_index, T, y=None):
        pos_index = X[:, feature_index] > T
        neg_index = X[:, feature_index] <= T
        pos_X_sub = X[pos_index]
        neg_X_sub = X[neg_index]
        if y is not None:
            pos_y_sub = y[pos_index]
            neg_y_sub = y[neg_index]
            return pos_X_sub, neg_X_sub, pos_y_sub, neg_y_sub
        return pos_X_sub, neg_X_sub


    def predict(self, X, is_train=False, *args):
        X = np.asarray(X)
        if X.ndim > 1 and X.shape[0] > 1:
            pred = np.zeros((X.shape[0], 1))
            for i, x in enumerate(X):
                x = x[np.newaxis, ...]
                pred[i] = self.root.predict(self.root, x, self.is_classify)
            return pred
        return self.root.predict(self.root, X, self.is_classify)







def DecisionTreeClassifier(criterion='gini', max_depth=None, max_features=None, max_leaf_nodes=None,*args, **kwargs):
    criterion = criterion.lower()
    if criterion == 'entropy':
        return ID3Tree(max_depth=max_depth, max_features=max_features, max_leaf_nodes=max_leaf_nodes, criterion=criterion, *args, **kwargs)
    elif criterion == 'entropy_ratio':
        return C45Tree(max_depth=max_depth, max_features=max_features, max_leaf_nodes=max_leaf_nodes, criterion=criterion, *args, **kwargs)
    elif criterion == 'gini':
        return CartTree(max_depth=max_depth, max_features=max_features, max_leaf_nodes=max_leaf_nodes, criterion=criterion, *args, **kwargs)



def DecisionTreeRegressor(max_depth=None, max_features=None, max_leaf_nodes=None, *args, **kwargs):
    return CartTree(is_classify=False, max_depth=max_depth, max_features=max_features, max_leaf_nodes=max_leaf_nodes)

