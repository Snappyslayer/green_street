/* Green Street coordinator model for Spin/Promela.
   Purpose: verify that the coordinator never commands undefined brightness
   and eventually returns to adaptive control after recovery.
*/

#define LOW 30
#define MEDIUM 60
#define HIGH 100
#define SAFE_DEFAULT 50
#define UNDEFINED -1

bool node_online = true;
bool motion = false;
byte ambient_dark = 1;
byte adaptive_control = 1;
int brightness = LOW;

proctype Coordinator()
{
    do
    :: node_online && motion ->
        brightness = HIGH;
        adaptive_control = 1;
        assert(brightness != UNDEFINED)

    :: node_online && !motion && ambient_dark ->
        brightness = MEDIUM;
        adaptive_control = 1;
        assert(brightness != UNDEFINED)

    :: node_online && !motion && !ambient_dark ->
        brightness = LOW;
        adaptive_control = 1;
        assert(brightness != UNDEFINED)

    :: !node_online ->
        brightness = SAFE_DEFAULT;
        adaptive_control = 0;
        assert(brightness != UNDEFINED)
    od
}

proctype Environment()
{
    do
    :: node_online = false
    :: node_online = true
    :: motion = !motion
    :: ambient_dark = 1 - ambient_dark
    od
}

init
{
    run Coordinator();
    run Environment();
}

/* LTL safety property:
   [] (brightness != UNDEFINED)
*/
ltl safety { [] (brightness != UNDEFINED) }

/* LTL liveness property:
   whenever the node is online, adaptive control should eventually resume.
*/
ltl liveness { [] (node_online -> <> adaptive_control) }
