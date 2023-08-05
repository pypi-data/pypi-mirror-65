import os
from pydoc import locate

from cloudmesh.common.Tabulate import Printer
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters


class ProviderCommand(PluginCommand):

    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/KeyCommand.py
    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/AkeyCommand.py

    # noinspection PyUnusedLocal
    @command
    def do_provider(self, args, arguments):
        """
        ::

           Usage:
             provider list [--output=OUTPUT]

           Arguments:
             NAME           The name of the key.

           Options:
              --output=OUTPUT               the format of the output [default: table]


           Description:

                THIS IS NOT YET IMPLEMENTED

                Managing the providers
        """

        map_parameters(arguments, 'output')

        if arguments.list:

            _paths = []

            def find(names,
                     template="cloudmesh.compute.{name}",
                     kind=None,
                     on_error="not loaded"):
                _paths = []
                for _name in names:
                    _active = False
                    try:
                        _where = os.path.dirname(
                            locate(template.format(name=_name)).__file__)
                        _active = True
                    except Exception as e:
                        _where = on_error.format(name=_name)
                    _paths.append({
                        "path": _where,
                        "name": _name,
                        "active": _active,
                        "kind": kind
                    })
                return _paths

            # cloud_dir = os.path.dirname(locate("cloudmesh.compute").__file__)

            #
            # compute
            #
            candidates_compute_name = ["docker",
                                       "libcloud",
                                       "virtualbox",
                                       "vm"]

            candidates_name_compute = ["openstack",
                                       "azure",
                                       "google",
                                       "aws"
                                       "multipass"]

            _paths = find(candidates_compute_name,
                          template="cloudmesh.compute.{name}",
                          kind="compute",
                          on_error="load with pip install cloudmesh-cloud") + \
                     find(candidates_name_compute,
                          template="cloudmesh.{_name}.compute",
                          kind="compute",
                          on_error="load with pip install cloudmesh-{name}")

            #
            # storage
            #
            candidates_storage_name = [
                "awss3",
                "azureblob",
                "box",
                "gdrive",
                "local",
                "parallelawss3",
                "parallelgdrive",
                "parallelazureblob"]

            candidates_name_storage = [
                "google",
                "oracle"]

            _paths += find(candidates_storage_name,
                           template="cloudmesh.storage.provider.{name}",
                           kind="storage",
                           on_error="load with pip install cloudmesh-storage") + \
                      find(candidates_name_storage,
                           template="cloudmesh.{_name}.storage",
                           kind="storage",
                           on_error="load with pip install cloudmesh-{name}")

            candidates_volume = [
                "aws",
                "azure"
                "google",
                "multipass",
                "opensatck"
                "oracle"]

            _paths += find(candidates_volume,
                           template="cloudmesh.volume.provider.{name}",
                           kind="volume",
                           on_error="load with pip install cloudmesh-volume")

            print(
                Printer.write(_paths, order=["kind", "name", "active", "path"]))

        return ""
