import sys
import os

# Ensure app.py is importable from this directory
sys.path.insert(0, os.path.dirname(__file__))

from app import app


def test_header_is_present(dash_duo):
    """The H1 header element is rendered with the correct title."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")
    assert header.text == "Pink Morsel Sales Visualiser"


def test_chart_is_present(dash_duo):
    """The sales line chart is rendered on the page."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None


def test_region_picker_is_present(dash_duo):
    """The region radio button filter is rendered with all five options."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    radio = dash_duo.find_element("#region-filter")
    assert radio is not None

    # Verify all five region options are present
    options = dash_duo.find_elements("#region-filter input[type='radio']")
    assert len(options) == 5
