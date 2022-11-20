import streamlit as st
from streamlit_ace import st_ace

from utils.persist import persist
from utils.utils import execute_and_clear

st.markdown(
    "This page allows you to directly type Streamlit code and execute it without having to start "
    "with `import streamlit as st`. "
    "You can test any new element you have learned during this training "
    "(and keep track of the ones you tried out in the below section). "
)

st.markdown(
    "Beginner and intermediate exercises can even be done there, but don't hesitate "
    "and try building your own Python file and launch it from your terminal."
)

with st.expander("Elements tested", expanded=True):
    cols = st.columns(3)
    cols[0].markdown("**Beginner**")
    for box in (
        "Text",
        "Button",
        "Checkbox",
        "Radio",
        "Select",
        "Slider",
        "Input",
        "Media",
    ):
        cols[0].checkbox(box, key=persist(box))

    cols[1].markdown("**Intermediate**")
    for box in (
        "Columns",
        "Load data",
        "Expander",
        "Form",
        "Metric",
        "Dataframe and charts",
        "Pandas profiling",
        "Lottie",
        "Aggrid",
    ):
        cols[1].checkbox(box, key=persist(box))

    cols[2].markdown("**Advanced**")
    cols[2].checkbox("Session state", key=persist("sessionstate"))
    for box in ("Theme", "Cache", "Multipages", "Access a PR keyvault", "Leon"):
        cols[2].checkbox(box, key=persist(box))

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
