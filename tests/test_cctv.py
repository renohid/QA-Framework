import re
from pages.home_page import HomePage
from playwright.sync_api import expect

def test_map_initialization(home_page: HomePage):
    """Scenario 1: Verify homepage loads and Leaflet map container renders."""
    home_page.load()
    expect(home_page.page).to_have_title(re.compile(r"CCTV", re.IGNORECASE))
    home_page.verify_map_is_visible()

def test_district_filter(home_page: HomePage):
    """Scenario 2: Select 'BLIMBING' from the district combobox."""
    home_page.load()
    home_page.verify_map_is_visible()
    
    home_page.filter_by_blimbing()
    
    # Assert that the visible text of the selected option is 'BLIMBING'
    expect(home_page.selected_option).to_have_text("BLIMBING")

def test_cctv_stream_modal(home_page: HomePage):
    """Scenario 3: Click a map marker to trigger a camera popup/modal."""
    home_page.load()
    home_page.verify_map_is_visible()

    home_page.filter_by_blimbing()
    
    home_page.open_first_cctv_stream()
    home_page.verify_video_modal_is_visible()