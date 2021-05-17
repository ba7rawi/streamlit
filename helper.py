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
        st.plotly_chart(fig)
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
    st.plotly_chart(fig)

def curr(n):
   return "${:,.2f}". format(n)