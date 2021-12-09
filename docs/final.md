---
layout: default
title: Final Report
---


## Video

## Project Summary

Our project is based on the game 'Red Light Green Light' depict in the popualr Netlflix show, Squid Game. Our agent will spawn at one end of an arena, and attempt to reach the finish line at the other end. At the end of the arena (farthest from the agent spawn), there is a line of blocks denoting the finish line and 5 light blocks. These light blocks will repeatedly light up sequentially from left to right. The agent will need to read these light blocks from the observation space, and move only when the rightmost light is unlit. In other words, the agent will be eliminated if it moves while the rightmost light is lit. Through rewards and penalties, the agent should ultimately learn to sotp moving when the rightmost light (the "Red light") is lit and to anticipate this light turning on. 

To further increase the complexity of this task, we have implemented additional features. The first is that the delta or duration between the light blocks will be different between rounds. This will prevent the agent from quickly memorizing the light timings.

Additionally, the agent must contend with a momentum wrapper that we have added to Malmo. This will simulate real movement by implementing accelaration and momentum into the agents movements. The wrapper effectively prevents the agent from stopping immediately right before the last light is turned on, and from starting immediately when the last light is turned off. This adds further complexity because the agent must learn when to start slowing down based on the duration between the lights of that particular sequence. 

As for movement, the agent is reward and penalized for moving forwards towards the goal and backwards towards the start, respectively. The acceleration/momentum wrapper directly affects the speed of the agent. 

As the agent moves foward or backwards, it may experience obstacles that will obstruct its movement. Lava pits will be randomly spawned on each run such that the agent must avoid them. A run in with these lava pits will obviously result in death and reset. To enable the agent to avoid the pits, the agent will be allowed to strafe left and right around the pits. However, the agent will not be able to turn.


## Approaches

## Evaluation

Currently, our methods of evaluation consist of the agent’s performance based on completion, directional distance travelled, and efficiency of the path. Our evaluation of completion is reliant on many factors affected by the agent’s movements. More specifically, while the only way the agent can complete the mission is to reach the finish line, there are multiple ways for the agent to fail to complete the mission. For example, if the agent touches a lava pit (in one approach) or moves while the last light is on (in all approaches), it is eliminated from the game. In any case, the agent is rewarded or penalized heavily, according to the outcome observed. 
Similarly, our evaluation of directional distance travelled is determined solely by whether the agent moves forward or backward. Specifically, for each step that the agent takes forward, it is rewarded slightly, and for each step that the agent takes backward, it is penalized by the same amount. This method of evaluation ensures that the agent learns the importance of incrementally taking steps forward, rather than backward, and the objective of the game, which is to reach the finish line without moving while the rightmost light is on. 
Our evaluation of the efficiency of the path is mainly determined by the left and right strafing of the agent. To improve the efficiency of our agent’s movements, we have also considered rewarding or penalizing the agent for moving left and right unnecessarily; however this proved to be ineffective. We found that disregarding left and right movements of the agent, for the purposes of training, was satisfactory, as it allowed the agent to discover an efficient path, avoiding the obstacles, without any consequences for doing so. 
 
Our qualitative evaluation of the agent’s performance is based on similar principles. To evaluate completion, we consider the mission a success if the agent reaches the finish line, and we consider it a failure if the agent moves while the rightmost light is on or if the agent touches a lava pit. In any of these cases, the mission ends and the agent is removed from the game. We also consider any unnecessary moves that the agent makes. Specifically, we want to minimize backward movements from the agent. While backward movements may be necessary in some scenarios, due to the obstacles we have included in the arena, moving backward is usually inefficient and it can be seen visually. In this sense, we evaluate the “smoothness” of the agent’s movements, where the agent stops in anticipation of the rightmost light turning on, remains immobile for the entire duration, and begins moving immediately after it turns off. This will require preemptive stopping and moving from the agent, due to the implementation of acceleration and momentum within our agent. Ultimately, we want to see the agent move as efficiently as possible, to minimize the amount of time it takes to reach the finish line. 
 
Below are plots of our agent’s performance across numerous rounds of training and with various learning algorithms and environments:


## References

- [Minecraft Wiki](https://minecraft.fandom.com/wiki/Minecraft_Wiki)
- [Project Malmo Documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
- [Malmo and RLlib Tutorials Youtube Playlist](https://www.youtube.com/playlist?list=PLa9uQbheNAMn7QuE-OnXBGWfRyVGiJSpU)
- [Project Malmo Gitter](https://gitter.im/Microsoft/malmo)
- [Ray Documentation](https://docs.ray.io/en/latest/rllib.html)
- [Gym Documentation](http://gym.openai.com/docs/)