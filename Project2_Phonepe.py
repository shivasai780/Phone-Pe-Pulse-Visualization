import pandas as pd
import json
import os
from pprint import pprint
import plotly.express as px
import plotly.graph_objects as go
import re
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards


mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               password='12345678'
                              )
mycursor = mydb.cursor()
sql = "Use Project2_Phonepe"
mycursor.execute(sql)

# A csv file with states name in standard form
statesdf = pd.read_csv(r"C:\Users\HP\GUVI\GUVI_Course_New_Batch\Captsone\PhonePe_Pulse_Data_Viz\statesdf.csv")


# Function to convert states to code from
def state_change(state):
    if state =="Andaman & Nicobar":
        state_changed = "andaman-&-nicobar-islands"
    elif state =='Dadra and Nagar Haveli and Daman and Diu':
        state_changed = "dadra-&-nagar-haveli-&-daman-&-diu"
    else:
        state = state.lower()
        state_changed = re.sub(r'\s+','-',state)
    return state_changed



st.set_page_config(
    page_title="PhonePe Pulse Data Visualisation by Devadath",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This app was developed by Devadath G Nair!"
    }
)

with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard", 'About'], icons=['bi bi-bar-chart-fill', 'bi bi-info-circle-fill'], menu_icon="cast", default_index=0)
    
