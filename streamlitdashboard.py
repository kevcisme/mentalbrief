import streamlit as st

#Age sidebar
age_sidebar = st.sidebar.text_input("Age", 28)


# Add a selectbox to the sidebar:
gender_sidebar = st.sidebar.selectbox(
    'What is your gender?',
    ('Female', 'Male', 'Non-Binary')
)

state_sidebar = st.sidebar.selectbox(
    'Which state do you primarily practice in?',
    ('AL','AZ','CA','CO','CT','DC','FL','GA','IA','ID','IL',
        'IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS',
        'NC','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA',
        'RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY')
    )
self_employed_sidebar = st.sidebar.selectbox(
    'Are you self-employed?',
    ('Yes', 'No')
    )

# add in boutique firm? if yes, then start
# to filter by 

firm_employee_size_sidebar = st.sidebar.selectbox(
    'How many employees does your firm employ?',
    ('1-5', '6-25',  '26-100','100-500', '500-1000','More than 1000', )
    )

family_history_sidebar = st.sidebar.selectbox(
    'Do you have a family history of mental illness?',
    ('Yes', 'No')
    )

main_panel_text_input = st.text_input(
    'Tell us about how things are going...'
    )


# if main_panel_text_input:
#     st.latex(r'''
# ...     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
# ...     \sum_{k=0}^{n-1} ar^k =
# ...     a \left(\frac{1-r^{n}}{1-r}\right)
# ...     ''')

#sidebar_inputs = [age_sidebar, gender_sidebar, state_sidebar, self_employed_sidebar]

#if 

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )

