from OpenweatherAPI import OpenweatherAPI
from list_of_phrases import lst_negative_temperature10, lst_negative_temperature0_10, positive_temperature1_10, \
    positive_temperature10_20
import re
from tqdm import tqdm
import time
from random import choice


def write_location(city_name: str, code_name: str) -> None:
    """
    writes the city and country code to the log file
    """
    with open('log.txt', 'w', encoding='utf-8') as file:
        file.write(
            f'City:  [ {city_name.title().strip()} ]' + '--->  ' + '\n' + f'Code country: [ {code_name.title().strip()} ]')


def show_location() -> str:
    """
    reads from log.txt and returns a string
    :return: str
    """
    with open('log.txt', 'r', encoding='utf-8') as file:
        return ''.join([x.strip() for x in file.readlines()])


def choose_location(city_name: str, city_code: str) -> tuple:
    """
    inside the function, an instance of the OpenweatherAPI class is created, 2 parameters are added here,
    after which the method that returns the weather data is thrown
    :param city_name:
    :param city_code:
    :return: tuple
    """

    try:
        client = OpenweatherAPI(city_name, city_code)
        weather = client.get_forecast()
        write_location(city_name, city_code)
        return weather
    except LookupError as ex:
        raise ValueError(f'Incorrect city name or code. Type ERR: {ex}')


def agree_city() -> tuple:
    """
    This function uses regular expressions to find the city and code in the log.txt file.
    In return calls another function that returns the weather
    :return tuple
    """
    input_string = show_location()
    pattern = r"City:\s*\[\s*(\w+)\s*\]\s*--->\s*Code country:\s*\[\s*(\w+)\s*\]"
    match = re.match(pattern, input_string)
    city_name, city_code = match[1], match[2]
    [time.sleep(0.50) for _ in tqdm(range(3), desc='Loading...')]

    return choose_location(city_name, city_code)


def phrase_generator(temp: float) -> str:
    """
    Chooses a random phrase value
    :param temp:
    :return: str
    """
    if 0 > temp >= -10:
        return choice(lst_negative_temperature0_10)
    elif temp <= -10:
        return choice(lst_negative_temperature10)
    elif 1 <= temp <= 10:
        return choice(positive_temperature1_10)
    else:
        return choice(positive_temperature10_20)


def main():
    """
    The main event creation function.
    For example, show the City or exit the programs
    The main event creation function.
    For example, show the City or exit the programs
    """
    while True:
        flag = True
        print('Do you want to choose another city or is this one suitable for you?')
        print()
        print('Current location:')
        print(show_location())
        print()
        time.sleep(1)
        print('Please make your choice...')
        print('[ 1 ] --- I agree.', '[ 2 ] --- Show location.', '[ 3 ] --- Change location.',
              '[ 4 ] --- Exit the program.', sep='\n')

        try:
            number = int(input('Write the number: '))
            if number == 1:
                date = agree_city()
                temp, feels_like, latitude, longitude = date[0], date[1], date[2], date[3]
                print(f'Temperature in the city: {temp}', f'Feels like: {feels_like}', f"Latitude: {latitude}",
                      f"Longitude: {longitude}",
                      sep='\n')

                time.sleep(1)
                print()
                print(phrase_generator(temp))
                print()
                time.sleep(1)
                input('If you want to continue, press Enter')

            elif number == 2:
                print(show_location())
                time.sleep(1)
                print()
                input('If you want to continue, press Enter')
            elif number == 3:
                try:
                    city_name, city_code = [input(f'{x}: ') for x in ['Choose a city [e.g., Kiev, Helsinki]',
                                                                      'Choose a code [e.g., ua, fi]']]
                    date = choose_location(city_name, city_code)
                    [time.sleep(0.50) for _ in tqdm(range(3), desc='Loading...')]

                    temp, feels_like, latitude, longitude = date[0], date[1], date[2], date[3]
                    print(f'Temperature in the city: {temp}', f'Feels like: {feels_like}', f"Latitude: {latitude}",
                          f"Longitude: {longitude}",
                          sep='\n')
                    time.sleep(1)
                    print()
                    print(phrase_generator(temp))
                    print()
                    time.sleep(1)

                    if input('If you want to continue press [ Enter ] or press [ 4 ] and  [ Enter ] to exit: ') == "4":
                        print('Goodbye')
                        break
                    else:
                        continue
                except Exception as e:
                    print(f'Error: {e}')
                    time.sleep(1)
            elif number == 4:
                print('Goodbye')
                break

            else:
                print('You have exceeded the range of numbers.', 'Please repeat again.', sep='\n')
                continue
        except ValueError:
            print('I only accept numbers.')
            time.sleep(1)
            continue


# run
if __name__ == '__main__':
    main()
