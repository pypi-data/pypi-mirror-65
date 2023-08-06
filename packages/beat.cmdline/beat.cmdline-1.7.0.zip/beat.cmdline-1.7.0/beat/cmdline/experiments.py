#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


import os
import logging
import glob
import click
import simplejson
import six
import curses
import textwrap
import threading
import queue
import signal

from datetime import timedelta

from beat.core.experiment import Experiment
from beat.core.execution import DockerExecutor
from beat.core.execution import LocalExecutor
from beat.core.execution import SubprocessExecutor
from beat.core.utils import NumpyJSONEncoder
from beat.core.data import CachedDataSource, load_data_index
from beat.core.dock import Host
from beat.core.hash import toPath
from beat.core.hash import hashDataset

from . import common
from . import commands

from .webapi import WebAPIError

from .plotters import plot_impl as plotters_plot
from .plotters import pull_impl as plotters_pull

from .decorators import raise_on_error

from .click_helper import AliasedGroup
from .click_helper import MutuallyExclusiveOption
from .click_helper import AssetCommand
from .click_helper import AssetInfo


logger = logging.getLogger(__name__)


def run_experiment(
    configuration, name, force, use_docker, use_local, run_environment_path, quiet
):
    """Run experiments locally"""

    def load_result(executor):
        """Loads the result of an experiment, in a single go"""

        f = CachedDataSource()
        success = f.setup(
            os.path.join(executor.cache, executor.data["result"]["path"] + ".data"),
            executor.prefix,
        )

        if not success:
            raise RuntimeError("Failed to setup cached data source")

        data, start, end = f[0]
        return data

    def print_results(executor):
        data = load_result(executor)
        r = reindent(
            simplejson.dumps(data.as_dict(), indent=2, cls=NumpyJSONEncoder), 2
        )
        logger.info("  Results:\n%s", r)

    def reindent(s, n):
        """Re-indents output so it is more visible"""
        margin = n * " "
        return margin + ("\n" + margin).join(s.split("\n"))

    def simplify_time(s):
        """Re-writes the time so it is easier to understand it"""

        minute = 60.0
        hour = 60 * minute
        day = 24 * hour

        if s <= minute:
            return "%.2f s" % s
        elif s <= hour:
            minutes = s // minute
            seconds = s - (minute * minutes)
            return "%d m %.2f s" % (minutes, seconds)
        elif s <= day:
            hours = s // hour
            minutes = (s - (hour * hours)) // minute
            seconds = s - (hour * hours + minute * minutes)
            return "%d h %d m %.2f s" % (hours, minutes, seconds)
        else:
            days = s // day
            hours = (s - (day * days)) // hour
            minutes = (s - (day * days + hour * hours)) // minute
            seconds = s - (day * days + hour * hours + minute * minutes)
            return "%d days %d h %d m %.2f s" % (days, hours, minutes, seconds)

    def simplify_size(s):
        """Re-writes the size so it is easier to understand it"""

        kb = 1024.0
        mb = kb * kb
        gb = kb * mb
        tb = kb * gb

        if s <= kb:
            return "%d bytes" % s
        elif s <= mb:
            return "%.2f kilobytes" % (s / kb)
        elif s <= gb:
            return "%.2f megabytes" % (s / mb)
        elif s <= tb:
            return "%.2f gigabytes" % (s / gb)
        return "%.2f terabytes" % (s / tb)

    def index_experiment_databases(cache_path, experiment):
        for block_name, infos in experiment.datasets.items():
            filename = toPath(
                hashDataset(infos["database"].name, infos["protocol"], infos["set"]),
                suffix=".db",
            )
            database_index_path = os.path.join(cache_path, filename)
            if not os.path.exists(database_index_path):
                logger.info(
                    "Index for database %s not found, building it",
                    infos["database"].name,
                )
                view = infos["database"].view(infos["protocol"], infos["set"])
                view.index(database_index_path)

    dataformat_cache = {}
    database_cache = {}
    algorithm_cache = {}
    library_cache = {}

    experiment = Experiment(
        configuration.path,
        name,
        dataformat_cache,
        database_cache,
        algorithm_cache,
        library_cache,
    )

    if not experiment.valid:
        logger.error("Failed to load the experiment `%s':", name)
        for e in experiment.errors:
            logger.error("  * %s", e)
        return 1

    if not os.path.exists(configuration.cache):
        os.makedirs(configuration.cache)
        logger.info("Created cache path `%s'", configuration.cache)

    index_experiment_databases(configuration.cache, experiment)

    scheduled = experiment.setup()

    if use_docker:
        # load existing environments
        host = Host(raise_on_errors=False)

    # can we execute it?
    for key, value in scheduled.items():

        # checks and sets-up executable
        executable = None  # use the default

        if use_docker:
            env = value["configuration"]["environment"]
            search_key = "%s (%s)" % (env["name"], env["version"])
            if search_key not in host:
                logger.error(
                    "Cannot execute block `%s' on environment `%s': "
                    "environment was not found' - please install it",
                    key,
                    search_key,
                )
                return 1

        if run_environment_path is not None:
            executor = SubprocessExecutor(
                prefix=configuration.path,
                data=value["configuration"],
                cache=configuration.cache,
                dataformat_cache=dataformat_cache,
                database_cache=database_cache,
                algorithm_cache=algorithm_cache,
                library_cache=library_cache,
                custom_root_folders=configuration.database_paths,
                python_path=run_environment_path,
            )
        elif use_docker:
            executor = DockerExecutor(
                host=host,
                prefix=configuration.path,
                data=value["configuration"],
                cache=configuration.cache,
                dataformat_cache=dataformat_cache,
                database_cache=database_cache,
                algorithm_cache=algorithm_cache,
                library_cache=library_cache,
            )
        elif use_local:
            executor = LocalExecutor(
                prefix=configuration.path,
                data=value["configuration"],
                cache=configuration.cache,
                dataformat_cache=dataformat_cache,
                database_cache=database_cache,
                algorithm_cache=algorithm_cache,
                library_cache=library_cache,
                custom_root_folders=configuration.database_paths,
            )
        else:
            raise RuntimeError("Invalid parameters")

        if not executor.valid:
            logger.error("Failed to load the execution information for `%s':", key)
            for e in executor.errors:
                logger.error("  * %s", e)
            return 1

        if executor.outputs_exist and not force:
            logger.info(
                "Skipping execution of `%s' for block `%s' " "- outputs exist",
                executor.algorithm.name,
                key,
            )
            if executor.analysis and not quiet:
                logger.extra("  Outputs produced:")
                print_results(executor)
            continue

        logger.info("Running `%s' for block `%s'", executor.algorithm.name, key)
        if executable is not None:
            logger.extra("  -> using executable at `%s'", executable)
        else:
            logger.extra("  -> using fallback (default) environment")

        with executor:
            result = executor.process()

        if result["status"] != 0:
            logger.error("Block did not execute properly - outputs were reset")
            logger.error("  Standard output:\n%s", reindent(result["stdout"], 4))
            logger.error("  Standard error:\n%s", reindent(result["stderr"], 4))
            logger.error(
                "  Captured user error:\n%s", reindent(result["user_error"], 4)
            )
            logger.error(
                "  Captured system error:\n%s", reindent(result["system_error"], 4)
            )
            logger.extra("  Environment: %s" % "default environment")
            return 1
        elif use_docker:
            stats = result["statistics"]
            cpu_stats = stats["cpu"]
            data_stats = stats["data"]

            cpu_total = cpu_stats["total"]
            # Likely means that GPU was used
            if not cpu_total:
                cpu_total = 1.0

            logger.extra(
                "  CPU time (user, system, total, percent): " "%s, %s, %s, %d%%",
                simplify_time(cpu_stats["user"]),
                simplify_time(cpu_stats["system"]),
                simplify_time(cpu_total),
                100.0 * (cpu_stats["user"] + cpu_stats["system"]) / cpu_total,
            )
            logger.extra("  Memory usage: %s", simplify_size(stats["memory"]["rss"]))
            logger.extra(
                "  Cached input read: %s, %s",
                simplify_time(data_stats["time"]["read"]),
                simplify_size(data_stats["volume"]["read"]),
            )
            logger.extra(
                "  Cached output write: %s, %s",
                simplify_time(data_stats["time"]["write"]),
                simplify_size(data_stats["volume"]["write"]),
            )
            logger.extra(
                "  Communication time: %s (%d%%)",
                simplify_time(data_stats["network"]["wait_time"]),
                100.0 * data_stats["network"]["wait_time"] / cpu_total,
            )
        else:
            logger.extra("  Environment: %s" % "local environment")

        if not quiet:
            if executor.analysis:
                print_results(executor)

            logger.extra("  Outputs produced:")
            if executor.analysis:
                logger.extra("    * %s", executor.data["result"]["path"])
            else:
                for name, details in executor.data["outputs"].items():
                    logger.extra("    * %s", details["path"])
        else:
            logger.info("Done")

    return 0


