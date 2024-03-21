import streamlit as st
import requests
import time

base_url = st.secrets["BASE_URL"]

# Set the title and prevent line breaks
st.markdown(
    "<h1 style='white-space: nowrap;'>Titanic Survival Prediction</h1>",
    unsafe_allow_html=True,
)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("titanic.jpeg", width=int(600 * 0.6))

# Let the user input the username and password
username = st.text_input('Username')
password = st.text_input('Password', type='password')

# Get the token
def get_token(username, password):
    response = requests.post(f'{base_url}/token', data={'username': username, 'password': password})
    token = response.json()['access_token']
    return token

# If the user clicks the 'Get Token' button, get the token
if st.button('Get Token'):
    API_TOKEN = get_token(username, password)
    st.write(f'Token: {API_TOKEN}')

# Let the user choose the api endpoint called
endpoint = st.selectbox("Choose an endpoint", ("RandomForest", "GradientBoosting"))

# Combine the base URL with the endpoint
if endpoint == "RandomForest":
    endpoint = "predict"
else:
    endpoint = "predict2"
url = base_url + endpoint

# Create a form
with st.form(key="prediction_form"):
    st.write("Fill out the form to get a prediction")
    col1, col2 = st.columns(2)

    with col1:
        PassengerId = st.number_input("PassengerId", value=892)
        Pclass = st.number_input("Pclass", value=3)
        Sex = st.number_input("Sex", value=1)
        Age = st.number_input("Age", value=34.5)

    with col2:
        SibSp = st.number_input("SibSp", value=0)
        Parch = st.number_input("Parch", value=0)
        Fare = st.number_input("Fare", value=7.8292)
        Embarked = st.number_input("Embarked", value=1)

    submit_button = st.form_submit_button(label="Get Prediction")

# If the form is submitted, make a POST request to the API
if submit_button:
    data = {
        "PassengerId": PassengerId,
        "Pclass": Pclass,
        "Sex": Sex,
        "Age": Age,
        "SibSp": SibSp,
        "Parch": Parch,
        "Fare": Fare,
        "Embarked": Embarked,
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        # Use markdown to display the prediction result
        st.markdown(f"## The prediction is: {response.json()['prediction'][0]}")
        # Create a delay
        time.sleep(1)

        if response.json()["prediction"][0] == 1:
            st.markdown("### which is good")
        else:
            st.markdown("### which is sad")

    except requests.exceptions.RequestException:
        st.write("Error connecting to API")
