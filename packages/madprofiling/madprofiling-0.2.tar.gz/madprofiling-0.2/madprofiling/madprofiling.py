class madprofiling(df):
    
    def madunique(df):
        names=list(df.columns)
        unique=[]
        for var_i in names:
            unique.append(len(df[var_i].unique()))
        df_unique=pd.DataFrame(unique,index=list(df.columns))
        df_unique.columns=['unique']
        return df_unique

    def madprofiling_sub(df):
        profiling=pd.DataFrame(df.dtypes)
        profiling.columns=['type']
        profiling.loc[profiling.type=='object', 'categorical'] = 1  
        profiling.loc[profiling.type!='object', 'categorical'] = 0
        profiling['total']=(len(df))
        profiling=pd.concat([profiling,madunique(df)],axis=1,sort=False)
        profiling['null']=pd.DataFrame(df.isnull().sum())
        profiling['na']=pd.DataFrame(df.isna().sum())
        profiling['null_pcnt']=round(profiling.null/profiling.total,1)
        profiling['na_pcnt']=round(profiling.na/profiling.total,1)
        profiling=profiling.sort_values(by='null_pcnt')
        return profiling