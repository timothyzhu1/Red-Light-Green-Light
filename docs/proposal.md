---
layout: default
title: Proposal
---

## Summary of the Project
Our project is based on the game Red Light, Green Light from Squid Game, which we will implement with Malmo. Our agent will start at one end of the room, and endeavour to reach the other end. There will be a traffic light presented in the arena that can either be red or green at any given time. The challenge for our agent is that it can only move forward and when the light is green. If it moves when the light is red, it is eliminated from the game. The inputs to the engine will be the color of the light and the remaining distance to the finish line. The outputs of the engine will be the movement and survival of the agent. A possible application of this project is traffic light recognition of cars on the road.  

## AI/ML Algorithms
Reinforcement learning with computer vision

## Evaluation Plan
Quantitatively, we will measure the agent’s final distance from the goal and its success rate. We will also measure its time performance. Specifically, we will implement a time limit that the agent must reach the finish line by, and if it reaches the destination within this time limit, we will score its performance based on how long it took. As a baseline, we will measure how long it should take the agent to reach the goal, if it played optimally. Since this is hard to achieve, we expect our agent to be much slower than this baseline, especially in the earlier iterations. We also expect our agent to constantly fail the mission in the initial iterations. As training goes on, it will improve and eventually successfully reach the goal. As training improves further, it will reduce the amount of time it takes to reach the goal. 

Qualitatively, we will evaluate the success of this project by seeing if the agent reaches the goal or not. We will also want to see the agent make as few unnecessary moves as possible. We want to see smooth movements, where the agent stops in anticipation to a red light and remains immobile for the entire duration of the red light. Since our agent will have delayed movements and stopping (to simulate human reaction time), we would ideally want to see our agent be able to accurately judge when the light will turn red or green, preemptively stopping and moving. With each iteration, we want to see the agents move as efficiently as possible, to minimize the amount of time it takes to reach the finish line.


## Appointment with the Instructor
October 26, 2021 3PM 