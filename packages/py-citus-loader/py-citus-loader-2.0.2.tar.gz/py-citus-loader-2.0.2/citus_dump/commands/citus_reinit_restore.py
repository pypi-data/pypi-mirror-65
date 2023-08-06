import click


from ..configuration import *
from ..restore_utils import perform_reinit_restore
from ..formation_utils import retrieve_formation_data, init_formation


@click.command()
@click.option('--config-file', required=True, type=click.Path(),
              help='JSON file containing the configuration for the command')
def citus_reinit_restore(config_file):


    config_args = {
        'config_file': config_file,
        'restore_only': True
    }

    configuration = Configuration(**config_args)

    path_metadata_file = os.path.join(configuration.dump_folder,
                                      'source_coordinator_metadata.yml')

    print('Retrieving data for old formation')
    data = retrieve_formation_data(from_file=path_metadata_file)
    coordinator = init_formation(configuration, data)

    perform_reinit_restore(coordinator)
