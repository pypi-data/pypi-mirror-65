=================
Simulation module
=================

Module to interact easily with the NEST simulator. It allows to:

* build a NEST network from :class:`~nngt.Network` or
  :class:`~nngt.SpatialNetwork` objects,
* monitor the activity of the network (taking neural groups into account)
* plot the activity while separating the behaviours of predefined neural groups


Content
=======

.. autosummary::

    nngt.simulation.ActivityRecord
    nngt.simulation.activity_types
    nngt.simulation.analyze_raster
    nngt.simulation.get_nest_adjacency
    nngt.simulation.get_recording
    nngt.simulation.make_nest_network
    nngt.simulation.monitor_groups
    nngt.simulation.monitor_nodes
    nngt.simulation.plot_activity
    nngt.simulation.randomize_neural_states
    nngt.simulation.raster_plot
    nngt.simulation.reproducible_weights
    nngt.simulation.save_spikes
    nngt.simulation.set_minis
    nngt.simulation.set_noise
    nngt.simulation.set_poisson_input
    nngt.simulation.set_step_currents

Details
=======

.. automodule:: nngt.simulation
