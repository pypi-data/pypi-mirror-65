#!/usr/bin/env python3

import logging
import os
from typing import Any, Dict, List

import fblearner.flow.api as flow
import torchelastic.rendezvous  # noqa F401
import torchelastic.rendezvous.parameters as parameters
from fblearner.flow.core.future import fut
from fblearner.flow.core.operatorregistry import LexicalContext
from torchelastic import metrics
from torchelastic.agent.server.api import WorkerGroupFailureException, WorkerSpec
from torchelastic.agent.server.local_elastic_agent import LocalElasticAgent


logger = logging.getLogger(__name__)


class MissingElasticDecoratorException(Exception):
    """
    Exception that is raised the ElasticLaunch is invoked on the function
    that is not annotated with the elastic decorator.
    """

    pass


class LaunchConfig:
    __slots__ = [
        "min_nodes",
        "max_nodes",
        "nproc_per_node",
        "rdzv_backend",
        "rdzv_endpoint",
        "run_id",
        "role",
        "rdzv_timeout",
        "max_restarts",
        "monitor_interval",
        "function_start_method",
        "gang_schedule",
        "flow_context",
        "flow_context_params",
    ]

    def __init__(
        self,
        min_nodes: int,
        max_nodes: int,
        nproc_per_node: int,
        rdzv_endpoint: str = "",
        rdzv_backend: str = "zeus-adapter",
        # pyre-fixme[9]: run_id has type `str`; used as `None`.
        run_id: str = None,
        role: str = "default_role",
        rdzv_timeout=300,
        max_restarts=10,
        monitor_interval=60,
        function_start_method="spawn",
        gang_schedule=True,
        flow_context=None,
        flow_context_params=None,
    ):
        """
        min_nodes (int): Minimum amount of nodes that the user function will
                         be launched on. Elastic agent ensures that the user
                         function start only when the min_nodes amount enters
                         the rendezvous.
        max_nodes (int): Maximum amount of nodes that the user function
                         will be launched on.
        nproc_per_node (int): On each node the elastic agent will launch
                              this amount of workers that will execute user
                              defined function.
        rdzv_backend: rdzv_backend to use in the rendezvous (zeus-adapter, etcd).
        rdzv_endpoint: The endpoint of the rdzv sync. storage.
        rdzv_id: The unique run id of the job (defaults to flow workflow run id).
        role: User defined role of the worker (defaults to "trainer")
        max_restarts: The maximum amount of restarts that elastic agent will conduct
                      on workers before failure.
        monitor_interval: The interval in seconds that is used by the elastic_agent
                          as a period of monitoring workers.
        function_start_method: The method is used by the elastic agent
                               to start the workers (spawn, fork, forkserver).
        gang_schedule: If True, schedules the nodes as a gang, if False, uses
                       pseudo-gangs. Gangs have an all-or-nothing semantic,
                       all nodes should be available to start running the job,
                       if one node fails all nodes are torn down and the job
                       restarts with the restart policy defined in the workflow.
                       Pseudo-gangs behave similar to parallel operators,
                       the job starts running as soon as one node is available
                       (but waits on rendezvous for min_nodes). If a node fails,
                       only that node is restarted. Note that pseudo-gangs can
                       cause deadlocks in the entitlement if jobs are not using
                       elasticity (all jobs will hold nodes and wait for min_nodes
                       and eventually fail on rendezvous timeout).
        flow_context: Implementation of fblearner.flow.core.operatorregistry.
        flow_context_params: Parameters that will be used to instantiate
                             fblearner.flow.core.operatorregistry.
                             Note: flow_context and flow_context_params are
                             mutually exclusive parameters.

        """
        self.min_nodes = min_nodes
        self.max_nodes = max_nodes
        self.nproc_per_node = nproc_per_node
        self.rdzv_backend = rdzv_backend
        self.rdzv_endpoint = rdzv_endpoint
        if run_id is None:
            workflow_id = flow.get_flow_environ().workflow_run_id
            # to support parallel elastic gangs we need to use
            # gang_id (CHRONOS_JOB_ID) because workflow_id will be
            # the same for everything that runs under the workflow
            # CHRONOS_JOB_ID is the same for all nodes in the gang
            # CHRONOS_JOB_RUN_ID is different for each node
            gang_id = os.environ.get("CHRONOS_JOB_ID", "")
            self.run_id = f"{workflow_id}_{gang_id}"

        else:
            self.run_id = run_id
        self.role = role
        self.rdzv_timeout = rdzv_timeout
        self.max_restarts = max_restarts
        self.monitor_interval = monitor_interval
        self.function_start_method = function_start_method
        self.gang_schedule = gang_schedule
        self.flow_context = flow_context
        self.flow_context_params = flow_context_params

        assert 0 < self.min_nodes <= self.max_nodes
        assert self.nproc_per_node > 0

        if flow_context is not None and flow_context_params is not None:
            raise ValueError(
                "Set up flow_context OR flow_context_params. "
                "You cannot set up both, since flow_context "
                "will be set up from flow_context_params."
            )


