from ipywidgets.widgets.widget import _show_traceback
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import locale
import helper as mylib
import pickle
import  glob
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="Analytics Tool",
    layout="wide",
    initial_sidebar_state="expanded",
)


menu = ["About", "Dashboard","Machine Learning","Create Your Own Report"]
choice = st.sidebar.selectbox("Menu",menu)


if choice == 'Create Your Own Report':
    
    # files = glob.glob("datasets/*.csv")
    # st.write(files)
    filename = st.text_input('Plesae Enter File Name')
    
    if filename:
        df = pd.read_csv(r"{0}".format(filename)+".csv")
        col1, col2 = st.beta_columns(2)
        with col2:
            cols = st.multiselect('Select Columns to view',df.columns.tolist(), default=['Item_Type','Item_Outlet_Sales', 'Outlet_Size', 'Outlet_Type'])
        with col1:
            if st.checkbox('Select All Columns'):
                cols = df.columns
            n_rows = st.select_slider('Choose how many rows', [i for i in range(100)], value=5)     
        mylib.plot_table(df.head(n_rows), cols)
        st.write("Let's Vizualize it!")
        col_to_viz = st.selectbox('Choose a Column to Vizualize', [None] + df.columns.tolist())
        if col_to_viz:
            viz_type = st.selectbox('Check Other Vizualizations Types', ['Pie Chart', 'Histogram'])
            mylib.plot(df, col_to_viz, viz_type)

        st.write("Have Some Insights!")
        col_to_groupby = st.selectbox('Choose a Column to Group-by', [None] + df.columns.tolist())
        if col_to_groupby:
            grouped = mylib.group_by(df, col_to_groupby)
            st.write(grouped)
            fig = go.Figure(data=[go.Pie(labels=grouped.index.tolist(), values=grouped.values)])
            st.plotly_chart(fig)
    
elif choice == 'Dashboard':
    try:
        box_color = st.sidebar.color_picker('boxes background color', value='#1a322d')
    except:
        box_color = '#1a322d'
    try:
        num_color = st.sidebar.color_picker('numbers color', value = '#d8e131')
    except:
        num_color = '#d8e131'
    st.write('# Dashboard')
    filename = 'Train'
    if filename:
        df = pd.read_csv(r"{0}".format(filename)+".csv")    

        st.write(df.head())
        st.write('## **Sales per Item Type**')
        kpi01, kpi02, kpi03, kpi04, kpi05 = st.beta_columns(5)
    
        grouped = mylib.group_by(df, 'Item_Type').sort_values(ascending=False)
        with kpi01:
            st.markdown(f"### {grouped.index[0]}")
            st.markdown(f"<h2 style='text-align: center; color: {num_color};background-color: {box_color}; width: fit-content;padding:20px'>{mylib.curr(grouped[0])}</h1>", unsafe_allow_html=True)

        with kpi02:
            st.markdown(f"### {grouped.index[1]}")
            st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content;padding:20px'>{mylib.curr(grouped[1])}</h1>", unsafe_allow_html=True)

        with kpi03:
            st.markdown(f"### {grouped.index[2]}")
            st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content;padding:20px'>{mylib.curr(grouped[2])}</h1>", unsafe_allow_html=True)

        with kpi04:
            st.markdown(f"### {grouped.index[3]}")
            st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content;padding:20px'>{mylib.curr(grouped[3])}</h1>", unsafe_allow_html=True)

        with kpi05:
            st.markdown(f"### {grouped.index[4]}")
            st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content;padding:20px'>{mylib.curr(grouped[4])}</h1>", unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: center;' >Total</h1>", unsafe_allow_html=True)
        total_amt = df['Item_Outlet_Sales'].sum()
        st.markdown(f"<h1 style='text-align: center; color: {num_color}; background-color: {box_color};padding:20px'>{mylib.curr(total_amt)}</h1>", unsafe_allow_html=True)

        st.markdown("<hr/>",unsafe_allow_html=True)

        
        p1, p2 = st.beta_columns(2)
        with p1:
            st.markdown('### Sales per Outlet Location Type')
            mylib.plot(df, 'Outlet_Location_Type', 'Pie Chart')
        with p2:
            st.markdown('### Sales per Outlet Size')
            mylib.plot(df, 'Outlet_Size','Histogram')

elif choice == 'Machine Learning':
    box_color = st.sidebar.color_picker('boxes background color', value='#1a322d')
    num_color = st.sidebar.color_picker('numbers color', value = '#d8e131')
    dst = pickle.load(open('dst.sav', 'rb'))
    ss = [  'Item_MRP',
            'Outlet_Type_Grocery Store',
            'Item_Visibility',
            'Item_Weight',
            'Outlet_Establishment_Year'
            ]
    item_mrp = st.text_input('Please Enter Item MRP', value=0)
    outlet_type = st.radio('Please Select Outlet Type', ['Grocery Store', 'Other'])
    outlet_type_val = 1 if outlet_type == 'Grocery Store' else 0 
    item_v = st.text_input('Please Enter Item Visibility', value=0)
    Item_weight = st.text_input('Please Enter Item Weight', value=0)
    year = st.slider('Please Choose Outlet Establishment Year', 1980, 2020)
    scaled_year = (float(year) - 1997.831867)/8.371760
    st.markdown("<h1 style='text-align: center;' >Prediction Results</h1>", unsafe_allow_html=True)
    
    
    total_amt = dst.predict([[
        float(item_mrp),
         float(outlet_type_val),
          float(item_v), 
          float(Item_weight), 
          scaled_year]])[0]
          
    st.markdown(f"<h1 style='text-align: center; color: {num_color}; background-color: {box_color};padding:20px'>{mylib.curr(total_amt)}</h1>", unsafe_allow_html=True)
elif choice == 'About':
    b1, b2 = st.beta_columns(2)
    with b1:
        st.write('# Made by Ibrahim Al-Bahri')
        st.write('## Supervisor: Dr. Wissam Sammouri')
        st.write('## MSBA CLASS 2021')
        st.markdown("## <a style='text-align: center;' href='https://www.linkedin.com/in/ibrahim-al-bahri/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
    with b2:
        st.image('myphoto.jfif')
