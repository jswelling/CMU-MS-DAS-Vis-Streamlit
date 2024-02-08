import streamlit as st
import subprocess
from pprint import pprint
import base64
from io import StringIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_svg import FigureCanvasSVG


def draw_matplotlib_figure(fig, axes, label="",
                           spines=True, log_scale=False):
    """
    This is completely normal matplotlib code.
    """
    axes.plot([0.0, 1.0, 2.0, 3.0], [0.0, 1.0, 4.0, 9.0])

    if not spines:
        # Hide the right and top spines
        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        axes.yaxis.set_ticks_position('left')
        axes.xaxis.set_ticks_position('bottom')
        
    if log_scale:
        axes.set_yscale('log')

    if label != "":
        axes.set_title(label)


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


def main():
    """
    Draw the page
    """

    st.title("Curve Renderer")
    label_text = st.text_input(label="Graph Label")
    show_spine = st.radio("Show Graph Spine", [True, False])
    log_scale = st.radio("Log Scale", [True, False], index=1)

    # Note that we have to avoid saying 'plt.subplots' because
    # matplotlib.pyplot is not thread-safe. This works, though.
    # The Figure provides SVG support because of our imports.
    fig = Figure()
    axes = fig.subplots()
    draw_matplotlib_figure(fig, axes,
                           label=label_text,
                           spines=show_spine,
                           log_scale=log_scale)
    image_holder = StringIO()
    FigureCanvasSVG(fig).print_svg(image_holder)
    svg_write(image_holder.getvalue())

if __name__ == "__main__":
    main()
