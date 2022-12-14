import streamlit as st
from streamlit_ace import st_ace
from utils.utils import create_expander, execute_and_clear

i = 1
for widget in [
    "Columns",
    "Download and upload data",
    "Expander",
    "Form",
    "Metric",
    "Dataframe and chart",
    "Useful external librairies",
]:
    create_expander(widget, i)
    i = i + 1

st.subheader("Editor")
content = st_ace(
    language="python",
    theme="twilight",
    keybinding="vscode",
    key="ace",
)

if content:
    with open("ace_code/generated_code.py", "w") as f:
        f.write(content)

    st.markdown("""---""")
    with st.container():
        execute_and_clear("ace_code/generated_code.py")
