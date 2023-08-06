# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import logging

from collections import OrderedDict

from atpbar import atpbar

from alphatwirl.misc.deprecation import _deprecated
from alphatwirl.misc.deprecation import _deprecated_class_method_option

from .EventLoop import EventLoop
from .merge import merge_in_order

##__________________________________________________________________||
@_deprecated(msg='replaced with alphatwirl.datasetloop.CollectorComposite')
class CollectorComposite(object):

    """A composite of collectors.

    This class is a composite in the composite pattern.

    Examples of collectors are instances of `Collector`,
    `NullCollector`, and this class.

    """

    @_deprecated_class_method_option('progressReporter')
    def __init__(self, progressReporter=None):

        self.components = [ ]

    def __repr__(self):
        name_value_pairs = (
            ('components',       self.components),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def add(self, collector):
        """add a collector


        Args:
            collector: the collector to be added

        """
        self.components.append(collector)

    def collect(self, dataset_readers_list):
        """collect results


        Returns:
            a list of results

        """

        ret = [ ]
        for i, collector in enumerate(atpbar(self.components, name='collecting results')):
            ret.append(collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
                                          for dataset, readerComposites in dataset_readers_list]))
        return ret

        ## in one line without the progress bar
        #return [collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
        #                           for dataset, readerComposites in dataset_readers_list])
        #        for i, collector in enumerate(self.components)]

##__________________________________________________________________||
@_deprecated(msg='replaced with alphatwirl.datasetloop.EventDatasetReader')
class EventDatasetReader(object):
    """This class manages objects involved in reading events in data sets.

    On receiving a data set, this class calls the function
    split_into_build_events(), which splits the data set into chunks,
    creates the function build_events() for each chunk, and returns a
    list of the functions. Then, for each build_events(), This class
    creates a copy of the reader, creates an event loop, and send it
    to the event loop runner.

    At the end, this class receives results from the event loop runner
    and have the collector collect them.

    """
    def __init__(self, eventLoopRunner, reader, collector,
                 split_into_build_events):

        self.eventLoopRunner = eventLoopRunner
        self.reader = reader
        self.collector = collector
        self.split_into_build_events = split_into_build_events

        self.EventLoop = EventLoop

        self.runids = [ ]
        self.runid_dataset_map = { }
        self.dataset_runid_reader_map = OrderedDict()

        name_value_pairs = (
            ('eventLoopRunner', self.eventLoopRunner),
            ('reader', self.reader),
            ('collector', self.collector),
            ('split_into_build_events', self.split_into_build_events),
        )
        self._repr = '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __repr__(self):
        return self._repr

    def begin(self):
        self.eventLoopRunner.begin()

        self.runids = [ ]
        self.runid_dataset_map = { }
        self.dataset_runid_reader_map = OrderedDict()

    def read(self, dataset):
        build_events_list = self.split_into_build_events(dataset)
        eventLoops = [ ]
        for build_events in build_events_list:
            reader = copy.deepcopy(self.reader)
            eventLoop = self.EventLoop(build_events, reader, dataset.name)
            eventLoops.append(eventLoop)
        runids = self.eventLoopRunner.run_multiple(eventLoops)

        self.runids.extend(runids)
        # e.g., [0, 1, 2]

        self.runid_dataset_map.update({i: dataset.name for i in runids})
        # e.g., {0: 'dataset1', 1: 'dataset1', 2: 'dataset1', 3: 'dataset3'}

        self.dataset_runid_reader_map[dataset.name] = self.dataset_runid_reader_map.get(dataset.name, OrderedDict())
        self.dataset_runid_reader_map[dataset.name].update(((i, None) for i in runids))
        # e.g.,
        # OrderedDict(
        #     [
        #         ('dataset1', OrderedDict([(0, None), (1, None), (2, None)])),
        #         ('dataset2', OrderedDict()),
        #         ('dataset3', OrderedDict([(3, None)]))
        #     ])

    def end(self):

        runids_towait = self.runids[:]
        while runids_towait:
            runid, reader = self.eventLoopRunner.receive_one()
            self._merge(runid, reader)
            runids_towait.remove(runid)

        dataset_readers_list = [(d, list(rr.values())) for d, rr in self.dataset_runid_reader_map.items()]
        # e.g.,
        # [('dataset1', reader), ('dataset2', []), ('dataset3', reader)]

        return self.collector.collect(dataset_readers_list)

    def _merge(self, runid, reader):
        dataset = self.runid_dataset_map[runid]
        runid_reader_map = self.dataset_runid_reader_map[dataset]
        merge_in_order(runid_reader_map, runid, reader)

##__________________________________________________________________||
