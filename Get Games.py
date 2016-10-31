from bs4 import BeautifulSoup
import requests
import urllib
import os

# URL for BasketballData repository snapshot as of 1/24/16
url = 'https://github.com/neilmj/BasketballData/tree/b46f92a9438df7661ddce203ed10625c1c4e586a/2016.NBA.Raw.SportVU.Game.Logs'

# Fetch page with list of files
page = requests.get(url)

# Initialize empty list to store links
links = []

# Parse the webpage using BeautifulSoup, find the first URL, add it to the list
soup = BeautifulSoup(page.content, 'html.parser')
first_link = soup.find('a', attrs={'class': 'js-navigation-open'})
links.append(first_link['href'])

# Find the next URL
next_link = first_link.find_next('a', attrs={'class': 'js-navigation-open'})

# Comb through the page for links, adding each one to the list, until there are no more links left
while next_link != None:
    try:
        links.append(next_link['href'])
        next_link = next_link.find_next('a', attrs={'class': 'js-navigation-open'})
    except:
        break

# Initialize an empty list to store links that have been properly formatted
fixed_links = []

# Loop through the list of links and check each one to see if it's a .7z archive file
# If it is, add the github URL stem, and replace /blob/ with /raw/ to allow direct download
# Add ONLY THE FIXED LINKS to the fixed_links list
for link in links:
    if '.7z' in link:
        fixed_link = 'https://github.com' + link.replace('/blob/', '/raw/')
        fixed_links.append(fixed_link)

# Loop through the list of game archive links, request each one for download
# Save each file using the filename (basename) with which it's stored on the server
for url in fixed_links:
    filename = os.path.basename(url)
    urllib.request.urlretrieve(url, filename)
