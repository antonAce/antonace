# AUTOMATED SCRIPT FOR GENERATING WORDCLOUD
# FOR README.MD FROM TOPICS OF PUBLIC REPOSITORIES

import os
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from json import loads
from requests import get


AUTH_TOKEN = os.getenv('AUTH_TOKEN')
PROFILE_NAME = 'antonace'
GITHUB_ACCEPTABLE_HEADERS = \
    {
        'Accept': 'application/vnd.github.mercy-preview+json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }

WORDCLOUD_IMAGE_FILE_PATH = 'wordcloud.png'


def fetch_topics(repository_name: str) -> list:
    topics_response = get(f'https://api.github.com/repos/{PROFILE_NAME}/{repository_name}/topics',
                          headers=GITHUB_ACCEPTABLE_HEADERS)
    topics = loads(str(topics_response.text))
    return [topic.replace('-', '_') for topic in topics["names"]]


print('FETCHING REPOSITORIES\' TOPICS')

response = get(f'https://api.github.com/users/{PROFILE_NAME}/repos', headers=GITHUB_ACCEPTABLE_HEADERS)
repositories = loads(str(response.text))
repositories_topics = [' '.join(fetch_topics(repo["name"])) for repo in repositories]
joined_topics = ' '.join(repositories_topics)


print('GENERATING WORDCLOUD FROM TOPICS')

cloud = WordCloud(width=800, height=600, background_color='white', colormap="rainbow").generate(joined_topics)
cloud.to_file(WORDCLOUD_IMAGE_FILE_PATH)

print('WORDCLOUD SAVED SUCCESSFULLY')
