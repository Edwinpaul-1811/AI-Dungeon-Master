% Transitions
path(start, explore, atrium).
path(start, shout, echo).

path(atrium, upstairs, library).
path(atrium, downstairs, crypt).

path(library, open, curse).
path(library, leave, balcony).

path(balcony, jump, portal).
path(balcony, retreat, atrium).

path(crypt, approach, guardian).
path(crypt, run, pitfall).

path(guardian, 'wish for power', corruption).
path(guardian, 'wish for peace', ascend).

% Endings
ending(echo).
ending(curse).
ending(pitfall).
ending(portal).
ending(corruption).
ending(ascend).
