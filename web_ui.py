import streamlit as st
import pandas as pd
import time

from collections import OrderedDict
from opensyslog_helper import OpensyslogHelper

if "helper" not in st.session_state:
    st.session_state['helper'] = OpensyslogHelper("/config/")

st.set_page_config(layout="wide")
def get_devices():
    dhcp_ack_json = st.session_state['helper'].load_dhcpack_status_json()
    if len(dhcp_ack_json) > 0:
        return dhcp_ack_json
    return {}

def get_notifications():
    history_json = st.session_state['helper'].load_notification_history_json()
    if len(history_json):
        sorted_json = OrderedDict(sorted(history_json.items(), reverse=True))
    return sorted_json

def highlight_rows(row):
    if not st.session_state['helper'].lookup_device_name_from_csv(row['mac']):
    
        return ['background-color: yellow; color: red; font-weight: bold'] * len(row)
    else:
        return [''] * len(row)

def refresh_table():    
    data = get_devices()
    if data: 
        df = pd.DataFrame(data).T
        df_reset = df.reset_index().rename(columns={'index': 'mac'})
        df_reset =  df_reset.style.apply(highlight_rows, axis=1)
        maintable.dataframe(df_reset)

# Sidebar navigation with buttons
st.sidebar.title("Navigation")
active_devices = st.sidebar.button("Active Devices", key="home")
notifications = st.sidebar.button("Notifications", key="data")
add_device = st.sidebar.button("Add device to csv", key="about")


if 'page' not in st.session_state:
    st.session_state.page = 'active_devices'

if active_devices:
    st.session_state.page = 'active_devices'
elif notifications:
    st.session_state.page = 'notifications'
elif add_device:
    st.session_state.page = 'add_device'

if st.session_state.page == 'active_devices':
    
    st.title("Connected Devices")
    refresh_but = st.button("Refresh")
           
    maintable = st.empty()
    refresh_table()
    if refresh_but:
        refresh_table()

elif st.session_state.page == 'notifications':
    data = get_notifications()
    df = pd.DataFrame({"Mac_address" : data.keys(), "Notifications": data.values()})
    st.dataframe(df)

elif st.session_state.page == 'add_device':
    if 'mac' not in st.session_state:
        st.session_state.mac = ""
    if 'ip' not in st.session_state:
        st.session_state.ip = ""
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    def handle_submit():
        # Handle the button press
        st.session_state['helper'].setup_lookup_csv_file([st.session_state.ip, st.session_state.mac, st.session_state.name])
        # Clear the input fields
        st.session_state.mac = ""
        st.session_state.ip = ""
        st.session_state.name = ""
        # Update submission status
        st.session_state.submitted = True
        # Wait for 2 seconds to show the message
       
        

    # Create input text boxes
    mac = st.text_input("Device Mac", key="mac")
    ip = st.text_input("Device IP", key="ip")
    name = st.text_input("Device Name", key="name")

    # Create a button and assign the callback function
    st.button("Add Device", on_click=handle_submit)

    # Display a message if the form was submitted
    if st.session_state.submitted:
        st.success('Submitted!')
        time.sleep(2)
        st.session_state.submitted = False
        

