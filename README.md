# wordle-scoreboard

A discord bot that compiles, and schedules messages of a wordle weekly scoreboard in a discord channel, from user wordle score messages. 
Weekly scoreboard can be set to schedule messages, and commands exist to display the current scoreboard.


The bot is not online to add to discord servers, and I don't plan to run a 24/7 server to keep it up. Send me a message and I will make it live!

- The bot is added to the discord server
- Users post their wordle results
- users can use the !scoreboard command to calculate and post a scoreboard among those that posted their wordle results this week.


Example wordle result message:

Wordle 642 5/6*

🟩⬜🟩🟨⬜

🟩🟩🟩🟩⬜

🟩🟩🟩🟩⬜

🟩🟩🟩🟩⬜

🟩🟩🟩🟩🟩


!scoreboard command:

week of 03-20-2023
╒════════╤═══════════════╤════════════╤═══════╤═════════════╤═════════════════╕
│ placed │ player        │  avg_score │  wins │ submissions │ S M T W T F S   │
╞════════╪═══════════════╪════════════╪═══════╪═════════════╪═════════════════╡
│      1 │ Oliverinspace │        4.2 │     5 │           5 │ - 3 5 - 6 4 3   │
├────────┼───────────────┼────────────┼───────┼─────────────┼─────────────────┤
│      2 │ Krest_12      │        4   │     2 │           2 │ - - 4 4 - - -   │
╘════════╧═══════════════╧════════════╧═══════╧═════════════╧═════════════════╛
 weekly scoreboard closes in: 1 day, 12:56:25

