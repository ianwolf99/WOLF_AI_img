import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

try:
    def extract_google_news(keywords, count):
        # Create the search query by appending the keywords to the Google News URL
        search_query = 'https://news.google.com/search?q=' + keywords.replace(' ', '%20')

        # Send a GET request to the Google News URL
        response = requests.get(search_query)

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
            # Extract the title and published_at information
            title = article.find('h3', class_='ipQwMb ekueJc RD0gLb').text
            published_at = article.find('time')['datetime']

            # Get the URL of the full article
            article_link = article.find('a', class_='VDXfz')
            article_url = urljoin(search_query, article_link['href'])

            # Send a GET request to the article URL
            article_response = requests.get(article_url)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')

            # Find all paragraph tags within the article page
            paragraphs = article_soup.find_all('p')

            # Filter out unwanted elements based on CSS classes or other criteria
            filtered_paragraphs = [
                p.get_text() for p in paragraphs 
                if 'unwanted-class' not in p.get('class', []) and 'unwanted-id' not in p.get('id', '') 
                and not p.find_parent(['footer', 'header'])
                and not p.find(class_='unwanted-class')
                and not p.get('style') == 'display:none;'
                and 'Sign Up' not in p.get_text()  # Exclude text containing 'Sign Up'
                and 'Sign In' not in p.get_text()  # Exclude text containing 'Sign In'
                and 'Terms and Conditions' not in p.get_text()  # Exclude text containing 'Terms and Conditions'
                # Add more conditions as needed to exclude unwanted elements
            ]

            # Concatenate the filtered text content of the paragraphs
            news_text = '\n'.join(filtered_paragraphs)

            # Create a dictionary to store the extracted information
            news = {
                'title': title,
                'text': news_text,
                'published_at': published_at
            }

            # Append the news to the news_list
            news_list.append(news)

            # Save the image with the article title
            image_url = article.find('img')['src']
            image_response = requests.get(image_url)
            image_filename = f'{title}.jpg'  # Set the image extension to JPG
            image_path = os.path.join(directory, image_filename)

            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)

            print(f'Saved image {i}/{count}: {image_filename}')

        return news_list

except Exception as err:
        print('An error occurred while processing an article:', str(err))

if __name__ == "__main__":
    news = extract_google_news("Celebrities newsin the United States", 2)

    # Print the extracted news articles
    for article in news:
        print('Title:', article['title'])
        print('Text:', article['text'])
        print('Published At:', article['published_at'])
        print('---')
