import os
import time
from playwright.sync_api import sync_playwright, expect

def test_export_chat():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Login
        print("Navigating to app...")
        page.goto("http://localhost:8501")

        # Wait for app to load
        print("Waiting for login inputs...")
        try:
            # Use role textbox which is more specific than label
            page.wait_for_selector('input[aria-label="Email or Username"]', timeout=30000)
        except Exception:
             page.reload()
             page.wait_for_selector('input[aria-label="Email or Username"]', timeout=30000)

        # Fill login
        # Use get_by_role to avoid ambiguity with Help buttons
        page.get_by_role("textbox", name="Email or Username").fill("admin")

        # Password
        # Password inputs usually don't have role="textbox".
        # We can use get_by_label with exact=True if available, or fallback to locator.
        # But wait, there are TWO password fields (Login and Register).
        # We want the one in the Login tab.
        # We can narrow down by the Login tab container if possible,
        # or just assume the first one is login.
        # Use locator with aria-label directly to be precise.
        password_inputs = page.locator('input[aria-label="Password"]')
        # Expect at least one
        expect(password_inputs.first).to_be_visible()
        password_inputs.first.fill("admin123")

        print("Clicking login...")
        page.get_by_role("button", name="🔐 Login").click()

        # Wait for main app
        print("Waiting for dashboard...")
        expect(page.get_by_text("Control Panel")).to_be_visible(timeout=30000)

        # 3. Open Export Popover
        print("Opening Export popover...")
        export_btn = page.get_by_role("button", name="💾 Export")
        expect(export_btn).to_be_visible()
        export_btn.click()

        # Wait for popover content
        time.sleep(1)

        # 4. Check for Download buttons
        print("Verifying download buttons...")
        expect(page.get_by_role("button", name="📄 Download as Text")).to_be_visible()
        expect(page.get_by_role("button", name="📦 Download as JSON")).to_be_visible()

        # 5. Take Screenshot
        page.screenshot(path="verification/verification.png")
        print("Screenshot saved to verification/verification.png")

        browser.close()

if __name__ == "__main__":
    test_export_chat()
