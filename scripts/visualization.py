import matplotlib.pyplot as plt 
import seaborn as sns 
from Scripts.App_log import logger
import pandas as pd
import numpy as np

class all_viz():
    def __init__(self):
        """
        -- initialize the class
        """
        pass

    def plot_hist(self,df:pd.DataFrame,column:str,color:str)->None:
        """
        -- plot distribution 
        """
        plt.figure(figsize=(10, 8))
        sns.displot(data=df, x=column, color=color, height=7, aspect=2)
        plt.title(f'Distribution of {column}', size=15, fontweight='bold')
        plt.show()
        logger.info("successfully plot distribution")

    def heatmap(self, df: pd.DataFrame, title: str) -> None:
        """
        --plot a heatmap
        """
        correlation = df.corr()
        matrix = np.triu(correlation)
        plt.figure(figsize=(20, 17))
        sns.heatmap(correlation, annot=True, linewidth=.8, mask=matrix, cmap="rocket")
        plt.title(title, size=18, fontweight='bold')
        plt.show()
        logger.info("successfully plot heatmap")

    def plot_bar(self, column, title, xlabel, ylabel):
         plt.figure(figsize=(7,5))
         sns.barplot(y=column.index, x=column.values) 
         plt.title(title, size=15, fontweight="bold")
         plt.xlabel(xlabel, size=10, fontweight="bold") 
         plt.ylabel(ylabel, size=10, fontweight="bold")
         plt.show() 
         logger.info("successfully plot bar plot")


    def multiple_boxplot(self, x, y, start: int = 0, num_features: int = 10):
        data = pd.concat([y, x.iloc[:, start:num_features]], axis=1)
        data = pd.melt(data,
                    id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
        plt.figure(figsize=(20, 12))
        sns.boxplot(x="features", y="value", hue="diagnosis", data=data)
        plt.xticks(rotation=90)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.show()
        logger.info("successfully plot boxplot")

    def plot_displot(self, df, x):    

        fig,ax = plt.subplots(nrows = 6, ncols = 5, figsize = (12,24),dpi=80)
        axes = ax.ravel()

        for col,ax in zip(x.columns,axes):
            # plots
            sns.kdeplot(df[col], ax = ax, shade = True ,
                        palette=["red", "green"],
                        alpha = 0.5, linewidth = 1, ec = 'black',
                        hue = df['diagnosis'], hue_order = ['M','B'],
                        legend = False)

            # plot setting
            xlabel = ' '.join([value.capitalize() for value in str(col).split('_') ])
            ax.axes.set_xlabel(xlabel,{'font':'serif','size':10, 'weight':'bold'}, alpha = 1)

        plt.tight_layout(pad= 2,h_pad = 1, w_pad = 1)

        fig.text(0.615,1, "\n       Benign",{'font':'serif','size':14, 'weight':'bold', 'color':"green"}, alpha = 1)
        fig.text(0.735,1, '|',{'font':'serif','size':16, 'weight':'bold'})
        fig.text(0.75,1, "  Malignant",{'font':'serif','size':14, 'weight':'bold','color':"red"}, alpha = 1)

        fig.show()

    def plot_pair(self, df: pd.DataFrame, title: str, hue: str) -> None:
        plt.figure(figsize=(10,8))
        sns.pairplot(df,
                     hue=hue,
                     diag_kind='kde',
                     plot_kws={'alpha': 0.6, 's': 80, 'edgecolor': 'k'},
                     height=4)
        plt.title(title, size=15)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.show()

    def fix_outlier(self):
        column_name=list(self.df.columns[2:])
        for i in column_name:
            upper_quartile=self.df[i].quantile(0.75)
            lower_quartile=self.df[i].quantile(0.25)
            self.df[i]=np.where(self.df[i]>upper_quartile,self.df[i].median(),np.where(self.df[i]<lower_quartile,self.df[i].median(),self.df[i]))
        return self.df 