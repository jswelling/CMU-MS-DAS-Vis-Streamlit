import streamlit as st
import subprocess
from pprint import pprint
import base64
from io import StringIO

def svg_write(svg_string, center=True):
    # Encode as base 64
    b64 = base64.b64encode(svg_string.encode("utf-8")).decode("utf-8")

    # Add some CSS on top
    css_justify = "center" if center else "left"
    css = '<p style="text-align:center; display: flex; justify-content: {};">'.format(css_justify)
    html = r'{}<img src="data:image/svg+xml;base64,{}"/>'.format(
        css, b64
    )

    # Write the HTML
    st.write(html, unsafe_allow_html=True)

st.title('Graph Renderer')
tab1, tab2 = st.tabs(["Write And Render", "Render A Dot File"])
dot_string = None
with tab1:
    dot_string = st.text_area('Dot Language To Render')
with tab2:
    uploaded_file = st.file_uploader("Choose a dot file",
                                     type="dot")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        dot_string = stringio.read()

layout_engine = st.selectbox('layout engine',
                             ['dot', 'neato', 'twopi',
                              'circo', 'fdp', 'sfdp',
                              'osage', 'patchwork'])
action = st.radio('What do you want to do?', ['render dot',
                                              'render but do not layout',
                                              'layout only'],
                  label_visibility='collapsed')
st.write(dot_string)
if dot_string:
    cmd_l = [f"{layout_engine}", "-Tsvg"]
    rslt = subprocess.run(cmd_l,
                          input=dot_string.encode(),
                          capture_output=True)
    if rslt.returncode:
        st.error(f"An error occurred: {rslt.stderr.decode()}")
    else:
        svg_write(rslt.stdout.decode())
