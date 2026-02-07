# Time Guardian CLI Commands

# NOTE: YOU HAVE TO PLACE THIS FOLDER INTO THE PATH "/home/<username>/Applications/Open-source/Time guardian" BECUASE THEN THE COMMANDS ARE NOT GOING TO WORK

## This app is open-sourec so if you know how to work with bash and python files, modify the commands to be tailored to your custom path

Time Guardian is a headless and GUI app for tracking daily computer usage. These commands let you control and monitor your usage from the terminal.

## Commands

### `tg-time`

Shows how much time you have used and how much time is remaining.

Example command:
tg-time


Example output:
Used: 12m 30s
Remaining: 107m 30s

### `tg-help`

Shows all commands an their purposes.

Example command:
tg-help

Example output:
Time Guardian CLI Commands
-------------------------

tg-time        : Shows how much time you have used and how much time is remaining.
tg-live.time   : Shows a live updating timer of your usage in the terminal.
disable-tg     : Disables Time Guardian and stops the headless background process.
enable-tg      : Enables Time Guardian and starts the headless background process.
reset-tg       : Resets your usage counters back to 0.
tg-limit       : Sets your daily time limit. Can be run interactively or with arguments.
tg-help        : Shows this help message with all commands and their purposes.

Usage:
  tg-time
  tg-live.time
  disable-tg
  enable-tg
  reset-tg
  tg-limit
  tg-help


### `tg-live.time`

Shows a live updating timer of your usage in the terminal. Updates every second.

Example command:
tg-live.time


Example output:
Used: 13m 5s | Remaining: 106m 55s


Press `Ctrl+C` to exit.

### `disable-tg`

Disables Time Guardian and stops the headless background process.

Example command:
disable-tg


Output:
Time Guardian has been disabled.


### `enable-tg`

Enables Time Guardian and starts the headless background process.

Example command:
enable-tg


Output:
Time Guardian has been enabled.


### `reset-tg`

Resets your usage counters back to 0. The headless app continues counting from zero.

Example command:
reset-tg


Output:
Time Guardian usage has been reset.


### `tg-limit`

Sets your daily time limit for usage. Can be run interactively or with arguments.

#### Interactive:

Example command:
tg-limit


You will be prompted to enter your daily limit:
Enter daily limit in minutes: 90
Enter additional seconds (0 if none): 30


Output:
Daily limit set to 90m 30s


#### With arguments:

Example command:
tg-limit 60 15


Output:
Daily limit set to 60m 15s


## Notes

- All commands work with the headless background app.
- Notifications still work even if no GUI is open.
- Paths are absolute: `/home/waffle/Applications/Open-source/Time guardian/data/`.
- Make sure all scripts are executable in `/usr/local/bin`.