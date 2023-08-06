# Networks dynamics simulation base class
#
# Copyright (C) 2017--2019 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

import epyc
import networkx


class Dynamics(epyc.Experiment, object):
    '''An abstract simulation framework for running a process over a network.
    This is the abstract base class
    for implementing different kinds of dynamics as computational experiments
    suitable for running under ``epyc``. Sub-classes provide synchronous and stochastic
    (Gillespie) simulation dynamics.

    The dynamics runs a network process provided as a :class:`Process`
    object. It optionally takes a prototype network over which the process runs, which
    is copied for every run. If not provided at construction, the prototype should be
    proivided by calling :meth:`setPrototypeNetwork` beefore trying to run a simulation.

    :param p: network process to run
    :param g: prototype network (optional)'''

    # Additional metadata elements
    TIME = 'simulation_time'      #: Metadata element holding the logical simulation end-time.
    EVENTS = 'simulation_events'  #: Metadata element holding the number of events that happened.

    def __init__( self, p, g = None ):
        super(Dynamics, self).__init__()
        self._graphPrototype = g                 # prototype copied for each run
        self._graph = None                       # working copy of prototype
        self._process = p                        # network process to run


    # ---------- Configuration ----------

    def network( self ):
        '''Return the network this dynamics is running over. This will return None
        unless we're actually running a simulation.

        :returns: the network'''
        return self._graph

    def setNetworkPrototype( self, g ):
        '''Set the network the dynamics will run over. This will be
        copied for each run of an individual experiment.

        :param g: the network'''
        self._graphPrototype = g

    def networkPrototype( self ):
        '''Return the prototype network used to create the working
        copy.

        :returns: the prototype network'''
        return self._graphPrototype
    
    def process(self):
        '''Return the network process being run.

        :returns: the process'''
        return self._process


    # ---------- Results ----------

    def experimentalResults(self):
        '''Report the process' experimental results. This simply calls through to
        the :meth:`Process.results` method of the process being simulated.

        :returns: the results of the process'''
        return self._process.results()


    # ---------- Set-up and tear-down ----------

    def setUp(self, params):
        '''Set up the experiment for a run. This performs the inherited actions, then
        copies the prototype network and builds the network process that the dynamics is to run.

        :params params: the experimental parameters'''
        super(Dynamics, self).setUp(params)

        # make a copy of the network prototype
        self._graph = self.networkPrototype().copy()

        # build the process
        self._process.reset()
        self._process.setNetwork(self.network())
        self._process.build(params)
        self._process.setUp(params)

    def tearDown(self):
        '''At the end of each experiment, throw away the copy and any posted by un-executed events.'''
        self._process.tearDown()
        super(Dynamics, self).tearDown()
        
        # throw away the worked-on model and any posted events that weren't run
        self._graph = None
        self._posted = []


    # ---------- Pending event handling ----------

    def runPendingEvents(self, t):
        '''Retrieve and fire any pending events at time t. This method handles
        the case where firing an event posts another event that needs to be run
        before other already-posted events coming before time t: in other words,
        it ensures that the simulation order is respected.

        :param t: the current time
        :returns: the number of events fired'''
        n = 0
        while True:
            pef = self._process.nextPendingEventBefore(t)
            if pef is None:
                # no more pending events, return however many we've fired already
                return n
            else:
                # fire the event
                pef()
                n += 1

