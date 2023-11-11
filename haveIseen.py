#!/usr/bin/env -S python3.10 -O

import argparse
import asyncio

from diskcache import Cache
import setlist_fm_client
import time
from datetime import datetime
import math
from tqdm import tqdm

from colorama import init, Fore, Style

import warnings
warnings.filterwarnings("ignore") #suppress warning in fuzzywuzzy 
from fuzzywuzzy import process


def parse_args():
    parser = argparse.ArgumentParser(description="Retrieves Information about concerts you have attended of a specific artist, based on your 'setlist.fm' user account.")

    # Add command-line arguments
    parser.add_argument('artist', help='artist to check')
    parser.add_argument('-api', '--api-key', help='\'setlist.fm\' API key', required=True)
    parser.add_argument('-id', '--user-id', help='\'setlist.fm\' user name', required=True)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the parsed arguments
    api_key = args.api_key
    user = args.user_id
    artist = args.artist

    return api_key, user, artist


def get_setlists(user, api_key):
    #caches setlists in .cache -- only queries all setlists if cache is empty or new concerts have been attended
    cache = Cache('.cache')
    
    #load first page of setlists -- to get total number of setlists
    tmp = setlist_fm_client.get_setlists_of_concerts_attended_by_user(user, api_key=api_key, serialize=True)
    time.sleep(0.6)

    try:
        setlists = cache[user]
        if len(setlists) != tmp.total:
            raise KeyError
        else:
            print(f'{Style.DIM}Read concert and setlist info of {user} from cache.{Style.RESET_ALL}')
    except KeyError:
        setlists = []
    
    if len(setlists) == 0:
        no_pages = math.ceil( tmp.total / tmp.items_per_page )
        print(f'{Style.DIM}Fetching concert and setlist info of {user}.{Style.RESET_ALL}')
        for pg in tqdm(range(1, no_pages+1)):
            setlists += setlist_fm_client.get_setlists_of_concerts_attended_by_user(user, p=pg, api_key=api_key, serialize=True).setlist
            time.sleep(0.6)
        #store setlists in cache
        cache[user] = setlists
    return setlists


def main():
    api_key,user,artist = parse_args()

    setlists = get_setlists(user, api_key)

    conc_dict = {}
    for c in setlists:
        c_art = c.artist.name
        if not(c_art in conc_dict):
            conc_dict[ c_art ] = []
        conc_dict[ c_art ].append( c )
    print(f"You have attended {Fore.GREEN}{len(setlists)}{Style.RESET_ALL} concerts by {Fore.GREEN}{len(conc_dict)}{Style.RESET_ALL} different artists.")

    date_dict = {}
    for c in setlists:
        c_date = c.event_date
        if not(c_date in date_dict):
            date_dict[ c_date ] = []
        date_dict[ c_date ].append( c )
    
    #fuzzy search for 'nearest' artist
    matching = process.extract(artist,conc_dict.keys())
    poss_matches = [x[0] for x in matching if x[1] > 85]
    if(poss_matches == []):
        poss_matches = [x[0] for x in matching[:3]]
    if len(poss_matches) > 1:
        print(f"Found multiple matches for {artist}: {poss_matches}")
        print(f'{Fore.GREEN}Please select the artist you were searching for:')
        print(f'{Fore.CYAN}0:{Style.RESET_ALL} None of the above '+', '.join([f'{Fore.CYAN}{i+1}:{Style.RESET_ALL} {x}' for i,x in enumerate(poss_matches)]))
        input_str = input()
        if input_str == '0':
            print(f"{Fore.RED}It seems you have not seen {artist} yet.")
            return
        else:
            artist = poss_matches[int(input_str)-1]
    else:
        artist = poss_matches[0]
    
    #now artist is properly chosen, print attended concerts
    print(f"Found {Fore.GREEN}{len(conc_dict[artist])}{Style.RESET_ALL} concerts for {Fore.GREEN}{artist}{Style.RESET_ALL}. You have been at:")
    for c in conc_dict[artist]:
        print( f" {Fore.CYAN+Style.BRIGHT}{datetime.strftime(c.event_date, '%d.%m.%Y')}{Style.RESET_ALL} at {Style.BRIGHT}{c.venue.name}{Style.RESET_ALL} in {Style.BRIGHT}{c.venue.city.name}{Style.RESET_ALL} " + (f"on the tour {Style.BRIGHT}{c.tour.name}{Style.RESET_ALL} " if c.tour!=None else ""), end='' )
        if len(date_dict[c.event_date])>1:
            print( f"{Style.NORMAL}along with {Fore.LIGHTWHITE_EX+Style.DIM}{', '.join(c.artist.name for c in date_dict[c.event_date] if c.artist.name!=artist)}{Style.RESET_ALL}" )
        else:
            print("")


if __name__ == "__main__":
    main()


