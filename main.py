import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
from PIL import Image
from streamlit_option_menu import option_menu

data=pd.read_csv("G:\\SK\\Ds\\AirBnb\\AirBnb.csv")
df=data.copy()


#streamlit part
st.set_page_config(page_title="Airbnb",layout="wide")
st.title(":red[AIRBNB ANALYSIS]")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>",unsafe_allow_html=True)

#option_menu
with st.sidebar:
    select = option_menu("Menu",["Home", "Analysis", "About"],
    icons=['house','activity','info-circle-fill'], menu_icon="cast", default_index=1)

#Home
if select == "Home":
    st.subheader("About Airbnb",divider=True)
    col1,col2=st.columns([3,2])
    with col1:
        st.write("")
        st.write('''***Airbnb is an online marketplace that connects people who want to rent out
                their property with people who are looking for accommodations,
                typically for short stays. Airbnb offers hosts a relatively easy way to
                earn some income from their property.Guests often find that Airbnb rentals
                are cheaper and homier than hotels.***''')
        st.write("")
    with col2:
        img = Image.open("G:\\SK\\Ds\\AirBnb\\Airbnb 1.jpeg")
        st.image(img,width=260)

    st.write('''***Airbnb Inc (Airbnb) operates an online platform for hospitality services.
                  The company provides a mobile application (app) that enables users to list,
                  discover, and book unique accommodations across the world.
                  The app allows hosts to list their properties for lease,
                  and enables guests to rent or lease on a short-term basis,
                  which includes vacation rentals, apartment rentals, homestays, castles,
                  tree houses and hotel rooms. The company has presence in China, India, Japan,
                  Australia, Canada, Austria, Germany, Switzerland, Belgium, Denmark, France, Italy,
                  Norway, Portugal, Russia, Spain, Sweden, the UK, and others.
                  Airbnb is headquartered in San Francisco, California, the US.***''')

#Analysis
elif select == "Analysis":
    tab1, tab2, tab3, tab4, tab5= st.tabs(["***Price Analysis***","***Availability Analysis***","***Location-Based Insights***", "***Geospatial Visualization***", "***Insights***"])

# Price Analysis
    with tab1:
        st.subheader("Price Analysis")

        df_price_c = ['_id', 'country', 'room_type', 'price', 'property_type', 'review_scores','beds','bedrooms',
                    'number_of_reviews', 'host_response_time','accommodates']
        
        df_price = df[df_price_c].copy()
        with st.container(border=True):
            col1, col2 = st.columns(2)

            # Multiselect for country
            with col1:
                selected_countries = st.multiselect("Select the Country", df["country"].unique(),default='Portugal')

            df1 = df_price[df_price["country"].isin(selected_countries)]
            df1.reset_index(drop=True, inplace=True)

            # Multiselect for room type
            with col2:
                selected_room_types = st.multiselect("Select the Room Type", df1["room_type"].unique(),default='Private room')
            
            with col1:
                df2 = df1[df1["room_type"].isin(selected_room_types)]
                df2.reset_index(drop=True, inplace=True)
                
                df_b = df2.groupby("property_type").agg({"price":"mean", "review_scores":"mean", "number_of_reviews":"sum"}).reset_index()
                
                fig_bar_1 = px.bar(df_b, x='price', y="property_type",
                                title="Average Prices by Property Type", orientation='h',
                                hover_data=["number_of_reviews", "review_scores"],
                                color_discrete_sequence=px.colors.sequential.Redor_r, width=500, height=600)
                st.plotly_chart(fig_bar_1)

            with col2:
                df_b2=df2.groupby("accommodates").agg({"price":"mean","beds":"mean","bedrooms":"mean","review_scores":"mean","number_of_reviews":"sum"}).reset_index()
                fig_bar_2 = px.bar(df_b2,x='price',y='accommodates', orientation='h',
                                title="Average Price by Accommodation Capacity",
                                hover_data=["bedrooms","beds","number_of_reviews", "review_scores"],
                                color_discrete_sequence=px.colors.sequential.Bluered, width=480, height=600)
                st.plotly_chart(fig_bar_2)
        #sunburst chart
        fig_sun= px.sunburst(df_price, path=["country","room_type","host_response_time"], 
                            values="price",width=600,height=500,
                            title="Analyzing Price Patterns: Country, Room Type, and Host Response Time",
                            color_discrete_sequence=px.colors.sequential.BuPu_r)
        st.plotly_chart(fig_sun)

        # pie chart (property_type)
        property_counts = df_price.groupby('property_type').size().reset_index(name='count')

        df_price = pd.merge(df_price, property_counts, on='property_type')

        fig_pie= px.pie(df_price, values='price', names='property_type',
                    title='Distribution of Property Types by Price',
                    hover_data=['property_type', 'count'],
                    labels={'property_type': 'Property Type', 'count': 'Count'},
                    hole=0.5,width=600,height=500)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie)