if selected == "Dashboard":
    st.title('PhonePe Pulse Data Visualisation')
    st.text('By Devadath G Nair')

    # SECTION 1
    # 3 Top Widegets

    col10,col11,col12 = st.columns(3)
    #Most Users
    sql="select sum(registered_users),state from map_user group by state order by sum(registered_users) desc limit 1;"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    state = data[0][1]
    state = state.title().replace('-', ' ')
    users = str(int(data[0][0]))
    col10.metric("Most Users",value=state,delta=users+' Users')
    #st.subheader('Most Users')
    #st.title(state)

    #Most Transactions
    sql="select state,sum(transaction_count) from map_transaction group by state order by sum(transaction_count) desc limit 1;"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    state_tc = data[0][0]
    state_tc = state_tc.title().replace('-', ' ')
    tra_cnt = str(int(data[0][1]))
    col11.metric('Most Transactions',value=state_tc,delta=tra_cnt+' Transactions')
    #st.subheader('Most Transactions')
    #st.title(state_tc)

    #Highest Transaction Amounts
    sql="select state,sum(transaction_amount) from map_transaction group by state order by sum(transaction_amount) desc limit 1;"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    state_tr = data[0][0]
    state_tr = state_tr.title().replace('-', ' ')
    tra_amt = str(data[0][1])
    col12.metric('Highest Transaction Amounts',value=state_tr,delta='₹'+tra_amt)
    #st.subheader('Highest Transaction Amounts')
    #st.title(state_tr)
    style_metric_cards(background_color='#4C2881', border_color="#4C2881", border_left_color="#3a1d66")
    st.divider()


    # SECTION 2
    # Live Geo locations
    # Columns for input dropdown
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        type = st.selectbox(
            'Transactions or Users',
            ('Transactions', 'Users'))
        
    with col2:
        state = st.selectbox(
            'State',
            ('All','Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand',
        'Uttar Pradesh', 'West Bengal'))

    with col3:
        year = st.selectbox(
            'Year',
            ('2018','2019','2020','2021','2022','2023'))
        
    with col4:
        quarter = st.selectbox(
            'Quarter',
            ('1', '2', '3', '4'))

    # Output Map
    if year=='2023' and quarter=='4':
        st.write('Data for the fourth quarter of 2023 is currently unavailable as it corresponds to the ongoing quarter.')
    else:
        if type == 'Transactions':
            if state!='All':
                values =[year,quarter,state_change(state)]
                try:
                    sql = """select state, sum(transaction_amount) as Transaction_Amount, sum(transaction_count) as Transaction_Count 
                            from map_transaction  where year=(%s) and quarter=(%s) and state=(%s)
                            group by state order by state;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['State','Transaction Amount','Transaction Count'])
                    #st.write(data_df)
                except Exception as e:
                    print(e)
                    
            else:
                values =[year,quarter]
                try:
                    sql = """select state, sum(transaction_amount) as Transaction_Amount, sum(transaction_count) as Transaction_Count 
                            from map_transaction  where year=(%s) and quarter=(%s)
                            group by state order by state;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['State','Transaction Amount','Transaction Count'])
                    #st.write(data_df)
                except Exception as e:
                    print(e)

            if state=='All':
                data_df['State'] = statesdf['state']
            else:
                data_df['State'] = state

            # If it is based on TRANSACTION AMOUNT
            df = data_df
            with st.container():
                st.header("Total Transaction Amount In Each State")
                fig = go.Figure(go.Choropleth(
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations=df['State'],
                z=df['Transaction Amount'],
                colorscale='purp',
                colorbar_title='Transaction Amount'
            ))
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(height=600, width=800)
                st.plotly_chart(fig,use_container_width=True)


        elif type == 'Users':
            if state!='All':
                values =[year,quarter,state_change(state)]
                try:
                    sql = """select state, sum(registered_users) as Total_Users 
                            from map_user where year=(%s) and quarter=(%s) and state=(%s)
                            group by state order by state;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['State','Total Users'])
                    print(data_df)
                except Exception as e:
                    print(e)
                
            else:
                values =[year,quarter]
                try:
                    sql = """select state, sum(registered_users) as Total_Users 
                            from map_user where year=(%s) and quarter=(%s)
                            group by state order by state;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['State','Total Users'])
                    print(data_df)
                except Exception as e:
                    print(e)
            
            if state=='All':
                data_df['State'] = statesdf['state']
            else:
                data_df['State'] = state

            df = data_df
            with st.container():
                st.header("Total Users In Each State")
                fig = go.Figure(go.Choropleth(
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations=df['State'],
                    z=df['Total Users'],
                    colorscale='purp',  
                    colorbar_title='Total Users'
                ))

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(height=600, width=800)
                st.plotly_chart(fig,use_container_width=True)

    #SECTION 3
    # 2 widgets to show the total transaction count and amount based on the transaction type
    col1, col3, col2 = st.columns([3,1,3])
    #Widget 1 total transaction count based on menu_items
    with col1:
        st.subheader("Transaction Count Based on Type")
        col4,col5,col6 = st.columns(3)
        with col4:
            state_for_tr_count = st.selectbox(
            'State',
            ('All','Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand',
        'Uttar Pradesh', 'West Bengal'),key='statetrcn')
        
        with col5:
            year_for_tr_count = st.selectbox(
                'Year',
                ('2018','2019','2020','2021','2022','2023'),key='yrtrcn')
            
        with col6:
            quarter_for_tr_count = st.selectbox(
                'Quarter',
                ('1', '2', '3', '4'),key='qtrtrcn')
        
        if year_for_tr_count=='2023' and quarter_for_tr_count=='4':
            st.write('Data for the fourth quarter of 2023 is currently unavailable as it corresponds to the ongoing quarter.')
        else:
            if state_for_tr_count!='All':
                values =[year_for_tr_count,quarter_for_tr_count,state_change(state_for_tr_count)]
                try:
                    sql = """select transaction_type, sum(transaction_count) from aggregated_transaction  
                            where year=(%s) and quarter=(%s) and state=(%s)
                            group by transaction_type;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['Transaction Type','Total Transaction Count'])
                    #st.write(data_df)
                except Exception as e:
                    print(e)
                    
            else:
                values =[year_for_tr_count,quarter_for_tr_count]
                try:
                    sql = """select transaction_type, sum(transaction_count) from aggregated_transaction  
                            where year=(%s) and quarter=(%s)
                            group by transaction_type;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['Transaction Type','Total Transaction Count'])
                    #st.write(data_df)
                except Exception as e:
                    print(e)
            
            #st.subheader("Channel vs Number Of Videos")
            fig = px.bar(data_df,
                            x='Transaction Type',
                            y='Total Transaction Count',
                            color='Transaction Type')
            st.plotly_chart(fig,use_container_width=True)
            
    #Widget 2 total transaction amount based on menu_items Donut Chart
    with col2:
        st.subheader("Transaction Amount Based on Type")
        col4,col5,col6 = st.columns(3)
        with col4:
            state_for_tr_amt = st.selectbox(
            'State',
            ('All','Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand',
        'Uttar Pradesh', 'West Bengal'),key='statetram')
        
        with col5:
            year_for_tr_amt = st.selectbox(
                'Year',
                ('2018','2019','2020','2021','2022','2023'),key='yrtram')
            
        with col6:
            quarter_for_tr_amt = st.selectbox(
                'Quarter',
                ('1', '2', '3', '4'),key='qtrtram')
        
        if year_for_tr_amt=='2023' and quarter_for_tr_amt=='4':
            st.write('Data for the fourth quarter of 2023 is currently unavailable as it corresponds to the ongoing quarter.')
        else:
            if state_for_tr_amt!='All':
                values =[year_for_tr_amt,quarter_for_tr_amt,state_change(state_for_tr_amt)]
                try:
                    sql = """select transaction_type, sum(transaction_amount) from aggregated_transaction  
                            where year=(%s) and quarter=(%s) and state=(%s)
                            group by transaction_type;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['Transaction Type','Total Transaction Amount'])
                    #st.write(data_df)
                except Exception as e:
                    print(e)
                    
            else:
                values =[year_for_tr_amt,quarter_for_tr_amt]
                try:
                    sql = """select transaction_type, sum(transaction_amount) from aggregated_transaction  
                            where year=(%s) and quarter=(%s)
                            group by transaction_type;"""
                    mycursor.execute(sql,values)
                    data = mycursor.fetchall()
                    data_df = pd.DataFrame(data,columns=['Transaction Type','Total Transaction Amount'])
                    #st.write(data_df)
                except Exception as e:
                    print(e)
            
            
            fig = px.pie(data_df, values='Total Transaction Amount',names='Transaction Type',hole=0.5,color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig,use_container_width=True)

    #SECTION 4
    # Line chart to show transaction amount in each quarter for different years
    with st.container(border=True):
        st.subheader("Total Transaction Amount for Each Quarter")
        sql="select sum(transaction_amount), year,quarter from map_transaction group by quarter, year;"
        mycursor.execute(sql)
        data_line_chart = mycursor.fetchall()
        data_line_chart_df = pd.DataFrame(data_line_chart,columns=['Transaction Amount','Year','Quarter'])
        fig = px.line(data_line_chart_df,x='Quarter',y='Transaction Amount', color='Year')
        st.plotly_chart(fig,use_container_width=True)

    # Line chart to show total registered users in each quarter for different years
    with st.container(border=True):
        st.subheader("Total Registered Users for Each Quarter")
        sql="select sum(registered_users), year, quarter from map_user group by quarter,year;"
        mycursor.execute(sql)
        data_line_chart = mycursor.fetchall()
        data_line_chart_df = pd.DataFrame(data_line_chart,columns=['Registered Users','Year','Quarter'])
        fig = px.line(data_line_chart_df,x='Quarter',y='Registered Users', color='Year')
        st.plotly_chart(fig,use_container_width=True)

elif selected == "About":
    st.title('PhonePe Pulse Data Visualisation')
    st.text('By Devadath G Nair')
    st.subheader(":violet[**PROJECT TITLE** :] _Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly_", divider='violet')
    st.subheader(":violet[**SKILLS TAKE AWAY FROM THIS PROJECT** :] _Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, Plotly and Live Geo Visualization._", divider='violet')
    st.subheader(":violet[**DOMAIN** :] _Fintech_", divider='violet')
    st.subheader("**:violet[PROBLEM STATEMENT]**")

    multi = """The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain
insights and information that can be visualized in a user-friendly manner. The solution must include the following steps:
1. Extract data from the Phonepe pulse Github repository through scripting and clone it.
2. Transform the data into a suitable format and perform any necessary cleaning and pre-processing steps.
3. Insert the transformed data into a MySQL database for efficient storage and retrieval.
4. Create a live geo visualization dashboard using Streamlit and Plotly in Python to display the data in an interactive and visually appealing manner.
5. Fetch the data from the MySQL database to display in the dashboard.
6. Provide different widget options for users to select different facts and figures to display on the dashboard.
The solution must be secure, efficient, and user-friendly. The dashboard must be
easily accessible and provide valuable insights and information about the data in the
Phonepe pulse Github repository.
"""
    st.markdown(multi)
