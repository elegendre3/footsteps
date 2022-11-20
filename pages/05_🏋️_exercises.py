import streamlit as st

from utils.persist import persist

st.markdown(
    "This page provides some exercises or ideas so you can try Streamlit out"
    " and improve your skills. The objective here is really that you can get your hands"
    " on Streamlit and try things, there is no right or wrong answers so feel free to"
    " create a Streamlit app with new concepts!"
)

st.markdown(
    "Beginner and intermediate exercises can even be done on the editor page, but don't hesitate "
    "and try building your own Python file and launch it from your terminal."
)

with st.expander("Ideas", expanded=True):
    cols = st.columns(3)
    cols[0].markdown("**Beginner**")
    cols[0].checkbox("Create a page with multiple widgets", key=persist("ex1"))
    cols[0].checkbox("Recursively create x sliders from a number input", key=persist("ex2"))
    cols[0].checkbox(
        "Generate a radio or a slider widget chosen from a select widget", key=persist("ex3")
    )
    cols[1].markdown("**Intermediate**")
    cols[1].checkbox(
        "Load dataframes from .csv and display them in two columns", key=persist("ex4")
    )
    cols[1].checkbox(
        "Choose columns of a dataframe to be displayed from a multiselect widget",
        key=persist("ex5"),
    )
    cols[1].checkbox("Generate metrics from a form", key=persist("ex6"))
    cols[1].checkbox("Have a Lottie GIF while loading a file to a dataframe", key=persist("ex7"))
    cols[2].markdown("**Advanced**")
    cols[2].checkbox("Load a heavy .csv to a dataframe in cache", key=persist("ex8"))
    cols[2].checkbox(
        "Load files from the datalake using the PR Python Toolbox and keyvaults",
        key=persist("ex9"),
    )
    cols[2].checkbox("Create a multipages app with session state", key=persist("ex10"))

st.subheader("Final exam")
st.markdown(
    "Also, to **pass this training**, we except that you create a simple Streamlit app described below, "
    "and successfully deploy it to Leon. We want to demonstrate how easy it is to convert "
    "an existing notebook into a Leon. "
    "To help you with Leon deployment, you can use insights from "
    "[Leon Documentation](https://webprhstreamlitdocumentationdev.azurewebsites.net/). \n"
    "Your app should include:"
)
st.markdown(
    """
    1. A sidebar with a button to upload
    [this csv](https://raw.githubusercontent.com/insaid2018/Term-1/master/Data/Casestudy/titanic_train.csv).
    2. A slider on the Age column to only keep data where people above a threshold
    3. A plot of the distribution of people by age (from the filtered data
    """  # noqa
)

st.markdown(
    "Every useful steps are described in "
    "[this notebook](https://adb-1759922713033457.17.azuredatabricks.net/?o=1759922713033457#notebook/4043684121984923/command/4043684121985497)."  # noqa
    " That way, you will see how easy it is to "  # noqa
    "go from a notebook to a Streamlit app. Make sure you open a second terminal to launch your "
    "Streamlit so you don't close this one."
)

st.markdown(
    "Here are few pieces of advice, in addition of readin the "
    "[doc](https://webprhstreamlitdocumentationdev.azurewebsites.net/):"
)

st.markdown(
    """
    1. Make sure you have created a branch with your name.
    2. Create a folder named 'my_streamlit'.
    3. Within it you need to have: \n
        3a. An 'app.py' file containing your code. \n
        3b. A 'requirements.txt' with all the dependencies needed. \n
        3c. A 'Dockerfile' (remove unnecesarly lines from the one present in this training). \n
        3d. An 'azure-pipeline.yaml' file. \n
    """
)

st.video("data/final_exam_demo.mov")
