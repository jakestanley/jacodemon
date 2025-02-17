# In progress

# Planned

- Enemies count in map picker (optional)
- In depth analysis, which maps were easy? How many attempts before you completed a map for the first time?
- WAD locations and PWAD search (uses WAD.TXT if available)
- WADSeeker integration
- Download map? list archive?
- Add FINISHED to auto-records output file rename
- Option to delete recording instead of saving
- 3.0.0 release which will be free of bugs and the code will be decent (lmao)
- Tag/rate maps. Tags like "awesome-music", "challenging", etc. Memento Mori's "Galaxy" is great!

# Done
- Replay buffer naming

# Out of scope

## Other source ports

I'm thinking if you've got to the point you want to use a tool like this to 
handle recording your Doom career, you've probably already realised that 
DSDA Doom is one of the best tools for this, so at this point I will not be 
supporting other ports, though I do wish to make the code extensible enough 
to support such options. I made this scope decision in February 2025 after I 
have already written some code for Crispy/Chocolate Doom, so I'll leave that 
in for now, unused.

# Bugs
- If you quit during saving the replay buffer, then the replay buffer does not get renamed

None that I know of at the moment yay
