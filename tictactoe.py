import requests
from bs4 import BeautifulSoup
import json
import os
import random


LINKS = {"Tile 0": "https://cntr.click/5xW31GG",
         "Tile 1": "https://cntr.click/k6m4pLh",
         "Tile 2": "https://cntr.click/0Jy1NdB",
         "Tile 3": "https://cntr.click/y4BYk8p",
         "Tile 4": "https://cntr.click/VCtRg6b",
         "Tile 5": "https://cntr.click/b0a0hMb",
         "Tile 6": "https://cntr.click/sGaY2s4",
         "Tile 7": "https://cntr.click/5B5pmVK",
         "Tile 8": "https://cntr.click/SG7sV89"}


def get_tile_count():
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {"email": os.environ['EMAIL'], "password": os.environ['PASSWORD'], "loginSubmit": "Sign In"}
    url = "https://www.linkclickcounter.com/userAccount.php"

    r = requests.post(url=url, headers=headers, data=payload)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")

    tile_click_count_new = {}
    tile_click_count_difference = {}
    table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            tile_click_count_new[cells[3].find(text=True)] = int(cells[4].find(text=True))

    if not os.path.exists("tile_count.json"):
        tile_click_count_difference = tile_click_count_new.copy()
    else:
        with open("tile_count.json", 'r') as f:
            tile_click_counter_old = json.load(f)
            tile_click_count_difference = {key: tile_click_count_new[key] - tile_click_counter_old.get(key, 0) for key in tile_click_count_new}

    with open("tile_count.json", 'w') as f:
        json.dump(tile_click_count_new, f)

    print(f"Click since last run:{tile_click_count_difference}")
    return tile_click_count_difference


def tictactoe(tile_click_count):
    if not os.path.exists("game_state.json"):
        game_state = {"last_played": None, "tiles": {"Tile 0": None, "Tile 1": None, "Tile 2": None, "Tile 3": None, "Tile 4": None, "Tile 5": None, "Tile 6": None, "Tile 7": None, "Tile 8": None}}

    else:
        with open("game_state.json", 'r') as f:
            game_state = json.load(f)

    if game_state["last_played"] is None:
        game_state["last_played"] = random.choice([True, False])

    move = max(tile_click_count, key=lambda x: tile_click_count[x] if game_state["tiles"][x] is None else -1)

    print(game_state)
    print(move)

    game_state["last_played"] = not game_state["last_played"]
    game_state["tiles"][move] = game_state["last_played"]

    print(game_state)

    winner = None
    for row in range(3):
        if game_state["tiles"][f"Tile {3*row}"] is not None and game_state["tiles"][f"Tile {3*row}"] == game_state["tiles"][f"Tile {3*row + 1}"] == game_state["tiles"][f"Tile {3*row + 2}"]:
            winner = game_state["tiles"][f"Tile {3*row}"]

    for col in range(3):
        if game_state["tiles"][f"Tile {col}"] is not None and game_state["tiles"][f"Tile {col}"] == game_state["tiles"][f"Tile {col+3}"] == game_state["tiles"][f"Tile {col+6}"]:
            winner = game_state["tiles"][f"Tile {col}"]

    if game_state["tiles"]["Tile 0"] is not None and game_state["tiles"]["Tile 0"] == game_state["tiles"]["Tile 4"] == game_state["tiles"]["Tile 8"]:
        winner = game_state["tiles"]["Tile 0"]

    if game_state["tiles"]["Tile 2"] is not None and game_state["tiles"]["Tile 2"] == game_state["tiles"]["Tile 4"] == game_state["tiles"]["Tile 6"]:
        winner = game_state["tiles"]["Tile 2"]

    if winner is None and all(v is not None for k, v in game_state["tiles"].items()):
        winner = "Draw"

    print(winner)

    if winner is not None and os.path.exists("game_state.json"):
        os.remove("game_state.json")
    else:
        with open("game_state.json", 'w') as f:
            json.dump(game_state, f)

    return game_state, winner


