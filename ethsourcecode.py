import requests
from bs4 import BeautifulSoup
import logging
import cfscrape
import re

import os
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.environ['ETHERSCAN_API_KEY']

logging.basicConfig(level=logging.INFO)


def get_etherscan_url(contract_address):
    return f"https://etherscan.io/address/{contract_address}#code"


def get_contract_source_code(contract_address):
    base_url = "https://api.etherscan.io/api"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address,
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1" and data["message"] == "OK":
            source_code = data["result"][0]["SourceCode"]
            source_code_lines = source_code.split("\n")
            return source_code_lines[:50]
    return None


# def get_contract_source_code(url):
#     logging.info(f"Fetching source code from {url}")
#     scraper = cfscrape.create_scraper()
#     response = scraper.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     code_block = soup.find("pre", class_="js-sourcecopyarea")

#     if code_block:
#         code_lines = code_block.get_text().split("\n")
#         logging.info(
#             f"First two lines of the source code:\n{code_lines[0]}\n{code_lines[1]}")
#         return code_lines[:50]
#     return None


def filter_links(lines):
    filtered_lines = []
    for line in lines:
        if re.search(r'https?://\S+|t\.me/\S+', line):
            filtered_lines.append(line)
    return filtered_lines


def main():
    contract_address = input("Enter an Ethereum contract address: ")
    etherscan_url = get_etherscan_url(contract_address)
    source_code_snippet = get_contract_source_code(etherscan_url)

    if source_code_snippet:
        filtered_lines = filter_links(source_code_snippet)
        if filtered_lines:
            print("Lines containing a website or a Telegram username:\n" +
                  "\n".join(filtered_lines))
        else:
            print("No lines containing a website or a Telegram username were found.")
    else:
        print("Unable to fetch the source code.")


if __name__ == "__main__":
    main()
