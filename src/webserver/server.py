import streamlit as st
import subprocess
from pprint import pprint
import base64
from io import StringIO

# the dot_string field on session_state will hold the dot we want to render
if "dot_string" not in st.session_state:
    st.session_state["dot_string"] = ""
    
def svg_write(svg_string, center=True):
    """
    Draw an SVG in the browser window.  "center=True" causes the
    figure to be centered in the window; False causes left alignment.
    """
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


def text_area_change():
    st.session_state["dot_string"] = st.session_state["_dot_text"]


def file_upload_change():
    
    st.session_state["dot_string"] = st.session_state["_dot_text"]
    uploaded_file = st.session_state["_dot_file"]
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        dot_string = stringio.read()
        st.session_state["dot_string"] = dot_string


def main():
    """
    Draw the page
    """

    st.title("Graph Renderer")
    tab1, tab2 = st.tabs(["Write And Render", "Render A Dot File"])
    with tab1:
        st.text_area("Dot Language To Render",
                     key="_dot_text",
                     on_change=text_area_change)
    with tab2:
        st.file_uploader("Choose a dot file",
                         type="dot",
                         key="_dot_file",
                         on_change=file_upload_change)

    layout_engine = st.selectbox("layout engine",
                                 ["dot", "neato", "twopi",
                                  "circo", "fdp", "sfdp",
                                  "osage", "patchwork"])
    action = st.radio("What do you want to do?", ["render dot",
                                                  "layout only",
                                                  "layout only (xdot)",
                                                  "render but do not layout"],
                      label_visibility="collapsed")
    if st.session_state["dot_string"]:
        if action == "render dot":
            cmd_l = [f"{layout_engine}", "-Tsvg"]
            rslt = subprocess.run(cmd_l,
                                  input=st.session_state["dot_string"].encode(),
                                  capture_output=True)
            if rslt.returncode:
                st.error(f"An error occurred: {rslt.stderr.decode()}")
            else:
                svg_write(rslt.stdout.decode())
        elif action == "layout only":
            cmd_l = [f"{layout_engine}", "-Tdot"]
            rslt = subprocess.run(cmd_l,
                                  input=st.session_state["dot_string"].encode(),
                                  capture_output=True)
            if rslt.returncode:
                st.error(f"An error occurred: {rslt.stderr.decode()}")
            else:
                st.write(rslt.stdout.decode())
        elif action == "layout only (xdot)":
            cmd_l = [f"{layout_engine}", "-Txdot"]
            rslt = subprocess.run(cmd_l,
                                  input=st.session_state["dot_string"].encode(),
                                  capture_output=True)
            if rslt.returncode:
                st.error(f"An error occurred: {rslt.stderr.decode()}")
            else:
                st.write(rslt.stdout.decode())
        elif action == "render but do not layout":
            cmd_l = ["neato", "-n2", "-Tsvg"]
            rslt = subprocess.run(cmd_l,
                                  input=st.session_state["dot_string"].encode(),
                                  capture_output=True)
            if rslt.returncode:
                st.error(f"An error occurred: {rslt.stderr.decode()}")
            else:
                svg_write(rslt.stdout.decode())
        else:
            st.error(f"Unknown action {action}")

if __name__ == "__main__":
    main()
