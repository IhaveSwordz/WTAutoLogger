
# SQBDotEXE
(A bad name a good friend of mine made up and it works enough, possibly up to change) \
Tthis is a program that helps with logging of SRB games by using data found on the localhost:8111 webserver the game hosts. It stores this data in a SQLlite3 database for use in looking at player statistics, vehicle statistics, squadron statistics, etc...
This uses the UI development framework QT through the Pyside6 python module
# Current Features
 - Logging of battles
 - Displaying up to date infromation of the current battle
 - Ability to look up statistics based on recorded battles
 - can read replays (to a limited capacity) to gain extra info about a battle
# Issues
- The Logger is not always reliable with a lot of edge cases that need catching
- this has only be tested and developed for a windows environment, probably wont change
# TODO
 - Look up a squadrons statistics and how they compare to another squadron (ie: their w/l record (this is still in dev))
- needs a lot of general exception handling
- finish up and create different tabs
- makes sure the environment works outside my .venv and path variables (half there)
- make a compiled executable that is actually runnable on download (currently needs manual setup for directories and git)




## Authors

- [@IhaveSwordz](https://github.com/IhaveSwordz), am member of P1KE dont doss me


