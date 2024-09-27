import pandas as pd
import numpy as np

def data_profiling(df):
    analysis=[]
    for column in df.columns:
        row_count=len(df)
        missing_percentage=(df[column].isnull().sum()/row_count)*100
        column_count=df[column].count()
        unique_count=df[column].nunique()
        sample_value=df[column].unique()[:10]
        val_count=df[column].value_counts(dropna=False).head(5)
        val_str=', '.join(str(val) if val is not None else '' for val in sample_value)
        top_5_frequency='; '.join([f"'{value}':{count}" for value,count in zip(val_count.index,val_count.values)])
        res=pd.DataFrame({
            'Column Name': [column],
            'Data Type' : [df[column].dtype],
            'Row Count' : [row_count],
            'Missing (%)' : [round(missing_percentage,2)],
            'Unique Value Counts' : [unique_count],
            'Sample Values' : [val_str],
            'Top 5 Values' : [top_5_frequency]
        })
        analysis.append(res)
    return pd.concat(analysis,ignore_index=True)

df=pd.DataFrame({
    'col1': ['A', 'B', '', 'D', np.nan],
    'col2': [1, 2, 3, np.nan, 5],
    'col3': ['NA', '', 'E', np.nan, 'F']
}
)
an=data_profiling(df)
print(an.head())


