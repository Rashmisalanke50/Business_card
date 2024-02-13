import streamlit as st
import base64
import PIL
from PIL import Image
import mysql.connector
import re
import easyocr
import pandas as pd
from sqlalchemy import create_engine

# Database Connection
newdb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="EMPATH.6",
    database="Cards")
cursor = newdb.cursor()
# Create a MySQL Engine and cursor using SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:EMPATH.6@localhost:3306/Cards', echo=False)

custom_theme = """
[theme]
primaryColor="#F0F2F6"
backgroundColor="#F9F7F7"
secondaryBackgroundColor="#F0F2F6"
textColor="#000000"
font="sans-serif"
layout="wide"
"""
# Set the Streamlit theme
st.write(custom_theme, unsafe_allow_html=True)

# Set the Streamlit theme
def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
   
# Streamlit App Title
st.markdown(
    "<h1 style='color: #002060; font-family: Times New Roman, Times, serif; text-align: center; font-size: 70px;'><b>Business Card Information Extraction</b></h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='color: #3333DE; font-family: Times New Roman, Times, serif; text-align: center; font-size: 35px;'><b>Upload a card to save it!!</h2>",
    unsafe_allow_html=True
)
side_bg = 'C:/Users/rashm/OneDrive/Desktop/streamlit/capstone3/cards/side.png'
sidebar_bg(side_bg)

# User input for image upload
card_image = st.text_input("Paste the image path here:")
a = Image.open(card_image)
st.image(a, caption='Uploaded Image', use_column_width=True)

# Function to extract information from business card image using EasyOCR
reader = easyocr.Reader(['en']) 

# Button to trigger card data extraction and storage
if st.button("Extract and Save Card Data"):
    result = reader.readtext(card_image, paragraph=False)
    dict=[]  
    for i in result:
        a=str(i[1])
        dict.append(a)
    data1 = ', '.join([str(item) for item in dict])
    columns1={"ID":[], "Name":[], "Email_Id":[], "Website":[], "Pincode":[], "Phone_Number": [], "State": [], "Company_Name": [], "Designation": []}
    card_name = re.findall(r'^([A-Za-z\s]+)', data1) or re.findall(r'^([A-Za-z]+)', data1)
    Email_Id= re.findall(r'\w+@\w+.\w+', data1)
    Website= re.findall(r'WWW\w+.\w+', data1) or re.findall(r'wWW\w+.\w+', data1) or re.findall(r'www.\w+.\w+', data1) or re.findall(r'WWW.\w+.\w+', data1)
    Pincode= re.findall(r'\b\d{6}\b', data1)
    columns1={"Name":[], "Email_Id":[], "Website":[], "Pincode":[], "Phone_Number": [], "State": [], "Company_Name": [], "Designation": []}
    phone_number_match= re.search(r'\+\d{2}-\d{3}-\d{4}', data1) or re.search(r'\+\d{3}-\d{3}-\d{4}', data1)
    if phone_number_match:
        Phone_Number = phone_number_match.group()
    else:
        Phone_Number = "Empty"
    columns1["Phone_Number"]=Phone_Number
    State= re.findall(r'TamilNadu', data1)
    Company_Name= re.findall(r'([^,]+$)', data1)
    Designation= re.findall(r'\w+ Executive', data1) or re.findall(r'\w+ Manager', data1) or re.findall(r'\w+ CEO', data1) or re.findall(r'\w+ MANAGER', data1)
    # Replace null values with "Empty"
    columns1["Name"] = card_name if card_name else ["Empty"]
    columns1["Email_Id"] = Email_Id if Email_Id else ["Empty"]
    columns1["Website"] = Website if Website else ["Empty"]
    columns1["Pincode"] = Pincode if Pincode else ["Empty"]
    columns1["Phone_Number"] = Phone_Number if Phone_Number else ["Empty"]
    columns1["State"] = State if State else ["Empty"]
    columns1["Company_Name"] = Company_Name if Company_Name else ["Empty"]
    columns1["Designation"] = Designation if Designation else ["Empty"]
    unique_id = int(hash(card_name[0])) % 1000
    id_pattern = f"{unique_id:03d}_{card_name[0]}"
    columns1["ID"] = id_pattern
    card_data = pd.DataFrame(columns1)

    #table creation in sql
    card_data.to_sql('card_data',if_exists="append", con=engine, index=False)

# Function to display SQL table in Streamlit
def display_sql_table(table_name):
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", con=engine)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error occurred while fetching data from MySQL table: {e}")

# Get unique IDs from the SQL table
unique_ids = pd.read_sql_query("SELECT DISTINCT ID FROM card_data", con=engine)["ID"].tolist()
# Dropdown to select unique ID
selected_id = st.selectbox("Select Unique ID", unique_ids)
selected_row = pd.read_sql_query(f"SELECT * FROM card_data WHERE ID = '{selected_id}'", con=engine)
# Button to edit and update the selected card
update_queries = {
    "Name": "UPDATE card_data SET Name = %s WHERE ID = %s",
    "Email_Id": "UPDATE card_data SET Email_Id = %s WHERE ID = %s",
    "Website": "UPDATE card_data SET Website = %s WHERE ID = %s",
    "Pincode": "UPDATE card_data SET Pincode = %s WHERE ID = %s",
    "Phone_Number": "UPDATE card_data SET Phone_Number = %s WHERE ID = %s",
    "State": "UPDATE card_data SET State = %s WHERE ID = %s",
    "Company_Name": "UPDATE card_data SET Company_Name = %s WHERE ID = %s",
    "Designation": "UPDATE card_data SET Designation = %s WHERE ID = %s"}

# Streamlit App Title
st.sidebar.title("Card Actions")

# Button to view the cards
if st.sidebar.button("View Cards"):
        display_sql_table("card_data")
                
# Button to edit the selected row
st.title("Edit Card")
st.dataframe(selected_row)
field = st.selectbox("Select field to update:", options=list(update_queries.keys()))
new_value = st.text_input(f"Enter new value for {field}:")
if st.button("Update"):
    if field not in update_queries:
        st.error("Invalid field selected.")
    else:
        update_query = update_queries[field]
        cursor.execute(update_query, (new_value, selected_id))
        newdb.commit()
        if cursor.rowcount > 0:
            st.success(f"{field} updated successfully!")
        else:
            st.warning("No rows were updated.")
cursor.close()
newdb.close()

# Button to delete the selected row
if st.sidebar.button("Delete Card"):
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM card_data WHERE ID = '{selected_id}'")
        connection.commit()
        st.sidebar.write("Card deleted successfully!")
    except Exception as e:
        st.sidebar.error(f"Error occurred while deleting row: {e}")
    finally:
        cursor.close()
        connection.close()



     