# Availability Analysis
    with tab2:
        df_avail_c = ['country','first_review','room_type','property_type', 'availability_30', 'availability_60', 'availability_90', 'availability_365']
        df_avail = df[df_avail_c].copy()

        df_avail['first_review'] = pd.to_datetime(df_avail['first_review'])

        availability_30 = df_avail.groupby(df_avail['first_review'].dt.year)['availability_30'].mean().reset_index()
        availability_60 = df_avail.groupby(df_avail['first_review'].dt.year)['availability_60'].mean().reset_index()
        availability_90 = df_avail.groupby(df_avail['first_review'].dt.year)['availability_90'].mean().reset_index()
        availability_365 = df_avail.groupby(df_avail['first_review'].dt.year)['availability_365'].mean().reset_index()

        # Combine availability data into a single DataFrame
        availability_combined = pd.merge(availability_30, availability_60, on='first_review', suffixes=('_30', '_60'))
        availability_combined = pd.merge(availability_combined, availability_90, on='first_review')
        availability_combined = pd.merge(availability_combined, availability_365, on='first_review')

        # Plotting
        st.subheader('Availability Trends Over Time')
        fig_line = px.line(availability_combined, x='first_review', 
                    y=['availability_30', 'availability_60', 'availability_90', 'availability_365'])
        fig_line.update_layout(xaxis_title='Year', yaxis_title='Availability')
        st.plotly_chart(fig_line)


        def availability(a):
            with st.container(border=True):
                col1, col2 = st.columns([5, 4])
                with col1:
                    st.header(f"Availability_{a} days")
                    # st.write("")
                    s_country = st.selectbox("Select the country", df_avail['country'].unique(), key=f"country_select{a}")
                    df_avail_sc=df_avail.loc[df_avail["country"]==s_country].copy()
                    df_avail_sc.reset_index(drop=True,inplace=True)
                    # Convert 'first_review' column to datetime
                    df_avail_sc['first_review'] = pd.to_datetime(df_avail_sc['first_review'], errors='coerce')

                    df_avail_sc['year'] = df_avail_sc['first_review'].dt.year
                    df_avail_py = df_avail_sc.groupby(['year', 'property_type'])[f'availability_{a}'].mean().reset_index()

                    # heatmap 
                    fig_heat = px.imshow(df_avail_py.pivot(index='property_type', columns='year',
                                                                        values=f'availability_{a}'),
                                        labels=dict(x="Year", y="property_type", color="Availability"),
                                        title=f'Availability Heatmap by Month and Year ({a} days)',
                                        color_continuous_scale='rainbow', width=525, height=450)
                    st.plotly_chart(fig_heat)

                with col2:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")

                    s_property = st.selectbox("Select the property ", df_avail_sc['property_type'].unique(),key=f"s_property{a}")
                    df_avail_pt = df_avail_sc[df_avail_sc['property_type'] == s_property]
                    df_avail_pt.reset_index(drop=True, inplace=True)

                    df_avail_rt = df_avail_pt.groupby('room_type')[f'availability_{a}'].mean().reset_index()

                    # bar chart to visualize availability trends
                    fig_bar = px.bar(df_avail_rt, x='room_type', y=f'availability_{a}',
                                    title=f'Average Availability by Room type in {s_property} ({a} days)',
                                    labels={'room_type': 'Room Type', f'availability_{a}': 'Average Availability'},
                                    color=f'availability_{a}', width=440, height=442.5,
                                    color_continuous_scale=px.colors.sequential.Viridis)
                    fig_bar.update_xaxes(type='category')
                    st.plotly_chart(fig_bar)

        # Call the function for different durations
        availability(365)
        availability(90)
        availability(60)
        availability(30)

