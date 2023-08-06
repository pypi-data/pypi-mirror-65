from __future__ import print_function
import six
import sys, os.path, time, bz2
import json
from zope.interface import implementer
from twisted.python import usage
from twisted.internet import reactor
from foolscap.logging.interfaces import IIncidentReporter
from foolscap.logging import levels, app_versions, flogfile
from foolscap.eventual import eventually
from foolscap.util import move_into_place
from foolscap import base32

TIME_FORMAT = "%Y-%m-%d--%H-%M-%S"

class IncidentQualifier:
    """I am responsible for deciding what qualifies as an Incident. I look at
    the event stream and watch for a 'triggering event', then signal my
    handler when the events that I've seen are severe enought to warrant
    recording the recent history in an 'incident log file'.

    My event() method should be called with each event. When I declare an
    incident, I will call my handler's declare_incident(ev) method, with the
    triggering event. Since event() will be fired from an eventual-send
    queue, the incident will be declared slightly later than the triggering
    event.
    """

    def set_handler(self, handler):
        self.handler = handler

    def check_event(self, ev):
        if ev['level'] >= levels.WEIRD:
            return True
        return False

    def event(self, ev):
        if self.check_event(ev) and self.handler:
            self.handler.declare_incident(ev)

@implementer(IIncidentReporter)
class IncidentReporter:
    """Once an Incident has been declared, I am responsible for making a
    durable record all relevant log events. I do this by creating a logfile
    (a series of JSON lines, one per log event dictionary) and copying
    everything from the history buffer into it. I can copy a small number of
    future events into it as well, to record what happens as the application
    copes with the situtation.

    I am responsible for just a single incident.

    I am created with a reference to a FoolscapLogger instance, from which I
    will grab the contents of the history buffer.

    When I have closed the incident logfile, I will notify the logger by
    calling their incident_recorded() method, passing it the local filename
    of the logfile I created and the triggering event. This can be used to
    notify remote subscribers about the incident that just occurred.
    """

    TRAILING_DELAY = 5.0 # gather 5 seconds of post-trigger events
    TRAILING_EVENT_LIMIT = 100 # or 100 events, whichever comes first

    def __init__(self, basedir, logger, tubid_s):
        self.basedir = basedir
        self.logger = logger
        self.tubid_s = tubid_s
        self.active = True
        self.timer = None

    def is_active(self):
        return self.active

    def format_time(self, when):
        return time.strftime(TIME_FORMAT, time.gmtime(when)) + "Z"

    def incident_declared(self, triggering_event):
        self.trigger = triggering_event
        # choose a name for the logfile
        now = time.time()
        unique = os.urandom(4)
        unique_s = base32.encode(unique)
        self.name = "incident-%s-%s" % (self.format_time(now), unique_s)
        filename = self.name + ".flog"
        self.abs_filename = os.path.join(self.basedir, filename)
        self.abs_filename_bz2 = self.abs_filename + ".bz2"
        self.abs_filename_bz2_tmp = self.abs_filename + ".bz2.tmp"
        # open logfile. We use both an uncompressed one and a compressed one.
        self.f1 = open(self.abs_filename, "wb")
        self.f2 = bz2.BZ2File(self.abs_filename_bz2_tmp, "wb")

        # write header with triggering_event
        self.f1.write(flogfile.MAGIC)
        self.f2.write(flogfile.MAGIC)
        flogfile.serialize_header(self.f1, "incident",
                                  trigger=triggering_event,
                                  versions=app_versions.versions,
                                  pid=os.getpid())
        flogfile.serialize_header(self.f2, "incident",
                                  trigger=triggering_event,
                                  versions=app_versions.versions,
                                  pid=os.getpid())

        if self.TRAILING_DELAY is not None:
            # subscribe to events that occur after this one
            self.still_recording = True
            self.remaining_events = self.TRAILING_EVENT_LIMIT
            self.logger.addObserver(self.trailing_event)

        # use self.logger.buffers, copy events into logfile
        events = list(self.logger.get_buffered_events())
        events.sort(key=lambda a: a['num'])
        for e in events:
            flogfile.serialize_wrapper(self.f1, e,
                                       from_=self.tubid_s, rx_time=now)
            flogfile.serialize_wrapper(self.f2, e,
                                       from_=self.tubid_s, rx_time=now)

        self.f1.flush()
        # the BZ2File has no flush method

        if self.TRAILING_DELAY is None:
            self.active = False
            eventually(self.finished_recording)
        else:
            # now we wait for the trailing events to arrive
            self.timer = reactor.callLater(self.TRAILING_DELAY,
                                           self.stop_recording)

    def trailing_event(self, ev):
        if not self.still_recording:
            return

        self.remaining_events -= 1
        if self.remaining_events >= 0:
            now = time.time()
            flogfile.serialize_wrapper(self.f1, ev,
                                       from_=self.tubid_s, rx_time=now)
            flogfile.serialize_wrapper(self.f2, ev,
                                       from_=self.tubid_s, rx_time=now)
            return

        self.stop_recording()

    def new_trigger(self, ev):
        # it is too late to add this to the header. We could add it to a
        # trailer, though.
        pass

    def stop_recording(self):
        self.still_recording = False
        self.active = False
        if self.timer and self.timer.active():
            self.timer.cancel()

        self.logger.removeObserver(self.trailing_event)
        # Observers are notified through an eventually() call, so we might
        # get a few more after the observer is removed. We use
        # self.still_recording to hush them.
        eventually(self.finished_recording)

    def finished_recording(self):
        self.f2.close()
        move_into_place(self.abs_filename_bz2_tmp, self.abs_filename_bz2)
        # the compressed logfile has closed successfully. We no longer care
        # about the uncompressed one.
        self.f1.close()
        os.unlink(self.abs_filename)

        # now we can tell the world about our new incident report
        eventually(self.logger.incident_recorded,
                   self.abs_filename_bz2, self.name, self.trigger)

