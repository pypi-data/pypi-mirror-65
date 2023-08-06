#!/usr/bin/env python

__copyright__ = 'Copyright 2013-2014, http://radical.rutgers.edu'
__license__   = 'MIT'

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
def state_cb(thing, state):
    print('CB: %s: %s' % (thing.uid, thing.state))


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()
    path    = '/home/merzky/radical/radical.pilot.devel/examples/'

    try:

        pmgr   = rp.PilotManager(session=session)
        umgr   = rp.UnitManager(session=session)
        pmgr.register_callback(state_cb)
        umgr.register_callback(state_cb)

        pd_init = {'resource'      : 'local.prte',
                   'runtime'       : 30,
                   'exit_on_error' : True,
                   'cores'         : 16
                  }
        pdesc = rp.ComputePilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)

        n = 2  # number of units to run

        umgr.add_pilots(pilot)
        cuds = list()
        for i in range(0, n):

            cud = rp.ComputeUnitDescription()
            cud.executable    = '%s/hello_rp.sh' % path
            cud.cpu_processes = 1
            cud.gpu_processes = 3
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()


    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