# Location Analysis
    with tab3:
        location =['host_neighbourhood','property_type','country','price','host_total_listings_count']
        df_loc = df[location].copy()

        sel_country=st.selectbox("Select the Country",df_loc['country'].unique())
        df_location = df_loc[df_loc['country']==sel_country]
        df_location.reset_index(drop=True, inplace=True)

        with st.container(border=True):
            c1,c2=st.columns([5.1,3.3])
            with c1:
                property_type_distribution = df_location.groupby(['host_neighbourhood', 'property_type'])['host_total_listings_count'].sum().unstack()
                property_type_distribution = property_type_distribution.reset_index()

                fig = px.bar(property_type_distribution, x=property_type_distribution.columns[1:], y='host_neighbourhood',
                            title='Property Type Distribution by Neighbourhood',orientation='h',height=900,width=620,
                            labels={'host_neighbourhood': 'Neighbourhood', 'value': 'Total Host Listings Count', 'variable': 'Property Type'},
                            barmode='stack')
                st.plotly_chart(fig)

                with c2:
                    with st.container(border=True):
                        costly = df_location.groupby('host_neighbourhood')[['price']].mean().reset_index()
                        costly_1=costly.sort_values(by='price',ascending=False)
                        cost=costly_1.iloc[0:5]
                        fig_t5= px.bar(cost, x='host_neighbourhood', y='price',width=370,height=450,
                                    title='Top 5 Costliest Nieghbourhood',color='price',
                                    color_discrete_sequence=px.colors.sequential.Viridis,
                                    labels={'host_neighbourhood': 'Neighbourhood', 'price': 'Average  Price'})
                        st.plotly_chart(fig_t5)
                        cheap=costly.sort_values(by='price',ascending=True)
                        cost_1=cheap.iloc[0:5]
                        fig_t5= px.bar(cost_1, x='host_neighbourhood', y='price',width=370,height=450,
                                    title='Top 5 Cheapest Nieghbourhood',color='price',
                                    color_discrete_sequence=px.colors.sequential.Viridis,
                                    labels={'host_neighbourhood': 'Neighbourhood', 'price': 'Average  Price'})
                        st.plotly_chart(fig_t5)

