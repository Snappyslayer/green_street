mtype = { ONLINE, OFFLINE, MOTION, NO_MOTION, LOW_20, HIGH_100, SAFE_DEFAULT_60 };

mtype node_status = ONLINE;
mtype node_event = NO_MOTION;
mtype coord_cmd = LOW_20;

bool turn_coordinator = false; // Synchronizes the bounded reaction time

active proctype Node() {
    do
    :: !turn_coordinator -> // Node's turn to simulate real-world events
       if
       :: node_status = ONLINE; node_event = MOTION;
       :: node_status = ONLINE; node_event = NO_MOTION;
       :: node_status = OFFLINE; node_event = NO_MOTION;
       fi;
       turn_coordinator = true; // Pass control to Coordinator
    od
}

active proctype Coordinator() {
    do
    :: turn_coordinator -> // Coordinator calculates the adaptive policy
       if
       :: node_status == OFFLINE -> coord_cmd = SAFE_DEFAULT_60;
       :: node_status == ONLINE && node_event == MOTION -> coord_cmd = HIGH_100;
       :: node_status == ONLINE && node_event == NO_MOTION -> coord_cmd = LOW_20;
       fi;
       turn_coordinator = false; // Pass control back to Node
    od
}

// 1. Safety: If offline, coordinator eventually commands safe fallback
ltl safety { [] ((node_status == OFFLINE) -> <> (coord_cmd == SAFE_DEFAULT_60)) }

// 2. Liveness: If motion detected, brightness eventually goes to 100%
ltl liveness { [] ((node_status == ONLINE && node_event == MOTION) -> <> (coord_cmd == HIGH_100)) }
