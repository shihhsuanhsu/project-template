# Shih-Hsuan Hsu
# April 15, 2024
# This script set the default behavior of plotly to simple_white.

import itertools
import plotly.io as pio
import plotly.graph_objects as go

COLOR_SCALE = "Inferno"
"""color scale for the scatter plot"""

MARKER_SIZE = 8
"""size of the marker"""

DEAFULT_WIDTH = 960
"""default width of the figure"""
DEFAULT_HEIGHT = 540
"""default height of the figure"""
DEAFULT_WIDTH2 = 800
"""default width of the figure"""
DEFAULT_HEIGHT2 = 600
"""default height of the figure"""
IMAGE_FORMATS = ["pdf", "html"]
"""image formats"""

INDICATOR_COLOR_SCALE = [
    (0, "#6a9f58"),
    (0.5, "#ffff99"),
    (1, "#d1615d"),
]
"""color scale for the indicator choropleth map"""

RECESSION_COLOR = "lightgray"
"""color for the recession area"""

# modification of the default template
pio.templates["my_mod"] = go.layout.Template(
    layout={
        "font": {
            "size": 16,
            "family": "Roboto",
        },
        "legend": {
            "font": {"size": 12, "color": "black"},
            "traceorder": "normal",
        },
        "margin": {"l": 20, "r": 20, "t": 35, "b": 20},
        "yaxis": {"color": "black", "showgrid": True},
        "xaxis": {"color": "black", "showgrid": True},
        "title": {
            "font": {
                "color": "black",
            }
        },
    }
)

# set the default template
pio.templates.default = "simple_white+my_mod"

# set the default scale of the image
SCALE = 1.5

