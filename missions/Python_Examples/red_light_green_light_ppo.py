# Rllib docs: https://docs.ray.io/en/latest/rllib.html
# Malmo XML docs: https://docs.ray.io/en/latest/rllib.html

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

import gym, ray
from gym.spaces import Discrete, Box
from ray.rllib.agents import ppo, impala

import malmoutils

import random

import _thread

class RedLightGreenLightGame(gym.Env):
    
    def __init__(self, env_config):
        self.obs_size = 60
        self.max_episode_steps = 100000000
        self.log_frequency = 10


        self.action_space = Box(np.array([-1]), np.array([1]))
        self.observation_space = Box(-2, 2, shape=(5 * self.obs_size * self.obs_size, ), dtype=np.float32)
        self.currVelo = 0



        self.Game_Player = MalmoPython.AgentHost()
        self.Game_Runner = MalmoPython.AgentHost()
        try:
            malmoutils.parse_command_line(self.Game_Player)
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.Game_Player.getUsage())
            exit(1)

        self.obs = None
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []
    
    def reset(self):
        #reset malmo
        world_state = self.init_malmo()

        #reset variables
        self.returns.append(self.episode_return)
        current_step =  self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0
        

        #log
        if len(self.returns) > self.log_frequency + 1 and \
            len(self.returns) % self.log_frequency == 0:
            self.log_returns()
        
        #get observation
        self.obs = self.get_observation(world_state)

        return self.obs
    
    def game_runner_threaded(self, gr, gp):
        tpval = [618.5, 621.5, 624.5, 627.5, 630.5, 615.5]
        while self.Game_Player.peekWorldState().is_mission_running and self.Game_Runner.peekWorldState().is_mission_running:
            i = 0
            timeDiff = 1 + random.random() * 2
            while self.Game_Player.peekWorldState().is_mission_running and self.Game_Runner.peekWorldState().is_mission_running and i < len(tpval):
                time.sleep(timeDiff)
                self.Game_Runner.sendCommand(f"tpx {str(tpval[i])}")
                i += 1
    
    def step(self, action):
        def momentum(acceleration):
            #increase time val
            for i in range(10000):
                self.currVelo += acceleration * 0.0001
                if self.currVelo < 0:
                    self.currVelo = 0
                elif self.currVelo > 1:
                    self.currVelo = 1
                command1 = f"move {self.currVelo}"
                self.Game_Player.sendCommand(command1)
                time.sleep(0.0001)
        # Get Action
        momentum(action[0])
        self.episode_step += 1

        #Get Observation
        world_state = self.Game_Player.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
        self.obs = self.get_observation(world_state)


        # Get Done
        done = not world_state.is_mission_running
        
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()
        self.episode_return += reward


        if (len(np.argwhere(self.obs == 2)) >= 1) and self.currVelo != 0:
            print("velo =", self.currVelo)
            done = True
            self.episode_return -= 200
            self.Game_Runner.sendCommand("tpx 652.5")
            self.Game_Runner.sendCommand("tpy 4")
            self.Game_Runner.sendCommand("tpz 777.5")
        
        return self.obs, reward, done, dict()

    def get_mission_xml(self):
        #<AgentQuitFromReachingCommandQuota total="100" />
        def get_world_path():
            # Amar
            # filePath ="\"C:\\malmo\\malmo\\Minecraft\\run\\saves\\CS175Main\""
            # Tim
            # filePath = ""
            # Vik
            # filePath = "\"C:\\Users\\Timothy\\Desktop\\175_test\\redlightgreenlight\\CS175world_new\""
            # filePath = "\"/Users/vikram/Documents/CS175_malmo/MalmoPlatform/Minecraft/run/saves/CS175world_new\""
            filePath = "\"/home/vikram/Desktop/uci_stuff/fourth_year/CS_175/MalmoPlatform/Minecraft/run/saves/CS175world_new\""

            fileWorldGenerator = f"<FileWorldGenerator src ={filePath} />"

            return fileWorldGenerator


        def get_all_movement_reward_locations():
            out = "<RewardForReachingPosition>"
            i = 826.5
            while (i >= 777.5):
                out +=  '''
                            <Marker x="624.5" y="4" z="''' + str(i) + '''" reward = "1" tolerance="0.25" />
                        '''
                i -= 1
            out += '\n</RewardForReachingPosition>'
            return out
        
        return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <About>
                    <Summary>two agent test</Summary>
                </About>

                <ServerSection>
                    <ServerInitialConditions>
                        <Time>
                            <StartTime>0</StartTime>
                        </Time>
                        <Weather>clear</Weather>
                    </ServerInitialConditions>
                    <ServerHandlers>''' \
                        + get_world_path() + '''
                        <ServerQuitFromTimeUp description="" timeLimitMs="1000000"/>
                        <ServerQuitWhenAnyAgentFinishes description=""/>
                    </ServerHandlers>
                </ServerSection>


                <AgentSection mode="Survival">
                    <Name>CS175_project</Name>
                    <AgentStart>
                        <Placement x="624.5" y="4" z="825.5" pitch="15" yaw="180"/>
                        <Inventory>
                            <InventoryItem slot="0" type="map"/>
                        </Inventory>
                    </AgentStart>
                    <AgentHandlers>
                        <ObservationFromFullStats/>
                        <ObservationFromRay/>
                        <ObservationFromGrid>
                            <Grid name="floorAll">
                                <min x="-'''+str(int(30))+'''" y="-1" z="-'''+str(int(60))+'''"/>
                                <max x="'''+str(int(30))+'''" y="4" z="'''+str(int(0))+'''"/>
                            </Grid>
                        </ObservationFromGrid>
                        <RewardForTouchingBlockType>
                            <Block reward="100" type="iron_block" /> 
                        </RewardForTouchingBlockType>''' \
                        + get_all_movement_reward_locations() + '''
                        <AgentQuitFromTouchingBlockType>
                            <Block type="iron_block" />
                        </AgentQuitFromTouchingBlockType>
                        <ContinuousMovementCommands/>
                        <VideoProducer>
                            <Width>860</Width>
                            <Height>480</Height>
                        </VideoProducer>
                    </AgentHandlers>
                </AgentSection>

                <AgentSection mode="Survival">
                    <Name>Game_Runner</Name>
                    <AgentStart>
                        <Placement x="618.5" y="4" z="763.5" pitch="15" yaw="100"/>
                    </AgentStart>
                    <AgentHandlers>
                        <AgentQuitFromTouchingBlockType>
                            <Block type="iron_block" />
                        </AgentQuitFromTouchingBlockType>
                        <AbsoluteMovementCommands/>
                    </AgentHandlers>
                </AgentSection>
            </Mission>'''
        
    def safeStartMission(self, game_runner, my_mission, my_client_pool, my_mission_record, role, expId):
        print("Starting Mission {}.".format(role))
        max_retries = 5
        for retry in range(max_retries):
            try:
                game_runner.startMission(
                    my_mission, my_client_pool, my_mission_record, role, expId)
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)
    
    def safeWaitForStart(self, agent_hosts):
        start_flags = [False for a in agent_hosts]
        start_time = time.time()
        time_out = 120
        while not all(start_flags) and time.time() - start_time < time_out:
            states = [a.peekWorldState() for a in agent_hosts]
            start_flags = [w.has_mission_begun for w in states]
            errors = [e for w in states for e in w.errors]
            if len(errors) > 0:
                print("Errors waiting for mission start")
                for e in errors:
                    print(e.text)
                exit(1)
            time.sleep(0.1)
            print(".", end=' ')
        if time.time() - start_time >= time_out:
            print("Timed out while waiting for mission to start.")
            exit(1)
        print()
        print("Mission has started.")
    
    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)

        player_recording_spec = MalmoPython.MissionRecordSpec()
        runner_recording_spec = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        client_pool = MalmoPython.ClientPool()
        client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10002))
        client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10003))
        self.safeStartMission(self.Game_Player, my_mission, client_pool,
                 player_recording_spec, 0, '')
        self.safeStartMission(self.Game_Runner, my_mission, client_pool,
                 runner_recording_spec, 1, '')

        self.safeWaitForStart([self.Game_Player, self.Game_Runner])
        time.sleep(2)
        _thread.start_new_thread(self.game_runner_threaded, (self.Game_Runner, self.Game_Player))

        world_state = self.Game_Player.getWorldState()
        return world_state
    
    def get_observation(self, world_state):
        """
        Use the agent observation API to get a flattened 5 x 60 x 60 grid around the agent. 
        The agent is in the center square facing up.

        Args
            world_state: <object> current agent world state

        Returns
            observation: <np.array> the state observation
        """

        obs = np.zeros((5 * 60 * 60))

        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = self.Game_Player.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:

                msg = world_state.observations[-1].text
                observations = json.loads(msg)

                # Get observation
                grid = observations['floorAll']
                # print("grid =", len(grid))
                # print(grid)
                blockTypes = {}
                for i, x in enumerate(grid):
                    blockTypes[x] = True
                
                for i, x in enumerate(grid):
                    if x == 'lit_redstone_lamp':
                        obs[i] = 1
                    elif x == 'redstone_lamp':
                        obs[i] = -1
                
                index_minus = np.argwhere(obs == -1)
                index_minus = index_minus[-1] if len(index_minus) >= 1 else -1
                index_pos = np.argwhere(obs == 1)
                index_pos = index_pos[-1] if len(index_pos) >= 1 else -1
                maxIndex = max(index_minus, index_pos)
                val = obs[maxIndex]
                obs[maxIndex] = -2 if val == -1 else 2
                
                break

        return obs

    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns[1:], box, mode='same')
        plt.clf()
        plt.plot(self.steps[1:], returns_smooth)
        plt.title('Red Light Green Light Game')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns_ppo_torch.png')

        with open('returns_ppo_torch.txt', 'w') as f:
            for step, value in zip(self.steps[1:], self.returns[1:]):
                f.write("{}\t{}\n".format(step, value)) 

if __name__ == '__main__':
    ray.init()
    # trainer_impala = impala.ImpalaTrainer(env=RedLightGreenLightGame, config={
    #     'env_config': {},           # No environment parameters to configure
    #     'framework': 'tf',       # Use pyotrch instead of tensorflow
    #     'num_gpus': 1,              # We aren't using GPUs
    #     'num_workers': 0            # We aren't using parallelism
    # })
    trainer_ppo = ppo.PPOTrainer(env=RedLightGreenLightGame, config={
        'env_config': {},           # No environment parameters to configure
        'framework': 'torch',       # Use pyotrch instead of tensorflow
        'num_gpus': 1,              # We aren't using GPUs
        'num_workers': 0            # We aren't using parallelism
    })

    while True:
        print(trainer_ppo.train())
        