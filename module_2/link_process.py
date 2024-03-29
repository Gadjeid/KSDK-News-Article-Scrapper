from bs4 import BeautifulSoup
import requests
import os
import json
# Take article links and article scrap to .txt file, returns nothing
# Single Responsibilty Principle & Open-Closed Principle, module recieves the links and processes them
# and outputs to .txt files. As a result, the code is concise and cohesive with the rest of the program.
# Futhermore, if I wanted to add new functionality or add to the file output, doing so in this module
# wouldn't affect the rest of the program (open closed)
def soup_scrap(article_links):
    for index, link in enumerate(article_links, 0):
        # Make a request to each article link
        response = requests.get(link)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # If found, parse
            soup = BeautifulSoup(response.text, 'html.parser')
            # Raw file with everything
            raw_file = response.text

            # Find the h1 (title), author, summary, and all paragraphs
            headline = soup.find('h1')
            author = soup.find('div', class_="article__author")
            summary = soup.find('div', class_="article__summary")
            article = soup.find_all('p')

            # Removing unnecessary information, cleaning up output
            classes_to_remove = ['video__endslate-solo-countdown', 
                     'video__endslate-countdown', 
                     'video__endslate-solo-title', 
                     'video__endslate-title video__endslate-title_primary_true']

            for class_name in classes_to_remove:
                for p_tag in soup.find_all('p', class_=class_name):
                    p_tag.decompose()

            # Specify the folder path
            output_folder = "Data/processed"
            raw_html = "Data/unprocessed"

            # Set up file output location
            output_filename = os.path.join(output_folder, f"article_{index+1}.txt")    
            output_raw = os.path.join(raw_html, f"raw_{index+1}.txt")            
        
            # Save raw file with all tags
            with open(output_raw, 'w', encoding='utf-8') as output_file:
                content = raw_file
                output_file.write(content)

            # Print all for each article (headline, author, summary, article)
            with open(output_filename, 'w') as output_file:
                headline_text = headline.text.strip() if headline else "No Headline"
                author_text = author.text.strip() if author else "No Author"
                summary_text = summary.text.strip() if summary else "No Summary"

                headline_file = "Headline: " + headline_text + "\n"
                author_file = author_text + "\n"
                summary_file = "Summary: " + summary_text + "\n"
            
                output_file.write(headline_file)
                output_file.write(author_file)
                output_file.write(summary_file)

                content=""
                for a in article:
                    content+= str(a.text.strip()) + " "
                output_file.write("Article: " + content + "\n")
            print(f"article {index+1} scrapped, output in {output_folder}")
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
