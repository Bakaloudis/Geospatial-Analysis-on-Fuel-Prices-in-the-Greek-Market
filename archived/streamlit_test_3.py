import streamlit as st

def main():
    st.title("Streamlit App with Buttons")

    # Add buttons on the left side
    selected_option = st.sidebar.radio("Select an option", ["Option 1", "Option 2", "Option 3"])

    # Display content based on the selected option
    if selected_option == "Option 1":
        show_option_1()
    elif selected_option == "Option 2":
        show_option_2()
    elif selected_option == "Option 3":
        show_option_3()

def show_option_1():
    st.header("Option 1")
    st.write("This is the content for Option 1.")
    # Add more content specific to Option 1

def show_option_2():
    st.header("Option 2")

    # Add an additional drop-down list
    additional_option = st.sidebar.selectbox("Select an additional option", ["Option A", "Option B", "Option C"])

    st.write("This is the content for Option 2.")
    st.write(f"Additional option selected: {additional_option}")
    # Add more content specific to Option 2

def show_option_3():
    st.header("Option 3")
    st.write("This is the content for Option 3.")
    # Add more content specific to Option 3

if __name__ == "__main__":
    main()