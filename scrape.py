from bs4 import BeautifulSoup
import requests

# def fetch_tops():
#     url = 'https://www.hollisterco.com/shop/wd/mens-tops'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     products = []
#     #product_items = soup.find_all('div', class_='product-card')  # Adjust the class name based on actual HTML
#     product_titles = soup.find_all('h2', {'data-aui': 'product-card-name'})
#     product_prices = soup.find_all('span', {'class': 'product-price-text'})
#     product_images = soup.find_all('img', {'data-aui': 'product-card-image'})

#     for title in product_titles:
#         title = title.get_text().strip()
#         products.append({
#             'title': title
#         })

#     for price in product_prices:
#         price = price.get_text().strip()
#         products.append({
#             'price': price
#         })

#     for img in product_images:
#         img = img['src']
#         products.append({
#             'image': img
#         })

#     return products

def fetch_tops():
    url = 'https://www.hollisterco.com/shop/wd/mens-tops'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    
    # Fetching titles, prices, and images
    product_titles = soup.find_all('h2', {'data-aui': 'product-card-name'})
    product_prices = soup.find_all('span', {'class': 'product-price-text'})
    product_images = soup.find_all('img', {'data-aui': 'product-card-image'})
    
    # Check lengths
    len_titles = len(product_titles)
    len_prices = len(product_prices)
    len_images = len(product_images)
    print(f"Titles: {len_titles}, Prices: {len_prices}, Images: {len_images}")

    # Combine the lists into a single list of dictionaries
    for i in range(min(len_titles, len_prices, len_images)):
        title = product_titles[i].get_text().strip()
        price = product_prices[i].get_text().strip()
        image = product_images[i]['src']
        
        products.append({
            'title': title,
            'price': price,
            'image': image
        })

    return products

def fetch():
    url = 'https://www.hollisterco.com/shop/ca/mens-t-shirts-and-henleys-tops'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print raw HTML to debug
    with open('raw_page.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    return []  # Temporarily return an empty list


# Run this function to see if it fetches the expected data
fetch()
print(fetch_tops())