# colors for line and CI
COLORS = [
    ("rgba(31, 119, 180, 1)", "rgba(31, 119, 180, 0.2)"),  # Blue
    ("rgba(255, 127, 14, 1)", "rgba(255, 127, 14, 0.2)"),  # Orange
    ("rgba(214, 39, 40, 1)", "rgba(214, 39, 40, 0.2)"),  # Red
    ("rgba(44, 160, 44, 1)", "rgba(44, 160, 44, 0.2)"),  # Green
    ("rgba(148, 103, 189, 1)", "rgba(148, 103, 189, 0.2)"),  # Purple
    ("rgba(140, 86, 75, 1)", "rgba(140, 86, 75, 0.2)"),  # Brown
    ("rgba(227, 119, 194, 1)", "rgba(227, 119, 194, 0.2)"),  # Pink
    # ('rgba(127, 127, 127, 1)', 'rgba(127, 127, 127, 0.2)'),  # Gray
    ("rgba(188, 189, 34, 1)", "rgba(188, 189, 34, 0.2)"),  # Olive
    ("rgba(23, 190, 207, 1)", "rgba(23, 190, 207, 0.2)"),  # Cyan
    ("rgba(255, 187, 120, 1)", "rgba(255, 187, 120, 0.2)"),  # Light Orange
    ("rgba(152, 223, 138, 1)", "rgba(152, 223, 138, 0.2)"),  # Light Green
    ("rgba(255, 152, 150, 1)", "rgba(255, 152, 150, 0.2)"),  # Light Red
    ("rgba(197, 176, 213, 1)", "rgba(197, 176, 213, 0.2)"),  # Light Purple
    ("rgba(196, 156, 148, 1)", "rgba(196, 156, 148, 0.2)"),  # Light Brown
    ("rgba(247, 182, 210, 1)", "rgba(247, 182, 210, 0.2)"),  # Light Pink
    ("rgba(199, 199, 199, 1)", "rgba(199, 199, 199, 0.2)"),  # Light Gray
    ("rgba(219, 219, 141, 1)", "rgba(219, 219, 141, 0.2)"),  # Light Olive
    ("rgba(158, 218, 229, 1)", "rgba(158, 218, 229, 0.2)"),  # Light Cyan
    ("rgba(255, 205, 86, 1)", "rgba(255, 205, 86, 0.2)"),  # Yellow
    ("rgba(75, 192, 192, 1)", "rgba(75, 192, 192, 0.2)"),  # Teal
    ("rgba(255, 99, 132, 1)", "rgba(255, 99, 132, 0.2)"),  # Coral
    ("rgba(153, 102, 255, 1)", "rgba(153, 102, 255, 0.2)"),  # Lavender
    ("rgba(255, 159, 64, 1)", "rgba(255, 159, 64, 0.2)"),  # Orange-Yellow
    ("rgba(54, 162, 235, 1)", "rgba(54, 162, 235, 0.2)"),  # Sky Blue
    ("rgba(201, 203, 207, 1)", "rgba(201, 203, 207, 0.2)"),  # Light Blue Gray
    ("rgba(255, 204, 204, 1)", "rgba(255, 204, 204, 0.2)"),  # Light Pink-Red
    ("rgba(204, 235, 197, 1)", "rgba(204, 235, 197, 0.2)"),  # Light Mint
    ("rgba(222, 203, 228, 1)", "rgba(222, 203, 228, 0.2)"),  # Light Lavender
    ("rgba(255, 255, 179, 1)", "rgba(255, 255, 179, 0.2)"),  # Light Yellow
    ("rgba(128, 222, 234, 1)", "rgba(128, 222, 234, 0.2)"),  # Light Teal
    ("rgba(255, 153, 204, 1)", "rgba(255, 153, 204, 0.2)"),  # Light Coral
    (
        "rgba(204, 204, 255, 1)",
        "rgba(204, 204, 255, 0.2)",
    ),  # Light Lavender-Blue
    (
        "rgba(255, 204, 153, 1)",
        "rgba(255, 204, 153, 0.2)",
    ),  # Light Orange-Yellow
    ("rgba(153, 204, 255, 1)", "rgba(153, 204, 255, 0.2)"),  # Light Sky Blue
    ("rgba(229, 229, 229, 1)", "rgba(229, 229, 229, 0.2)"),  # Light Gray-White
    ("rgba(255, 229, 229, 1)", "rgba(255, 229, 229, 0.2)"),  # Light Pink-White
    ("rgba(229, 255, 229, 1)", "rgba(229, 255, 229, 0.2)"),  # Light Mint-White
    (
        "rgba(242, 229, 255, 1)",
        "rgba(242, 229, 255, 0.2)",
    ),  # Light Lavender-White
    (
        "rgba(255, 255, 229, 1)",
        "rgba(255, 255, 229, 0.2)",
    ),  # Light Yellow-White
    ("rgba(204, 255, 255, 1)", "rgba(204, 255, 255, 0.2)"),  # Light Cyan-White
    ("rgba(255, 229, 242, 1)", "rgba(255, 229, 242, 0.2)"),  # Light Coral-White
    (
        "rgba(229, 229, 255, 1)",
        "rgba(229, 229, 255, 0.2)",
    ),  # Light Lavender-Blue-White
    (
        "rgba(255, 242, 229, 1)",
        "rgba(255, 242, 229, 0.2)",
    ),  # Light Orange-Yellow-White
    (
        "rgba(229, 242, 255, 1)",
        "rgba(229, 242, 255, 0.2)",
    ),  # Light Sky Blue-White
]


def color_iter():
    """
    Return an iterator of colors.
    """
    return itertools.cycle(COLORS)


def marker_iter():
    """
    Return an iterator of marker symbols.
    """
    return itertools.cycle([0, 2, 4, 1, 3, 17, 18, 22, 23, 24])


def save_figure(
    fig: go.Figure,
    name: str,
    width: int = DEAFULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    two_aspect_ratio: bool = False,
    width2: int = DEAFULT_WIDTH2,
    height2: int = DEFAULT_HEIGHT2,
) -> None:
    """
    Save the figure as the `IMAGE_FORMATS` file to `../output/` with the given file name.
    """
    for format in IMAGE_FORMATS:
        if format == "html":
            fig.write_html(f"../output/{name}.html")
        else:
            fig.write_image(
                f"../output/{name}.{format}", width=width, height=height
            )
            if two_aspect_ratio:
                fig.write_image(
                    f"../output/{name}_2.{format}", width=width2, height=height2
                )
