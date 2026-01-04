from playwright.sync_api import sync_playwright
import pandas as pd
import time
from tqdm import tqdm

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

def scrape_course(course_code):
    url = "https://nimbus-ssl.mcgill.ca/exsa/search/searchEquivalency"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_selector("div.course-panel div:has(div span:has-text('Course Number')) input")

        # Fill in the search form (adjust selectors)
        page.locator("div.course-panel div:has(div span:has-text('Course Number')) input").fill(course_code)
        page.locator("span:has(label:has-text('Include Expired Decisions')) input[type=checkbox]").click()
        page.click("button:has-text('Search')")

        # Wait until results table body is loaded
        try:
            page.wait_for_selector("div.search-result-grid table[id*='cave'] tr.z-row", timeout=2500)

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

def extract(courses, category):
    all_data = []
    for c in tqdm(courses):
        rows = scrape_course(c)
        all_data.extend(rows)

    headers = ['McGill Course', 'McGill Title', 'External Course', 'External Title', 'External Institution', 'Country', 'Status', 'Message']

    df = pd.DataFrame(all_data, columns=headers)
    print(df.head())
    df.to_csv(f"{category}_equivalencies.csv", index=False)

course_lists = {
    "MINOR": [
        "MATH242",
        "MATH223",
        "MATH247",
        "MATH243",
        "MATH264",
        "MATH316",
        "MATH319",
        "MATH326",
        "MATH378",
        "MATH417",
        "MATH427",
        "MATH447",
        "MATH463",
        "MATH475",
        "MATH478",
        "MATH563",
    ],
    "TCA": [
        "ECSE325",
        "ECSE415",
        "ECSE416",
        "ECSE422",
        "ECSE439",
        "ECSE444",
        "ECSE544",
    ],
    "TCB": [
        "COMP307",
        "COMP330",
        "COMP350",
        "COMP370",
        "COMP417",
        "COMP424",
        "COMP445",
        "COMP520",
        "COMP521",
        "COMP525",
        "COMP529",
        "COMP533",
        "COMP547",
        "COMP549",
        "COMP550",
        "COMP551",
        "COMP559",
        "COMP562",
        "COMP579",
        "ECSE343",
        "ECSE421",
        "ECSE424",
        "ECSE425",
        "ECSE437",
        "ECSE446",
        "ECSE507",
        "ECSE509",
        "ECSE525",
        "ECSE526",
        "ECSE532",
        "ECSE551",
        "ECSE552",
        "ECSE554",
        "ECSE556",
        "ECSE557",
        "ECSE561",
        "MATH247"
    ],
    "CORE": ["COMP302", "COMP360", "ECSE427", "ECSE428", "ECSE429", "ECSE421", "ECSE420"],
    "IMPACT": ["ANTH212", "ARCH515", "BTEC502", "COMS200", "COMS411", "ECON225", "ECON347", "ENVR201", "GEOG203", "GEOG205", "GEOG302", "INSY331", "INSY334", "INSY455", "LLCU212", "MGCR331", "MGPO440", "MGPO460", "MGPO485", "PHIL343", "SEAD500", "SEAD530", "SOCI235", "SOCI312", "SOCI325"]
}

for category, courses in course_lists.items():
    print(f"Extracting {category} courses...")
    extract(courses, category)
    print(f"Done extracting {category}\n\n\n")