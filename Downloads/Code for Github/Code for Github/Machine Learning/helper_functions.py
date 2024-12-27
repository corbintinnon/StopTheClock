import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

import sklearn
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

def setXY(df, df_ess, col = "KGR", classes=[], maxY = 0):
    Y = df_ess[col]
    #drop all potential Y
    if "FLR_growth_rate_week" in df:
        df = df.drop("FLR_growth_rate_week",axis=1)
    if "follow_up_TLV" in df:
        df = df.drop("follow_up_TLV",axis=1)
    if "KGR" in df:
        df = df.drop("KGR",axis=1)
    X = df
    #normalize X
    X = (X - X.mean(axis=0))/(X.max(axis=0) - X.min(axis=0)+1e-50)
    if col != "follow_up_TLV":
        Y = classifyY(Y, classes)
    else:
        #normalize Y
        Y = Y / maxY
    return X, Y

def classifyY(Y, classBounds):
    #classify Y into a certain class
    num_classes = np.size(classBounds)
    y_class = np.zeros((np.size(Y),num_classes+1))
    for i in range(np.size(Y)):
        for j in range(num_classes):
            if (Y[i] <= classBounds[j]):
                y_class[i,j] = 1
                break
        if (np.all(y_class[i] == 0)):
            y_class[i,num_classes] = 1
    return y_class

def splitXY(df_perc, df_ess, col = "KGR", classes = [], random=True, maxY = 0):
    #first normalize values
    x_vol, y_vol = setXY(df_perc, df_ess, col=col, classes = classes, maxY = maxY)
    ess = df_ess.to_numpy()
    #split into train and test
    if random:
        return train_test_split(x_vol, y_vol, test_size=0.30, random_state=None)
    else:
        return train_test_split(x_vol, y_vol, test_size=0.30, random_state=42)

def dropFutureValues(df):
    #only use baseline data for predictions
    q = df.columns.str.contains("post", case=False)
    df = df.drop(df.loc[:,q].columns, axis=1)
    
    q = df.columns.str.contains("follow_up", case=False)
    df = df.drop(df.loc[:,q].columns, axis=1)
    
    df = df.drop(['patient number'],axis=1)
    df = df.drop(['KGR'],axis=1)
    return df

def getCorrelatedInputs(df_X, df_ess, threshold, col = "FLR_growth_rate_week", verbose = 0, heatmap = False):
    #initialize variables
    if "patient number" in df_ess:
        df_ess = df_ess.drop(["patient number"], axis=1)
    df_new = pd.concat([df_X, df_ess], axis=1)
    corr_mat = df_new.astype('float64').corr()
    corr_mat = corr_mat[[col]]
    #to visualize correlation
    if heatmap:
        fig, ax = plt.subplots(figsize=(30, 15)) 
        sns.heatmap(corr_mat, vmax=1.0, square=False, ax=ax);
        
    #get inputs
    df_corr = pd.DataFrame()
    count=0
    numFeat = df_X.count(axis=1)[0]
    corrFeat = [""]*numFeat
    corrVal = [""]*numFeat
    for i in range(numFeat):
        if (abs(corr_mat.iloc[i].values[0]) >= threshold):
            df_corr = pd.concat([df_corr, df_X.iloc[::,i]],axis=1)
            corrFeat[count] = df_X.iloc[::,i].name
            corrVal[count] = corr_mat.iloc[i].values[0]
            count += 1
    #display to user
    print("Number of inputs (including 2Ys): ", np.shape(df_corr)[1])
    if (verbose == 1):
        display(df_corr.head())
    if (verbose == 2):
        display(df_corr.head())
        corrFeat = np.reshape(corrFeat,(numFeat,1))
        corrVal = np.reshape(corrVal,(numFeat,1))
        featVal = np.append(corrFeat,corrVal, axis=1)
        print("Correlation:")
        print(featVal[:count])
    if (verbose >= 3):
        display(df_corr)
    return df_corr

def exclude_correlated_features_trainingset(input_df, threshold =0.90):
    #exclude highly correlated features
    df = input_df.copy()
    
    cor_matrix = df.corr().abs()
    upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(np.bool_))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]
    
    new_df = df.drop(df[to_drop], axis=1)
    
    return new_df, to_drop

def drop_correlated_features_evaluation(input_df, to_drop):
    #drop columns that are given
    df = input_df.copy()
    new_df = df.drop(df[to_drop], axis=1)
    return new_df

def funcNNEpochs(fit, numEpochs, grow=False, save=False):
    #plot epochs for neural networks
    plt.plot(fit.history['loss'][0:numEpochs], c=[0,135/255,215/255])
    plt.plot(fit.history['val_loss'][0:numEpochs], c=[1,0,0])
    #plt.title('model loss')
    if grow:
        plt.ylabel('Root Mean Squared Error')
    else:
        plt.ylabel('Cross-Entropy Loss')
    plt.xlabel('Epochs')
    plt.legend(['Train', 'Test'], loc='upper right')
    if save: 
        if grow:
            plt.savefig("growthRateEpochs.png")
        else:
            plt.savefig("FLRvolEpochs.png")
    plt.show()
    
def funcGraphClasses(pred, y_test, save):
    #visualize accuracy of prediction
    colors = np.zeros((np.size(pred,axis=0),3))
    predI = np.argmax(pred,axis=1)
    for i in range(np.size(predI)):
        if (y_test[i,predI[i]]):
            colors[i] = [31/255,209/255,102/255]
        else:
            colors[i] = [1,0,0.2]
    plt.bar(list(range(len(y_test))),np.amax(pred,axis=1),color=colors)
    plt.ylim(top=1)
    plt.ylabel("Predicted highest percentage")
    plt.yticks([0,0.25,0.5,0.75,1])
    if save: 
        plt.savefig("FLRvolPred.png")
    plt.show()
    
def plotROC(fpr, tpr):
    #visualize FPR-TPR curve
    fpr_tpr = np.stack((fpr, tpr), axis=1)
    sort_F_T = fpr_tpr[fpr_tpr[:, 0].argsort()]

    plt.title('ROC-AUC curve')
    plt.scatter(sort_F_T[:,0], sort_F_T[:,1])
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([-0.01, 1])
    plt.ylim([0, 1.01])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    
def chart_regression(pred, y, maxY, save=False, name="error.png", sort=True):
    #visualize similarity btwn prediction and truth
    Xs = np.arange(1,np.size(y)+1)
    scaledY = y*maxY
    scaledPred = pred*maxY
    t = pd.DataFrame({'pred': scaledPred, 'y': scaledY})
    if sort:
        t.sort_values(by=['y'], inplace=True)
    colors = np.ones((np.size(y),1))*[0,135/255,215/255]
    colors2 = np.ones((np.size(y),1))*[1,0,0]
    plt.scatter(Xs, t['y'].tolist(), 20, label='Expected', c=colors)
    plt.scatter(Xs, t['pred'].tolist(), 20, label='Prediction', c=colors2)
    plt.ylabel('FLR Growth Rate per Week')
    plt.legend(loc='upper left')
    if save: 
        plt.savefig(name)
    plt.show()