def caches_impl(configuration, name, ls, delete, checksum):
    """List all cache files involved in this experiment"""

    dataformat_cache = {}
    database_cache = {}
    algorithm_cache = {}
    library_cache = {}

    experiment = Experiment(
        configuration.path,
        name,
        dataformat_cache,
        database_cache,
        algorithm_cache,
        library_cache,
    )

    if not experiment.valid:
        logger.error("Failed to load the experiment `%s':", name)
        for e in experiment.errors:
            logger.error("  * %s", e)
        return 1

    scheduled = experiment.setup()

    block_list = []
    for key, value in scheduled.items():
        block = {
            "name": key,
            "algorithm": value["configuration"]["algorithm"],
            "is_analyser": False,
            "paths": [],
        }

        if "outputs" in value["configuration"]:  # normal block
            for name, data in value["configuration"]["outputs"].items():
                block["paths"].append(data["path"])
        else:  # analyzer
            block["is_analyser"] = True
            block["paths"].append(value["configuration"]["result"]["path"])

        block_list.append(block)

    for block in block_list:
        block_type = "analyzer" if block["is_analyser"] else "algorithm"
        logger.info("block: `%s'", block["name"])
        logger.info("  %s: `%s'", block_type, block["algorithm"])

        for path in block["paths"]:
            # prefix cache path
            path = os.path.join(configuration.cache, path)
            logger.info("  output: `%s'", path)

            if ls:
                for file in glob.glob(path + ".*"):
                    logger.info("    %s" % file)

            if delete:
                for file in glob.glob(path + ".*"):
                    logger.info("removing `%s'...", file)
                    os.unlink(file)

                common.recursive_rmdir_if_empty(
                    os.path.dirname(path), configuration.cache
                )

            if checksum:
                if not load_data_index(configuration.cache, path + ".data"):
                    logger.error("Failed to load data index for {}".format(path))
                logger.info("index for `%s' can be loaded and checksums", path)

    return 0


