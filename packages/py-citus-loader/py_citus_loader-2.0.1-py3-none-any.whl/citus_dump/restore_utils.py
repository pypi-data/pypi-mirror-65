import os
from multiprocessing.pool import ThreadPool

from subprocess import STDOUT, call

from .formation_utils import *
from .coordinator_utils import (restore_coordinator,
                                restore_coordinator_sequences)
from .node_utils import *
from .configuration import *


def run(cmd):
    print('run statement %s' % cmd)
    return cmd, os.system(cmd)


def perform_restore(coordinator):
    configuration = coordinator.configuration

    print('Connecting to destination host')
    destination_conn = configuration.destination_connection()
    print('Connected to destination host')

    if configuration.restore_schema:
        restore_coordinator('postgres://%s:%s@%s:%s/%s?sslmode=require' % (
            configuration.destination_user, configuration.destination_pwd,
            configuration.destination_host, configuration.destination_port,
            configuration.destination_db), configuration)

    data = retrieve_formation_data(connection=destination_conn)
    new_coordinator = init_formation(configuration, data,
                                     destination=True)

    set_future_shards(new_coordinator, coordinator)

    statements = get_nodes_pg_restore_statements(coordinator)

    # Rename shards before restore
    dump_rename_node_shards_to_old_file(new_coordinator, configuration)
    dump_rename_node_shards_to_new_file(new_coordinator, configuration)

    if configuration.restore_data:
        rename_node_shards(new_coordinator, configuration)

        if not coordinator.dump_files_exist():
            raise Exception('Data dump files don\'t exist')

        if configuration.restore_coordinator_data:
            os.system(new_coordinator.pg_restore_statement)

        pool = ThreadPool(configuration.parallel_tasks)
        for cmd, rc in pool.imap_unordered(run, statements):
            print('{cmd} return code: {rc}'.format(**vars()))

        pool.close()
        pool.join()

        # Rename shards after restore
        rename_node_shards(new_coordinator, configuration, old=False)

    # restore sequences to new coordinator
    restore_coordinator_sequences(new_coordinator)



def perform_reinit_restore(coordinator):
    configuration = coordinator.configuration

    print('Connecting to destination host')
    destination_conn = configuration.destination_connection()
    print('Connected to destination host')

    data = retrieve_formation_data(connection=destination_conn)
    new_coordinator = init_formation(configuration, data,
                                     destination=True)

    set_future_shards(new_coordinator, coordinator)

    for node in new_coordinator.nodes:
        statements = get_reinit_node_shards_statements(node, configuration)

        connection = psycopg2.connect(node.connection_string)

        for statement in statements:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(statement)
                    connection.commit()
                    print(statement)
                except:
                    connection.rollback()

    for table in new_coordinator.distributed_tables + new_coordinator.reference_tables:
        statement = 'DROP TABLE %s CASCADE;' % table.name
        with destination_conn.cursor() as cursor:
            cursor.execute(statement)
            destination_conn.commit()

    drop_statements = []
    # Drop other tables owned by citus user, this is pretty specific to citus cloud / hyperscale
    with destination_conn.cursor() as cursor:
        cursor.execute('''
        SELECT
        schemaname || '.' || tablename
        FROM
        pg_catalog.pg_tables
        WHERE
        schemaname != 'pg_catalog'
        AND schemaname != 'information_schema' AND tableowner = 'citus';
        ''')

        for table_name in cursor.fetchall():
            drop_statements.append('DROP TABLE %s CASCADE;' % table_name[0])

    for statement in drop_statements:
        with destination_conn.cursor() as cursor:
            try:
                cursor.execute(statement)
                destination_conn.commit()
                print(statement)
            except:
                destination_conn.rollback()

    print('Finished re-initialising the destination cluster')