class NonTrailingIncidentReporter(IncidentReporter):
    TRAILING_DELAY = None


class ClassifyOptions(usage.Options):
    stdout = sys.stdout
    stderr = sys.stderr
    synopsis = "Usage: flogtool classify-incident [options] INCIDENTFILE.."

    optFlags = [
        ("verbose", "v", "show trigger details for unclassifiable incidents"),
        ]
    optParameters = [
        ("classifier-directory", "c", ".",
         "directory with classify_*.py functions to import"),
        ]

    def parseArgs(self, *files):
        self.files = files


class IncidentClassifierBase:

    def __init__(self):
        self.classifiers = []

    def add_classifier(self, f):
        # there are old .tac files that call this explicitly
        self.classifiers.append(f)

    def add_classify_files(self, plugindir):
        plugindir = os.path.expanduser(plugindir)
        for fn in os.listdir(plugindir):
            if not (fn.startswith("classify_") and fn.endswith(".py")):
                continue
            f = open(os.path.join(plugindir, fn), "r").read()
            localdict = {}
            six.exec_(f, localdict)
            self.add_classifier(localdict["classify_incident"])

    def load_incident(self, abs_fn):
        assert abs_fn.endswith(".bz2")
        events = flogfile.get_events(abs_fn)
        header = next(events)["header"]
        wrapped_events = [event["d"] for event in events]
        return (header, wrapped_events)

    def classify_incident(self, incident):
        categories = set()
        for f in self.classifiers:
            (header, events) = incident
            trigger = header["trigger"]
            c = f(trigger)
            if c: # allow the classifier to return None, or [], or ["foo"]
                if isinstance(c, str):
                    c = [c] # or just "foo"
                categories.update(c)
        if not categories:
            categories.add("unknown")
        return categories

class IncidentClassifier(IncidentClassifierBase):
    def run(self, options):
        self.add_classify_files(options["classifier-directory"])
        out = options.stdout
        for f in options.files:
            abs_fn = os.path.expanduser(f)
            incident = self.load_incident(abs_fn)
            categories = self.classify_incident(incident)
            print(u"%s: %s" % (f, ",".join(sorted(categories))), file=out)
            if list(categories) == ["unknown"] and options["verbose"]:
                (header, events) = incident
                trigger = header["trigger"]
                from foolscap.logging.log import format_message
                print(format_message(trigger), file=out)
                #pprint(trigger, stream=out)
                print(six.ensure_text(json.dumps(trigger)), file=out)
                if 'failure' in trigger:
                    print(u" FAILURE:", file=out)
                    lines = str(trigger['failure']).split("\n")
                    for line in lines:
                        print(u" %s" % (line,), file=out)
                print(u"", file=out)

