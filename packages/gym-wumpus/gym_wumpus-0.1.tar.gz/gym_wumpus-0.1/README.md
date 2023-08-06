## Wumpus World gym Environment
This package implements the famous wampus world enviornment. Below you can see a sample loaded environment.

```
#################################
#   .   |   .   |   .   |   .   #
#-------------------------------#
#   W   |   G   |   P   |   .   #
#-------------------------------#
#   .   |   .   |   .   |   .   #
#-------------------------------#
#   ^   |   .   |   P   |   .   #
#################################
```

The flash shows the agent, while 'W' shows the wumpus, 'P' indicates a pit, and 'G' shows the gold. The goal for the agent is to pickup the gold and get out of the maze from its entry point.

### Actions
The actions are as follow:
```
TurnRight: turns the agent's heading to right
TurnLeft: turns the agent's heading to left
Climb: climbs the wall. The agent can only climbs the wall(s) on its entry point
Forward: the agent moves forward one step based on its current heading
Shoot: the agent shoots an arrow (has only 1 arrow)
Grab: grabs the gold if its on the agent's location
```

### Rewards
The rewards are as follow:

```
-1: for each performed action
+1000: if the agent leaves with gold
-1000: if the agent dies (gets eaten by the wumpus or falls into a pit)
```