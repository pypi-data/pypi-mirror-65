from __future__ import print_function
import six
from twisted.trial import unittest
from twisted.python import components, failure, reflect
from foolscap.test.common import TargetMixin, HelperTarget

from foolscap import copyable, tokens
from foolscap.api import Copyable, RemoteCopy
from foolscap.tokens import Violation
from foolscap.schema import StringConstraint

# MyCopyable1 is the basic Copyable/RemoteCopy pair, using auto-registration.

class MyCopyable1(Copyable):
    typeToCopy = "foolscap.test_copyable.MyCopyable1"
    pass
class MyRemoteCopy1(RemoteCopy):
    copytype = MyCopyable1.typeToCopy
    pass
#registerRemoteCopy(MyCopyable1.typeToCopy, MyRemoteCopy1)

# MyCopyable2 overrides the various Copyable/RemoteCopy methods. It
# also sets 'copytype' to auto-register with a matching name

class MyCopyable2(Copyable):
    def getTypeToCopy(self):
        return "MyCopyable2name"
    def getStateToCopy(self):
        return {"a": 1, "b": self.b}
class MyRemoteCopy2(RemoteCopy):
    copytype = "MyCopyable2name"
    def setCopyableState(self, state):
        self.c = 1
        self.d = state["b"]

# MyCopyable3 uses a custom Slicer and a custom Unslicer

class MyCopyable3:
    def getAlternateCopyableState(self):
        return {"e": 2}

class MyCopyable3Slicer(copyable.CopyableSlicer):
    def slice(self, streamable, banana):
        yield b'copyable'
        yield b"MyCopyable3name"
        state = self.obj.getAlternateCopyableState()
        for k,v in state.items():
            yield six.ensure_binary(k)
            yield v

class MyRemoteCopy3:
    pass
class MyRemoteCopy3Unslicer(copyable.RemoteCopyUnslicer):
    def __init__(self):
        self.schema = None
    def factory(self, state):
        obj = MyRemoteCopy3()
        obj.__dict__ = state
        return obj
    def receiveClose(self):
        obj,d = copyable.RemoteCopyUnslicer.receiveClose(self)
        obj.f = "yes"
        return obj, d

# register MyCopyable3Slicer as an ISlicer adapter for MyCopyable3, so we
# can verify that it overrides the inherited CopyableSlicer behavior. We
# also register an Unslicer to create the results.
components.registerAdapter(MyCopyable3Slicer, MyCopyable3, tokens.ISlicer)
copyable.registerRemoteCopyUnslicerFactory("MyCopyable3name",
                                           MyRemoteCopy3Unslicer)


# MyCopyable4 uses auto-registration, and adds a stateSchema

class MyCopyable4(Copyable):
    typeToCopy = "foolscap.test_copyable.MyCopyable4"
    pass
class MyRemoteCopy4(RemoteCopy):
    copytype = MyCopyable4.typeToCopy
    stateSchema = copyable.AttributeDictConstraint(
        ('foo', int),
        ('bar', StringConstraint(1000)))
    pass

# MyCopyable5 disables auto-registration

class MyRemoteCopy5(RemoteCopy):
    copytype = None # disable auto-registration


