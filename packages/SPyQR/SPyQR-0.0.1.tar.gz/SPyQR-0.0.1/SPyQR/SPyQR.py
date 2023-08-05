"""
SPyQR is an inclusive python project that dreams of allowing all backgrounds to be able to program in python, even
if all you speak is ancient Latin. <3
"""


class Roman:
    """
    Takes an integer and turns it into a Roman Numeral.

    This class should emulate integers in all aspects, except display a Roman Numeral.
    It will hijack any class if it interacts with them through operation.
    It will ruin your day and make you realise why we stopped using this cursed, cursed system.

    :param n: number, the number to be converted into Roman Numerals
    """

    def __init__(self, n):
        def to_int(RN):
            Ndict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
            r = 0

            for i, letter in enumerate(RN):
                if i + 1 < len(RN):
                    try:
                        if Ndict[RN[i]] >= Ndict[RN[i + 1]]:
                            r = r + Ndict[letter]
                        else:
                            r = r - Ndict[letter]
                    except KeyError:
                        raise TypeError(f"'{RN[i + 1] if letter in Ndict.keys() else letter}' is not one the standard "
                                        f"Roman Numerals I,V,X,L,C,D,M")
                else:
                    try:
                        r = r + Ndict[letter]
                    except KeyError:
                        raise TypeError(f"'{letter}' is not one the standard Roman Numerals I,V,X,L,C,D,M")

            if str(Roman(r)) == n:
                return r
            else:
                raise TypeError(f"{n} is not a standard Roman Numeral. Did you mean {Roman(r)}?")

        try:
            m = int(n)
        except ValueError:
            m = to_int(n)

        if m < 1:
            raise ZeroDivisionError("there are no Roman Numerals for non-positive numbers")
        elif m >= 4000:
            raise OverflowError("unfortunately, Romans can't count that high")
        else:
            self.n = m

    def __repr__(self):
        def to_RN(n):
            Rdict = {1: "I", 5: "V", 10: "X", 50: "L", 100: "C", 500: "D", 1000: "M"}
            Sdict = {5: 1, 10: 1, 50: 10, 100: 10, 1000: 100}
            RN = []
            r = n
            l = list(Rdict.keys())
            l.sort(reverse=True)

            while r > 0:
                for i, d in enumerate(l):
                    if r >= d:
                        RN.append(Rdict[d])
                        r = r - d
                        break
                    elif d in Sdict.keys():
                        if r >= d - Sdict[d]:
                            RN.append(Rdict[Sdict[d]] + Rdict[d])
                            r = r - d + Sdict[d]
                    else:
                        pass

            return ''.join(RN)

        return to_RN(self.n)

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        return Roman(int(self) + int(other))

    def __radd__(self, other):
        return Roman(int(other) + int(self))

    def __sub__(self, other):
        return Roman(int(self) - int(other))

    def __rsub__(self, other):
        return Roman(int(other) - int(self))

    def __mul__(self, other):
        return Roman(int(self) * int(other))

    def __rmul__(self, other):
        return Roman(int(other) * int(self))

    def __truediv__(self, other):
        if float(self) / float(other) > 1:
            return Roman(int(self) / int(other))
        else:
            raise ZeroDivisionError("there is no Roman Numeral for 0")

    def __rtruediv__(self, other):
        if float(other) / float(self) > 1:
            return Roman(int(other) / int(self))
        else:
            raise ZeroDivisionError("there is no Roman Numeral for 0")

    def __pow__(self, other):
        return Roman(int(self) ** other)

    def __rpow__(self, other):
        return Roman(other ** int(self))

    def __eq__(self, other):
        return self.n == other

    def __lt__(self, other):
        return self.n < other

    def __gt__(self, other):
        return self.n > other

    def __le__(self, other):
        return self.n <= other

    def __ge__(self, other):
        return self.n >= other

    def __int__(self):
        return self.n

    def __float__(self):
        return float(self.n)

    def __index__(self):
        return int(self)

    def __abs__(self):
        return self

    def __floor__(self):
        return self

    def __hash__(self):
        return hash(self.n)

    def __bool__(self):
        return True

    def __invert__(self):
        return 4000 - self

    def __mod__(self, other):
        return Roman(int(self) % int(other))

    def __rmod__(self, other):
        return Roman(int(other) % int(self))


class enumeRate(enumerate):
    def __init__(self, obj, start=1):
        self.__enumerate = enumerate(obj, start=start)

    def __next__(self):
        n, coll = next(self.__enumerate)
        return (Roman(n), coll)


def Romanise(int_list):
    if isinstance(int_list, list):
        return [Roman(x) for x in int_list]
    if isinstance(int_list, tuple):
        return tuple([Roman(x) for x in int_list])
    if isinstance(int_list, set):
        return set([Roman(x) for x in int_list])
    if isinstance(int_list, str):
        try:
            return Roman(int_list)
        except TypeError:
            import re
            s = int_list
            re_ints = re.findall(r'\d+', s)
            for i in re_ints:
                try:
                    s = re.sub(i, str(Roman(i)), s)
                except OverflowError:
                    s = re.sub(i, "OverflowError", s)
            return s
    else:
        try:
            return Roman(int_list)
        except TypeError:
            raise TypeError(f"{type(int_list)} is not supported by Romanise.")


class Range:
    def __init__(self, *args):
        args = Romanise(args)
        if len(args) > 3:
            raise TypeError(f"Range expected at most 3 arguments, got {len(args)}")
        if len(args) < 1:
            raise TypeError(f"Range expected at least 1 argument, got {len(args)}")
        if len(args) == 1:
            self.stop = args
            self.start, self.step = Romanise((1, 1))
        if len(args) == 2:
            self.start, self.stop = args
            self.step = Romanise(1)
        if len(args) == 3:
            self.start, self.stop, self.step = args

        self.__range = range(self.start, self.stop, self.step)

    def __repr__(self):
        return f"Range{(self.start, self.stop, self.step) if self.step != 1 else (self.start, self.stop)}"

    def __eq__(self, other):
        return other == self.__range

    def __contains__(self, other):
        return self.__range(other)

    def __hash__(self):
        return hash(self.__range)

    def __iter__(self):
        return Range_iterator(self.__range)


class Range_iterator:
    def __init__(self, R):
        """This is only built for Range object"""
        self.Range_iterator = R.__iter__()

    def __next__(self):
        return Romanise(next(self.Range_iterator))