def update_readme(game_state, winner):

    tile_content = {}
    for tile in range(9):
        if game_state['tiles'][f'Tile {tile}'] is None:
            tile_content[f"Tile {tile}"] = f"[![Tile {tile}](https://github.com/snerz13/snerz13/blob/main/assets/{game_state['tiles'][f'Tile {tile}']}.png)]({LINKS[f'Tile {tile}']})"
        else:
            tile_content[f"Tile {tile}"] = f"[![Tile {tile}](https://github.com/snerz13/snerz13/blob/main/assets/{game_state['tiles'][f'Tile {tile}']}.png)](https://github.com/snerz13)"

    README = f"""<h1 align="middle"> Hey there!👋🏻, I'm Jash Desai !! </h1>

<p align="middle"> <img src="https://komarev.com/ghpvc/?username=jash-desai&label=Profile%20views&color=ff4da6&style=plastic" alt="jash-desai" /> </p>
<h3> A bit of Intro: </h3>
- 🔭 I’m currently working on <b>Flutter Projects.</b> </br>
- 🌱 I’m currently learning <b>C++, Flutter and WebDev.</b></br>
- 🤔 I’m looking for help with <b>OpenSource and CP.</b></br>
- 📫 How to reach me: Mail me at : <b>jash.13.desai@gmail.com</b> or <b>jashkdesai@gmail.com</b></br>
- ⚡ Fun fact: If you find an account with <a href ="https://raw.githubusercontent.com/jash-desai/jash-desai/main/Labyrinth.jpeg" />Labyrinth </a> and a •!!•, it's definitely me!</br>
<!-- - 👯 I’m looking to collaborate on 
<!-- - 💬 Ask me about -->

<h3> Connect with me: </h3>
<a href="https://www.linkedin.com/in/jade13/">
  <img align="left" alt="LinkedIn" width="30px" src="https://raw.githubusercontent.com/jash-desai/jash-desai/main/assets/linkedin.svg" />
</a>
<a href="https://instagram.com/_jade13._" target="blank">
 <img align="left" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/22064237dce9d9052582c108ace3c161b646dfd9/src/images/icons/Social/instagram.svg" alt="_jade13._" height="30" width="30" />
</a>
<a href="https://open.spotify.com/user/vvghoq1frj9jgqpgne20hkoo9">
  <img align="left" alt="Spotify" width="30px" src="https://raw.githubusercontent.com/jash-desai/jash-desai/main/assets/spotify.svg" />
</a>
<a href="https://github.com/jash-desai">
  <img align="left" alt="GitHub" width="30px" src="https://raw.githubusercontent.com/jash-desai/jash-desai/main/assets/github.svg" />
</a>
<a href="http://discordapp.com/users/776025704818671637">
  <img align="left" alt="Discord" width="30px" src="https://raw.githubusercontent.com/jash-desai/jash-desai/main/assets/discord.svg" />
</a>
<a href="https://www.facebook.com/jash.x.desai.13/">
  <img align="left" alt="Facebook" width="30px" src="https://raw.githubusercontent.com/jash-desai/jash-desai/main/assets/facebook.svg" />
</a>
</br>
 
<h3>Languages and Tools:</h3>

<a href="https://www.cprogramming.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/c/c-original.svg" alt="c" width="40" height="40"/> </a> &nbsp;
<a href="https://www.w3schools.com/cpp/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg" alt="cplusplus" width="40" height="40"/> </a>  &nbsp;
<a href="https://dart.dev" target="_blank"> <img src="https://www.vectorlogo.zone/logos/dartlang/dartlang-icon.svg" alt="dart" width="40" height="40"/> </a>  &nbsp;
<a href="https://firebase.google.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/firebase/firebase-icon.svg" alt="firebase" width="40" height="40"/> </a>  &nbsp;
<a href="https://flutter.dev" target="_blank"> <img src="https://www.vectorlogo.zone/logos/flutterio/flutterio-icon.svg" alt="flutter" width="40" height="40"/> </a>  &nbsp;
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a>  &nbsp;

 
 <h3>GitHub Stats:</h3>

 <img align="left" src="https://github-readme-stats.vercel.app/api/top-langs?username=jash-desai&show_icons=true&theme=dracula&hide_border=true&disable_animations =false&locale=en" alt="jash-desai" /> 
 <img align="center" src="https://github-readme-stats.vercel.app/api?username=jash-desai&show_icons=true&theme=dracula&hide_border=true&disable_animations =false&locale=en" alt="jash-desai" />
  
[![Spotify -](https://spotify-github-profile.vercel.app/api/view?uid=vvghoq1frj9jgqpgne20hkoo9&cover_image=true&theme=novatorem)](https://open.spotify.com/user/vvghoq1frj9jgqpgne20hkoo9)


<h3 align="middle">Why not play a game of Tic-Tac-Toe while you're here!</h3>
Click on a Tile to play  
The most picked move is chosen every minute.

Current turn: <img src= "https://github.com/snerz13/snerz13/blob/master/assets/False.png" alt="Current Turn" width="32"/>


| [![Tile 0](https://github.com/snerz13/snerz13/blob/master/assets/False.png)](https://github.com/snerz13) | [![Tile 1](https://github.com/sner13/sner13/blob/master/assets/True.png)](https://github.com/sner13) | [![Tile 2](https://github.com/sner13/sner13/blob/master/assets/None.png)](https://cntr.click/0Jy1NdB) |
| [![Tile 3](https://github.com/snerz13/snerz13/blob/master/assets/None.png)](https://cntr.click/y4BYk8p) | [![Tile 4](https://github.com/snerz13/snerz13/blob/master/assets/True.png)](https://github.com/snerz13) | [![Tile 5](https://github.com/snerz13/snerz13/blob/master/assets/None.png)](https://cntr.click/b0a0hMb) |
| [![Tile 6](https://github.com/snerz13/snerz13/blob/master/assets/None.png)](https://cntr.click/sGaY2s4) | [![Tile 7](https://github.com/snerz13/snerz13/blob/master/assets/None.png)](https://cntr.click/5B5pmVK) | [![Tile 8](https://github.com/snerz13/snerz13/blob/master/assets/False.png)](https://github.com/snerz13) |

</br>

<a href="https://github.com/jash-desai">
  <img align="middle" src = "https://raw.githubusercontent.com/jash-desai/jash-desai/main/bottom-footer.svg">
</a>

"""

    with open("README.md", "w") as f:
        f.write(README)


if __name__ == "__main__":
    tile_click_count = get_tile_count()
    game_state, winner = tictactoe(tile_click_count)
    update_readme(game_state, winner)