def pull_impl(webapi, prefix, names, force, indentation, format_cache):
    """Copies experiments (and required toolchains/algorithms) from the server.

    Parameters:

      webapi (object): An instance of our WebAPI class, prepared to access the
        BEAT server of interest

      prefix (str): A string representing the root of the path in which the
        user objects are stored

      names (:py:class:`list`): A list of strings, each representing the unique
        relative path of the objects to retrieve or a list of usernames from
        which to retrieve objects. If the list is empty, then we pull all
        available objects of a given type. If no user is set, then pull all
        public objects of a given type.

      force (bool): If set to ``True``, then overwrites local changes with the
        remotely retrieved copies.

      indentation (int): The indentation level, useful if this function is
        called recursively while downloading different object types. This is
        normally set to ``0`` (zero).


    Returns:

      int: Indicating the exit status of the command, to be reported back to
        the calling process. This value should be zero if everything works OK,
        otherwise, different than zero (POSIX compliance).

    """

    from .algorithms import pull_impl as algorithms_pull
    from .databases import pull_impl as databases_pull

    if indentation == 0:
        indentation = 4

    status, names = common.pull(
        webapi,
        prefix,
        "experiment",
        names,
        ["declaration", "description"],
        force,
        indentation,
    )

    if status != 0:
        logger.error("could not find any matching experiments - widen your search")
        return status

    # see what dataformats one needs to pull
    databases = set()
    toolchains = set()
    algorithms = set()
    for name in names:
        try:
            obj = Experiment(prefix, name)
            if obj.toolchain:
                toolchains.add(obj.toolchain.name)
            databases |= obj.databases.keys()
            algorithms |= obj.algorithms.keys()

        except Exception as e:
            logger.error("loading `%s': %s...", name, str(e))

    # downloads any formats to which we depend on
    format_cache = {}
    library_cache = {}
    tc_status, _ = common.pull(
        webapi,
        prefix,
        "toolchain",
        toolchains,
        ["declaration", "description"],
        force,
        indentation,
    )
    db_status = databases_pull(
        webapi, prefix, databases, force, indentation, format_cache
    )
    algo_status = algorithms_pull(
        webapi, prefix, algorithms, force, indentation, format_cache, library_cache
    )

    return status + tc_status + db_status + algo_status


