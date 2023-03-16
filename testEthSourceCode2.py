from ethsourcecode2 import get_contract_source_code
from dotenv import load_dotenv

load_dotenv()

# Replace with your desired contract address
contract_address = "0xFbD5fD3f85e9f4c5E8B40EEC9F8B8ab1cAAa146b"

source_code_lines = get_contract_source_code(contract_address)

if source_code_lines:
    for line in source_code_lines:
        print(line)
else:
    print("Failed to fetch source code.")
