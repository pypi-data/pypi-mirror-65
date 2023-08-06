from mosaik_scenario_tools.scenario_tools.source.source_model import \
    SourceModel

SOURCE_SIMULATOR_META = {
    'models': {
        SourceModel.__name__: {
            'public': True,
            'params': [],
            'attrs': [
                'my_attribute',  # output
            ],
        },
    },
}
