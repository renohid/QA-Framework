from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://cctv.malangkota.go.id/"
        
        # Locators
        self.map_container = self.page.locator(".leaflet-container")
        self.district_select = self.page.get_by_role("combobox")
        self.selected_option = self.page.locator("#kecamatan-dropdown option:checked")
        self.cctv_marker = self.page.locator("img.leaflet-marker-icon").first
        self.lihat_detail_btn = self.page.get_by_role("button", name="Lihat Detail").first
        self.video_modal = self.page.get_by_role("heading", name="Stream Camera")

    def load(self):
        self.navigate(self.url)

    def verify_map_is_visible(self):
        expect(self.map_container).to_be_visible(timeout=10000)

    def filter_by_blimbing(self):
        # Select specifically using the visible label 
        self.district_select.select_option(label="BLIMBING")
        self.page.wait_for_timeout(1000)

    def open_first_cctv_stream(self):
        # 1. Click the pin on the map
        self.cctv_marker.wait_for(state="attached")
        self.cctv_marker.evaluate("node => node.click()")

        # 2. Click the "Lihat Detail" button in the popup
        self.lihat_detail_btn.wait_for(state="visible")
        self.lihat_detail_btn.click()
        
    def verify_video_modal_is_visible(self):
        expect(self.video_modal).to_be_visible(timeout=10000)