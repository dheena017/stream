
from playwright.sync_api import sync_playwright, expect
import os

def test_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            # Navigate to app
            page.goto("http://localhost:8501")

            # Wait for app to load
            page.wait_for_load_state("networkidle")

            # Login Flow
            print("Checking for Login...")
            username_input = page.get_by_placeholder("Enter email or username")
            if username_input.is_visible():
                print("Logging in...")
                username_input.fill("admin")
                page.get_by_placeholder("Enter password").fill("admin123")

                login_btn = page.get_by_role("button", name="🔐 Login", exact=True)
                login_btn.click()

                # Wait for reload
                page.wait_for_timeout(3000)

            # Navigate to Chat Page
            print("Navigating to Chat Page...")
            # Using get_by_role might trigger the button.
            # Looking at sidebar.py: if st.button("💬 Chat", ...)
            chat_nav_btn = page.get_by_role("button", name="💬 Chat")
            chat_nav_btn.click()

            page.wait_for_timeout(3000)

            # Check if Welcome Screen exists
            print("Checking Welcome Screen...")
            welcome = page.get_by_text("Welcome back")
            expect(welcome).to_be_visible(timeout=20000)

            # Check for buttons in Welcome Screen
            print("Checking Welcome Buttons...")
            # Try partial text
            btn = page.get_by_role("button", name="🚀 Explain Quantum Computing")
            expect(btn).to_be_visible()

            # Check Sidebar
            print("Checking Sidebar...")
            control_panel = page.get_by_text("Control Panel")
            expect(control_panel).to_be_visible()

            # Check Model Selection (grouped)
            print("Checking Model Selection...")
            model_selection = page.get_by_text("Model Selection")
            expect(model_selection).to_be_visible()

            # Take Screenshot
            os.makedirs("verification", exist_ok=True)
            page.screenshot(path="verification/ui_verification.png", full_page=True)
            print("Screenshot saved to verification/ui_verification.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error_screenshot.png", full_page=True)
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    try:
        test_ui()
        print("Verification Successful")
    except Exception as e:
        print(f"Verification Failed")
        exit(1)
