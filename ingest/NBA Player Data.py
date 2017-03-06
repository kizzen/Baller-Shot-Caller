#!/usr/bin/env python

# This file queries the NBA Stats API to gather team- and player-specific data for a single season.


##########################################################################
## Imports
##########################################################################

# 3rd party
from nba_py.constants import TEAMS
from nba_py import team
from nba_py import player
import pandas as pd


# These are some NBA Stats API endpoints that might be relevant.

# playercareerstats
# shotchartdetail
# teamplayerdashboard
# teamplayeronoffdetails


##########################################################################
## Module Variables/Constants
##########################################################################


# Create a list of team abbreviations.

all_teams_list = list(TEAMS.keys())


##########################################################################
## Functions
##########################################################################


def get_player_attributes(all_teams_list):

    player_ids = []

    for team_abbr in all_teams_list:

        current_team = TEAMS[team_abbr]
        players_json = team.TeamPlayers(team_id=current_team['id']).json
        player_data_list = players_json['resultSets'][1]
        for player_data in player_data_list['rowSet']:

            player_id = player_data[1]
            player_ids.append(player_id)

    player_summary_list = []

    for player_id in player_ids:

        player_summary_json = player.PlayerSummary(player_id).json
        player_info = player_summary_json['resultSets'][0]

        player_headers = player_info['headers']
        player_stats = player_info['rowSet'][0]

        player_summary_dict = dict(zip(player_headers, player_stats))
        player_summary_list.append(player_summary_dict)

        print("Gathered data for {}".format(player_stats[3]))

    df = pd.DataFrame(player_summary_list)

    df = df[player_headers]

    df.to_excel('2016-17 NBA Player Attributes.xlsx')


def get_team_players(all_teams_list):

    all_players_list = []

    for team_abbr in all_teams_list:

        current_team = TEAMS[team_abbr]

        print('Gathering player data for {}'.format(current_team['name']))

        players_json = team.TeamPlayers(team_id=current_team['id']).json

        player_data = players_json['resultSets'][1]

        player_headers = player_data['headers']
        player_stats_list = player_data['rowSet']

        for player_stats in player_stats_list:
            player_stats_dict = dict(zip(player_headers, player_stats))
            all_players_list.append(player_stats_dict)

    df = pd.DataFrame(all_players_list)

    df = df[player_headers]

    df.to_csv('2016-17 Player Stats.csv')


def get_team_stats(all_teams_list):

    team_overall_list = []

    for team_abbr in all_teams_list:

        current_team = TEAMS[team_abbr]

        print('Gathering overall data for {}'.format(current_team['name']))

        players_json = team.TeamPlayers(team_id=current_team['id']).json

        team_stats = players_json['resultSets'][0]

        team_overall_headers = team_stats['headers']
        team_overall_stats = team_stats['rowSet'][0]

        team_overall_dict = dict(zip(team_overall_headers, team_overall_stats))

        team_overall_list.append(team_overall_dict)

    df = pd.DataFrame(team_overall_list)

    df = df[team_overall_headers]

    df.to_csv('2016-17 Overall Team Stats.csv')


##########################################################################
## Execution
##########################################################################

	
if __name__ == "__main__":
    get_team_players(all_teams_list)

    get_team_stats(all_teams_list)

    get_player_attributes(all_teams_list)