class Copyable(TargetMixin, unittest.TestCase):

    def setUp(self):
        TargetMixin.setUp(self)
        self.setupBrokers()
        if 0:
            print()
            self.callingBroker.doLog = "TX"
            self.targetBroker.doLog = " rx"

    def send(self, arg):
        rr, target = self.setupTarget(HelperTarget())
        d = rr.callRemote("set", obj=arg)
        d.addCallback(self.assertTrue)
        # some of these tests require that we return a Failure object, so we
        # have to wrap this in a tuple to survive the Deferred.
        d.addCallback(lambda res: (target.obj,))
        return d

    def testCopy0(self):
        d = self.send(1)
        d.addCallback(self.assertEqual, (1,))
        return d

    def testFailure1(self):
        self.callingBroker.unsafeTracebacks = True
        try:
            raise RuntimeError("message here")
        except:
            f0 = failure.Failure()
        d = self.send(f0)
        d.addCallback(self._testFailure1_1)
        return d
    def _testFailure1_1(self, xxx_todo_changeme):
        #print "CopiedFailure is:", f
        #print f.__dict__
        (f,) = xxx_todo_changeme
        self.assertIn("RuntimeError", reflect.qual(f.type))
        self.assertTrue(f.check, RuntimeError)
        self.assertEqual(f.value, "message here")
        self.assertEqual(f.frames, [])
        self.assertEqual(f.tb, None)
        self.assertEqual(f.stack, [])
        # there should be a traceback
        self.assertTrue(f.traceback.find("raise RuntimeError") != -1,
                        "no 'raise RuntimeError' in '%s'" % (f.traceback,))
        # older Twisted (before 17.9.0) used a Failure class that could be
        # pickled, so our derived CopiedFailure class could be round-tripped
        # through pickle correclty. Twisted-17.9.0 changed that, so we no
        # longer try that.
        ## p = pickle.dumps(f)
        ## f2 = pickle.loads(p)
        ## self.failUnlessEqual(reflect.qual(f2.type), "exceptions.RuntimeError")
        ## self.failUnless(f2.check, RuntimeError)
        ## self.failUnlessEqual(f2.value, "message here")
        ## self.failUnlessEqual(f2.frames, [])
        ## self.failUnlessEqual(f2.tb, None)
        ## self.failUnlessEqual(f2.stack, [])
        ## self.failUnless(f2.traceback.find("raise RuntimeError") != -1,
        ##                 "no 'raise RuntimeError' in '%s'" % (f2.traceback,))

    def testFailure2(self):
        self.callingBroker.unsafeTracebacks = False
        try:
            raise RuntimeError("message here")
        except:
            f0 = failure.Failure()
        d = self.send(f0)
        d.addCallback(self._testFailure2_1)
        return d
    def _testFailure2_1(self, xxx_todo_changeme1):
        #print "CopiedFailure is:", f
        #print f.__dict__
        (f,) = xxx_todo_changeme1
        self.assertIn("RuntimeError", reflect.qual(f.type))
        self.assertTrue(f.check, RuntimeError)
        self.assertEqual(f.value, "message here")
        self.assertEqual(f.frames, [])
        self.assertEqual(f.tb, None)
        self.assertEqual(f.stack, [])
        # there should not be a traceback
        self.assertEqual(f.traceback, "Traceback unavailable\n")

        ## # we should be able to pickle CopiedFailures, and when we restore
        ## # them, they should look like the original
        ## p = pickle.dumps(f)
        ## f2 = pickle.loads(p)
        ## self.failUnlessEqual(reflect.qual(f2.type), "exceptions.RuntimeError")
        ## self.failUnless(f2.check, RuntimeError)
        ## self.failUnlessEqual(f2.value, "message here")
        ## self.failUnlessEqual(f2.frames, [])
        ## self.failUnlessEqual(f2.tb, None)
        ## self.failUnlessEqual(f2.stack, [])
        ## self.failUnlessEqual(f2.traceback, "Traceback unavailable\n")

    def testCopy1(self):
        obj = MyCopyable1() # just copies the dict
        obj.a = 12
        obj.b = "foo"
        d = self.send(obj)
        d.addCallback(self._testCopy1_1)
        return d
    def _testCopy1_1(self, xxx_todo_changeme2):
        (res,) = xxx_todo_changeme2
        self.assertTrue(isinstance(res, MyRemoteCopy1))
        self.assertEqual(res.a, 12)
        self.assertEqual(res.b, "foo")

    def testCopy2(self):
        obj = MyCopyable2() # has a custom getStateToCopy
        obj.a = 12 # ignored
        obj.b = "foo"
        d = self.send(obj)
        d.addCallback(self._testCopy2_1)
        return d
    def _testCopy2_1(self, xxx_todo_changeme3):
        (res,) = xxx_todo_changeme3
        self.assertTrue(isinstance(res, MyRemoteCopy2))
        self.assertEqual(res.c, 1)
        self.assertEqual(res.d, "foo")
        self.assertFalse(hasattr(res, "a"))

    def testCopy3(self):
        obj = MyCopyable3() # has a custom Slicer
        obj.a = 12 # ignored
        obj.b = b"foo" # ignored
        d = self.send(obj)
        d.addCallback(self._testCopy3_1)
        return d
    def _testCopy3_1(self, xxx_todo_changeme4):
        (res,) = xxx_todo_changeme4
        self.assertTrue(isinstance(res, MyRemoteCopy3))
        self.assertEqual(res.e, 2)
        self.assertEqual(res.f, "yes")
        self.assertFalse(hasattr(res, "a"))

    def testCopy4(self):
        obj = MyCopyable4()
        obj.foo = 12
        obj.bar = b"bar"
        d = self.send(obj)
        d.addCallback(self._testCopy4_1, obj)
        return d
    def _testCopy4_1(self, xxx_todo_changeme5, obj):
        (res,) = xxx_todo_changeme5
        self.assertTrue(isinstance(res, MyRemoteCopy4))
        self.assertEqual(res.foo, 12)
        self.assertEqual(res.bar, b"bar")

        obj.bad = b"unwanted attribute"
        d = self.send(obj)
        d.addCallbacks(lambda res: self.fail("this was supposed to fail"),
                       self._testCopy4_2, errbackArgs=(obj,))
        return d
    def _testCopy4_2(self, why, obj):
        why.trap(Violation)
        self.failUnlessSubstring("unknown attribute 'bad'", str(why))
        del obj.bad

        obj.foo = b"not a number"
        d = self.send(obj)
        d.addCallbacks(lambda res: self.fail("this was supposed to fail"),
                       self._testCopy4_3, errbackArgs=(obj,))
        return d
    def _testCopy4_3(self, why, obj):
        why.trap(Violation)
        self.failUnlessSubstring("STRING token rejected by IntegerConstraint",
                                 str(why))

        obj.foo = 12
        obj.bar = b"very long " * 1000
        # MyRemoteCopy4 says .bar is a String(1000), so reject long strings
        d = self.send(obj)
        d.addCallbacks
        d.addCallbacks(lambda res: self.fail("this was supposed to fail"),
                       self._testCopy4_4)
        return d
    def _testCopy4_4(self, why):
        why.trap(Violation)
        self.failUnlessSubstring("token too large", str(why))

