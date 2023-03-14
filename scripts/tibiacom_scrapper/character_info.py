# Return dict with information about specific character

import requests
from bs4 import BeautifulSoup


def check_name(name):
    player_name = name

    # Checking if name contains letters only, if yes than it perform scrapping data
    if player_name.replace(" ", "").isalpha():
        info = get_char_info(player_name)
        does_it_exist = info[1]
        information = info[0]
        return does_it_exist, information
    else:
        information = "The name contains characters that are not allowed."
        does_it_exist = False
        return does_it_exist, information


# scrapping information about specific character and return dictionary with information from tibia.com
def get_char_info(name):
    player_name = name
    player_info = {}
    rows_count = 0
    url = (
        "https://www.tibia.com/community/?subtopic=characters&name="
        + player_name
    )
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    find_cell = soup.findAll("td")
    is_char = find_cell[0].text
    if is_char.find("does not exist") >= 0:
        player_info.update({player_name: " does not exist."})
        does_it_exist = False
    else:
        raw_cells = soup.findAll("td")
        player_info_list = []
        del raw_cells[0]
        for i in raw_cells:
            player_info_list.append(i.text)

        del player_info_list[0]
        for i in player_info_list:
            rows_count += 1
            if i == "Premium Account" or i == "Free Account":
                break

        for i in range(0, rows_count, 2):
            player_info.update(
                {player_info_list[i].replace(":", ""): player_info_list[i + 1]}
            )
            i -= 1

        # Deleting comment section from data
        for key in player_info.keys():
            if key == "Comment":
                player_info.pop("Comment")
                break

        does_it_exist = True

    return player_info, does_it_exist
