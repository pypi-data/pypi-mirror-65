import os
import psycopg2

from functools import partial
from multiprocessing.pool import ThreadPool

from .utils import run


def get_nodes_pg_dump_statements(coordinator):
    configuration = coordinator.configuration

    commands = []

    for node in coordinator.nodes:
        if (configuration.dump_nodes_data
            and node.name not in configuration.dump_nodes_data):
            continue
        commands.append(node.dump_statement)

    return commands


def get_rename_node_shards_statements(node, configuration, old=True):
    statements = []
    statement_first = []
    for shard in node.shards:
        if not shard.old_shard:
            continue

        if (shard.old_shard
            and configuration.restore_nodes_data
            and shard.old_shard.node.name not in configuration.restore_nodes_data):
            continue

        if old:
            statements.append('ALTER TABLE %s_%d RENAME TO %s_%d_old;\n' % (
                shard.table.name, shard.id,
                shard.table.name, shard.id))
        else:
            statement_first.append('ALTER TABLE %s_%d RENAME TO %s_%d_new;\n' % (
                shard.old_shard.table.name,
                shard.old_shard.id,
                shard.old_shard.table.name,
                shard.old_shard.id))
            statements.append('ALTER TABLE %s_%d_new RENAME TO %s_%d;\n' % (
                shard.old_shard.table.name,
                shard.old_shard.id,
                shard.table.name,
                shard.id))
            statements.append('DROP TABLE %s_%d_old CASCADE;\n' % (shard.table.name, shard.id))

    return statement_first + statements


def get_reinit_node_shards_statements(node, configuration):
    statements_rename = []
    statements_drop = []

    for shard in node.shards:
        if not shard.old_shard:
            continue

        statements_rename.append('ALTER TABLE %s_%d_old RENAME TO %s_%d;\n' % (
            shard.table.name, shard.id,
            shard.table.name, shard.id))

        statements_drop.append('DROP TABLE %s_%d CASCADE;\n' % (
            shard.old_shard.table.name,
            shard.old_shard.id
        ))

    return statements_drop + statements_rename


def dump_rename_node_shards_to_old_file(coordinator, configuration):
    for node in coordinator.nodes:
        f = open(os.path.join(configuration.dump_folder, '%s_rename_shard_old.sql' % node.name), "w+")
        statements = get_rename_node_shards_statements(node, configuration)
        for statement in statements:
            f.write(statement)


def rename_node_shards(coordinator, configuration, old=True):
    command = 'psql "%s" -f %s -q'

    statements = []
    for node in coordinator.nodes:
        if old:
            file_path = os.path.join(configuration.dump_folder, '%s_rename_shard_old.sql' % node.name)
        else:
            file_path = os.path.join(configuration.dump_folder, '%s_rename_shard_new.sql' % node.name)

        statements.append(command % (node.connection_string, file_path))

    pool = ThreadPool(configuration.parallel_tasks)
    for cmd, rc in pool.imap_unordered(run, statements):
        print('{cmd} return code: {rc}'.format(**vars()))

    pool.close()
    pool.join()


def dump_rename_node_shards_to_new_file(coordinator,  configuration):
    for node in coordinator.nodes:
        f = open(os.path.join(configuration.dump_folder, '%s_rename_shard_new.sql' % node.name), "w+")
        statements = get_rename_node_shards_statements(node, configuration, old=False)
        for statement in statements:
            f.write(statement)


def get_nodes_pg_restore_statements(coordinator):

    command = "%(pg_restore)s --no-acl --no-owner -j %(jobs)d -d '%(host)s' %(path)s --disable-triggers --section=pre-data --section=data"

    commands = []

    for node in coordinator.nodes:
        if (coordinator.configuration.restore_nodes_data
            and node.name not in coordinator.configuration.restore_nodes_data):
            continue

        future_shards = {}

        for shard in node.shards:
            if not shard.future_shard:
                continue

            if shard.future_shard.node not in future_shards:
                future_shards[shard.future_shard.node] = ' -t %s_%d' % (shard.table.name, shard.id)
            else:
                future_shards[shard.future_shard.node] += ' -t %s_%d' % (shard.table.name, shard.id)

        for new_node, shards in future_shards.items():
            commands.append(command % {
                'pg_restore': coordinator.configuration.pg_restore,
                'host': new_node.connection_string,
                'path': node.dump_file,
                'jobs': coordinator.configuration.dump_jobs
            } + shards)

    return commands
