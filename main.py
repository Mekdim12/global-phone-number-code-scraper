from bs4 import BeautifulSoup
import requests 
import json

url = 'https://countrycode.org/'
url2 = 'http://country.io/phone.json'

target_file_name = 'country_code_scraped.json'
def  fetch_the_table_contents():
    """Fetches the table contents from the URL."""
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    table_body = soup.find('tbody').find_all('tr')

    country_codes = []
    for table in table_body:
        data = table.find_all('td')
        codes = str(data[2].text).split('/')
        dial_code = str(data[1].text).strip()
        # dial_code = dial_code if '-' not in dial_code else dial_code.replace('-','')
        country_codes.append({
            'name':data[0].text,
            "short_code":codes[0].strip(),
            "long_code":(codes[1]).strip(),
            'dial_code':f'+{dial_code}',

        })
    return country_codes

def dump_to_json(country_codes):
    with open(target_file_name,'w') as json_file_writer:
        json.dump(country_codes,json_file_writer,indent=4)

def json_reader(file_name):
    """Reads a JSON file and returns the data."""
    try:
        with open(file_name,'r') as json_file_reader:
            data = json.load(json_file_reader)
        return data
    except IOError as e:
        print(f"Error: {e}")
        return []

def compare_json_files_and_point(newly_scrapped_country_code ,  downloaded_from_gist_country_code):
    """Compares two lists of country codes and prints any differences."""
    for country_code in newly_scrapped_country_code:
        for country_code_ in downloaded_from_gist_country_code:
            if country_code['name'] == country_code_['name']:
                if country_code['short_code'] != country_code_['code']:
                    print(f"Short Code Mismatch for {country_code['name']}") 
                if country_code['dial_code'] != country_code_['dial_code']:
                    print(f"Dial Code Mismatch for {country_code['name']}")
                break
def compare_and_find_difference(newly_scrapped_country_code ,  downloaded_from_gist_country_code):
    list_of_country_codes_found_missing = []
    for country_code in downloaded_from_gist_country_code:
        is_found = False
        for country_code_ in newly_scrapped_country_code:
            if country_code['name'] == country_code_['name']:
                is_found = True
                break
        if not is_found:
            list_of_country_codes_found_missing.append(country_code)

def fetch_check_to_make_sure():
    """Fetches phone codes and checks them against the final country code."""
    try:
        response = requests.get(url2)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        
        
    phone_codes = response.json()   
    final_country_code  = json_reader('country_code_final.json')
    for country_code in final_country_code:

        code = country_code['short_code']
        if not phone_codes.get(code, None):
            print(f"Country Code {code} not found in the phone.json")
    

if __name__ == '__main__':
    # list_of_country_codes = fetch_the_table_contents()  
    # dump_to_json(list_of_country_codes)
    

    # revised_country_code_from_gist = json_reader('CountryCodes.json')
    # newly_created_country_code = json_reader(target_file_name )

    # compare_json_files_and_point(newly_created_country_code, revised_country_code_from_gist)
    # compare_and_find_difference(newly_created_country_code, revised_country_code_from_gist)

    # fetch_check_to_make_sure()
    pass

