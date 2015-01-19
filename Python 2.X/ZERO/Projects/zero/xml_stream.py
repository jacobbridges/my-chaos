'''Module for XML event streams.

This module provides several classes for creating,
saving, and delaying the processing of XML events.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'February 11, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
J. Clark, for creating the Expat parser.
P. Dazon, for testing code that led to this module.'''

################################################################################

import os as _os
import sys as _sys
import xml.sax as _xml_sax

################################################################################

class _Event:

    '_Event(*args) -> _Event'

    def __init__(self, *args):
        'Initialize the _Event object.'
        self.__args = args

    def __repr__(self):
        'Return the object\'s representation.'
        return '%s(%s)' % (self.__class__.__name__, ', '.join(map(repr, self.__args)))

    def __call__(self, handler=None):
        'Either return arguments or process handler.'
        if handler is None:
            return self.__args
        else:
            getattr(handler, self.__class__.__name__)(*self.__args)

class setDocumentLocator(_Event): pass
class startDocument(_Event): pass
class endDocument(_Event): pass
class startPrefixMapping(_Event): pass
class endPrefixMapping(_Event): pass
class startElement(_Event): pass
class endElement(_Event): pass
class startElementNS(_Event): pass
class endElementNS(_Event): pass
class characters(_Event): pass
class ignorableWhitespace(_Event): pass
class processingInstruction(_Event): pass
class skippedEntity(_Event): pass

################################################################################

class Stream:

    'Stream(filename_or_stream_or_string) -> Stream'

    def __init__(self, filename_or_stream_or_string):
        'Initialize the Stream object.'
        self.__stream = []
        if isinstance(filename_or_stream_or_string, str):
            if _os.path.exists(filename_or_stream_or_string):
                _xml_sax.parse(filename_or_stream_or_string, self)
            else:
                _xml_sax.parseString(filename_or_stream_or_string, self)
        else:
            _xml_sax.parse(filename_or_stream_or_string, self)
        self.__maximized = self.__minimized = False

    def __getattr__(self, name):
        'Dynamically create and bind Methods.'
        self.__dict__[name] = Method(self.__stream, name)
        return self.__dict__[name]

    def __iter__(self):
        'Return an iterator.'
        return iter(self.__stream)

    def parse(self, handler):
        'Simulate events on a handler.'
        for event in self:
            event(handler)

    def maximize(self, style):
        'Prepare the stream for printing.'
        if not self.__maximized:
            self.minimize()
            self.__minimized = False
            self.__maximized = True
            if isinstance(self.__stream[0], setDocumentLocator):
                index =  2
            else:
                index =  1
            level = 0
            cancel = False
            while True:
                event = self.__stream[index]
                if isinstance(event, (startPrefixMapping, startElement, startElementNS)):
                    self.__stream.insert(index, characters(style * level))
                    index += 2
                    if not isinstance(self.__stream[index], (endDocument, endPrefixMapping, endElement, endElementNS)):
                        self.__stream.insert(index, characters('\n'))
                        index += 1
                        level += 1
                elif isinstance(event, (endPrefixMapping, endElement, endElementNS)):
                    if not isinstance(self.__stream[index - 1], (startDocument, startPrefixMapping, startElement, startElementNS)):
                        level -= 1
                        if cancel:
                            cancel = False
                            index += 1
                        else:
                            self.__stream.insert(index, characters(style * level))
                            index += 2
                    else:
                        index += 1
                    self.__stream.insert(index, characters('\n'))
                    index += 1
                elif isinstance(event, endDocument):
                    break
                elif isinstance(event, characters):
                    del self.__stream[index - 1]
                    cancel = True

    def minimize(self):
        'Prepare the stream for data extraction.'
        if not self.__minimized:
            self.__maximized = False
            self.__minimized = True
            if isinstance(self.__stream[0], setDocumentLocator):
                index = 2
            else:
                index = 1
            inside = True
            while index < len(self.__stream):
                event = self.__stream[index]
                if isinstance(event, (startPrefixMapping, startElement, startElementNS)):
                    inside = True
                    index = self.__prune(index)
                elif isinstance(event, (endDocument, endPrefixMapping, endElement, endElementNS)):
                    if inside:
                        inside = False
                        index = self.__join(index)
                    else:
                        index = self.__prune(index)
                index += 1

    def __prune(self, index):
        'Private class method.'
        temp = index - 1
        event = self.__stream[temp]
        while not isinstance(event, (startDocument, startPrefixMapping, endPrefixMapping, startElement, endElement, startElementNS, endElementNS)):
            if isinstance(event, characters):
                del self.__stream[temp]
                index -= 1
            temp -= 1
            event = self.__stream[temp]
        return index

    def __join(self, index):
        'Private class method.'
        temp = index - 1
        event_1 = self.__stream[temp]
        while not isinstance(event_1, (startDocument, startPrefixMapping, startElement, startElementNS)):
            if isinstance(event_1, characters):
                event_2 = self.__stream[temp - 1]
                if isinstance(event_2, characters):
                    self.__stream[temp] = characters(event_2()[0] + event_1()[0])
                    del self.__stream[temp - 1]
                    index -= 1
            temp -= 1
            event_1 = self.__stream[temp]
        return index

################################################################################

class Method:

    'Method(stream, name) -> Method'

    def __init__(self, stream, name):
        'Initialize the Method object.'
        self.__stream = stream
        self.__name = name

    def __call__(self, *args):
        'Dynamically create and add events to the stream.'
        self.__stream.append(globals()[self.__name](*args))

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
