# eCardCreator
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Artrios/eCardCreator)

A flask app that provides a GUI for creating custom e-Reader cards for the Generation 3 Pokémon games.
This is an extension of the [pokecarde](https://github.com/Artrios/pokecarde) project mainly to make it easier to make custom cards without needing to edit the necessary text files.
Currently it only supports the Battle-e cards for Pokemon Ruby and Sapphire, other Battle-e style cards are still being developed.

I'm hosting an instance of this [here](https://tools.paccypad.com/ecardcreator) for people to use.

## Usage
The web app provides a simple form to develop custom e-Reader Battle-e cards. Nearly every aspect of the trainer and their Pokemon can be set. Cards can be output into `.raw` files for emulators, `.bmp` files to print and use on hardware or a zip file with the previous files plus the `asm` files used to make the card.

This Program is still in beta so bugs are to be expected.

## Installation

### Docker
For easy installation a docker-compose file is included, simply run `docker compose up`.

### Manual
This method requires python 3.12 at a minimum.
Install all the package requirements by running `pip install -r requirements.txt`. After they're all installed the pweb app can be setup by running `waitress-serve --host 127.0.0.1 eCardCreator:create_app`.
