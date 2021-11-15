try:
    from malmo import MalmoPython
except:
    import MalmoPython

import time

import malmoutils

import random

import _thread
import numpy as np
import json

def safeStartMission(agent_host, my_mission, my_client_pool, my_mission_record, role, expId):
    print("Starting Mission {}.".format(role))
    max_retries = 5
    for retry in range(max_retries):
        try:
            agent_host.startMission(
                my_mission, my_client_pool, my_mission_record, role, expId)
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:", e)
                exit(1)
            else:
                time.sleep(2)


def safeWaitForStart(agent_hosts):
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


def get_world_path():
    # Amar
    # filePath ="\"C:\\malmo\\malmo\\Minecraft\\run\\saves\\CS175Main\""
    # Tim
    # filePath = ""
    # Vik
    # filePath = "\"C:\\Users\\Timothy\\Desktop\\175_test\\redlightgreenlight\\CS175world_new\""
    filePath = "\"/Users/vikram/Documents/CS175_malmo/MalmoPlatform/Minecraft/run/saves/CS175world_new\""

    fileWorldGenerator = f"<FileWorldGenerator src ={filePath} />"

    return fileWorldGenerator

def game_runner_threaded(game_runner, game_player):
    while game_player.peekWorldState().is_mission_running and game_runner.peekWorldState().is_mission_running:
        timeDiff = 0.5 + random.random() * 1.5
        # print(timeDiff)
        game_runner.sendCommand("tpx 618.5")
        time.sleep(timeDiff)
        game_runner.sendCommand("tpx 621.5")
        time.sleep(timeDiff)
        game_runner.sendCommand("tpx 624.5")
        time.sleep(timeDiff)
        game_runner.sendCommand("tpx 627.5")
        time.sleep(timeDiff)
        game_runner.sendCommand("tpx 630.5")
        time.sleep(timeDiff)
        game_runner.sendCommand("tpx 615.5")
        time.sleep(1 + random.random() * 4)


def get_observation():
    """
    Use the agent observation API to get a flattened 2 x 5 x 5 grid around the agent. 
    The agent is in the center square facing up.

    Args
        world_state: <object> current agent world state

    Returns
        observation: <np.array> the state observation
        allow_break_action: <bool> whether the agent is facing a diamond
    """
    obs = np.zeros((60*60 ))
    world_state = Game_Player.getWorldState()
    while world_state.is_mission_running:
        time.sleep(0.1)
        world_state = Game_Player.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:

            msg = world_state.observations[-1].text
            observations = json.loads(msg)

            # Get observation
            grid = observations['floorAll']
            print("grid =", grid[0])
            # print(grid)
            # blockTypes = {}
            # for i, x in enumerate(grid):
            #     blockTypes[x] = True
            # print(blockTypes.keys())
            # for i, x in enumerate(grid):
            #     obs[i] = x == 'diamond_ore' or x == 'lava'

            # # Rotate observation with orientation of agent
            # obs = obs.reshape((2, self.obs_size, self.obs_size))
            # yaw = observations['Yaw']
            # if yaw >= 225 and yaw < 315:
            #     obs = np.rot90(obs, k=1, axes=(1, 2))
            # elif yaw >= 315 or yaw < 45:
            #     obs = np.rot90(obs, k=2, axes=(1, 2))
            # elif yaw >= 45 and yaw < 135:
            #     obs = np.rot90(obs, k=3, axes=(1, 2))
            # obs = obs.flatten()

        
        break

    return obs



xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
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
                <Name>Game_Player</Name>
                <AgentStart>
                    <Placement x="624.5" y="4" z="825.5" pitch="15" yaw="180"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_pickaxe"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <ObservationFromFullStats/>
                    <ObservationFromRay/>
                    <ObservationFromGrid>
                        <Grid name="floorAll">
                            <min x="-'''+str(int(7))+'''" y="-1" z="-'''+str(int(60))+'''"/>
                            <max x="'''+str(int(7))+'''" y="7" z="'''+str(int(0))+'''"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ContinuousMovementCommands/>
                    <VideoProducer>
                        <Width>860</Width>
                        <Height>480</Height>
                    </VideoProducer>
                    <AgentQuitFromReachingCommandQuota total="100" />
                </AgentHandlers>
            </AgentSection>


            <AgentSection mode="Survival">
                <Name>Game_Runner</Name>
                <AgentStart>
                    <Placement x="618.5" y="4" z="763.5" pitch="15" yaw="100"/>
                </AgentStart>
                <AgentHandlers>
                    <AbsoluteMovementCommands/>
                </AgentHandlers>
            </AgentSection>
            
        </Mission>'''

Game_Player = MalmoPython.AgentHost()
Game_Runner = MalmoPython.AgentHost()
malmoutils.parse_command_line(Game_Player)

my_mission = MalmoPython.MissionSpec(xml, True)

client_pool = MalmoPython.ClientPool()
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000))
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10001))

actual_recording_spec = MalmoPython.MissionRecordSpec()
dummy_recording_spec = MalmoPython.MissionRecordSpec()

safeStartMission(Game_Player, my_mission, client_pool,
                 actual_recording_spec, 0, '')
safeStartMission(Game_Runner, my_mission, client_pool,
                 dummy_recording_spec, 1, '')

safeWaitForStart([Game_Player, Game_Runner])

_thread.start_new_thread(game_runner_threaded, (Game_Runner, Game_Player))

while Game_Player.peekWorldState().is_mission_running and Game_Runner.peekWorldState().is_mission_running:
    # Game_Player.sendCommand("move 1")
    # time.sleep(0.5)
    Game_Player.sendCommand("move 0")
    time.sleep(2)
    get_observation()
    # print("moved Forward")
    # Testing_Dummy.sendCommand("tpx 5.5")
    # Testing_Dummy.sendCommand("tpz 5.5")
    # time.sleep(0.5)
    # print("stop")
    # Testing_Dummy.sendCommand("tpx 0.5")
    # Testing_Dummy.sendCommand("tpz 0.5")
    # time.sleep(0.5)


print("mission ended")


exit(1)
