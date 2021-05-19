import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

def get_vals(dic,keys):
    values = []
    for i in keys:
        values.append(dic[i])
    return values

def plot(df,col, v_type):
    if v_type:
        keys = df[col].unique()
        vals = df[col].value_counts()
        num_of_keys = len(df[col].unique()) 
        if num_of_keys > 10:
            top_n = st.select_slider('Choose How Many Categories to View',[i for i in range(0,num_of_keys)], value=10)
            st.write(f'Column Contains too many keys ({num_of_keys}), So We Picked the Top {top_n} Categories in this Column')
            dic = dict(zip(df[col].unique(),df[col].value_counts()))
            sorted_keys = sorted(dic, key=dic.get)
            sorted_keys.reverse()
            keys = sorted_keys[:top_n] 
            vals = get_vals(dic, sorted_keys[:top_n])
    
        if v_type == 'Pie Chart':
            fig = go.Figure(data=[go.Pie(labels=keys, values=vals)])
        elif v_type =='Histogram':
            fig = go.Figure(data=[go.Bar(x=keys, y=vals)])

        fig.update_xaxes(title=col)
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"### {keys[0]} category has the conquared the other categories with a value of {vals[0]}")

def group_by(df, group_on, target_col='Item_Outlet_Sales'):
    grouped = df.groupby([group_on]).sum()[target_col]
    return grouped

def plot_table(df, cols):
    """
    documentaion
    """
    fig = go.Figure(data=[go.Table(
        header=dict(values=cols,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in cols],
                fill_color='lavender',
                align='left'))
    ])
    st.plotly_chart(fig, use_container_width=True)

def curr(n):
   return "${:,.2f}". format(n)

def clean_dataset(df, num_strategy='median', cat_strategy='most_frequent'):
    
    report_before = pd.DataFrame(np.sum(df.isnull())).T
    
    cat_features = df.select_dtypes(include=['object']).columns.tolist()
    num_features = df.select_dtypes(include=['float64', 'int64', 'int', 'float']).columns.tolist()
    
    num_imputer = SimpleImputer(missing_values=np.nan, strategy=num_strategy)
    num_fitted = num_imputer.fit_transform(df[num_features])
    num_df = pd.DataFrame(num_fitted, columns = num_features)
    
    cat_imputer = SimpleImputer(missing_values=np.nan, strategy=cat_strategy)
    cat_fitted = cat_imputer.fit_transform(df[cat_features])
    cat_df = pd.DataFrame(cat_fitted, columns = cat_features)
    
    smaller = cat_df if cat_df.shape[0] <= num_df.shape[0] else num_df
    larger = cat_df if cat_df.shape[0] > num_df.shape[0] else num_df
    for col in smaller.columns:
        larger[col] = smaller[col]
    
    report_after = pd.DataFrame(np.sum(larger.isnull())).T
    return larger

def remove_outliers(df):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    return df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]

import base64

# @st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

