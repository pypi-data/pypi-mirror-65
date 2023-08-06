from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from quicktions import Fraction

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import ValueGenerator, ValueGeneratorException
from musurgia.quantize import get_quantized_values


class BreatheException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ChordFieldException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoNextChordError(ChordFieldException):
    def __init__(self, *args):
        super().__init__(*args)


class LongEndingError(ChordFieldException):
    def __init__(self, delta, *args):
        msg = 'delta={}'.format(float(delta))
        super().__init__(msg, *args)


class ShortEndingError(ChordFieldException):
    def __init__(self, delta, *args):
        msg = 'delta={}'.format(float(delta))
        super().__init__(msg, *args)


class ParentSetQuarterDurationError(ChordFieldException):
    def __init__(self, *args):
        msg = 'parent\'s quarter_duration cannot be set'
        super().__init__(msg, *args)


class ParentSetEndingModesError(ChordFieldException):
    def __init__(self, *args):
        msg = 'parent\'s endings modes cannot be set'
        super().__init__(msg, *args)


class ChordField(object):
    def __init__(self, quarter_duration=None, duration_generator=None, midi_generator=None, chord_generator=None,
                 long_ending_mode=None, short_ending_mode=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self._duration_generator = None
        self._midi_generator = None
        self._chord_generator = None
        self._chords = None
        self._long_ending_mode = None
        self._short_ending_mode = None
        self._children = None
        self._parent = None
        self._position = 0
        self._name = None

        self.quarter_duration = quarter_duration
        self.duration_generator = duration_generator
        self.midi_generator = midi_generator
        self.chord_generator = chord_generator
        self.long_ending_mode = long_ending_mode
        self.short_ending_mode = short_ending_mode

    def _get_value_generators(self):
        return [value_generator for value_generator in
                (self.chord_generator, self.duration_generator, self.midi_generator) if value_generator is not None]

    def _get_private_value_generators(self):
        return [value_generator for value_generator in
                (self._chord_generator, self._duration_generator, self._midi_generator) if value_generator is not None]

    def _set_up_value_generator(self, value_generator, value_mode=None):
        if not isinstance(value_generator, ValueGenerator):
            raise TypeError('value_generator must be of type ValueGenerator not {}'.format(
                type(value_generator)))
        value_generator.value_mode = value_mode
        try:
            value_generator.duration = self.quarter_duration
        except ValueGeneratorException:
            if self.quarter_duration is None:
                raise ValueGeneratorException()
            factor = Fraction(self.quarter_duration, value_generator.duration)
            for child in value_generator.children:
                child.duration *= factor

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def add_child(self, child):
        if self._quarter_duration:
            raise ParentSetQuarterDurationError()
        if self.long_ending_mode is not None or self.short_ending_mode is not None:
            raise ParentSetEndingModesError()
        if not isinstance(child, ChordField):
            raise TypeError()
        if self._children is None:
            self._children = []

        self._children.append(child)
        if child.duration_generator:
            if self.duration_generator is None:
                self.duration_generator = ValueGenerator()
                self.duration_generator.add_child(child.duration_generator)
            elif self.duration_generator.children:
                self.duration_generator.add_child(child.duration_generator)
            else:
                pass
        if child.midi_generator:
            if self.midi_generator is None:
                self.midi_generator = ValueGenerator()
                self.midi_generator.add_child(child.midi_generator)
            elif self.midi_generator.children:
                self.midi_generator.add_child(child.midi_generator)
            else:
                pass
        if child.chord_generator:
            if self.chord_generator is None:
                self.chord_generator = ValueGenerator()
                self.chord_generator.add_child(child.chord_generator)
            elif self.chord_generator.children:
                self.chord_generator.add_child(child.chord_generator)
            else:
                pass
        child._parent = self
        self._update_durations()
        return child

    def _update_durations(self):
        for value_generator in self._get_value_generators():
            try:
                value_generator.duration = self.quarter_duration
            except ValueGeneratorException:
                pass

    @property
    def quarter_duration(self):
        if self.children:
            children_quarter_durations = [child.quarter_duration for child in self.children]
            if None in children_quarter_durations:
                return None
            else:
                return sum(children_quarter_durations)
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            if self.children:
                raise ParentSetQuarterDurationError()
            else:
                self._quarter_duration = value
                self._update_durations()
                if self.parent:
                    self.parent._update_durations()

    @property
    def duration_generator(self):
        if not self._duration_generator and self.parent and self.parent.duration_generator:
            return self.parent.duration_generator
        return self._duration_generator

    @duration_generator.setter
    def duration_generator(self, value):
        self._duration_generator = value
        if value:
            self._set_up_value_generator(self.duration_generator, 'duration')

    @property
    def midi_generator(self):
        if not self._midi_generator and self.parent and self.parent.midi_generator:
            return self.parent.midi_generator
        return self._midi_generator

    @midi_generator.setter
    def midi_generator(self, value):
        self._midi_generator = value
        if value:
            self._set_up_value_generator(self.midi_generator, 'midi')

    @property
    def chord_generator(self):
        if not self._chord_generator and self.parent:
            return self.parent.chord_generator
        return self._chord_generator

    @chord_generator.setter
    def chord_generator(self, value):
        self._chord_generator = value
        if value:
            self._set_up_value_generator(self.chord_generator, 'chord')

    @property
    def position(self):
        return self._position

    @property
    def position_in_parent(self):
        index = self.parent.children.index(self)
        if index == 0:
            return 0
        return sum([child.quarter_duration for child in self.parent.children[:index]])

    @property
    def long_ending_mode(self):
        return self._long_ending_mode

    @long_ending_mode.setter
    def long_ending_mode(self, val):
        if val is not None and self.children is not None:
            raise ParentSetEndingModesError()
        """
        :param val: can be None, 'self_extend', 'cut', 'omit', 'omit_and_add_rest', 'omit_and_stretch'
        for dealing with last chord, if it is too long and ends after self.quarter_duration
        None: raises Error
        self_extend: self.quarter_duration will be prolonged.
        cut: last chord will be cut short.
        omit: last chord will be omitted and self.quarter_duration cut short.
        omit_and_add_rest: last chord will be omitted and rests will be added.
        omit_and_stretch: last chord will be omitted and the new last chord  will be extended.
        """
        permitted = [None, 'self_extend', 'cut', 'omit', 'omit_and_add_rest', 'omit_and_stretch']
        if val not in permitted:
            raise ValueError('long_ending_mode.value {} must be in {}'.format(val, permitted))
        self._long_ending_mode = val

    @property
    def short_ending_mode(self):
        return self._short_ending_mode

    @short_ending_mode.setter
    def short_ending_mode(self, val):
        if val is not None and self.children is not None:
            raise ParentSetEndingModesError()
        """
        :param val: can be None, 'self_shrink', 'add_rest', 'stretch'
        for dealing with last chord, if it is too long and ends after self.quarter_duration
        None: raises Error
        self_shrink: self.quarter_duration will be shortened.
        omit: rests will be added.
        stretch: last chord will be prolonged.
        """
        permitted = [None, 'self_shrink', 'add_rest', 'stretch']
        if val not in permitted:
            raise ValueError('short_ending_mode.value {} must be in {}'.format(val, permitted))
        self._short_ending_mode = val

    @property
    def chords(self):
        if self.children:
            self._chords = [chord for child in self.children for chord in child.chords]
        else:
            list(self)
        return self._chords

    @property
    def simple_format(self):
        sf = SimpleFormat()
        if self.chords:
            for chord in self.chords:
                sf.add_chord(chord)
        return sf

    def _get_next_duration(self):
        if self.duration_generator:
            next_duration = self.duration_generator.__next__()
            self._position += next_duration
            for generator in self._get_value_generators():
                if generator != self.duration_generator:
                    generator._position += next_duration
            return next_duration
        else:
            return None

    def _get_next_midi(self):
        if self.midi_generator:
            # self.midi_generator._position = self.position
            return self.midi_generator.__next__()
        else:
            return None

    def _get_next_chord(self):
        next_chord = None
        next_midi = self._get_next_midi()
        next_duration = self._get_next_duration()

        if self.chord_generator:
            next_chord = self.chord_generator.__next__()

        if next_chord:
            if next_duration is not None:
                next_chord.quarter_duration = next_duration
            if next_midi is not None:
                next_chord.midis = next_midi
        else:
            if next_duration is None:
                raise NoNextChordError('next_duration is None!')
            if next_midi is None:
                raise NoNextChordError('next_midi is None!')
            next_chord = TreeChord(quarter_duration=next_duration, midis=next_midi)
        if self._chords is None:
            self._chords = []
        self._chords.append(next_chord)
        return next_chord

    def _check_quarter_duration(self):
        if self._chords:
            delta = sum([chord.quarter_duration for chord in self._chords]) - self.quarter_duration
            if delta > 0:
                if self.long_ending_mode == 'self_extend':
                    if self.parent:
                        try:
                            next_child = self.parent.children[self.parent.children.index(self) + 1]
                            next_child._position = delta
                        except IndexError:
                            pass
                    try:
                        self.quarter_duration += delta
                    except ParentSetQuarterDurationError:
                        self.children[-1].quarter_duration += delta
                elif self.long_ending_mode == 'cut':
                    self._chords[-1].quarter_duration -= delta
                elif self.long_ending_mode in ['omit', 'omit_and_add_rest', 'omit_and_stretch']:
                    self._chords.pop()
                    new_delta = self.quarter_duration - sum([chord.quarter_duration for chord in self._chords])
                    if self.long_ending_mode == 'omit_and_add_rest':
                        new_chord = TreeChord(midis=0, quarter_duration=new_delta)
                        new_chord.zero_mode = 'remove'
                        self._chords.append(new_chord)
                    elif self.long_ending_mode == 'omit_and_stretch':
                        self._chords[-1].quarter_duration += new_delta
                    else:
                        self.quarter_duration -= new_delta
                else:
                    raise LongEndingError(delta)

            elif delta < 0:
                if self.short_ending_mode == 'self_shrink':
                    self.quarter_duration += delta
                elif self.short_ending_mode == 'add_rest':
                    new_chord = TreeChord(midis=0, quarter_duration=-delta)
                    new_chord.zero_mode = 'remove'
                    self._chords.append(new_chord)
                elif self.short_ending_mode == 'stretch':
                    self._chords[-1].quarter_duration -= delta
                else:
                    raise ShortEndingError(delta)
            else:
                pass

    def __iter__(self):
        return self

    def __next__(self):
        try:
            next_chord = self._get_next_chord()
            return next_chord
        except StopIteration:
            self._check_quarter_duration()
            raise StopIteration()

    def __deepcopy__(self, memodict={}):
        if self.__class__ == Breathe:
            copied = self.__class__(proportions=self.proportions, breakpoints=self.breakpoints,
                                    quarter_duration=self.quarter_duration)
        else:
            copied = self.__class__(quarter_duration=self.quarter_duration)

        copied.long_ending_mode = self.long_ending_mode
        copied.short_ending_mode = self.short_ending_mode
        for generator in self._get_private_value_generators():
            if generator.value_mode == 'duration':
                copied._duration_generator = generator.__deepcopy__()
            elif generator.value_mode == 'midi':
                copied._midi_generator = generator.__deepcopy__()
            elif generator.value_mode == 'chord':
                copied._chord_generator = generator.__deepcopy__()
            else:
                raise NotImplementedError()
        if self.children:
            copied._children = []
            for child in self.children:
                copied_child = child.__deepcopy__()
                copied_child._parent = copied
                copied._children.append(copied_child)
        return copied


class Breathe(ChordField):
    def __init__(self, proportions, breakpoints=None, quarter_duration=None, quantize=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._proportions = None
        self._breakpoints = None
        self._quantize = None
        self.quantize = quantize
        self.proportions = proportions
        self.breakpoints = breakpoints
        self.quarter_duration = quarter_duration

    @property
    def quarter_durations(self):
        return [self.repose_1.quarter_duration, self.inspiration.quarter_duration, self.climax.quarter_duration,
                self.expiration.quarter_duration, self.repose_2.quarter_duration]

    def _generate_children(self, quarter_duration):
        names = ['repose_1', 'inspiration', 'climax', 'expiration', 'repose_2']
        fields = []
        child_quarter_durations = [Fraction(proportion * quarter_duration, sum(self.proportions)) for proportion in
                                   self.proportions]
        if self.quantize:
            child_quarter_durations = get_quantized_values(child_quarter_durations, grid_size=self.quantize)

        for index, child_quarter_duration in enumerate(child_quarter_durations):
            field = ChordField(quarter_duration=child_quarter_duration)
            field.name = names[index]
            fields.append(field)

        if not self.breakpoints:
            self.breakpoints = [0.25, 1, 0.25]

        for i in range(5):
            if i == 0:
                a1, an = self.breakpoints[0], self.breakpoints[0]
            elif i == 1:
                a1, an = self.breakpoints[0], self.breakpoints[1]
            elif i == 2:
                a1, an = self.breakpoints[1], self.breakpoints[1]
            elif i == 3:
                a1, an = self.breakpoints[1], self.breakpoints[2]
            else:
                a1, an = self.breakpoints[2], self.breakpoints[2]
            fields[i].duration_generator = ValueGenerator(ArithmeticProgression(a1=a1, an=an, correct_s=True))
        for field in fields:
            if field.quarter_duration:
                generator = field.duration_generator.generator
                if generator.n == 0:
                    raise BreatheException(
                        'field {}: ArithmeticProgression: a1={} s={} n={}'.format(field.name, generator.a1, generator.s,
                                                                                  generator.n))
                self.add_child(field)

    @ChordField.quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            self._generate_children(value)

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if not self._proportions:
            if len(values) != 5:
                ValueError('quarter_durations must have 5 elements.')
            self._proportions = values
        else:
            raise BreatheException('proportions can only be set during initialisation')

    @property
    def breakpoints(self):
        return self._breakpoints

    @breakpoints.setter
    def breakpoints(self, values):
        if not self._breakpoints:
            if len(values) != 3:
                ValueError('quarter_durations must have 3 elements.')
            self._breakpoints = values
        else:
            raise BreatheException('breakpoints can only be set during initialisation')

    @property
    def repose_1(self):
        return self.children[0]

    @property
    def inspiration(self):
        return self.children[1]

    @property
    def climax(self):
        return self.children[2]

    @property
    def expiration(self):
        return self.children[3]

    @property
    def repose_2(self):
        return self.children[4]