def plot_impl(
    webapi,
    configuration,
    prefix,
    names,
    remote_results,
    show,
    force,
    indentation,
    format_cache,
    outputfolder=None,
):
    """Plots experiments from the server.

    Parameters:

      webapi (object): An instance of our WebAPI class, prepared to access the
        BEAT server of interest

      configuration (object): An instance of the configuration, to access the
        BEAT server and current configuration for information

      prefix (str): A string representing the root of the path in which the
        user objects are stored

      names (:py:class:`list`): A list of strings, each representing the unique relative
        path of the objects to retrieve or a list of usernames from which to
        retrieve objects. If the list is empty, then we pull all available
        objects of a given type. If no user is set, then pull all public
        objects of a given type.

      remote_results(bool): If set to ``True``, then fetch results data
        for the experiments from the server.

      force (bool): If set to ``True``, then overwrites local changes with the
        remotely retrieved copies.

      indentation (int): The indentation level, useful if this function is
        called recursively while downloading different object types. This is
        normally set to ``0`` (zero).

      outputfolder (str): A string representing the path in which the
        experiments plot will be stored

    Returns:

      int: Indicating the exit status of the command, to be reported back to
        the calling process. This value should be zero if everything works OK,
        otherwise, different than zero (POSIX compliance).

    """

    status = 0
    RESULTS_SIMPLE_TYPE_NAMES = ("int32", "float32", "bool", "string")

    if indentation == 0:
        indentation = 4

    if remote_results:
        if outputfolder is None:
            output_folder = configuration.path
        else:
            # check if directory exists else create
            if not os.path.isdir(outputfolder):
                os.mkdir(os.path.join(configuration.path, outputfolder))
            output_folder = os.path.join(configuration.path, outputfolder)

    for name in names:
        if not remote_results:
            if outputfolder is None:
                output_folder = os.path.join(
                    configuration.path,
                    common.TYPE_PLURAL["experiment"],
                    name.rsplit("/", 1)[0],
                )
            else:
                # check if directory exists else create
                if not os.path.isdir(outputfolder):
                    os.mkdir(os.path.join(configuration.path, outputfolder))
                output_folder = os.path.join(configuration.path, outputfolder)

        check_plottable = False
        if not os.path.exists(configuration.cache) or remote_results:
            experiment = simplejson.loads(
                simplejson.dumps(
                    common.fetch_object(webapi, "experiment", name, ["results"])
                )
            )
            results = experiment["results"]["analysis"]
            for key, value in results.iteritems():
                # remove non plottable results
                if value["type"] not in RESULTS_SIMPLE_TYPE_NAMES:
                    output_name = name.rsplit("/", 1)[1] + "_" + key + ".png"
                    output_name = os.path.join(output_folder, output_name)
                    pl_status = plotters_pull(
                        webapi,
                        configuration.path,
                        [value["type"]],
                        force,
                        indentation,
                        {},
                    )
                    plot_status = plotters_plot(
                        webapi,
                        configuration.path,
                        [value["type"]],
                        show,
                        False,
                        False,
                        value["value"],
                        output_name,
                        None,
                        indentation,
                        format_cache,
                    )
                    status += pl_status
                    status += plot_status
                    check_plottable = True
        else:
            # make sure experiment exists locally or pull it
            pull_impl(
                webapi, configuration.path, [name], force, indentation, format_cache
            )

            # get information from cache
            dataformat_cache = {}
            database_cache = {}
            algorithm_cache = {}
            library_cache = {}

            experiment = Experiment(
                configuration.path,
                name,
                dataformat_cache,
                database_cache,
                algorithm_cache,
                library_cache,
            )

            scheduled = experiment.setup()
            for key, value in scheduled.items():
                executor = LocalExecutor(
                    configuration.path,
                    value["configuration"],
                    configuration.cache,
                    dataformat_cache,
                    database_cache,
                    algorithm_cache,
                    library_cache,
                    configuration.database_paths,
                )

                if "result" in executor.data:
                    f = CachedDataSource()
                    success = f.setup(
                        os.path.join(
                            executor.cache, executor.data["result"]["path"] + ".data"
                        ),
                        executor.prefix,
                    )
                    if not success:
                        raise RuntimeError("Failed to setup cached data source")

                    data, start, end = f[0]

                    for the_data in data.as_dict():
                        attr = getattr(data, the_data)
                        if attr.__class__.__name__.startswith("plot"):
                            datatype = attr.__class__.__name__.replace("_", "/")
                            # remove non plottable results
                            if datatype not in RESULTS_SIMPLE_TYPE_NAMES:
                                output_name = (
                                    name.rsplit("/", 1)[1] + "_" + the_data + ".png"
                                )
                                output_name = os.path.join(output_folder, output_name)
                                pl_status = plotters_pull(
                                    webapi,
                                    configuration.path,
                                    [datatype],
                                    force,
                                    indentation,
                                    {},
                                )
                                plot_status = plotters_plot(
                                    webapi,
                                    configuration.path,
                                    [datatype],
                                    show,
                                    False,
                                    False,
                                    data.as_dict()[the_data],
                                    output_name,
                                    None,
                                    indentation,
                                    format_cache,
                                )
                                status += pl_status
                                status += plot_status
                                check_plottable = True
        if not check_plottable:
            print("Experiments results are not plottable")

    return status


