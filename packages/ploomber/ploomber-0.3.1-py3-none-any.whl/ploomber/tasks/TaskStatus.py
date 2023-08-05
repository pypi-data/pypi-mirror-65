from enum import Enum


class DAGStatus(Enum):
    WaitingRender = 'waiting_render'
    WaitingExecution = 'waiting_execution'
    Executed = 'executed'
    Errored = 'errored'


class TaskStatus(Enum):
    WaitingRender = 'waiting_render'
    WaitingExecution = 'waiting_execution'
    WaitingUpstream = 'waiting_upstream'
    Executed = 'executed'
    Errored = 'errored'
    BrokenProcessPool = 'broken_process_pool'
