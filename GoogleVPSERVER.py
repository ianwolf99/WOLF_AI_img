import os
import requests
from bs4 import BeautifulSoup

try:
    def extract_google_news(keywords, count):
        # Create a session object to handle cookies
        session = requests.Session()

        # Set the User-Agent header to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        session.headers.update(headers)

        # Create the search query by appending the keywords to the Google News URL
        search_query = 'https://news.google.com/search?q=' + keywords.replace(' ', '%20')

        # Send a GET request to the Google News URL using the session object
        response = session.get(search_query)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the news articles on the page
        articles = soup.find_all('article')

        # Create a list to store the extracted news
        news_list = []

        # Create a directory based on the keywords
        directory = keywords.replace(' ', '_')
        os.makedirs(directory, exist_ok=True)

        # Extract the required number of news articles
        for i, article in enumerate(articles[:count], start=1):
            # Extract the title, text, and published_at information
            title = article.find('h3', class_='ipQwMb ekueJc RD0gLb').text

            text_element = None
            text_elements = [
                article.find('div', class_='Da10Tb'),
                article.find('div', class_='xBbh9')
            ]
            for element in text_elements:
                if element:
                    text_element = element
                    break

            text = text_element.get_text(separator='\n') if text_element else ''

            published_at = article.find('time')['datetime']

            # Create a dictionary to store the extracted information
            news = {
                'title': title,
                'text': text,
                'published_at': published_at
            }

            # Append the news to the news_list
            news_list.append(news)

            # Save the image with the article title
            image_url = article.find('img')['src']
            image_response = session.get(image_url)
            image_filename = f'{title}.jpg'  # Set the image extension to JPG
            image_path = os.path.join(directory, image_filename)

            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)

            print(f'Saved image {i}/{count}: {image_filename}')

        return news_list

except Exception as err:
    print('An error occurred while processing an article:', str(err))

if __name__ == "__main__":
    news = extract_google_news("Celebrities news in the United States", 10)

    # Print the extracted news articles
    for article in news:
        print('Title:', article['title'])
        print('Text:', article['text'])
        print('Published At:', article['published_at'])
        print('---')
