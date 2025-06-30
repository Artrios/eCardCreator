import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from eCardCreator.db import get_db

bp = Blueprint('ecard', __name__, url_prefix='/ecard')

@bp.route('/battle-e', methods=('GET', 'POST'))
def cardmaker():
    if request.method == 'POST':
        print_request_form(request.form)

    pokelist=[]
    classlist=[]
    naturelist=[]
    itemlist=[]
    movelist=[]
    easychat=[]

    with open("eCardCreator/data/Pokemon.txt","r") as infile:
        for line in infile:
            pokelist.append(line.strip())

    with open("eCardCreator/data/TrainerClass.txt","r") as infile:
        for line in infile:
            classlist.append(line.strip())

    with open("eCardCreator/data/Natures.txt","r") as infile:
        for line in infile:
            naturelist.append(line.strip())

    with open("eCardCreator/data/Items.txt","r") as infile:
        for line in infile:
            itemlist.append(line.strip())

    with open("eCardCreator/data/Moves.txt","r") as infile:
        for line in infile:
            movelist.append(line.strip())

    with open("eCardCreator/data/EasyChat.txt","r") as infile:
        for line in infile:
            easychat.append(line.strip())
    
    return render_template('ecard/battle-e.html', pokelist=pokelist, classlist=classlist, naturelist=naturelist, itemlist=itemlist, movelist=movelist, easychat=easychat)

def print_request_form(in_form):
    with open("request.asm","w") as outfile:
        outfile.write('INCLUDE "trainers/macros.asm"\n')
        outfile.write('    Battle_Trainer\n')
        outfile.write(f'    BT_Level {in_form["BTLevel"]}\n')
        outfile.write(f'    db {in_form["TrainerClass"]}\n')
        outfile.write(f'    BT_Floor {in_form["BTFloor"]}\n')
        outfile.write(f'    Text_EN "{in_form["TrainerName"]}"8\n')
        outfile.write(f'    OT_ID 00000,00000\n')
        outfile.write('\n')
        outfile.write(f'    Intro_EN {in_form["intro1"]},{in_form["intro2"]},{in_form["intro3"]},{in_form["intro4"]},{in_form["intro5"]},{in_form["intro6"]}\n')
        outfile.write(f'    Win_EN {in_form["win1"]},{in_form["win2"]},{in_form["win3"]},{in_form["win4"]},{in_form["win5"]},{in_form["win6"]}\n')
        outfile.write(f'    Lose_EN {in_form["lose1"]},{in_form["lose2"]},{in_form["lose3"]},{in_form["lose4"]},{in_form["lose5"]},{in_form["lose6"]}\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {in_form["Pokemon1"]}\n')
        outfile.write(f'    Holds {in_form["Pokemon1Item"]}\n')
        outfile.write(f'    Moves {in_form["Pokemon1Move1"]}, {in_form["Pokemon1Move2"]}, {in_form["Pokemon1Move3"]}, {in_form["Pokemon1Move4"]}\n')
        outfile.write(f'    Level {in_form["Pokemon1Level"]}\n')
        outfile.write(f'    PP_Ups 0,0,0,0\n')
        outfile.write(f'    EVs {in_form["Pokemon1HPEV"]},{in_form["Pokemon1AtkEV"]},{in_form["Pokemon1DefEV"]},{in_form["Pokemon1SpAtkEV"]},{in_form["Pokemon1SpDefEV"]},{in_form["Pokemon1SpdEV"]}\n')
        outfile.write(f'    OT_ID 00000,00000\n')
        outfile.write(f'    IVs {in_form["Pokemon1HPIV"]},{in_form["Pokemon1AtkIV"]},{in_form["Pokemon1DefIV"]},{in_form["Pokemon1SpAtkIV"]},{in_form["Pokemon1SpDefIV"]},{in_form["Pokemon1SpdIV"]}\n')
        outfile.write(f'    PV $00000000\n')
        outfile.write(f'    TEXT_EN {in_form["Pokemon1Nickname"]}\n')
        outfile.write(f'    Friendship 255\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {in_form["Pokemon2"]}\n')
        outfile.write(f'    Holds {in_form["Pokemon2Item"]}\n')
        outfile.write(f'    Moves {in_form["Pokemon2Move1"]}, {in_form["Pokemon2Move2"]}, {in_form["Pokemon2Move3"]}, {in_form["Pokemon2Move4"]}\n')
        outfile.write(f'    Level {in_form["Pokemon2Level"]}\n')
        outfile.write(f'    PP_Ups 0,0,0,0\n')
        outfile.write(f'    EVs {in_form["Pokemon2HPEV"]},{in_form["Pokemon2AtkEV"]},{in_form["Pokemon2DefEV"]},{in_form["Pokemon2SpAtkEV"]},{in_form["Pokemon2SpDefEV"]},{in_form["Pokemon2SpdEV"]}\n')
        outfile.write(f'    OT_ID 00000,00000\n')
        outfile.write(f'    IVs {in_form["Pokemon2HPIV"]},{in_form["Pokemon2AtkIV"]},{in_form["Pokemon2DefIV"]},{in_form["Pokemon2SpAtkIV"]},{in_form["Pokemon2SpDefIV"]},{in_form["Pokemon2SpdIV"]}\n')
        outfile.write(f'    PV $00000000\n')
        outfile.write(f'    TEXT_EN {in_form["Pokemon2Nickname"]}\n')
        outfile.write(f'    Friendship 255\n')
        outfile.write('\n')
        outfile.write(f'    Pokemon {in_form["Pokemon3"]}\n')
        outfile.write(f'    Holds {in_form["Pokemon3Item"]}\n')
        outfile.write(f'    Moves {in_form["Pokemon3Move1"]}, {in_form["Pokemon3Move2"]}, {in_form["Pokemon3Move3"]}, {in_form["Pokemon3Move4"]}\n')
        outfile.write(f'    Level {in_form["Pokemon3Level"]}\n')
        outfile.write(f'    PP_Ups 0,0,0,0\n')
        outfile.write(f'    EVs {in_form["Pokemon3HPEV"]},{in_form["Pokemon3AtkEV"]},{in_form["Pokemon3DefEV"]},{in_form["Pokemon3SpAtkEV"]},{in_form["Pokemon3SpDefEV"]},{in_form["Pokemon3SpdEV"]}\n')
        outfile.write(f'    OT_ID 00000,00000\n')
        outfile.write(f'    IVs {in_form["Pokemon3HPIV"]},{in_form["Pokemon3AtkIV"]},{in_form["Pokemon3DefIV"]},{in_form["Pokemon3SpAtkIV"]},{in_form["Pokemon3SpDefIV"]},{in_form["Pokemon3SpdIV"]}\n')
        outfile.write(f'    PV $00000000\n')
        outfile.write(f'    TEXT_EN {in_form["Pokemon3Nickname"]}\n')
        outfile.write(f'    Friendship 255\n')
        outfile.write('\n')
        outfile.write(f'    End_Trainer')


