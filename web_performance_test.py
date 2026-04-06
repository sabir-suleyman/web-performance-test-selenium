from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import statistics

websites = [
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.google.com",
    "https://stackoverflow.com"
]

test_count = 10
all_results = []
summary_results = []

options = Options()
options.binary_location = "/usr/bin/chromium"

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

print("Web performance test started.\n")

for website in websites:
    print(f"Testing: {website}")
    load_times = []

    for test_number in range(1, test_count + 1):
        driver.get(website)
        time.sleep(2)

        performance_data = driver.execute_script(
            "return window.performance.timing"
        )

        load_time = (
            performance_data["domComplete"]
            - performance_data["navigationStart"]
        )

        load_times.append(load_time)
        all_results.append([website, test_number, load_time])

        print(f"  Test {test_number}: {load_time} ms")

    average_time = round(statistics.mean(load_times), 2)
    minimum_time = min(load_times)
    maximum_time = max(load_times)

    summary_results.append([
        website,
        average_time,
        minimum_time,
        maximum_time
    ])

    print(f"  Average: {average_time} ms")
    print(f"  Minimum: {minimum_time} ms")
    print(f"  Maximum: {maximum_time} ms\n")

driver.quit()

with open("sonuclar.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["RAW RESULTS"])
    writer.writerow(["Website", "Test Number", "Load Time (ms)"])
    writer.writerows(all_results)

    writer.writerow([])

    writer.writerow(["SUMMARY RESULTS"])
    writer.writerow(["Website", "Average (ms)", "Minimum (ms)", "Maximum (ms)"])
    writer.writerows(summary_results)

print("All tests completed successfully and the results saved to sonuclar.csv. ")
