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
    
    files = glob.glob("datasets/*.csv")
    files_names = [i.split('/')[-1] for i in files]
    filename = st.selectbox('Plesae Enter File Name', files_names)
    
    if filename:
        df = pd.read_csv('datasets/' + filename)
        col1, col2 = st.beta_columns(2)
        with col2:
            cols = st.multiselect('Select Columns to view',df.columns.tolist(), default=df.columns.tolist()[:5])
        with col1:
            if st.checkbox('Select All Columns'):
                cols = df.columns
            n_rows = st.select_slider('Choose how many rows', [i for i in range(100)], value=5)     
        mylib.plot_table(df.head(n_rows), cols)
        st.write("## Let's Vizualize Columns!")
        col_to_viz = st.selectbox('Choose a Column to Vizualize', [None] + df.columns.tolist())
        if col_to_viz:
            viz_type = st.selectbox('Check Other Vizualizations Types', ['Pie Chart', 'Histogram'])
            mylib.plot(df, col_to_viz, viz_type)

        
        st.markdown("<hr/>",unsafe_allow_html=True)
        st.write("## Have Some Insights, by Grouping Sales Based on Columns!")
        col_to_groupby = st.selectbox('Choose a Column to Group-by', [None] + df.columns.tolist())
        num_features = df.select_dtypes(include=['float64', 'int64', 'int', 'float']).columns.tolist()

        group_on = st.selectbox('Choose A Column to Inspect', num_features)
        viz_type_g = st.selectbox('Try Other Vizualizations ?', ['Pie Chart', 'Histogram'])

        if col_to_groupby:
            grouped = mylib.group_by(df, col_to_groupby, target_col=group_on).sort_values(ascending=False)
            if len(grouped) > 10:
                n_cat = st.select_slider('Choose the number of categories to view', [i for i in range(0,len(grouped))], value=10)
                st.write(f'### Too many categories({len(grouped)}), so we picked the top {n_cat}')
                if viz_type_g == 'Pie Chart':
                    fig = go.Figure(data=[go.Pie(labels=grouped.index.tolist()[:n_cat], values=grouped.values[:n_cat])])
                elif viz_type_g == 'Histogram':
                    fig = go.Figure(data=[go.Bar(x=grouped.index.tolist()[:n_cat], y=grouped.values[:n_cat])])

            else:
                if viz_type_g == 'Histogram':
                    fig = go.Figure(data=[go.Bar(x=grouped.index.tolist(), y=grouped.values)])
                elif viz_type_g == 'Pie Chart':
                    fig = go.Figure(data=[go.Pie(labels=grouped.index.tolist(), values=grouped.values)])

            fig.update_xaxes(title='Sales per ' + col_to_groupby)
            st.plotly_chart(fig)
            st.write(f"### {grouped.index[0]} category has the lead over the other categories with a value of {mylib.curr(grouped.values[0])}")