# Geospatial Analysis
    with tab4:
        st.subheader("Geospatial Visualization")
        st.write("")
        geo=['property_type','room_type','latitude','longitude','price','number_of_reviews','name']
        df_geo=df[geo].copy()
       
        col1,col2=st.columns(2)
        with col1:
            property_type = st.multiselect('Select Property Type', df_geo['property_type'].unique(),default='Apartment')
        with col2:
            room_type = st.multiselect('Select Room Type', df_geo['room_type'].unique(),default='Private room')

        filtered_data = df_geo[(df_geo['property_type'].isin(property_type)) & 
                                    (df_geo['room_type'].isin(room_type))]

        fig_map = px.scatter_mapbox(filtered_data, 
                                lat='latitude', 
                                lon='longitude', 
                                color='price',
                                size='price',
                                hover_name='name',
                                hover_data=['price', 'number_of_reviews'],
                                zoom=1)
        fig_map.update_layout(width=800,height=350,mapbox_style="open-street-map")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map)
    
    with tab5:    
        df_ins = ['price','country','property_type','room_type','host_total_listings_count']
        df_insight = df[df_ins].copy()

        sum_of_price = df_insight['price'].sum().astype(int).astype(str)
        room_type_price = df.groupby('room_type')['price'].sum().astype(int).astype(str)

        c1,c2,c3 = st.columns([2.5,3.5,3.5], gap="large")
        with c1:
            st.write("")
            with st.container(border=True):
                st.subheader(":red[Sum of Prices]",divider='blue')
                st.subheader("$ "+sum_of_price)
            with st.container(border=True):
                st.subheader(":red[Room Types]",divider='blue')
                st.write("Entire home/apt :"+" $ "+room_type_price[0])
                st.write("Private room :"+" $ "+room_type_price[0])
                st.write("Shared room :"+" $ "+room_type_price[0])
                       
        with c2:
            df_country = df_insight.groupby('country')['price'].sum().reset_index().sort_values(by='price',ascending=False)

            fig_polar = px.bar_polar(df_country,r='price',theta='country',
                                    color_discrete_sequence=px.colors.sequential.haline,
                                    width=400,
                                    title='Price Distribution by Country')
            fig_polar.update_layout(polar=dict(bgcolor='grey'))
            st.plotly_chart(fig_polar)

        with c3:
            df_country = df_insight.groupby('country')['host_total_listings_count'].sum().reset_index().sort_values(by='host_total_listings_count',ascending=False)

            fig_polar = px.bar_polar(df_country,r='host_total_listings_count',theta='country',
                                    color_discrete_sequence=px.colors.sequential.haline,
                                    width=400,
                                    title='Listings Distribution by Country')
            fig_polar.update_layout(polar=dict(bgcolor='grey'))
            st.plotly_chart(fig_polar)
        c4,c5=st.columns(2)

        with c4:
            df_property = df_insight.groupby('property_type')['price'].sum().reset_index().sort_values(by='price',ascending=True)

            fig_bar_p= px.bar(df_property,x='price',y='property_type',
                                    color_discrete_sequence=px.colors.sequential.Redor_r,
                                    width=500,height=580,orientation='h',
                                    title='Price Distribution by Property type',
                                    labels={'property_type': 'Poperty Type','price':'Price' })
            st.plotly_chart(fig_bar_p)

        with c5:
            df_property_l = df_insight.groupby('property_type')['host_total_listings_count'].sum().reset_index().sort_values(by='host_total_listings_count',ascending=True)

            fig_bar_p= px.bar(df_property_l,x='host_total_listings_count',y='property_type',
                                    color_discrete_sequence=px.colors.sequential.Redor_r,
                                    width=500,height=580,orientation='h',
                                    title='Listings Distribution by Property type',
                                    labels={'property_type': 'Poperty Type','host_total_listings_count':"Total Listings" })
            st.plotly_chart(fig_bar_p)

elif select == "About":   

    st.write('''

### ***About Airbnb Analysis Project***

**Project Title :**  ***Airbnb Analysis***

**Domain :**  ***Travel Industry, Property Management, Tourism***

**Skills Takeaway :**  ***Python scripting, Data Preprocessing, Visualization (Plotly, Seaborn, Matplotlib), EDA, Streamlit, MongoDB, Power BI/Tableau.***

---

### ***Key Components:***

1. **Data Retrieval and Preparation:**
   - ***Establishing a connection to MongoDB Atlas, the project retrieves the Airbnb dataset efficiently.***
   - ***Through meticulous data cleaning and preparation, the dataset undergoes a transformation, ensuring accuracy and consistency in subsequent analyses.***

2. **Price and Availability Analysis:**
   - ***Dynamic plots and charts illuminate the fluctuations in Airbnb prices based on location, property type, and seasonal variations.***
   - ***Availability patterns are dissected, providing insights into occupancy rates, booking trends, and demand fluctuations throughout the year.***

3. **Location-Based Insights:**
   - ***Location-specific analyses unravel the nuances of pricing variations across different regions and neighborhoods. This granular examination aids in identifying lucrative investment opportunities and understanding market dynamics.***

4. **Geospatial Visualization:**
   - ***The Streamlit web application showcases interactive maps that visually represent the distribution of Airbnb listings across various locations. Users can explore pricing dynamics, ratings, and other pertinent factors seamlessly.***

             
5. **Interactive Visualizations and Dashboards:**
             
   - ***Interactive visualizations empower users to filter and drill down into the data, facilitating a personalized exploration experience.***
   - ***A comprehensive dashboard, crafted using Power BI or Tableau, synthesizes key insights from the analysis, offering stakeholders a holistic view of Airbnb trends and patterns.***

---

### ***Conclusion:***
             
***The Airbnb Analysis project amalgamates advanced data analytics techniques with cutting-edge visualization tools to deliver actionable insights pivotal for decision-making in the travel and property management sectors. Through a meticulous exploration of Airbnb data, this project equips stakeholders with the knowledge required to navigate the dynamic landscape of the hospitality industry effectively.***
''')