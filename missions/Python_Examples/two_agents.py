try:
    from malmo import MalmoPython
except:
    import MalmoPython

import time

import malmoutils

import random

import _thread

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
    filePath = "\"/Users/vikram/Documents/CS175_malmo/MalmoPlatform/Minecraft/run/saves/CS175world_new\""

    fileWorldGenerator = f"<FileWorldGenerator src ={filePath} />"

    return fileWorldGenerator

def game_runner_threaded(game_runner, game_player):
    while game_player.peekWorldState().is_mission_running and game_runner.peekWorldState().is_mission_running:
        timeDiff = random.random() * 4
        print(timeDiff)
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
                    <AgentQuitFromReachingCommandQuota total="100" />
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
    Game_Player.sendCommand("move 1")
    time.sleep(0.1)
    Game_Player.sendCommand("move 0")
    time.sleep(2)
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
