#e-*- coding: utf-8 -*-
"""Hospital_Clinics.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pW55Rizj9u61prHeFjbbClPe_kAhs-uj
"""

import time, sys, os, pygsheets, requests, pprint
from playsound import playsound
from google.colab import userdata
import pandas as pd

secret_key = userdata.get('SERP_API_KEY')
address = userdata.get('address')
print(secret_key)
print(address)

# Execute the SERP search
def find_healthcare_institutions_near_address(query, address, api_key):
    params = {
        "q": query + address,  # The search query for clinics near the address
        "location": address,  # The specific address
        "engine": "google_maps",  # Use the Google Maps engine
        "type": "search",  # We're looking for place search results,
        "location_requested": "New York, United States",
        "location_used": "New York,United States",
        "hl": "en",  # Language
        "gl": 'us',
        "api_key": api_key  # Your SerpAPI key
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    # Parse the results
    clinics = data.get("local_results", [])
    return clinics

clinics = find_healthcare_institutions_near_address("hospitals or clinics near ", address, secret_key)

# print(clinics)

# Display results
# for clinic in clinics:
#     print(f"Name: {clinic['title']}")
#     print(f"Address: {clinic['address']}")
#     print(f"Rating: {clinic.get('rating', 'No rating')}")
    # print(f"Link: {clinic['link']}")
    # print("---------------")

# Print the first object in the clinics array with indenting
# pprint.pprint(clinics[0], indent=3)

# address, hours, open_state, operating_housrs, phone, rating, title
# type, website
df = pd.DataFrame(clinics, columns=['title', 'phone', 'address', 'hours', 'open_state', 'operating_hours',
                                    'rating', 'website', 'type'])
# Remove rows without a website
filtered = df[df['website'].notnull()]
filtered.sort_values(by='rating', ascending=False)

shape = filtered.shape
print(f'There are {shape[0]} clinics in NY with {shape[1]} fields')

# Convert the Pandas df into Google Sheets
csv_data = filtered.to_csv();

# Install pygsheets

path = "/content/galvanic-augury-431216-k5-1a3cfbfcec7a.json"

# os.access(path, os.R_OK)

# Ensure file exists
if not os.path.exists(path):
    print("File does not exist.")
    exit()  # Exit if the file does not exist

# Authorize with Google Sheets API
# print(path)
gc = pygsheets.authorize(service_file=path)

spreadsheet = gc.open('Clinics')  # Replace with your sheet name

worksheet = spreadsheet.sheet1  # You can also use .get_worksheet(index) to specify the sheet

# Clear existing content (optional)
worksheet.clear()

# Update the sheet with DataFrame values
worksheet.set_dataframe(filtered, (1, 1))  # Starting from the first row and first column

print("DataFrame written to Google Sheets successfully!")

message = "Here is something to ponder \r\
about the way I may want to try creating\r \ the typewriter effect in Python. \r \ Here is something to ponder about the way I may want to try creating the typewriter effect in Python."

def type_effect(msg, speed = 0.05):
  for char in msg:
    # Write the individual character and wait before continuing.
    sys.stdout.write(char)
    sys.stdout.flush()

    # Check and pause if the character is a new line
    if (char != "\n"):
      time.sleep(speed)
    else:
      time.sleep(speed*2)

# type_effect(message, 0.1)
# playsound("sound.mp3", 0)

#
