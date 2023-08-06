
# The agent scheduler cpi is a thin API wrapper around the scheduler's ZMQ input
# protocol: it essentially translates task submissions into scsheduling requests
# for said tasks and subscribes to the state pubsub for state updates.
#
# we use `task.cpi.rpas.%06d` as task uids so that we don't conflict with other
# tasks.


class AgentSchedulerCPI(object):

    _skeleton = {
                 "_id"                  : "unit.000000",
                 "uid"                  : "unit.000000",
                 "type"                 : "unit",
                 "name"                 : "",
                 "umgr"                 : None,
                 "pilot"                : None,
                 "client_sandbox"       : None,
                 "cmd"                  : list(),
                 "control"              : "agent",
                 "exit_code"            : None,
                 "stderr"               : None,
                 "stdout"               : None,
                 "pilot_sandbox"        : None,
                 "unit_sandbox"         : None,
                 "unit_sandbox_path"    : None,
                 "resource_sandbox"     : "file://localhost/home/merzky/radical.pilot.sandbox",
                 "state"                : "AGENT_SCHEDULING_PENDING",
                 "states"               : [
                     "NEW",
                     "UMGR_SCHEDULING_PENDING",
                     "UMGR_SCHEDULING",
                     "UMGR_STAGING_INPUT_PENDING",
                     "UMGR_STAGING_INPUT",
                     "AGENT_STAGING_INPUT_PENDING"
                 ],
                 "description"          : {
                     "name"             : None,
                     "kernel"           : None,
                     "executable"       : None,
                     "arguments"        : list(),
                     "environment"      : dict(),
                     "cpu_process_type" : "",
                     "cpu_processes"    : 1,
                     "cpu_thread_type"  : "",
                     "cpu_threads"      : 1,
                     "gpu_process_type" : "",
                     "gpu_processes"    : 0,
                     "gpu_thread_type"  : "",
                     "gpu_threads"      : 1,
                     "lfs_per_process"  : 0,
                     "mem_per_process"  : 0,
                     "pilot"            : "",
                     "metadata"         : None,
                     "post_exec"        : list(),
                     "pre_exec"         : list(),
                     "restartable"      : False,
                     "sandbox"          : "",
                     "input_staging"    : list(),
                     "output_staging"   : list(),
                     "stderr"           : "",
                     "stdout"           : "",
                     "tags"             : dict(),
                     "cleanup"          : False
                 }
             }


    def __init__(self):

        # FIXME: connect to channels
        pass


    def register_callback(self, cb):
        pass


    def submit(self, tds):
        pass


