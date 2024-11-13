#importing packages 
import os
import nest_asyncio
import urllib.request
nest_asyncio.apply()

index_root = os.path.join(os.getcwd(), 'graph_index')
os.makedirs(os.path.join(index_root, 'input'), exist_ok=True)
url = "https://www.gutenberg.org/cache/epub/7785/pg7785.txt"
file_path = os.path.join(index_root, 'input', 'davinci.txt')
urllib.request.urlretrieve(url, file_path)
with open(file_path, 'r+', encoding='utf-8') as file:
    # If you want to save api key cost, you can truncate the text file to a smaller size.
    lines = file.readlines()
    file.seek(0)
    file.writelines(lines[:934])  # Decrease this number if you want to save api key cost.
    file.truncate()