def get_dependencies(ctx, asset_name):
    prefix = ctx.meta["config"].path
    exp = Experiment(prefix, asset_name)

    dependencies = {"toolchains": [exp.toolchain.name]}

    algorithms = list(exp.algorithms.keys())
    if algorithms:
        dependencies["algorithms"] = algorithms

    # databases are not considered as dependencies as they can't be uploaded.

    return dependencies


class ExperimentCommand(AssetCommand):
    asset_info = AssetInfo(
        asset_type="experiment",
        diff_fields=["declaration", "description"],
        push_fields=["name", "declaration", "toolchain", "description"],
        get_dependencies=get_dependencies,
    )


@click.group(cls=AliasedGroup)
@click.pass_context
def experiments(ctx):
    """experiments commands"""


CMD_LIST = ["list", "path", "edit", "check", "status", "fork", "rm", "diff", "push"]

commands.initialise_asset_commands(experiments, CMD_LIST, ExperimentCommand)


@experiments.command()
@click.argument("name", nargs=1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.option(
    "--docker",
    help="Uses the docker executor to execute the "
    "experiment using docker containers",
    is_flag=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["local", "environment"],
)
@click.option(
    "--local",
    help="Uses the local executor to execute the "
    "experiment on the local machine (default)",
    default=True,
    is_flag=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["docker", "environment"],
)
@click.option(
    "--environment",
    help="Uses the local executor to execute the "
    "experiment on the local machine using the given environment."
    "Given path should be to the python executable of the the environment",
    type=click.Path(exists=True),
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["docker", "local"],
)
@click.option("--quiet", help="Be less verbose", is_flag=True)
@click.pass_context
@raise_on_error
def run(ctx, name, force, docker, local, environment, quiet):
    """ Runs an experiment locally"""
    config = ctx.meta.get("config")
    return run_experiment(config, name, force, docker, local, environment, quiet)


@experiments.command()
@click.argument("name", nargs=1)
@click.option(
    "--list", help="List cache files matching output if they exist", is_flag=True
)
@click.option(
    "--delete",
    help="Delete cache files matching output if they "
    "exist (also, recursively deletes empty directories)",
    is_flag=True,
)
@click.option("--checksum", help="Checksums indexes for cache files", is_flag=True)
@click.pass_context
@raise_on_error
def caches(ctx, name, list, delete, checksum):
    """Lists all cache files used by this experiment"""
    config = ctx.meta.get("config")
    return caches_impl(config, name, list, delete, checksum)


@experiments.command()
@click.argument("names", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.pass_context
@raise_on_error
def pull(ctx, names, force):
    """Downloads the specified experiments from the server.

       $ beat experiments pull xxx.
    """
    config = ctx.meta.get("config")
    with common.make_webapi(config) as webapi:
        return pull_impl(webapi, config.path, names, force, 0, {})


@experiments.command()
@click.argument("names", nargs=-1)
@click.option(
    "--path",
    help="Use path to write files to disk (instead of the " "current directory)",
    type=click.Path(),
)
@click.pass_context
@raise_on_error
def draw(ctx, names, path):
    """Creates a visual representation of the experiment."""
    config = ctx.meta.get("config")
    return common.dot_diagram(config.path, "experiment", names, path, [])


@experiments.command()
@click.argument("names", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.option(
    "--remote", help="Only acts on the remote copy of the experiment", is_flag=True
)
@click.option("--show", help="Show...", is_flag=True)
@click.option("--output-folder", help="<folder>", type=click.Path(exists=True))
@click.pass_context
@raise_on_error
def plot(ctx, names, force, remote, show, output_folder):
    """Plots output images of the experiment."""
    config = ctx.meta.get("config")
    with common.make_webapi(config) as webapi:
        return plot_impl(
            webapi,
            config,
            "experiment",
            names,
            remote,
            show,
            force,
            0,
            {},
            output_folder,
        )


@experiments.command()
@click.argument("name", nargs=1)
@click.option("--watch", help="Start monitoring the execution", is_flag=True)
@click.pass_context
def start(ctx, name, watch):
    """Start an experiment on the platform"""

    config = ctx.meta.get("config")
    with common.make_webapi(config) as webapi:
        webapi.post("/api/v1/experiments/{}/start/".format(name))

    if watch:
        ctx.invoke(monitor, name=name)


@experiments.command()
@click.argument("name", nargs=1)
@click.pass_context
def cancel(ctx, name):
    """Cancel an experiment on the platform"""

    config = ctx.meta.get("config")
    with common.make_webapi(config) as webapi:
        webapi.post("/api/v1/experiments/{}/cancel/".format(name))


@experiments.command()
@click.argument("name", nargs=1)
@click.pass_context
def reset(ctx, name):
    """Reset an experiment on the platform"""

    config = ctx.meta.get("config")
    with common.make_webapi(config) as webapi:
        webapi.post("/api/v1/experiments/{}/reset/".format(name))


@experiments.command()
@click.argument("name", nargs=1)
@click.pass_context
def runstatus(ctx, name):
    """Shows the status of an experiment on the platform"""

    config = ctx.meta.get("config")

    with common.make_webapi(config) as webapi:
        fields = ",".join(
            [
                "status",
                "blocks_status",
                "done",
                "errors",
                "execution_info",
                "execution_order",
                "results",
                "started",
                "display_start_date",
                "display_end_date",
            ]
        )
        answer = webapi.get("/api/v1/experiments/{}/?fields={}".format(name, fields))

        print(simplejson.dumps(answer, indent=4))


# The monitoring implementation has been inspired from
# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679


class ProgramKilled(Exception):
    """CTRL + C has been used"""

    pass


def signal_handler(signum, frame):
    """Basic signal handler for processing keyboard interruption"""

    raise ProgramKilled


class ExperimentMonitor(threading.Thread):
    """Thread doing the monitoring of an experiment"""

    def __init__(self, interval, config, name):
        super(ExperimentMonitor, self).__init__()

        self.daemon = False
        self.stop_event = threading.Event()
        self.interval = interval
        self.config = config
        self.name = name
        self.stopped = False
        self.queue = queue.Queue()

    def stop(self):
        """Stop the thread cleanly"""

        self.stopped = True
        self.stop_event.set()
        self.join()

    def run(self):
        """Periodically calls the platform instance to get the status of the
        selected experiment.
        """

        fields = ",".join(["status", "blocks_status", "done"])
        self.stopped = False
        with common.make_webapi(self.config) as webapi:
            first_run = True
            while not self.stop_event.wait(
                0 if first_run else self.interval.total_seconds()
            ):

                try:
                    answer = webapi.get(
                        "/api/v1/experiments/{}/?fields={}".format(self.name, fields)
                    )
                except WebAPIError as error:
                    logger.error(
                        "failed to get current state of {} on `{}', reason: {}".format(
                            self.name,
                            webapi.platform,
                            error,
                        )
                    )
                    self.stop_event.set()
                    self.queue.put({"error": error})
                else:
                    self.queue.put(answer)

                if first_run:
                    first_run = False


def replace_line(pad, line, text):
    """Replaces the content of a ncurses pad line"""

    pad.move(line, 0)
    pad.clrtoeol()
    pad.addstr(line, 0, text)


def process_input(monitor, pad, delta, pad_height, height, width):
    """Processes the keyboard input of an ncurses pad"""

    if pad:
        try:
            ch = pad.getch()
        except curses.error:
            pass
        else:
            if ch == curses.KEY_UP:
                delta = max(delta - 1, 0)
            elif ch == curses.KEY_DOWN:
                delta = min(delta + 1, pad_height - height)
            elif ch == ord("q"):
                monitor.stop()
        pad.refresh(delta, 0, 0, 0, height - 1, width - 1)

    return delta


@experiments.command()
@click.argument("name", nargs=1)
@click.pass_context
def monitor(ctx, name):
    """Monitor a running experiment"""

    config = ctx.meta.get("config")

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    monitor = ExperimentMonitor(interval=timedelta(seconds=5), config=config, name=name)
    monitor.start()

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    initialised = False
    killed = False
    pad = None
    line = 0
    delta = 0
    height, width = stdscr.getmaxyx()
    pad_height = height
    STATIC_LINE_COUNT = 3  # Number of known lines that will be shown

    while True:
        try:
            try:
                data = monitor.queue.get(True, 0.2)
            except queue.Empty:
                delta = process_input(monitor, pad, delta, pad_height, height, width)

            else:
                if "error" in data:
                    killed = True
                    break

                height, width = stdscr.getmaxyx()

                if not initialised:
                    nb_blocks = len(data["blocks_status"]) + STATIC_LINE_COUNT
                    pad_height = max(nb_blocks, height)
                    pad = curses.newpad(pad_height, width)
                    pad.timeout(200)
                    pad.keypad(True)

                line = 0
                replace_line(
                    pad,
                    line,
                    textwrap.shorten("Name: {name}".format(name=name), width=width),
                )
                line += 1
                replace_line(
                    pad,
                    line,
                    textwrap.shorten("Status: {status}".format(**data), width=width),
                )

                blocks = data["blocks_status"]
                text_width = int(width / 2)
                for block_name, block_status in blocks.items():
                    line += 1
                    pad.move(line, 0)
                    pad.clrtoeol()
                    pad.addstr(
                        line,
                        0,
                        textwrap.shorten(
                            "Name: {block_name} ".format(block_name=block_name),
                            width=text_width,
                        ),
                    )
                    pad.addstr(
                        line,
                        text_width,
                        textwrap.shorten(
                            "Status: {block_status}".format(block_status=block_status),
                            width=text_width,
                        ),
                    )

                pad.refresh(delta, 0, 0, 0, height - 1, width - 1)

                if data["done"]:
                    monitor.stop()

                if not initialised:
                    initialised = True

            finally:
                delta = process_input(monitor, pad, delta, pad_height, height, width)

            if not monitor.isAlive():
                break

        except ProgramKilled:
            monitor.stop()
            killed = True
            break

    if not killed:
        line += 1
        if pad:
            pad.timeout(-1)
            pad.addstr(
                line,
                0,
                textwrap.shorten("Experiment done, press any key to leave", width=width),
                curses.A_BOLD,
            )
            pad.move(line, 0)
            pad.refresh(pad_height - height, 0, 0, 0, height - 1, width - 1)
            pad.getkey()

    curses.echo()
    curses.nocbreak()
    curses.endwin()
