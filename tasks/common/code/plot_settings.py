# Shih-Hsuan Hsu
# April 15, 2024
# This script set the default behavior of plotly to simple_white.

import itertools
import pikepdf
from pyparsing import Iterator
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

COLOR_SCALE = "Inferno"
"""color scale for the scatter plot"""

DEFAULT_WIDTH = 960
"""default width of the figure"""
DEFAULT_HEIGHT = 540
"""default height of the figure"""
DEFAULT_WIDTH2 = 800
"""default width of the figure"""
DEFAULT_HEIGHT2 = 600
"""default height of the figure"""
IMAGE_FORMATS = ["pdf", "html"]
"""image formats"""
# set the default scale of the image
SCALE = 1.5

INDICATOR_COLOR_SCALE = [
    (0, "#6a9f58"),
    (0.5, "#ffff99"),
    (1, "#d1615d"),
]
"""color scale for the indicator choropleth map"""

RECESSION_COLOR = "lightgray"
"""color for the recession area"""

LINE_OPACITY = 0.8
"""opacity for the line"""
CI_OPACITY = 0.2
"""opacity for the confidence interval"""

CUSTOM_TEMPLATE = {
    "layout": {
        "font": {
            "size": 18,
            "family": "Arial",
        },
        "legend": {
            "font": {
                "size": 16,
                "color": "black",
                "family": "Arial",
            },
            "traceorder": "normal",
        },
        "margin": {"l": 20, "r": 20, "t": 35, "b": 20},
        "yaxis": {"color": "black", "showgrid": True},
        "xaxis": {"color": "black", "showgrid": True},
        "title": {
            "font": {
                "color": "black",
                "family": "Arial",
            },
        },
    },
    "data": {
        "scatter": [
            go.Scatter(
                line={"width": 4}, marker={"size": 6}, opacity=LINE_OPACITY
            )
        ],
        "scattergl": [
            go.Scattergl(
                line={"width": 6}, marker={"size": 8}, opacity=LINE_OPACITY
            )
        ],
    },
}
"""custom template for the plots (16 by 9 aspect ratio)"""
CUSTOM_TEMPLATE_32 = CUSTOM_TEMPLATE.copy()
"""custom template for the plots (3 by 2 aspect ratio)"""
CUSTOM_TEMPLATE_32["layout"]["font"]["size"] += 4
CUSTOM_TEMPLATE_32["layout"]["legend"]["font"]["size"] += 4
CUSTOM_TEMPLATE_32["data"]["scatter"][0]["line"]["width"] += 1
CUSTOM_TEMPLATE_32["data"]["scattergl"][0]["line"]["width"] += 1
CUSTOM_TEMPLATE_32["data"]["scatter"][0]["marker"]["size"] += 1
CUSTOM_TEMPLATE_32["data"]["scattergl"][0]["marker"]["size"] += 1


# modification of the default template
pio.templates["my_mod"] = go.layout.Template(CUSTOM_TEMPLATE)
pio.templates["my_mod_32"] = go.layout.Template(CUSTOM_TEMPLATE_32)

# set the default template
pio.templates.default = "simple_white+my_mod"

COLORS = [
    (0, 114, 178),  # Blue
    (230, 159, 0),  # Orange
    (204, 121, 167),  # Magenta
    (0, 158, 115),  # Green
    (240, 228, 66),  # Yellow
    (213, 94, 0),  # Vermillion
    (86, 180, 233),  # Sky Blue
    (148, 148, 148),  # Gray
]
"""List of colors in RGB format. From: https://siegal.bio.nyu.edu/color-palette/"""

MARKERS = [0, 2, 4, 1, 3, 17, 18, 22, 23, 24]


def color_iter() -> Iterator[tuple[str, str]]:
    """
    Return an iterator of colors.
    Returns:
        Iterator[tuple[str, str]]: An iterator of colors in rgba format for:
            - first element: main color
            - second element: confidence intervals
    """
    while True:  # cycle through colors indefinitely
        for color in COLORS:
            r, g, b = color
            # yield main color and confidence interval color
            yield (
                f"rgba({r}, {g}, {b}, 1.0)",
                f"rgba({r}, {g}, {b}, {CI_OPACITY})",
            )


