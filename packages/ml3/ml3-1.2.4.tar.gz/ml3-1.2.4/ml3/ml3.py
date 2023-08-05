#Xdua Machine Learning 3 SDK

import datetime
import hashlib
import math

import matplotlib.dates as mdate
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr
from sklearn import metrics
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.mixture import GaussianMixture
from tqdm import *


class ml3:
    def __init__(self):
        pass 

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是TechYoung课程的机器学习辅助工具包")
        return True


class plot:
    def __init__(self):
        pass 

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是地球号旗下数据分析绘图包")
        return True

    """
    data必须是dataframe,column_name是特征名字
    """
    def histplot(data, column_name, **kwargs):
        try:
            skew = data[column_name].skew()
            kurt = data[column_name].kurt()
            X = np.array(data[column_name])
            X_min = min(X)
            X_max = max(X)
            X_range = X_max - X_min
            X_min = int(kwargs['xmin']) if 'xmin' in kwargs else min(X) - X_range *0.05
            X_max = int(kwargs['xmax']) if 'xmax' in kwargs else max(X) + X_range *0.05
            column_bins = np.arange(np.min(X), np.max(X), 0.1)
            column_mean = np.mean(X)
            column_std = np.std(X)
            plt.figure(figsize=(16, 8), dpi=100)
            plt.xlim(X_min, X_max)
            sns.distplot(X, kde=True, norm_hist=True, bins=column_bins, color="black")
            plt.title(column_name + " mean=%.1f std=%.1f skew=%.2f kurt=%.2f"
                      % (float(column_mean), float(column_std), skew, kurt))
            plt.axvline(x=column_mean, color="r", linewidth=5)
            plt.axvline(x=column_mean - column_std, color="r", linewidth=2)
            plt.axvline(x=column_mean + column_std, color="r", linewidth=2)
            plt.axvline(x=column_mean - 2*column_std, color="r", linewidth=1)
            plt.axvline(x=column_mean + 2*column_std, color="r", linewidth=1)
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True
        
        except Exception as err:
            print("An error occured!")
            print(err)
            return False
        
    def normal_distribution(mean, sigma):
        x = np.linspace(mean - 6*sigma, mean + 6*sigma, 100)
        return x, np.exp(-1*((x-mean)**2)/(2*(sigma**2)))/(math.sqrt(2*np.pi) * sigma)
    
    def gmmplot(data, column_names, k_range, **kwargs):
        try:
            if len(k_range) != 2:
                err = "n_range error."
                raise Exception(err)

            perplexity = int(kwargs['perplexity']) if 'perplexity' in kwargs else 30
            X = np.array(data[column_names])
            fname = []
            score_silhouette_list = []
            score_calinski_list = []
            for N_COMPONENTS in tqdm(range(k_range[0], k_range[1])):
                if len(column_names) == 1:
                    X_min = min(X)
                    X_max = max(X)
                    X_range = X_max - X_min
                    X_min = int(kwargs['xmin']) if 'xmin' in kwargs else min(X) - X_range * 0.05
                    X_max = int(kwargs['xmax']) if 'xmax' in kwargs else max(X) + X_range * 0.05
                    feature_bins = np.arange(np.min(X), np.max(X), 0.1)

                    X_array = X.reshape(len(X), 1)
                    gmm = GaussianMixture(n_components=N_COMPONENTS).fit(X_array)
                    #print(gmm.get_params(True))
                    #打印5个分布的权重
                    #print(gmm.weights_)
                    #打印5个分布的期望
                    #print(gmm.means_)
                    #打印5各分布的协方差,因为高斯混合模型是面向多维的，所以
                    #print(gmm.covariances_)
                    labels = gmm.predict(X_array)
                    score_silhouette = metrics.silhouette_score(X_array, labels)
                    score_calinski = metrics.calinski_harabasz_score(X_array, labels)
                    score_silhouette_list.append(score_silhouette)
                    score_calinski_list.append(score_calinski)
                    plt.figure(figsize=(16, 8), dpi=100)
                    plt.xlim(X_min, X_max)
                    plt.title("GMM: K=%d score_silhouette=%.3f Tsen_perplexity=%d" %
                              (N_COMPONENTS, score_silhouette, perplexity))
                    for k in range(N_COMPONENTS):
                        datask = []
                        for i in range(len(labels)):
                            if labels[i] == k:
                                datask.append(X[i])
                        weight = gmm.weights_[k]
                        mean = gmm.means_[k][0]
                        std = math.sqrt(gmm.covariances_[k][0][0])
                        label_str = "mean=%.2f std=%.2f weight=%.2f" % (mean, std, weight)
                        sns.distplot(datask, bins=feature_bins, norm_hist=True, kde=True, kde_kws={"label": label_str})
                        x, y = plot.normal_distribution(mean, std)
                        plt.plot(x, y, color="black")
                    datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                    file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                    file_name = file_name + ".png"
                    fname.append([file_name, N_COMPONENTS])
                    plt.savefig(file_name, dpi=100)

                elif len(column_names) >= 2:
                    gmm = GaussianMixture(n_components=N_COMPONENTS).fit(X)
                    labels = gmm.predict(X)
                    score_silhouette = metrics.silhouette_score(X, labels)
                    score_calinski = metrics.calinski_harabasz_score(X, labels)
                    score_silhouette_list.append(score_silhouette)
                    score_calinski_list.append(score_calinski)
                    plt.figure(figsize=(16, 8), dpi=100)
                    plt.title("GMM: K=%d score_silhouette=%.3f" % (N_COMPONENTS, score_silhouette))
                    X_tsen = X
                    if len(column_names) > 2:
                        tsne = TSNE(n_components=2, learning_rate=500, perplexity=perplexity)
                        tsne.fit_transform(X)
                        X_tsen = tsne.fit_transform(X)
                        plt.title("GMM: K=%d score_silhouette=%.3f" % (N_COMPONENTS, score_silhouette))
                    for k in range(N_COMPONENTS):
                        datask = []
                        for i in range(len(labels)):
                            if labels[i] == k:
                                datask.append(X_tsen[i])
                        weight = gmm.weights_[k]
                        label_str = "weight=%.2f" % weight
                        datask = np.array(datask)
                        sns.scatterplot(datask[:, 0], datask[:, 1], markers=".", alpha=0.7, label=label_str)
                    datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                    file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                    file_name = file_name + ".png"
                    fname.append([file_name, N_COMPONENTS])
                    plt.savefig(file_name, dpi=100)

            for row in fname:
                print("K=%d\n%s" % (row[1], row[0]))

            plt.figure(figsize=(16, 8), dpi=100)
            plt.title("GMM silhouette & calinski_harabasz")
            score_silhouette = np.array(score_silhouette_list)
            score_silhouette_max = np.max(score_silhouette)
            score_calinski = np.array(score_calinski_list)
            score_calinski_max = np.max(score_calinski)
            p1, = plt.plot(range(k_range[0], k_range[1]), score_silhouette / score_silhouette_max, marker='o')
            p2, = plt.plot(range(k_range[0], k_range[1]), score_calinski / score_calinski_max, marker='o')
            plt.legend([p1, p2], ["score_silhouette MAX=%.2f" % score_silhouette_max,
                                  "score_calinski MAX=%.2f" % score_calinski_max], loc='upper left')
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print("GMM score")
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True

        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def kmeansplot(data, column_names, k_range, **kwargs):
        try:
            perplexity = int(kwargs['perplexity']) if 'perplexity' in kwargs else 30
            X = np.array(data[column_names])
            iteration_info = []
            score_silhouette_list = []
            score_calinski_list = []
            inertia_list = []
            for N_CLUSTERS in tqdm(range(k_range[0], k_range[1])):
                if len(column_names) == 1:
                    X_min = min(X)
                    X_max = max(X)
                    X_range = X_max - X_min
                    X_min = int(kwargs['xmin']) if 'xmin' in kwargs else min(X) - X_range * 0.05
                    X_max = int(kwargs['xmax']) if 'xmax' in kwargs else max(X) + X_range * 0.05
                    feature_bins = np.arange(np.min(X), np.max(X), 0.1)

                    X_array = X.reshape(len(X), 1)

                    #调用kmeans类
                    clf = KMeans(n_clusters=N_CLUSTERS)
                    s = clf.fit(X_array)
                    #9个中心
                    #print(clf.cluster_centers_)
                    #每个样本所属的簇
                    #print(clf.labels_)
                    #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
                    #print(clf.inertia_)
                    #进行预测
                    labels = s.labels_
                    #保存模型
                    #joblib.dump(clf , 'km.pkl')
                    #载入保存的模型
                    #clf = joblib.load('km.pkl')
                    #print(gmm.get_params(True))
                    score_silhouette = metrics.silhouette_score(X_array, labels)
                    score_calinski = metrics.calinski_harabasz_score(X_array, labels)
                    score_silhouette_list.append(score_silhouette)
                    score_calinski_list.append(score_calinski)
                    inertia_list.append(s.inertia_)
                    plt.figure(figsize=(16, 8), dpi=100)
                    plt.xlim(X_min, X_max)
                    plt.title("Kmeans: K=%d score_silhouette=%.3f inertia=%.3f" %
                              (N_CLUSTERS, score_silhouette, s.inertia_))
                    for k in range(N_CLUSTERS):
                        datask = []
                        for i in range(len(labels)):
                            if labels[i] == k:
                                datask.append(X[i])
                        datask_np = np.array(datask)
                        cluster_mean = np.mean(datask_np)
                        cluster_std = np.std(datask_np)
                        center = s.cluster_centers_[k][0]
                        label_str = "mean=%.2f std=%.2f center=%.2f" %\
                                    (float(cluster_mean), float(cluster_std), center)
                        sns.distplot(datask, bins=feature_bins, norm_hist=True, kde=True, kde_kws={"label": label_str})
                        x, y = plot.normal_distribution(cluster_mean, cluster_std)
                        plt.plot(x, y, color="black")
                    datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                    file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                    file_name = file_name + ".png"
                    iteration_info.append([file_name, N_CLUSTERS, s.cluster_centers_])
                    plt.savefig(file_name, dpi=100)

                elif len(column_names) >= 2:
                    clf = KMeans(n_clusters=N_CLUSTERS)
                    s = clf.fit(X)
                    labels = s.labels_
                    score_silhouette = metrics.silhouette_score(X, labels)
                    score_calinski = metrics.calinski_harabasz_score(X, labels)
                    score_silhouette_list.append(score_silhouette)
                    score_calinski_list.append(score_calinski)
                    inertia_list.append(s.inertia_)
                    plt.figure(figsize=(16, 8), dpi=100)
                    plt.title("Kmeans: K=%d score_silhouette=%.3f inertia=%.3f" %
                              (N_CLUSTERS, score_silhouette, s.inertia_))
                    X_tsen = X
                    if len(column_names) > 2:
                        tsne = TSNE(n_components=2, learning_rate=500, perplexity=perplexity)
                        tsne.fit_transform(X)
                        X_tsen = tsne.fit_transform(X)
                        plt.title("Kmeans: K=%d score_silhouette=%.3f inertia=%.3f Tsen_perplexity=%d" %
                                  (N_CLUSTERS, score_silhouette, s.inertia_, perplexity))

                    for k in range(N_CLUSTERS):
                        datask = []
                        for i in range(len(labels)):
                            if labels[i] == k:
                                datask.append(X_tsen[i])
                        datask = np.array(datask)
                        sns.scatterplot(datask[:, 0], datask[:, 1], markers=".", alpha=0.7)
                    datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                    file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                    file_name = file_name + ".png"
                    iteration_info.append([file_name, N_CLUSTERS, s.cluster_centers_])
                    plt.savefig(file_name, dpi=100)

            for row in iteration_info:
                print("K=%d\n%s" % (row[1], row[0]))
                print(row[2])

            plt.figure(figsize=(16, 8), dpi=100)
            plt.title("GMM silhouette & calinski_harabasz & inertia")
            score_silhouette = np.array(score_silhouette_list)
            score_silhouette_max = np.max(score_silhouette)
            score_calinski = np.array(score_calinski_list)
            score_calinski_max = np.max(score_calinski)
            inertia = np.array(inertia_list)
            inertia_max = np.max(inertia)
            p1, = plt.plot(range(k_range[0], k_range[1]), score_silhouette / score_silhouette_max, marker='o')
            p2, = plt.plot(range(k_range[0], k_range[1]), score_calinski / score_calinski_max, marker='o')
            p3, = plt.plot(range(k_range[0], k_range[1]), inertia / inertia_max, marker='o')
            plt.legend([p1, p2, p3], ["score_silhouette MAX=%.2f" % score_silhouette_max,
                                      "score_calinski MAX=%.2f" % score_calinski_max,
                                      "inertia MAX=%.2f" % inertia_max], loc='upper left')
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print("Kmeans score")
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True

        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def metricplot(n_clusters_range, scores, scores2=[], **kwargs):
        try:
            X_LABEL = str(kwargs['x_label']) if 'x_label' in kwargs else "Number of clusters"
            Y_LABEL = str(kwargs['y_label']) if 'y_label' in kwargs else "Silhouette Score"
        
            range_space = n_clusters_range[1] - n_clusters_range[0]

            if not scores2:
                if range_space != len(scores):
                    err = "The length of scores %d doesn't match the n_clusters_range %d." % (len(scores), range_space)
                    raise Exception(err)

                plt.figure(figsize=(16, 8), dpi=100)

                plt.plot(range(n_clusters_range[0], n_clusters_range[1]), scores, marker='o')
                plt.xlabel(X_LABEL, fontsize=20)
                plt.ylabel(Y_LABEL, fontsize=20)
                plt.xticks(fontsize=14)
                plt.yticks(fontsize=14)

                datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                file_name = file_name + ".png"
                print(file_name)
                plt.savefig(file_name, dpi=100)
                return True

            else:
                if range_space != len(scores) != len(scores2):
                    err = "The length of scores %d, score2 %d doesn't match the n_clusters_range %d." % \
                          (len(scores), len(scores2), range_space)
                    raise Exception(err)

                plt.figure(figsize=(16, 8), dpi=100)
                ax1 = plt.subplot()
                plt.xlabel(X_LABEL, fontsize=20)
                plt.ylabel(Y_LABEL, fontsize=20)
                plt.xticks(fontsize=14)
                plt.yticks(fontsize=14)
                ax2 = ax1.twinx()
                plt.yticks(fontsize=14)
                p1, = ax1.plot(range(n_clusters_range[0], n_clusters_range[1]), scores, marker='o')
                p2, = ax2.plot(range(n_clusters_range[0], n_clusters_range[1]), scores2, marker='o', color="darkred")
                plt.legend([p1, p2], ["Left y", "Right y"], loc='upper left')

                datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                file_name = file_name + ".png"
                print(file_name)
                plt.savefig(file_name, dpi=100)
                return True
            
        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def do_errorbar_1d(x, y, yerr, kwargs):
        X_LABEL = str(kwargs['x_label']) if 'x_label' in kwargs else "time"
        Y_LABEL = str(kwargs['y_label']) if 'y_label' in kwargs else "value"
        TITLE = str(kwargs['title']) if 'title' in kwargs else "Errorbar plot"

        timeList = []
        for i in x:
            timeList.append(datetime.datetime.fromtimestamp(i))

        plt.figure(figsize=(24, 12), dpi=100)

        ax = plt.subplot()
        ax.errorbar(x=timeList, y=y, yerr=yerr, elinewidth=0.2, fmt=".", capsize=0.4)
        plt.title(TITLE, fontsize=20)
        plt.xlabel(X_LABEL, fontsize=20)
        plt.ylabel(Y_LABEL, fontsize=20)

        ax.xaxis.set_major_locator(ticker.MaxNLocator(15))
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
        plt.xticks(rotation=45, fontsize=14)
        plt.yticks(fontsize=14)

        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
        file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
        file_name = file_name + ".png"
        print(file_name)
        plt.savefig(file_name, dpi=100)
        return True

    def do_errorbar_2d(x, y, yerr, y2, y2err, kwargs):
        X_LABEL = str(kwargs['x_label']) if 'x_label' in kwargs else "time"
        Y_LABEL = str(kwargs['y_label']) if 'y_label' in kwargs else "value"
        TITLE = str(kwargs['title']) if 'title' in kwargs else "Errorbar plot"

        timeList = []
        for i in x:
            timeList.append(datetime.datetime.fromtimestamp(i))

        plt.figure(figsize=(24, 12), dpi=100)
        ax1 = plt.subplot()
        plt.title(TITLE, fontsize=20)
        plt.xlabel(X_LABEL, fontsize=20)
        plt.ylabel(Y_LABEL, fontsize=20)
        plt.xticks(rotation=45, fontsize=14)
        plt.yticks(fontsize=14)
        ax2 = ax1.twinx()
        plt.yticks(fontsize=14)
        p1 = ax1.errorbar(x=timeList, y=y, yerr=yerr, elinewidth=0.2, fmt=".", capsize=0.4, color="blue")
        p2 = ax2.errorbar(x=timeList, y=y2, yerr=y2err, elinewidth=0.2, fmt=".", capsize=0.4, color="red")
        plt.legend([p1, p2], ["Left y", "Right y"], loc='upper left')

        ax1.xaxis.set_major_locator(ticker.MaxNLocator(15))
        ax1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))

        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
        file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
        file_name = file_name + ".png"
        print(file_name)
        plt.savefig(file_name, dpi=100)
        return True

    def errorbarplot(data, x, y=[], y2=[], **kwargs):
        try:
            pd.plotting.register_matplotlib_converters()
            LIMIT = str(kwargs['limit']) if 'limit' in kwargs else "500"
            LIMIT = int(LIMIT)

            if not y:
                err = "y or y2 format error. y and y2 should be [str, str]."
                raise err
            if len(data[y[0]]) > LIMIT:
                data = data.iloc[0:LIMIT]

            if y and not y2:
                return plot.do_errorbar_1d(data[x], data[y[0]], data[y[1]], kwargs)
            elif y and y2:
                return plot.do_errorbar_2d(data[x], data[y[0]], data[y[1]], data[y2[0]], data[y2[1]], kwargs)
            else:
                err = "y or y2 format error. y and y2 should be [str, str]."
                raise err
        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def pcaplot(data, column_names, **kwargs):
        try:
            n_components = str(kwargs['n_components']) if 'n_components' in kwargs else 2
            TITLE = str(kwargs['title']) if 'title' in kwargs else "PCA plot %d" % n_components

            data = np.array(data[column_names])
            dataScale = preprocessing.StandardScaler().fit_transform(data)
            pca = PCA(n_components=n_components)
            pca.fit(dataScale)
            newData = data.dot(pca.components_.T)

            print("主成分方差占比：")
            print(pca.explained_variance_ratio_)
            print("主成分方差总和：")
            print(np.sum(pca.explained_variance_ratio_))

            if n_components == 2:
                g = sns.jointplot(x=newData[:, 0], y=newData[:, 1], marker=".", kind='reg')
                g.annotate(pearsonr)
                # plt.title(TITLE, fontsize=20)
                datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                file_name = file_name + ".png"
                print(file_name)
                plt.savefig(file_name, dpi=100)

            else:
                sns.pairplot(pd.DataFrame(newData), markers=".", kind='reg', diag_kind="kde", height=4)
                # plt.title(TITLE, fontsize=20)
                datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
                file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
                file_name = file_name + ".png"
                print(file_name)
                plt.savefig(file_name, dpi=100)
            return True
        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def tsenplot(data, column_names, **kwargs):
        try:
            n_components = str(kwargs['n_components']) if 'n_components' in kwargs else 2

            data = np.array(data[column_names])
            dataScaled = preprocessing.scale(data)
            plt.figure(figsize=(16, 16), dpi=100)
            for i in tqdm(range(16)):
                perplexity = (i * 5) + 10
                plt.subplot(4, 4, i+1)
                tsne = TSNE(n_components=2, learning_rate=500, perplexity=perplexity)
                tsne.fit_transform(dataScaled)
                info_tsne = tsne.fit_transform(dataScaled)
                plt.scatter(info_tsne[:, 0], info_tsne[:, 1], marker=".", alpha=1)
                plt.title('tsne perplexity=%d' % perplexity)
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True
        except Exception as err:
            print("An error occured!")
            print(err)
            return False


