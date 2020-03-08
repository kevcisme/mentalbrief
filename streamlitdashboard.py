import numpy as np
import pandas as pd
import pickle
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

with open("./treatment_rf.pkl", "rb") as pk:
    rf = pickle.load(pk)

#Age sidebar
age_sidebar = st.sidebar.text_input("Age", 28)

# Gender Sidebar:
gender_sidebar = st.sidebar.selectbox(
    'What is your gender?',
    ('Female', 'Male', 'Non-Binary')
)

# State Sidebar
state_sidebar = st.sidebar.selectbox(
    'Which state do you primarily practice in?',
    ('AL','AZ','CA','CO','CT','DC','FL','GA','IA','ID','IL',
        'IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS',
        'NC','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA',
        'RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY')
    )

# Self Employed Sidebar
self_employed_sidebar = st.sidebar.selectbox(
    'Are you self-employed?',
    ('Yes', 'No')
    )

# add in boutique firm? if yes, then start
# to filter by 

# Firm Size Sidebar 
firm_employee_size_sidebar = st.sidebar.selectbox(
    'How many employees does your firm employ?',
    ('1-5', '6-25',  '26-100','100-500', '500-1000','More than 1000', )
    )

# Family History of mental illness
family_history_sidebar = st.sidebar.selectbox(
    'Do you have a family history of mental illness?',
    ('Yes', 'No')
    )

# first text input box
main_panel_text_input = st.text_area(
    'Tell us about how things are going...'
    )


# if main_panel_text_input:
#     st.latex(r'''
# ...     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
# ...     \sum_{k=0}^{n-1} ar^k =
# ...     a \left(\frac{1-r^{n}}{1-r}\right)
# ...     ''')

sidebar_inputs = [age_sidebar, gender_sidebar, state_sidebar, self_employed_sidebar,firm_employee_size_sidebar,family_history_sidebar, main_panel_text_input]

#if all(sidebar_inputs):
# if sidebar_inputs:
#     if st.button('Submit'):
#         st.write('Press "Submit to see results"')
#     else:
#         #upon button click, inputs go here
#         st.write("here's what I have so far:")
#         #data = np.array(sidebar_inputs).reshape(1, -1)
#         #df = pd.DataFrame(data, columns = ['Age', 'Gender', 'State', 'Self-Employed Status',
#         #    'Firm Size', 'Comments'])
#         #st.write(df)
# else:
#     st.text("Please Finish the Survey")
#     st.text("here's what I have so far:")
#     data = np.array(sidebar_inputs).reshape(1, -1)
#     df = pd.DataFrame(data, columns = ['Age', 'Gender', 'State', 'Self-Employed Status',
#             'Firm Size', 'Comments'])
#     st.write(df)


def fix_columns( d, columns ):  

    add_missing_dummy_columns( d, columns )

    # make sure we have all the columns we need
    assert( set( columns ) - set( d.columns ) == set())

    extra_cols = set( d.columns ) - set( columns )
    if extra_cols:
        print ("extra columns:", extra_cols)

    d = d[ columns ]
    return d

def add_missing_dummy_columns( d, columns ):
    missing_cols = set( columns ) - set( d.columns )
    for c in missing_cols:
        d[c] = 0

feature_columns = ['AL', 'AZ', 'CA', 'CO', 'CT', 'DC', 'FL', 'GA', 'IA', 'ID', 'IL', 'IN',
       'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'NC', 'NE',
       'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
       'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY', 'Age', 'Gender',
       'self_employed', 'no_employees', 'family_history']

def model_clean(some_model_df):
    #model_df = some_model_df[streamlit_features].copy()
    some_model_df['state'] = some_model_df['state'].fillna(some_model_df['state'].mode()[0])
    some_model_df['self_employed'] = some_model_df['self_employed'].fillna(some_model_df['self_employed'].mode()[0])
    some_model_df['comments'] = some_model_df['comments'].apply(lambda x: np.random.choice(some_model_df['comments'].dropna().values))
    some_model_df['Gender'] = np.where(some_model_df['Gender'].str.lower().str.contains('f'), 'female', 'male')
    some_model_df['Gender'] = some_model_df['Gender'].replace({'female':1, 
                                                'male':0})
    some_model_df['self_employed'] = some_model_df['self_employed'].replace({'No':0, 'Yes':1})
    some_model_df['family_history'] = some_model_df['family_history'].replace({'No':0, 'Yes':1})
    some_model_df['no_employees'] = some_model_df['no_employees'].replace({'1-5':1,
                                                             '6-25':2, 
                                                             '26-100':3,
                                                             '100-500':4, 
                                                             '500-1000':5,
                                                             'More than 1000':6, 
                                                             })
    dummies_state = pd.get_dummies(some_model_df['state'])

    final_df = pd.concat([dummies_state, some_model_df.drop('state', 1)], 1)
    ready = fix_columns(final_df, feature_columns)

    return ready



    


if sidebar_inputs:
    st.text("here's what I have so far:")
    data = np.array(sidebar_inputs).reshape(1, -1)
    unfinished_df = pd.DataFrame(data, columns = ['Age', 'Gender', 'State', 'Self-Employed Status','Firm Size', 'Family History', 'Comments'])
    st.write(unfinished_df)
    st.text("please finish the survey")

    if all(sidebar_inputs):
        if st.button('Submit'):
            data = np.array(sidebar_inputs).reshape(1, -1)
            finished_df = pd.DataFrame(data, columns = ['Age', 'Gender', 'State', 'Self-Employed Status',
            'Firm Size', 'Family History', 'Comments'])
            #st.write(finished_df)

            finished_df.columns = ['Age', 'Gender', 'state', 'self_employed', 'no_employees',
       'family_history', 'comments']

            inference_df = model_clean(finished_df)
            predicted_value = rf.predict(inference_df)[0]

            if predicted_value == 0:
                predicted_value = "Needs Treatment"
            else:
                predicted_value =  "Generally doesn't need treatment"
            st.text(predicted_value)
        else:
            st.text('Press "Submit to see results"')




# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )

