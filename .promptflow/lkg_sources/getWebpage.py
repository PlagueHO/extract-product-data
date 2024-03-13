from promptflow import tool
import requests
from bs4 import BeautifulSoup
import html2text

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(url: str) -> str:

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the HTML content to Markdown
        soup = BeautifulSoup(response.text, 'html.parser')
        product_title = soup.find('div', class_='product__title')
        product_content = soup.find('div', class_='product__description')
        
        if product_content is not None:
            markdown_content = html2text.html2text(str(product_content))
            
            # Prepend the product title to the content
            markdown_content = f"# {product_title.text}\n\n{markdown_content}"

            return {
                "markdown": markdown_content
            }
        else:
            print(f"Failed to find shopify-section in web page.")    
    else:
        print(f"Failed to download the webpage. Status code: {response.status_code}")
