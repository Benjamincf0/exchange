from playwright.sync_api import sync_playwright
import pandas as pd
import time

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

def scrape_course(course_code):
    url = "https://nimbus-ssl.mcgill.ca/exsa/search/searchEquivalency"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_selector("div.course-panel div:has(div span:has-text('Course Number')) input")

        # Fill in the search form (adjust selectors)
        page.locator("div.course-panel div:has(div span:has-text('Course Number')) input").fill(course_code)
        page.locator("span:has(label:has-text('Include Expired Decisions')) input[type=checkbox]").click()
        page.click("button:has-text('Search')")

        # Wait until results table body is loaded
        try:
            page.wait_for_selector("div.search-result-grid table[id*='cave'] tr.z-row", timeout=5000)

        except Exception:
            print(f"No results for course {course_code}")
            browser.close()
            return []

        prev_count = -1
        while True:
            rows = page.query_selector_all("div.search-result-grid div.search-result-grid-body table tbody.z-rows tr.z-row")
            curr_count = len(rows)

            if curr_count == prev_count:  # no new rows after scrolling
                break

            prev_count = curr_count
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  # scroll to bottom
            page.wait_for_load_state("networkidle")

        # --- Get rows ---
        data = []
        for row in rows:
            cols = [c.inner_text().strip() for c in row.query_selector_all("td span.z-label")]
            cols_no_AND = [item for item in cols if item != 'AND']

            # Add status of course
            status_obj = row.query_selector("td.entrystatus img.z-image")
            status = status_obj.get_attribute('title') if status_obj else 'none'
            cols_no_AND.append(status)

            # Add AUs or other messages of course
            message = row.get_attribute('title')
            cols_no_AND.append(message)

            if len(cols_no_AND) == 8:
                data.append(cols_no_AND)

        browser.close()
        return data

courses = ["COMP302", "COMP360"]

all_data = []

for c in courses:
    rows = scrape_course(c)
    all_data.extend(rows)

headers = ['McGill Course', 'McGill Title', 'External Course', 'External Title', 'External Institution', 'Country', 'Status', 'Message']

df = pd.DataFrame(all_data, columns=headers)
print(df.head())
df.to_csv("CORE_equivalencies.csv", index=False)