def _merge_worker_return_values(*return_values):
    """
    workaround to deal with the fact that the return value of each
    agent operator is a Future. Takes return values (Future)
    (one for each agent) and returns a merged map of all return values
    for each worker. Note that the return value for the agent operator
    is a map of the local workers (mapped by global rank -> worker ret_val)
    See: https://fburl.com/qa/k1zrx6if
    """
    merged_ret_vals: Dict[int, Any] = {}
    for rv in return_values:
        merged_ret_vals.update(rv)
    return merged_ret_vals


class elastic_launch:
    """
    Launches an "elastic" gang where the gang size may vary between
    min and max. Each gang node runs as an ``elastic_operator``.
    The ``elastic_operator`` runs one or more local workers (user defined ``fn``).

    On each ``elastic_operator``, an ``ElasticAgent`` is created to manage
    the local workers. When workers fail, the agent restarts ALL local workers
    up to ``max_restarts`` as configured in ``LaunchConfig``. When all
    restarts have been exhausted or the agent itself fails then the node
    (flow operator) fails and respects the retry policy that is configured
    on the operator and workflow.

    NOTE:
        1. Pass the ``fn`` arguments as non ``kwargs`` (e.g. no named parameters)
        2. ``fn`` must NOT have any decorators
        3. Pass additional flow operator arguments as ``kwargs``
        4. ``elastic_operator`` has the operator param ``use_forkserver=True``
        5. The return value is a Future resolving to a map of each worker's
           output mapped by their respective global rank.

    Usage

    ::

    def worker_fn(foo):
        torch.distributed.init_process_group(backend="gloo")
        # ...

    @flow.registered()
    @flow.typed()
    def main():
        outputs = elastic_launch(LaunchConfig, worker_fn)(
            foo,
            resource_requirements=ResourceRequirements,
            parse_macros=True)

        # return rank 0's output
        return outputs[0]


    Invalid Usage

    ::

    @flow.flow_async() # INVALID; worker_fn should not be decorated
    def worker_fn(foo):
        pass

    @flow.registered()
    @flow.typed()
    def main():
        outputs = elastic_launch(LauncConfig, worker_fn)(
            foo = foo, # INVALID; must NOT pass worker_fn args as kwargs
        )

        outputs[0].bar # INVALID; cannot access Future's attributes
    """

    def __init__(self, config: LaunchConfig, fn):
        self._config = config
        self._fn = fn

    def __call__(self, *args, **kwargs):
        # holds return values of each gang node
        return_values = []
        with self._lexical_context():
            for i in range(self._config.max_nodes):
                logging.info(f"Launching gang node {i}")
                ret = elastic_operator(self._config, self._fn, list(args), **kwargs)
                return_values.append(ret)
        return fut(_merge_worker_return_values)(*return_values)

    def _lexical_context(self):
        if self._config.flow_context is not None:
            return self._config.flow_context
        fn_name = self._fn.__qualname__
        gang_schedule = self._config.gang_schedule
        gang_name = (
            f"elastic_gang:{fn_name}"
            if gang_schedule
            else f"elastic_pseudo_gang:{fn_name}"
        )
        lc = LexicalContext(gang_name, gang_schedule=gang_schedule)
        if self._config.flow_context_params is not None:
            for param_name, param_value in self._config.flow_context_params.items():
                if hasattr(lc, param_name):
                    setattr(lc, param_name, param_value)
        return lc


@flow.flow_async(saves_partial_results=True)
@flow.typed()
def elastic_operator(config: LaunchConfig, fn, fn_args: List[Any]) -> Dict[int, Any]:
    logger.info(
        f"Starting elastic_operator with launch configs:\n"
        f"\tuser fn: {fn.__name__}\n"
        f"\tmin_nodes: {config.min_nodes}\n"
        f"\tmax_nodes: {config.max_nodes}\n"
        f"\tnproc_per_node: {config.nproc_per_node}\n"
        f"\trun_id: {config.run_id}\n"
        f"\trdzv_backend: {config.rdzv_backend}\n"
        f"\trdzv_endpoint: {config.rdzv_endpoint}\n"
        f"\tmax_restarts: {config.max_restarts}\n"
        f"\tmonitor_interval: {config.monitor_interval}"
    )

    rdzv_parameters = parameters.RendezvousParameters(
        config.rdzv_backend,
        config.rdzv_endpoint,
        config.run_id,
        config.min_nodes,
        config.max_nodes,
        config=(
            f"timeout={config.rdzv_timeout}"
            f",min_nodes_timeout={config.rdzv_timeout}"
            ",waitfor_previous_rendezvous=False"
        ),
    )
    rdzv_handler = parameters.get_rendezvous(rdzv_parameters)

    spec = WorkerSpec(
        role=config.role,
        local_world_size=config.nproc_per_node,
        fn=fn,
        args=tuple(fn_args),
        rdzv_handler=rdzv_handler,
        max_restarts=config.max_restarts,
        monitor_interval=config.monitor_interval,
    )

    metrics.initialize_metrics()
    agent = LocalElasticAgent(spec, config.function_start_method)

    try:
        return agent.run()
    except WorkerGroupFailureException as e:
        # user-code error; propagate the one from the smallest
        # rank on this node
        excs = e.get_worker_exceptions()
        min_rank = min(excs.keys())
        raise excs[min_rank]
    except Exception as e:
        # this is an agent (platform) error
        # TODO clearly distingush and categorize user vs platform errors
        raise e
