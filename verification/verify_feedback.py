import os
import time
from playwright.sync_api import sync_playwright

def verify_feedback_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the app
        print("Navigating to app...")
        page.goto("http://localhost:8501")

        page.wait_for_timeout(2000)

        # Check if login is required
        if page.get_by_text("Sign In").count() > 0 or page.get_by_text("Login").count() > 0:
            print("Login page detected. Logging in...")

            # Username
            page.get_by_role("textbox").nth(0).fill("admin")

            # Password
            # Use .first to pick the one in the active tab (Login)
            page.get_by_role("textbox", name="Password").first.fill("admin123")

            # Click Login button
            if page.get_by_role("button", name="Sign In").count() > 0:
                page.get_by_role("button", name="Sign In").first.click()
            else:
                 page.get_by_role("button", name="Login").first.click()

            print("Login submitted...")
            page.wait_for_timeout(3000)

        # Wait for the sidebar to load
        print("Waiting for sidebar...")
        try:
            page.wait_for_selector("[data-testid='stSidebar']", timeout=10000)
        except Exception as e:
            print(f"Sidebar not found: {e}")
            page.screenshot(path="verification/error_sidebar.png")
            raise e

        # Click on "Feedback" button in the sidebar
        print("Clicking Feedback button...")
        try:
            # Scope to sidebar
            sidebar = page.locator("[data-testid='stSidebar']")
            feedback_btn = sidebar.get_by_role("button", name="📣 Feedback")
            feedback_btn.click()
        except Exception as e:
            print(f"Feedback button click failed: {e}")
            page.screenshot(path="verification/error_click.png")
            raise e

        # Wait for the Feedback page header
        print("Waiting for Feedback page...")
        page.wait_for_timeout(2000) # Give streamlit time to rerun

        # Check for "Feedback Center" text
        content = page.content()
        if "Feedback Center" not in content:
            print("Feedback Center header not found!")
            page.screenshot(path="verification/error_header.png")
            # Maybe we are still on dashboard?
        else:
            print("Feedback Center found.")

        # Take a screenshot of the feedback page
        page.screenshot(path="verification/feedback_page.png")

        # Fill out the form
        print("Filling form...")
        try:
            # First textarea
            # Use .last because sometimes there are hidden textareas or something
            page.get_by_role("textbox", name="Details").last.fill("Test feedback via Playwright")

            # Submit
            print("Submitting...")
            # There might be multiple buttons, ensure we get the form submit button
            page.get_by_role("button", name="Submit Feedback").click()

            # Wait for success message
            page.wait_for_timeout(2000)
            page.screenshot(path="verification/feedback_submitted.png")
            print("Done.")
        except Exception as e:
            print(f"Form interaction failed: {e}")
            page.screenshot(path="verification/error_form.png")

        browser.close()

if __name__ == "__main__":
    verify_feedback_page()
