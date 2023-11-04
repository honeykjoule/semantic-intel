import requests
import json
import time
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_all_opinions_for_judge(judge_id):
    api_url = f"https://www.courtlistener.com/api/rest/v3/opinions/?author__id={judge_id}"
    all_opinions = []
    try: 
        while api_url:
            response = requests.get(api_url)
            if response.status_code == 429:
                logging.warning("Rate limit reached. Sleeping for 10 seconds")
                time.sleep(10)
                continue
            response.raise_for_status()
            opinions_page = response.json()
            all_opinions.extend(opinions_page['results'])
            api_url = opinions_page['next']
            logging.info(f"Fetched page: {api_url or 'Done'}")
    except requests.HTTPError as http_error:
        logging.error(f'HTTP error occured: {http_error}')
    except Exception as err:
        logging.error(f'Error occured: {err}')
    return all_opinions

def save_opinions_to_json(opinions, filename):
    with open(filename, 'w') as file:
        json.dump(opinions, file, indent=4)

judge_id = 2738
opinions = fetch_all_opinions_for_judge(judge_id)
save_opinions_to_json(opinions, f"data/raw/{judge_id}.json")