def marker_iter() -> Iterator[int]:
    """
    Return an iterator of marker symbols.
    """
    return itertools.cycle(MARKERS)


def remove_pdf_metadata(filepath: str) -> None:
    """Aggressively remove all variable metadata from PDF."""
    with pikepdf.open(filepath, allow_overwriting_input=True) as pdf:
        # Remove XMP metadata
        with pdf.open_metadata(
            set_pikepdf_as_editor=False, update_docinfo=False
        ) as meta:
            meta.clear()

        # Remove Info dictionary entirely
        if "/Info" in pdf.trailer:
            del pdf.trailer["/Info"]

        # Remove ID array (contains unique identifiers)
        if "/ID" in pdf.trailer:
            del pdf.trailer["/ID"]

        # Remove Metadata stream from catalog
        if "/Metadata" in pdf.Root:
            del pdf.Root["/Metadata"]

        # Save without compression variations
        pdf.save(
            filepath,
            linearize=False,  # Disable linearization (web optimization)
            compress_streams=True,
            stream_decode_level=pikepdf.StreamDecodeLevel.generalized,
            deterministic_id=True,
        )


def save_figure(
    fig: go.Figure,
    name: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    two_aspect_ratio: bool = False,
    width2: int = DEFAULT_WIDTH2,
    height2: int = DEFAULT_HEIGHT2,
) -> None:
    """
    Save the figure as the `IMAGE_FORMATS` file to `../output/` with the given file name.
    """
    for format in IMAGE_FORMATS:
        if format == "html":
            # Save with a fixed plotly.js version for consistency
            fig.write_html(
                f"../output/{name}.html",
                include_plotlyjs="cdn",  # Fixed version
                config={"displayModeBar": False},
                auto_open=False,
                div_id="plot",  # Fixed div ID instead of random
            )
        else:
            fig.write_image(
                f"../output/{name}.{format}",
                width=width,
                height=height,
                engine="kaleido",  # Explicitly specify engine for consistency
            )
            if two_aspect_ratio:
                fig.update_layout(template="simple_white+my_mod_32")
                fig.write_image(
                    f"../output/{name}_2.{format}",
                    width=width2,
                    height=height2,
                    engine="kaleido",
                )
            if format.lower() == "pdf":
                print(f"Removing metadata from ../output/{name}.{format}")
                remove_pdf_metadata(f"../output/{name}.{format}")
                if two_aspect_ratio:
                    remove_pdf_metadata(f"../output/{name}_2.{format}")


def construct_shapes(
    df: pd.DataFrame,
    col_name: str,
    date_name: str,
    xref: str = "x",
    yref: str = "paper",
) -> list[dict]:
    """
    Construct shapes for the recession periods.
    """
    recession_periods = df[col_name].ne(df[col_name].shift()).cumsum()
    groups = df[df[col_name] == 1].groupby(recession_periods)
    return [
        {
            "type": "rect",
            "x0": group[date_name].iloc[0],
            "x1": group[date_name].iloc[-1],
            "y0": 0,
            "y1": 1,
            "xref": xref,
            "yref": yref,
            "fillcolor": RECESSION_COLOR,
            "opacity": 0.5,
            "layer": "below",
            "line_width": 0,
        }
        for _, group in groups
        if not group.empty
    ]


def move_legend_to_bottom(
    fig: go.Figure,
    y_position_padding: float = 0.0,
    additional_settings: dict = {},
) -> None:
    """
    Move the legend to the bottom of the figure with specified y position.
    Args:
        fig (go.Figure): The figure to modify.
        y_position_padding (float): The padding to adjust the y position of the legend. Default is 0.0.
    """
    fig.update_layout(
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.3 + y_position_padding,
            "xanchor": "center",
            "x": 0.5,
            "traceorder": "normal",
            **additional_settings,
        }
    )
