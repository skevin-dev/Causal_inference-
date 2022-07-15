from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler
import pandas as pd
import numpy as np
from Scripts.App_log import logger
from collections import Counter


class all_clean():

    def __init__(self):

        """
        -- initialize the class
        """
        pass

    def read_csv(self,filepath):

        """
        -- load the dataset 
        """
        try: 
            df = pd.read_csv(filepath)
            logger.info("successfully load the dataset")
            return df 

        except FileNotFoundError:
            logger.exception("file not found")

            
    def get_numerica_columns(self,df: pd.DataFrame)-> list:
        """
        --get numerical columns
        """     
        num_cols = df.select_dtypes(include='number').colums.tolist()
        logger.info("Get numerical columns")
        return num_cols

    def get_categorical_columns(self,df: pd.DataFrame)-> list:
        """
        -- get categorical columns
        """
        cat_cols = df.select_dtypes(include='object').colums.tolist()
        logger.info('get categorical columns')
        return cat_cols
            
    def percent_missing(self,df):

        """
        -- print out the percentage of missing values in a dataframe
        """

        total_observations = np.product(df.shape)

        Missing_values = df.isna().sum()

        total_missing = Missing_values.sum()

        percentage = (total_missing / total_observations) * 100

        logger.info("successfully retrieve the percentage of missing values")

        return percentage 

    def remove_rows(self, df: pd.DataFrame, columns: str)-> pd.DataFrame:
        """
        -- remove rows with missing values 
        """
        for column in columns:
            df = df[~df[column].isna()]
        
        logger.info('successfully remove rows with null values')
        return df 

    def unique_values(self,df:pd.DataFrame)-> pd.DataFrame:
        logger.info('successfully retrieve unique values')
        return(df.nunique())

    
    def normalizer(self, df, columns):
            norm = Normalizer()
            logger.info("successfully normalize data")
            return pd.DataFrame(norm.fit_transform(df), columns=columns)
            


    def scaler(self, df, columns, mode="minmax"):
        if (mode == "minmax"):
            minmax_scaler = MinMaxScaler()
            logger.info("successfully scale data")

            return pd.DataFrame(minmax_scaler.fit_transform(df), columns=columns)

        elif (mode == "standard"):
            scaler = StandardScaler()
            logger.info("successfully scale data")

            return pd.DataFrame(scaler.fit_transform(df), columns=columns)

    def save_csv(self, df, csv_path, index=False):
        """
        -- save csv file
        """
        try:
            df.to_csv(csv_path, index=index)
            logger.info("file saved as csv")

        except Exception:
            logger.exception("save failed")

    def detect_outliers(self,df):
        """
        -- detecting outliers 
        """
        outlier_i = []
    
        for col in df.columns[2:]:
            # 1st quartile
            Q1 = np.percentile(df[col],25)
            # 3rd quartile
            Q3 = np.percentile(df[col],75)
            # IQR
            IQR = Q3 - Q1
            # Outlier step
            outlier_step = IQR * 1.5
            # detect outlier and their indeces
            outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step)].index
            # store indeces
            outlier_i.extend(outlier_list_col)
            
        
        outlier_i = Counter(outlier_i)
        
        multiple_outliers = []
        for i in outlier_i.items(): 
            if i[-1]>2:
                multiple_outliers.append(i[0])
        logger.info("successfully detect outliers")       
        return len(multiple_outliers)
        

    def drop_cols(self,df:pd.DataFrame,columns: str ) -> pd.DataFrame:
        df.drop(columns,axis=1,inplace=True)
        logger.info('drop columns')
    def duplicates(self,df):
        dup = df.duplicated().sum()
        logger.info('successfully retrieve duplicates')
        return dup 

    

    def handling_outliers(self, df:pd.DataFrame,columns:str) -> pd.DataFrame:
        """
        -- handling missing values 
        """
        for col in columns:
            Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            IQR = Q3 - Q1
            cut_off = IQR * 1.5
            lower, upper = Q1 - cut_off, Q3 + cut_off

            df[col] = np.where(df[col] > upper, upper, df[col])
            df[col] = np.where(df[col] < lower, lower, df[col])

            logger.info("successfully handle outliers")
