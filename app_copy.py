import streamlit as st

# title, header, subheader, markdown, caption, code, expanders
# onclick: button, checkbox, radio, slider
# columns
# file upload and download
# form (to delay execution on submit)
# metrics

# CACHING
# st.experimental_memo() pour load initial
# SESSION STATE
# MULTIPAGE
# THEME


st.title('Hello World')
st.markdown(
    "Creating a Streamlit app is very easy. The only thing to do is to create a `filename.py`"
    " file containing your Streamlit code and run it from your terminal with "
    "`streamlit run filename.py`"
)
st.header("This is a header")
st.subheader("This is a subheader")
st.markdown(
    "You can write Markdown in Streamlit and use all classical features "
    "like _italic_ or **bold**. You can even write code blocks:"
)
code = """def streamlit_training(a: int, b: int):
    c = a + b
return c"""
st.code(body=code, language="python")

if st.button("See this code in <Scala>"):
    st.code(body=code, language="scala")

if st.button("See this code in <Java>"):
    st.code(body=code, language="java")
st.caption("Above is a code block example")

st.markdown('Better yet - Select your favorite language')
p, s, j = "python", "scala", "java"
def checkbox():
    checkbox_py = st.checkbox(f"{p.title()}")
    checkbox_sc = st.checkbox(f"{s.title()}")
    checkbo_jv = st.checkbox(f"{j.title()}")

    if checkbox_py:
        st.code(body=code, language=p)
    elif checkbox_sc:
        st.code(body=code, language=s)
    elif checkbo_jv:
        st.code(body=code, language=j)
    else:
        pass
checkbox()

st.markdown('Even Better - Radio Buttons!')
def radio_buttons():
    fav_lang = st.radio("Select your favorite language:", (p, s, j))
    if fav_lang == p:
        st.code(body=code, language=p)
    elif fav_lang == s:
        st.code(body=code, language=s)
    elif fav_lang == j:
        st.code(body=code, language=j)
    else:
        st.write("you didnt select anything")
radio_buttons()

st.header('have a play with columns')
def dynamic_columning():
    with st.expander("See what we'll try"):
        st.write("Dynamically change image sixe based on user input")

    st.subheader("Equal size columns")
    col2, col3 = st.columns(2)
    image_size_slider = col3.slider("Size of the image", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
    col2.image("https://static.streamlit.io/examples/dog.jpg", width=int(image_size_slider * 100))
dynamic_columning()