class seaborn:
    def __init__(self):
        pass 

    #LOG,INFO,WARN,ERROR,
    def intro():
        print("这是TechYoung课程的机器学习辅助工具包")
        return True

    def boxplot(x, y, **kwargs):
        try:
            X_LABEL = str(kwargs['x_label']) if 'x_label' in kwargs else "time"
            Y_LABEL = str(kwargs['y_label']) if 'y_label' in kwargs else "value"
            TITLE = str(kwargs['title']) if 'title' in kwargs else "Boxplot"

            plt.figure(figsize=(24, 12), dpi=100)
            ax = plt.subplot()

            sns.boxplot(x=x, y=y, width=0.5, linewidth=0.2, fliersize=0.5, ax=ax)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
            #ax.xaxis.set_major_locator(ticker.LinearLocator(10))
            #ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
            plt.title(TITLE, fontsize=20)
            plt.xlabel(X_LABEL, fontsize=20)
            plt.ylabel(Y_LABEL, fontsize=20)
            plt.xticks(rotation=45, fontsize=14)
            plt.yticks(fontsize=14)

            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True
        except Exception as err:
            print("An error occured!")
            print(err)
            return False

    def violinplot(x, y, **kwargs):
        try:
            X_LABEL = str(kwargs['x_label']) if 'x_label' in kwargs else "time"
            Y_LABEL = str(kwargs['y_label']) if 'y_label' in kwargs else "value"
            TITLE = str(kwargs['title']) if 'title' in kwargs else "Violinplot"

            plt.figure(figsize=(24, 12), dpi=100)
            ax = plt.subplot()
            sns.violinplot(x=x, y=y, width=5, linewidth=0.1, ax=ax)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
            plt.title(TITLE, fontsize=20)
            plt.xlabel(X_LABEL, fontsize=20)
            plt.ylabel(Y_LABEL, fontsize=20)
            plt.xticks(rotation=45, fontsize=14)
            plt.yticks(fontsize=14)

            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%f')
            file_name = hashlib.md5(datetime_str.encode(encoding='UTF-8')).hexdigest()
            file_name = file_name + ".png"
            print(file_name)
            plt.savefig(file_name, dpi=100)
            return True
        except Exception as err:
            print("An error occured!")
            print(err)
            return False


def main():
    ml3.intro()


if __name__ == '__main__':
     main()

