## Have I Seen *{artist}*?

While `setlist.fm` allows its users to track all the concerts they have attended, the website does not offer a search for artists and when you have attended concerts by them.
This `python3.10`-tool fills this gap. All you need for this is your `setlist.fm` username and an [API-key](https://www.setlist.fm/settings/api).
Setlists are cached locally to reduce API calls.

### Example Usage

Running the command as
```
./haveIseen.py -api API_KEY -id USER_ID 'Insomnium'
```
gives
```
Read concert and setlist info of USER_ID from cache.
You have attended 599 concerts by 397 different artists.
Found 10 concerts for Insomnium. You have been at:
 02.10.2022 at Eventhalle Airport in Obertraubling on the tour Vltima Ratio Fest 2022 along with Hinayana, Moonspell, Wolfheart, Borknagar
 07.12.2019 at Music Hall in Geiselwind on the tour Tour Like a Grave along with Kataklysm, The Black Dahlia Murder, Whitechapel, Fleshgod Apocalypse, Dyscarnate
 23.06.2019 at Boeretang in Dessel along with KISS, Sabaton, Gojira, In Flames, Orange Goblin, Kvelertak, Fleshgod Apocalypse, Deadland Ritual, Uncle Acid & the deadbeats, Def Leppard, Whitesnake, Hawkwind
 18.08.2017 at Flugplatz des Aeroclubs Dinkelsbühl in Dinkelsbühl along with Kreator, Wintersun, Amorphis, Belphegor, Cellar Darling, Sonata Arctica, Mors Principium Est, 1349, Crowbar
 27.01.2017 at Technikum in Munich on the tour Winter's Gate European Tour 2017 along with Wolfheart, Barren Earth
 11.11.2014 at Hansa 39 in Munich on the tour Shadows Of The Dying Sun Over Europe 2014 along with Stamina, Fleshgod Apocalypse
 18.10.2013 at Messehalle in Straubing on the tour Halo of Blood Over Europe 2013 along with Mynded, Children of Bodom, Immortal, Sodom, Collapsed Minds
```

The output is also highlighted nicely in most terminals, so it is easier to read.

Use `-h` to get additional help on the arguments.

### Requirements

The tool relies mainly on the package `setlist-fm-client`, see `requirements.txt` for details.

