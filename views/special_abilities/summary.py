import streamlit as st

def generate_pill_label(text):
    pill_html = f"""
    <style>
    .pill {{
        margin: 2px;
        display: inline-block;
        padding: 0px 10px;
        border-radius: 15px;
        background-color: #0d6efd;
        color: white;
        font-size: 14px;
        line-height: 22px;
    }}
    </style>
    <span class="pill">{text}</span>
    """
    return pill_html

def show(special_abilities):
    container = st.container()
    container.write("Special abilities:")

    # Iterate through each ability in the passed special_abilities dict
    for ability, details in special_abilities.items():
        # Check if the ability's value is greater than 0 or True (for boolean values)
        if details['value'] > 0 or (isinstance(details['value'], bool) and details['value']):
            # Replace (X) or (+X) with the actual value
            formatted_label = details['label'].replace('(X)', f'({details["value"]})').replace('(+X)', f'(+{details["value"]})')
            # Display each relevant ability as a pill
            container.markdown(generate_pill_label(formatted_label), unsafe_allow_html=True)