elif choice == 'Dashboard':
    
    st.write('# BigMart Sales Analysis')
    df = pd.read_csv("datasets/Train.csv")    
    clean = st.sidebar.checkbox("Clean Dataset")
    st.sidebar.image('imgs/cleaning-tools.png', width=40)
    if clean:
        num_strategy = st.sidebar.selectbox("Choose A strategy to replace the numerical values, it's Median by default", ['median', 'mean'])
        str_strategy = st.sidebar.selectbox("Choose A strategy to replace the categorical values, it's the most frequent by default", ['most_frequent', 'constant'])
        fill_val = 'missing'
        if str_strategy == 'constant':
            fill_val = st.sidebar.text_input('Please Enter the prefered value', value="missing")
        st.sidebar.markdown("<hr/>",unsafe_allow_html=True)
    
        if st.sidebar.checkbox(" Remove Outliers as well "):
            df = mylib.remove_outliers(df)
        df = mylib.clean_dataset(df,num_strategy=num_strategy, cat_strategy =str_strategy, fill_val=fill_val)
    
    
    st.sidebar.markdown("<hr/>",unsafe_allow_html=True)
    st.sidebar.write("## Try different colors")
    box_color = st.sidebar.color_picker('boxes background color', value='#1a322d')
    num_color = st.sidebar.color_picker('numbers color', value = '#d8e131')

    st.write('## Have a look at the data!')
    st.write(df.head())
    st.write('## **Sales per Item Type**')
    kpi01, kpi02, kpi03, kpi04, kpi05 = st.beta_columns(5)

    grouped = mylib.group_by(df, 'Item_Type').sort_values(ascending=False)
    with kpi01:
        st.markdown(f"### {grouped.index[0]}")
        st.markdown(f"<h2 style='text-align: center;color: {num_color};background-color: {box_color}; width: fit-content; padding:20px'>{mylib.curr(grouped[0])}</h1>", unsafe_allow_html=True)

    with kpi02:
        st.markdown(f"### {grouped.index[1]}")
        st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content; padding:20px'>{mylib.curr(grouped[1])}</h1>", unsafe_allow_html=True)

    with kpi03:
        st.markdown(f"### {grouped.index[2]}")
        st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content; padding:20px'>{mylib.curr(grouped[2])}</h1>", unsafe_allow_html=True)

    with kpi04:
        st.markdown(f"### {grouped.index[3]}")
        st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content;padding:20px'>{mylib.curr(grouped[3])}</h1>", unsafe_allow_html=True)

    with kpi05:
        st.markdown(f"### {grouped.index[4]}")
        st.markdown(f"<h2 style='text-align: center; color: {num_color}; background-color: {box_color}; width: fit-content; padding:20px'>{mylib.curr(grouped[4])}</h1>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;' >Total</h1>", unsafe_allow_html=True)
    total_amt = df['Item_Outlet_Sales'].sum()
    st.markdown(f"<h1 style='text-align: center; color: {num_color}; background-color: {box_color};padding:20px'>{mylib.curr(total_amt)}</h1>", unsafe_allow_html=True)

    st.markdown("<hr/>",unsafe_allow_html=True)
    st.write(f"### {grouped.index[0]}, and {grouped.index[1]} has achieved the highest amount of sales between all categories with values of {mylib.curr(grouped[0])}, {mylib.curr(grouped[1])} respectively!")
    st.markdown("<hr/>",unsafe_allow_html=True)
    
    p1, p2 = st.beta_columns(2)
    with p1:
        st.markdown('### Sales per Outlet Location Type')
        mylib.plot(df, 'Outlet_Location_Type', 'Pie Chart')
    with p2:
        st.markdown('### Sales per Outlet Size')
        mylib.plot(df, 'Outlet_Size','Histogram')
    
    st.markdown("<hr/> <br>",unsafe_allow_html=True)
    st.write('## The Below Area chart shows the amount of sales in all BigMart stores over the years from 1985 till 2009 ')
    gg = df.groupby(['Outlet_Establishment_Year']).sum()['Item_Outlet_Sales']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=gg.index, y=gg.values, fill='tozeroy', line_color='indigo',))
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        width=1500
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write("## The above area chart shows that BigMart had a great start in 1985 with total sales of $3.63M, but they faced a major sitback in 1998 they only made $188 k, and it took them one year to recover in 1999 to reach $2.2M.")

elif choice == 'Machine Learning':
    st.write('# Welcome to the Prediction Area')
    st.markdown("<hr/> <br>",unsafe_allow_html=True)
    box_color = st.sidebar.color_picker('boxes background color', value='#1a322d')
    num_color = st.sidebar.color_picker('numbers color', value = '#d8e131')
    dst = pickle.load(open('models/dst.sav', 'rb'))
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
    total_amt_ceil = total_amt+207
    total_amt_ground = total_amt-207
    st.markdown(f"<h1 style='text-align: center; color: {num_color}; background-color: {box_color};padding:20px'>{mylib.curr(total_amt)}</h1>", unsafe_allow_html=True)
    st.markdown("<hr/> <br>",unsafe_allow_html=True)
    st.write('## Summary')
    st.markdown(f"## We are predicting a value of {mylib.curr(total_amt)}, for the following values: \n Item MRP: {item_mrp} <br> Outlet Type: {outlet_type} <br> Item Visibility: {item_v} <br> Item Weight: {Item_weight}  \nOutlet Establishment Year: {year}", unsafe_allow_html=True)
    st.write(f"### RMSE is $207, therefore the actual value should be somewhere between {mylib.curr(total_amt_ground)} and {mylib.curr(total_amt_ceil)} ")
elif choice == 'About':
    b1, b2 = st.beta_columns([5,1])
    with b1:
        st.write('# Ibrahim Al-Bahri')
        st.write('## Supervisor: Dr. Wissam Sammouri')
        st.write('## MSBA CLASS 2021')
        st.markdown("## <a style='text-align: center;' href='https://www.linkedin.com/in/ibrahim-al-bahri/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
    with b2:
        st.image('imgs/ms42.jfif', width=200)
    mylib.set_png_as_page_bg('imgs/osb.jpg')
