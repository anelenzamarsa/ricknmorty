import requests
import csv
from tabulate import tabulate

API_BASE_URL = "https://rickandmortyapi.com/api/character/"


def initial_request(name):
    # Make the initial request to the Rick and Morty API with the provided character name
    params = {'name': name}
    query = requests.get(API_BASE_URL, params=params)
    return query.json()


def get_episode(endpoint):
    # Make a request to the provided endpoint and format the episode information
    result = requests.get(endpoint).json()
    return f"{result['name']}-({result['episode']})"


def save_to_file(request_output):
    # Extract character information from the API response and save it to a CSV file
    results = request_output['results']

    with open('data.csv', mode='a', newline='') as character_file:
        writer = csv.writer(character_file)

        for character in results:
            # Set 'type' to '-' if it's empty
            type_value = character.get('type', '-')
            # Join episode names and shortcuts into a string
            episodes = ", ".join([get_episode(e) for e in character['episode']])
            # Create a row to be inserted into the CSV file
            row = [character.get(key, '-') for key in ['id', 'name', 'status', 'species', 'type', 'gender']] + \
                  [character['origin']['name'], character['location']['name'], episodes]
            writer.writerow(row)


def workflow(name):
    # Create and truncate the CSV file, write column headers
    with open('data.csv', mode='w') as file:
        csv.writer(file).writerow(['ID', 'Name', 'Status', 'Species', 'Type', 'Gender', 'Origin', 'Location', 'Episodes'])

    response = initial_request(name=name)

    if 'error' in response:
        print(f"Error: {response['error']}")
    else:
        save_to_file(request_output=response)
        next_page = response['info']['next']

        while next_page:
            sub_output = requests.get(next_page).json()

            if 'error' in sub_output:
                print(f"Error: {sub_output['error']}")
                break

            save_to_file(request_output=sub_output)
            next_page = sub_output['info']['next']

        with open('data.csv', newline='') as csvfile:
            data = list(csv.reader(csvfile))
            print(tabulate(data, headers='firstrow', tablefmt='grid'))


if __name__ == '__main__':
    param = input("Let's find your Rick n Morty Character!!!\nPlease enter the character's name: ")
    workflow(param)
