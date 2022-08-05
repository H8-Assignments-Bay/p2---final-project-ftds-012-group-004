import streamlit as st
import requests
import json
from PIL import Image
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="centered", page_icon="🙌", page_title="Healing - Go Heal Your Day")

def set_bg_hack_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(https://i.pinimg.com/originals/98/0b/0b/980b0b4514e565b091843df1b5f1f40f.jpg);
             background-repeat: no-repeat;
             background-size: 1250px 1120px;
             background-position: center;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()

image = Image.open('healing.png')
st.image(image, use_column_width = True, caption='Lets go Healing!')

# User input

st.header("Healing Person's Information")

col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("Fill your Name")
    age = st.selectbox('Select your age range',('15-25','25-35','35-45','45-55','55-65','65-75','75-85','85-100'))
    gender = st.radio('Select your gender',('Female','Male'))
with col2:
    marital_status = st.selectbox('Select your marital status',('Divorcee','Married','Single','Remarried','Widower'))
    profession_status = st.selectbox('Select your profession',('Management','Employee','Unskilled worker','Foreman','Manual labourer','Technician','Other'))

# Hobbies selection

st.subheader("Select your hobbies (You can select more than one)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    reading = st.checkbox("Reading")
    music = st.checkbox("Music")
    cinema = st.checkbox("Cinema")
with col2:
    exhibition = st.checkbox("Exhibition")
    computer = st.checkbox("Computer")
    sport = st.checkbox("Sport")
with col3:
    walking = st.checkbox("Walking")
    traveling = st.checkbox("Travelling")
    gardening = st.checkbox("Gardening")
with col4:
    cooking = st.checkbox("Cooking")
    fishing = st.checkbox("Fishing")

hobby = [reading, music, cinema, exhibition, computer,sport, walking, traveling, gardening, cooking, fishing]
gender_data = gender
age_data = age
status_data = [marital_status, profession_status]

encode = []
encode2 = []


# Encode hobby input for clustering

for a in hobby:
    if a == True:
        encode.append(1)
    else :
        encode.append(0)

# Encode gender input for clustering

if gender_data == 'Female':
    encode2.append('F')
else:
    encode2.append('M')

# Encode age input for clustering

if age_data == '15-25':
    encode2.append('[15,25]')
elif age_data == '25-35':
    encode2.append('(25,35]')
elif age_data == '35-45':
    encode2.append('(35,45]')
elif age_data == '45-55':
    encode2.append('(45,55]')
elif age_data == '55-65':
    encode2.append('(55,65]')
elif age_data == '65-75':
    encode2.append('(65,75]')
elif age_data == '75-85':
    encode2.append('(75,85]')
else:
    encode2.append('(85,100]')    

# Encode marital status & profession input for clustering

for y in status_data:
    encode2.append(y)

# Collect all input for inferential

inf_data = {'Reading': encode[0],
        'Music': encode[1],
        'Cinema':encode[2],
        'Exhibition': encode[3],
        'Computer': encode[4],
        'Sport': encode[5],
        'Walking': encode[6],
        'Travelling': encode[7],
        'Gardening':encode[8],
        'Cooking': encode[9],
        'Fishing': encode[10],
        'Sex': encode2[0],
        'Age': encode2[1],
        'MaritalStatus': encode2[2],
        'Profession': encode2[3]
        }

# Access URL in backend

URL = "https://healing-fp-ftds-group004.herokuapp.com/predict"    
r = requests.post(URL,json=inf_data)
res = r.json()
result = res['result']

         
if result == '0':
    st.subheader(f"Select designated healing place")
    selection = st.radio("Please select your favorite one",
     ('Beach', 'Cafe', 'Dance Club', 'Park', 'Restaurant', 
     'View Point Restaurant', 'Bookstore', 'Zoo'))
 
elif result == '1':
    st.subheader(f"Select designated healing place")
    selection = st.radio("Please select your favorite one",
     ('Art Gallery', 'Beach', 'Cafe', 'Dance Club', 'Hotel',
      'Shopping Mall', 'Museum', 'Park', 'Library', 'Theatre', 'Bookstore'))

elif result == '2':
    st.subheader(f"Select designated healing place")
    selection = st.radio("Please select your favorite one",
     ('Art Gallery', 'Beach', 'Cafe', 'Dance Club', 'Hotel', 'Museum',
     'Park', 'Restaurant', 'View Point Restaurant', 'Bookstore', 'Zoo'))

else:
    st.subheader(f"Select designated healing place")
    selection = st.radio("Please select your favorite one",
     ('Art Gallery', 'Beach', 'Cafe', 'Hotel', 'Local Attraction',
      'Shopping Mall', 'Monument', 'Museum', 'Restaurant', 'Library', 'Theatre', 'Bookstore'))


# Gimmick filtering

st.subheader("Additional Information")
rating_filter = st.selectbox('Select your stress level',('Low','Middle','High'))
popularity_filter = st.selectbox('Select place popularity level',('Low','Middle','High'))

if st.button(label='Submit'):
    st.header(f"Recommended places for your healing are....")
    data_scrapping = pd.read_excel('ScrappingFinal.xlsx')


# Recommendation mapping

    if selection == 'Art Gallery':
        location = 'Art gallery'
    elif selection == 'Beach':
        location = 'Beach'
    elif selection == 'Cafe':
        location = 'Cafe'
    elif selection == 'Dance Club':
        location = 'Dance club'
    elif selection == 'Hotel':
        location = 'Hotel'
    elif selection == 'Local Attraction':
        location = 'Local'
    elif selection == 'Shopping Mall':
        location = 'Shopping mall'
    elif selection == 'Monument':
        location = 'Monument'
    elif selection == 'Museum':
        location = 'Museum'
    elif selection == 'Park':
        location = 'Park'
    elif selection == 'Restaurant':
        location = 'Restaurant'
    elif selection == 'View Point Restaurant':
        location = 'View point resto'
    elif selection == 'Library':
        location = 'Library'
    elif selection == 'Theatre':
        location = 'Theatre'
    elif selection == 'Bookstore':
        location = 'Book store'
    else:
        location = 'Zoo'

    dataloc = data_scrapping[(data_scrapping['category'] == location)]

    if popularity_filter == 'Low':
        datapop = dataloc[(dataloc['popularity'] == 'low')]
    elif popularity_filter == 'Middle':
        datapop = dataloc[(dataloc['popularity'] == 'middle')]
    elif popularity_filter == 'High':
        datapop = dataloc[(dataloc['popularity'] == 'high')]

    if rating_filter == 'Low':
        data = datapop[(datapop['avg_rating'] > 4.0)]
    elif rating_filter == 'Middle':
        data = datapop[(datapop['avg_rating'] > 4.3)]
    elif rating_filter == 'High':
        data = datapop[(datapop['avg_rating'] > 4.6)]

    
    layer1 = pdk.Layer(
            "ScatterplotLayer",
            data = data,
            pickable=True,
            opacity=1,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=20,
            get_position='[longitude,latitude]',
            get_radius=15,
            get_fill_color=[0,0,255]
    )

    # Setting up for map visualization
    
    view_state = pdk.ViewState(latitude=-6.1809851330724985, longitude=106.8286844119248, zoom=10.5)

    st.pydeck_chart(pdk.Deck(layers=[layer1], initial_view_state=view_state, 
                            tooltip={"text": "{name} \nAddress: {address} \nRating: {avg_rating}"},
                            map_style='mapbox://styles/mapbox/navigation-day-v1'))

    if data.shape[0] >= 3:
        n = 3
    elif data.shape[0] == 2:
        n= 2
    elif data.shape[0] == 1:
        n = 1
    else:
        n = 0
        st.write('Sorry there is no recomendation for your preferences input :(')

  # Healing place recommendation and filtering

    st.subheader("Place Recommendation")
    show_rec = data.sort_values('avg_rating', ascending = False).head(n)
    show_rec = show_rec.reset_index(drop = True)    


    col1, col2, col3 = st.columns(3)
    if show_rec.shape[0] == 1:
        with col1:
            st.image(show_rec['thumbnail'][0],width=230)
            st.markdown(show_rec['name'][0])
            st.markdown(show_rec['address'][0])
            st.write(show_rec['avg_rating'][0])
    elif show_rec.shape[0] == 2:
        with col1:
            st.image(show_rec['thumbnail'][0],width=230)
            st.markdown(show_rec['name'][0])
            st.markdown(show_rec['address'][0])
            st.write(show_rec['avg_rating'][0])
        with col2:
            st.image(show_rec['thumbnail'][1],width=230)
            st.markdown(show_rec['name'][1])
            st.markdown(show_rec['address'][1])
            st.write(show_rec['avg_rating'][1])
    elif show_rec.shape[0] == 3:
        with col1:
            st.image(show_rec['thumbnail'][0],width=230)
            st.markdown(show_rec['name'][0])
            st.markdown(show_rec['address'][0])
            st.write(show_rec['avg_rating'][0])
        with col2:
            st.image(show_rec['thumbnail'][1],width=230)
            st.markdown(show_rec['name'][1])
            st.markdown(show_rec['address'][1])
            st.write(show_rec['avg_rating'][1])
        with col3:
            st.image(show_rec['thumbnail'][2],width=230)
            st.markdown(show_rec['name'][2])
            st.markdown(show_rec['address'][2])
            st.write(show_rec['avg_rating'][2])

# Access link for feedback

st.subheader("Help us with your rating:")

link = '[Link](https://forms.gle/KTWkL3hft8odWD3i9)'
st.markdown(link, unsafe_allow_html=True)
