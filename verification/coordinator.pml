mtype = { ONLINE, OFFLINE, MOTION, NO_MOTION, LOW_20, HIGH_100, SAFE_DEFAULT_60 };

mtype node_status = ONLINE;
mtype node_event = NO_MOTION;
mtype coord_cmd = LOW_20;
bool turn_coordinator = false;

active proctype Node() {
    do
    :: !turn_coordinator -> 
       if
       :: node_status = ONLINE; node_event = MOTION;
       :: node_status = ONLINE; node_event = NO_MOTION;
       :: node_status = OFFLINE; node_event = NO_MOTION;
       fi;
       turn_coordinator = true;
    od
}

active proctype Coordinator() {
    do
    :: turn_coordinator -> 
       if
       :: node_status == OFFLINE -> coord_cmd = SAFE_DEFAULT_60;
       :: node_status == ONLINE && node_event == MOTION -> coord_cmd = HIGH_100;
       :: node_status == ONLINE && node_event == NO_MOTION -> coord_cmd = LOW_20;
       fi;
       turn_coordinator = false;
    od
}

// 1. Strict Safety: It is NEVER the case that the node is OFFLINE, the coordinator has processed the turn, and brightness is NOT SAFE_DEFAULT.
ltl safety { [] ((node_status == OFFLINE && !turn_coordinator) -> (coord_cmd == SAFE_DEFAULT_60)) }

// 2. Liveness: If motion is detected, the system will eventually hit HIGH_100.
ltl liveness { [] ((node_status == ONLINE && node_event == MOTION) -> <> (coord_cmd == HIGH_100)) }

// 3. Bounded Recovery: If the node is ONLINE, the coordinator recovers and does NOT command the failure state.
ltl recovery { [] ((node_status == ONLINE && !turn_coordinator) -> (coord_cmd != SAFE_DEFAULT_60)) }
