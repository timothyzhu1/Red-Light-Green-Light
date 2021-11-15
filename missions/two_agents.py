try:
    from malmo import MalmoPython
except:
    import MalmoPython

import time

import malmoutils


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
    filePath = "\"C:\\Desktop\\175_test\\redlightgreenlight\\CS175world_new\""

    fileWorldGenerator = f"<FileWorldGenerator src ={filePath} />"

    return fileWorldGenerator


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
                <Name>Testing_Actual</Name>
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
                <Name>Testing_Dummy</Name>
                <AgentStart>
                    <Placement x="618.5" y="4" z="763.5" pitch="15" yaw="100"/>
                </AgentStart>
                <AgentHandlers>
                    <ContinuousMovementCommands/>
                    <AgentQuitFromReachingCommandQuota total="100" />
                </AgentHandlers>
            </AgentSection>
            
        </Mission>'''

Testing_Actual = MalmoPython.AgentHost()
Testing_Dummy = MalmoPython.AgentHost()
malmoutils.parse_command_line(Testing_Actual)

my_mission = MalmoPython.MissionSpec(xml, True)

client_pool = MalmoPython.ClientPool()
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000))
client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10001))

actual_recording_spec = MalmoPython.MissionRecordSpec()
dummy_recording_spec = MalmoPython.MissionRecordSpec()

safeStartMission(Testing_Actual, my_mission, client_pool,
                 actual_recording_spec, 0, '')
safeStartMission(Testing_Dummy, my_mission, client_pool,
                 dummy_recording_spec, 1, '')

safeWaitForStart([Testing_Actual, Testing_Dummy])

while Testing_Actual.peekWorldState().is_mission_running or Testing_Dummy.peekWorldState().is_mission_running:
    pass
    Testing_Actual.sendCommand("move 1")
    time.sleep(0.1)
    Testing_Actual.sendCommand("move 0")
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
