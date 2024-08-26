
# SQBDotEXE
(A bad name a good friend of mine made up and it works enough, possibly up to change) \
Tthis is a program that helps with logging of SRB games by using data found on the localhost:8111 webserver the game hosts. It stores this data in a SQLlite3 database for use in looking at player statistics, vehicle statistics, squadron statistics, etc...
This uses the UI development framework QT through the Pyside6 python module
# Current Features
 - Logging of battles
 - Displaying up to date infromation of the current battle
 - Ability to look up statistics based on recorded battles
# Issues
- The Logger is not always reliable with a lot of edge cases that need catching
- I currently do not know a reliable way to record if you won or loss a battle
- this has only be tested and developed for a windows environment, probably wont change
# TODO
 - Look up a squadrons statistics and how they compare to another squadron (ie: their w/l record (this is still in dev))
- needs a lot of general exception handling and crashfile creation
- finish up and create different tabs
- makes sure the environment works outside my .venv and path variables





## Authors

- [@IhaveSwordz](https://github.com/IhaveSwordz), am member of P1KE dont doss me