class Registration(unittest.TestCase):
    def testRegistration(self):
        rc_classes = copyable.debug_RemoteCopyClasses
        copyable_classes = list(rc_classes.values())
        self.assertTrue(MyRemoteCopy1 in copyable_classes)
        self.assertTrue(MyRemoteCopy2 in copyable_classes)
        self.failUnlessIdentical(rc_classes["MyCopyable2name"],
                                 MyRemoteCopy2)
        self.assertFalse(MyRemoteCopy5 in copyable_classes)


##############
# verify that ICopyable adapters are actually usable


class TheThirdPartyClassThatIWantToCopy:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def copy_ThirdPartyClass(orig):
    return "TheThirdPartyClassThatIWantToCopy_name", orig.__dict__
copyable.registerCopier(TheThirdPartyClassThatIWantToCopy,
                        copy_ThirdPartyClass)

def make_ThirdPartyClass(state):
    # unpack the state into constructor arguments
    a = state['a']; b = state['b']
    # now create the object with the constructor
    return TheThirdPartyClassThatIWantToCopy(a, b)
copyable.registerRemoteCopyFactory("TheThirdPartyClassThatIWantToCopy_name",
                                   make_ThirdPartyClass)

class Adaptation(TargetMixin, unittest.TestCase):
    def setUp(self):
        TargetMixin.setUp(self)
        self.setupBrokers()
        if 0:
            print()
            self.callingBroker.doLog = "TX"
            self.targetBroker.doLog = " rx"
    def send(self, arg):
        rr, target = self.setupTarget(HelperTarget())
        d = rr.callRemote("set", obj=arg)
        d.addCallback(self.assertTrue)
        # some of these tests require that we return a Failure object, so we
        # have to wrap this in a tuple to survive the Deferred.
        d.addCallback(lambda res: (target.obj,))
        return d

    def testAdaptation(self):
        obj = TheThirdPartyClassThatIWantToCopy(45, 91)
        d = self.send(obj)
        d.addCallback(self._testAdaptation_1)
        return d
    def _testAdaptation_1(self, xxx_todo_changeme6):
        (res,) = xxx_todo_changeme6
        self.assertTrue(isinstance(res, TheThirdPartyClassThatIWantToCopy))
        self.assertEqual(res.a, 45)
        self.assertEqual(res.b, 91)

