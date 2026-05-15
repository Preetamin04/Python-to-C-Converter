import streamlit as st

st.set_page_config(layout="wide", page_title="Python to C Converter")

from main import run_compiler

# Hide menu
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("Python to C Converter")

# Initialize session state
if "code" not in st.session_state:
    st.session_state.code = ""

if "converted" not in st.session_state:
    st.session_state.converted = False

if "filename" not in st.session_state:
    st.session_state.filename = "manual_input"

# Upload file
uploaded_file = st.file_uploader("Upload .py file", type=["py"])

if uploaded_file is not None:

    # Read uploaded file
    file_content = uploaded_file.read().decode("utf-8")

    # Store code
    st.session_state.code = file_content

    # Store uploaded filename (without extension)
    st.session_state.filename = uploaded_file.name.split(".")[0]

# Text editor
st.session_state.code = st.text_area(
    "Enter Python Code",
    value=st.session_state.code,
    height=300
)

# Ask user for output filename
custom_filename = st.text_input(
    "Enter Output Filename (optional)",
    placeholder="Leave empty to use uploaded filename or manual_input"
)

# Convert button
if st.button("Convert"):

    if not st.session_state.code.strip():
        st.error("No code provided")

    else:

        # Decide final filename
        if custom_filename.strip():

            # User entered filename
            final_filename = custom_filename.strip()

        elif uploaded_file is not None:

            # Use uploaded filename
            final_filename = uploaded_file.name.split(".")[0]

        else:

            # Default filename when no upload + no custom name
            final_filename = "manual_input"

        # Run compiler
        result, path = run_compiler(
            st.session_state.code,
            final_filename
        )

        if path is None:
            st.error(result)
            st.session_state.converted = False

        else:
            st.session_state.c_code = result
            st.session_state.converted = True
            st.session_state.final_filename = final_filename

# Show output
if st.session_state.converted:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Python Code")

        st.code(st.session_state.code, language="python")

        st.download_button(
            "Download Python File",
            data=st.session_state.code,
            file_name=f"{st.session_state.final_filename}.py"
        )

    with col2:
        st.subheader("C Code")

        st.code(st.session_state.c_code, language="c")

        st.download_button(
            "Download C File",
            data=st.session_state.c_code,
            file_name=f"{st.session_state.final_filename}.c"
        )