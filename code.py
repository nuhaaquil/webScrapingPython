import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the HPRERA dashboard
base_url = "https://hprera.nic.in/"

# URL to scrape the registered projects
url = "https://hprera.nic.in/PublicDashboard"

# Get the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the first 6 projects under "Registered Projects"
projects = soup.select('a[href^="/Public/ReraProjectDetail"]')[:6]

# Initialize an empty list to store the project details
project_data = []

for project in projects:
    detail_url = base_url + project['href']
    detail_response = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_response.content, "html.parser")
    
    # Extract the required fields from the detail page
    gstin = detail_soup.find(text="GSTIN No").find_next("td").text.strip()
    pan = detail_soup.find(text="PAN No").find_next("td").text.strip()
    name = detail_soup.find(text="Name").find_next("td").text.strip()
    address = detail_soup.find(text="Permanent Address").find_next("td").text.strip()
    
    # Add the details to the project_data list
    project_data.append({
        "GSTIN No": gstin,
        "PAN No": pan,
        "Name": name,
        "Permanent Address": address
    })

# Convert the list of dictionaries to a DataFrame and save it as a CSV
df = pd.DataFrame(project_data)
df.to_csv("registered_projects.csv", index=False)
print("Data has been scraped and saved to registered_projects.csv")
