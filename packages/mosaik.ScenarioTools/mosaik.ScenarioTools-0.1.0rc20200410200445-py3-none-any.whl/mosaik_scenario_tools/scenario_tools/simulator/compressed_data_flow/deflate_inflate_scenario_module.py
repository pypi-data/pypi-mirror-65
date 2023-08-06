from mosaik import World
from mosaik_simconfig.simconfig.sim_config import SimConfig

from mosaik_scenario_tools.scenario_tools.connect.connect_one_to_one_module \
    import connect_one_to_one
from mosaik_scenario_tools.scenario_tools.simulator.compressed_data_flow. \
    create_deflate_source_model_module import create_deflate_source_model
from mosaik_scenario_tools.scenario_tools.simulator.compressed_data_flow. \
    create_inflate_sink_model_module import create_inflate_sink_model
from mosaik_scenario_tools.scenario_tools.simulator.compressed_data_flow. \
    deflate_simulator import DeflateSimulator
from mosaik_scenario_tools.scenario_tools.simulator.compressed_data_flow. \
    inflate_simulator import InflateSimulator


def deflate_inflate_scenario():
    sim_config = SimConfig()
    sim_config.add_in_process(simulator=DeflateSimulator)
    sim_config.add_in_process(simulator=InflateSimulator)
    world = World(sim_config=sim_config)

    source_model = create_deflate_source_model(world=world)
    sink_model = create_inflate_sink_model(world=world)

    connect_one_to_one(
        world=world,
        source=source_model,
        sink=sink_model,
        attribute_pairs='float',
    )
    connect_one_to_one(
        world=world,
        source=source_model,
        sink=sink_model,
        attribute_pairs='bool',
    )
    connect_one_to_one(
        world=world,
        source=source_model,
        sink=sink_model,
        attribute_pairs='int',
    )
    connect_one_to_one(
        world=world,
        source=source_model,
        sink=sink_model,
        attribute_pairs='str',
    )
    connect_one_to_one(
        world=world,
        source=source_model,
        sink=sink_model,
        attribute_pairs='None',
    )
    connect_one_to_one(
        world=world,
        source=source_model,
        sink=sink_model,
        attribute_pairs='dict',
    )

    end = 1
    world.run(until=end)
