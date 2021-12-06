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

## References

- [Minecraft Wiki](https://minecraft.fandom.com/wiki/Minecraft_Wiki)
- [Project Malmo Documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
- [Malmo and RLlib Tutorials Youtube Playlist](https://www.youtube.com/playlist?list=PLa9uQbheNAMn7QuE-OnXBGWfRyVGiJSpU)
- [Project Malmo Gitter](https://gitter.im/Microsoft/malmo)
- [Ray Documentation](https://docs.ray.io/en/latest/rllib.html)
- [Gym Documentation](http://gym.openai.com/docs/)