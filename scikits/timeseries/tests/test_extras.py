# pylint: disable-msg=W0611, W0612, W0511,R0201
"""Tests suite for MaskedArray.
Adapted from the original test_ma by Pierre Gerard-Marchant

:author: Pierre Gerard-Marchant & Matt Knox
:contact: pierregm_at_uga_dot_edu & mattknox_ca_at_hotmail_dot_com
:version: $Id: test_extras.py 3836 2008-01-15 13:09:03Z matthew.brett@gmail.com $
"""
__author__ = "Pierre GF Gerard-Marchant & Matt Knox ($Author: matthew.brett@gmail.com $)"
__revision__ = "$Revision: 3836 $"
__date__ = '$Date: 2008-01-15 08:09:03 -0500 (Tue, 15 Jan 2008) $'

import StringIO

import numpy as np
from numpy.testing import *
import numpy.ma as ma
from numpy.ma import masked
from numpy.ma.testutils import assert_equal, assert_almost_equal

from scikits.timeseries import Date, TimeSeries, date_array, time_series
import scikits.timeseries.const as _c
import scikits.timeseries.extras
from scikits.timeseries.extras import accept_atmost_missing, convert_to_annual, \
                                      count_missing, guess_freq, \
                                      isleapyear, tsfromtxt


#..............................................................................
class TestMisc(TestCase):
    "Base test class for MaskedArrays."

    def __init__(self, *args, **kwds):
        TestCase.__init__(self, *args, **kwds)


    def test_leapyear(self):
        leap = isleapyear([1900, 1901, 1902, 1903, 1904,
                           2000, 2001, 2002, 2003, 2004])
        assert_equal(leap, [0, 0, 0, 0, 1, 1, 0, 0, 0, 1])


    def test_convert_to_annual(self):
        "Test convert_to_annual"
        base = dict(D=1, H=24, T=24 * 60, S=24 * 3600)
        #for fq in ('D', 'H', 'T', 'S'):
        # Don't test for minuTe and Second frequency, too time consuming.
        for fq in ('D', 'H'):
            dates = date_array(start_date=Date(fq, '2001-01-01 00:00:00'),
                               end_date=Date(fq, '2004-12-31 23:59:59'))
            bq = base[fq]
            series = time_series(range(365 * bq) * 3 + range(366 * bq),
                                 dates=dates)
            control = ma.masked_all((4, 366 * bq), dtype=series.dtype)
            control[0, :58 * bq] = range(58 * bq)
            control[0, 59 * bq:] = range(58 * bq, 365 * bq)
            control[[1, 2]] = control[0]
            control[3] = range(366 * bq)
            test = convert_to_annual(series)
            assert_equal(test, control)
        #
        series = time_series(range(59, 365) + range(366) + range(365),
                             start_date=Date('D', '2003-03-01'))
        test = convert_to_annual(series)
        assert_equal(test[:, 59:62],
                     ma.masked_values([[-1, 59, 60], [59, 60, 61], [-1, 59, 60]],
                                      - 1))


    def test_guessfreq(self):
        "Test the guessing of frequency."

        dates = [
            (_c.FR_MIN,
             ['2001-01-01 00:00', '2001-01-01 00:30', '2001-01-01 01:00']),
            (_c.FR_MIN,
             ['2001-01-01 00:00', '2001-01-01 01:30', '2001-01-01 03:00']),
            (_c.FR_HR,
             ['2001-01-01 00:00', '2001-01-01 01:00', '2001-01-01 03:00']),
            (_c.FR_HR,
             ['2001-01-01 00:00', '2001-01-01 01:00', '2002-01-01 03:00']),
            (_c.FR_DAY,
             ['1959-01-01', '2009-07-31', '2009-08-01', '2009-08-02']),
            (_c.FR_BUS,
             ['2001-07-31', '2009-08-03', '2009-08-04']),
            (_c.FR_MTH,
             ['2001-01-01', '2001-02-01', '2002-03-01']),
            (_c.FR_MTH,
             ['2001-01-01', '2001-04-01', '2002-03-01']),
            (_c.FR_QTR,
             ['2004-01-01', '2004-04-01', '2005-01-01']),
            (_c.FR_WKTHU,
             ['2004-01-01', '2004-01-22', '2004-12-30']),
        ]

        for fr, dt in dates:
            assert_equal(guess_freq(dt), fr)

#..............................................................................
class TestCountmissing(TestCase):
    #
    def __init__(self, *args, **kwds):
        TestCase.__init__(self, *args, **kwds)
        data = time_series(np.arange(731),
                           start_date=Date(string='2003-01-01', freq='D'),
                           freq='D')
        self.data = data

    def test_count_missing(self):
        data = self.data
        assert_equal(count_missing(data), 0)
        assert_equal(count_missing(data.convert('A')), (0, 0))
        assert_equal(count_missing(data.convert('M')), [0] * 24)
        #
        series = data.copy()
        series[np.logical_not(data.day % 10)] = masked
        assert_equal(count_missing(series), 70)
        assert_equal(count_missing(series.convert('A')), (35, 35))
        assert_equal(count_missing(series.convert('M')),
                     [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] * 2)
        #
        series[series.day == 31] = masked
        assert_equal(count_missing(series), 84)
        assert_equal(count_missing(series.convert('A')), (42, 42))
        assert_equal(count_missing(series.convert('M')),
                     [4, 2, 4, 3, 4, 3, 4, 4, 3, 4, 3, 4] * 2)
    #
    def test_accept_atmost_missing(self):
        series = self.data.copy()
        series[np.logical_not(self.data.day % 10)] = masked
        result = accept_atmost_missing(series.convert('M'), 3, True)
        assert_equal(result._mask.all(-1), [0] * 24)
        result = accept_atmost_missing(series.convert('M'), 3, False)
        assert_equal(result._mask.all(-1), [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] * 2)
        result = accept_atmost_missing(series.convert('M'), 0.1, True)
        assert_equal(result._mask.all(-1), [0] * 24)
        result = accept_atmost_missing(series.convert('A'), 35, True)
        assert_equal(result._mask.all(-1), [0, 0])
        result = accept_atmost_missing(series.convert('A'), 35, False)
        assert_equal(result._mask.all(-1), [1, 1])
        result = accept_atmost_missing(series.convert('A'), 0.05, True)
        assert_equal(result._mask.all(-1), [1, 1])



class TestFromTxt(TestCase):
    "Test tsfromtxt"

    def test_nodateinfo(self):
        # No dates column specified: crash.
        "Test no date info"
        fcontent = StringIO.StringIO("""#
'Dates', 'One (S)','Two (I)','Three (F)','Four (M)','Five (-)','Six (C)'
'2007-01', 'strings',1,1.0,'mixed column',,1
'2007-02', 'with embedded "double quotes"',2,2.0,1.0,,1
'2007-03', 'strings',3,3.0E5,3,,1
'2007-05','strings',4,-1e-10,,,1
""")
        try:
            test = tsfromtxt(fcontent, delimiter=",", names="A,B,C,D,E,F,G")
        except TypeError:
            pass


    def test_with_names(self):
        "Tests w/ names"
        fcontent = StringIO.StringIO("""#
'Dates', 'One (S)','Two (I)','Three (F)','Four (M)','Five (-)','Six (C)'
'2007-01', 'strings',1,1.0,'mixed column',,1
'2007-02', 'with embedded "double quotes"',2,2.0,1.0,,1
'2007-03', 'strings',3,3.0E5,3,,1
'2007-05','strings',4,-1e-10,,,1
""")
        test = tsfromtxt(fcontent, delimiter=",", datecols=0, skip_header=2,
                         names="A,B,C,D,E,F", freq='M')
        assert(isinstance(test, TimeSeries))
        dlist = ['2007-%02i' % i for i in (1, 2, 3, 5)]
        assert_equal(test.dates.tovalue(),
                     date_array(dlist, freq='M').tovalue())
        assert_equal(test.dtype.names, ['A', 'B', 'C', 'D', 'E', 'F'])
        assert_equal(test['F'], [1, 1, 1, 1])
        assert_equal(test['E'].mask, [1, 1, 1, 1])
        assert_equal(test['C'], [1, 2, 300000, -1e-10])


    def test_without_names(self):
        "Test w/o names"
        fcontent = StringIO.StringIO("""#
'Dates', 'One (S)','Two (I)','Three (F)','Four (M)','Five (-)','Six (C)'
'2007-01', 'strings',1,1.0,'mixed column',,1
'2007-02', 'with embedded "double quotes"',2,2.0,1.0,,1
'2007-03', 'strings',3,3.0E5,3,,1
'2007-05','strings',4,-1e-10,,,1
""")
        test = tsfromtxt(fcontent, delimiter=",", skip_header=1, names=True,
                         freq='M')
        assert(isinstance(test, TimeSeries))
        dlist = ['2007-%02i' % i for i in (1, 2, 3, 5)]
        assert_equal(test.dates.tovalue(),
                     date_array(dlist, freq='M').tovalue())
        assert_equal(test.dtype.names,
                     ['One_S', 'Two_I', 'Three_F', 'Four_M', 'Five_', 'Six_C'])
        assert_equal(test['Six_C'], [1, 1, 1, 1])
        assert_equal(test['Five_'].mask, [1, 1, 1, 1])
        assert_equal(test['Three_F'], [1, 2, 300000, -1e-10])


    def test_with_datecols(self):
        "Test two datecols"
        fcontent = StringIO.StringIO("""
year, month, A, B
2009, 01, 1, 1.
2009, 03, 3, 3.
""")
        dateconv = lambda y, m: Date("M", year=int(y), month=int(m))
        test = tsfromtxt(fcontent, delimiter=",", skip_header=1, names=True,
                         converters={'dates': dateconv}, datecols=(0, 1))
        dates = date_array(['2009-01', '2009-03'], freq='M')
        assert_equal(test.dates.tovalue(), dates)
        assert_equal(test['A'], [1, 3])
        assert_equal(test['B'], [1., 3.])
        assert_equal(test.dtype, np.dtype([('A', int), ('B', float)]))

    def test_with_negative_datecols(self):
        "Test negative datecols"
        data = "380.00, 386.30, 200510\n386.85, 388.55, 200511\n"
        dconverter = lambda x: Date("M", "%s-%s" % (x[:4], x[4:6]))
        kwargs = dict(delimiter=",", datecols= -1, dateconverter=dconverter)
        ctrl = time_series([(380., 386.30), (386.85, 388.55)],
                           start_date="2005-10", freq="M",
                           dtype=[('open', "f4"), ('close', "f4")])
        test = tsfromtxt(StringIO.StringIO(data),
                         dtype=[('open', "f4"), ('close', "f4")],
                         **kwargs)
        assert_equal(test, ctrl)

    def test_unsorted_input(self):
        "Test tsfromtxt when the dates of the input are not sorted."
        datatxt = """dates,a,b
                    2007-04-02 01:00,,0.
                    2007-04-02 02:00,2.,20
                    2007-04-02 03:00,,
                    2007-04-02 00:00,0.,10.
                    2007-04-02 03:00,3.,30
                    2007-04-02 01:00,1.,10
                    2007-04-02 02:00,,
                    """
        data = StringIO.StringIO(datatxt)
        dates = [Date('H', '2007-04-02 0%i:00' % hour)
                 for hour in (1, 2, 3, 0, 1, 2)]
        controla = ma.masked_values([ 0, -1, 1, 2, -1, -1, 3], -1)
        controlb = ma.masked_values([10, 0, 10, 20, -1, -1, 30], -1)
        #
        data = StringIO.StringIO(datatxt)
        test = tsfromtxt(data, delimiter=',', names=True, freq='H')
        assert_equal(test.dtype.names, ['a', 'b'])
        assert_equal(test['a'], controla)
        assert_equal(test['a'].mask, controla.mask)
        assert_equal(test['b'], controlb)
        assert_equal(test['b'].mask, controlb.mask)


    def test_dates_on_several_columns(self):
        "Test tsfromtxt when the date spans several columns."
        datatxt = """
        2001, 01, 0.0, 10.
        2001, 02, 1.1, 11.
        2001, 02, 2.2, 12.
        """
        data = StringIO.StringIO(datatxt)
        dateconverter = lambda y, m: Date('M', year=int(y), month=int(m))
        test = tsfromtxt(data, delimiter=',', dtype=float, datecols=(0, 1),
                         dateconverter=dateconverter)
        assert_equal(test, [[0., 10.], [1.1, 11.], [2.2, 12.]])
        assert_equal(test.dates,
                     date_array(['2001-01', '2001-02', '2001-02'], freq='M'))


    def test_explicit_dtype(self):
        "Test tsfromtxt with an explicit dtype."
        dstr = "2009-01-14 12:00; 23; 46"
        test = tsfromtxt(StringIO.StringIO(dstr,),
                         delimiter=";", datecols=0, freq='H')
        self.failUnless(test.dtype.names is not None)
        assert_equal(test['f1'], 23)
        assert_equal(test['f2'], 46)
        #
        dstr = "2009-01-14 12:00; 23; 46"
        test = tsfromtxt(StringIO.StringIO(dstr,),
                         delimiter=";", datecols=0, dtype=int, freq='H')
        assert(test.dtype.names is None)
        assert_equal(test, [[23, 46]])

    def test_explicit_dtype_with_explicit_float(self):
        "Test w/ explicit dtype (and explicit float)"
        data = "200510, 380.00, 386.30\n200511, 386.85, 388.55\n"
        dconverter = lambda x: Date("M", "%s-%s" % (x[:4], x[4:6]))
        kwargs = dict(delimiter=",", datecols=0, dateconverter=dconverter)
        ctrl = time_series([(380., 386.30), (386.85, 388.55)],
                           start_date="2005-10", freq="M",
                           dtype=[('open', "f4"), ('close', "f4")])
        test = tsfromtxt(StringIO.StringIO(data),
                         dtype=[('open', "f4"), ('close', "f4")],
                         **kwargs)
        assert_equal(test, ctrl)


    def test_explicit_structured_dtype(self):
        "Test tsfromtxt with an explicit structured dtype"
        data = StringIO.StringIO("2007,12,31,24,34,56,0")
        dateconverter = lambda y, m, d: Date('D', year=int(y), month=int(m),
                                             day=int(d))
        ndtype = [('tobs', int), ('tmin', float), ('tmax', float),
                  ('rain', float)]
        test = tsfromtxt(data, delimiter=",", dtype=ndtype,
                         datecols=(0, 1, 2), dateconverter=dateconverter)
        control = time_series([(24, 34.0, 56.0, 0.0)],
                              dtype=ndtype,
                              start_date=Date('D', '2007-12-01'))
        assert_equal(test, control)
        #
        data = StringIO.StringIO("2007,12,31,24,34,56,0")
        ndtype = [('tobs', int), ('tmin', int), ('tmax', int),
                  ('rain', complex)]
        test = tsfromtxt(data, delimiter=",", dtype=ndtype,
                         datecols=(0, 1, 2), dateconverter=dateconverter)
        control = time_series([(24, 34.0, 56.0, 0.0)],
                              dtype=ndtype,
                              start_date=Date('D', '2007-12-01'))
        assert_equal(test, control)

    def test_explicit_names(self):
        "Test w/ explicit dtype (and explicit float)"
        data = "200510, 380.00, 386.30\n200511, 386.85, 388.55\n"
        dconverter = lambda x: Date("M", "%s-%s" % (x[:4], x[4:6]))
        kwargs = dict(delimiter=",", datecols=0, dateconverter=dconverter)
        ctrl = time_series([(380., 386.30), (386.85, 388.55)],
                           start_date="2005-10", freq="M",
                           dtype=[('open', "f4"), ('close', "f4")])
        test = tsfromtxt(StringIO.StringIO(data),
                         dtype=[('open', "f4"), ('close', "f4")],
                         **kwargs)
        assert_equal(test, ctrl)

    def test_explicit_names_with_usecols(self):
        "Make sure the proper names are given to entries when usecols is not None"
        a = "AAA,2010,1,1,2,3\nBBB,2010,2,10,20,30"
        dateconv = lambda y, m: Date('M', year=int(y), month=int(m))
        kwargs = dict(freq='M', delimiter=',', dateconverter=dateconv,
                      datecols=(1, 2), usecols=(1, 2, 3, 5), names="A, C")
        test = tsfromtxt(StringIO.StringIO(a), **kwargs)
        ctrl = time_series([(1, 3), (10, 30)],
                           start_date=Date('M', '2010-01'),
                           dtype=[('A', int), ('C', int)])
        assert_equal(test, ctrl)


    def test_with_converter(self):
        "Test tsfromtxt w/ an explicit converter"
        input = StringIO.StringIO("2001-01, 00mm\n2002-01, 10mm\n2003-01, 00mm")
        conv = converter = {1: lambda s:float(s.split('mm')[0])}
        test = tsfromtxt(input, delimiter=',', converters=conv, datecols=0,
                         freq='M', dtype=float)
        control = time_series([0., 10., 0.],
                              dates=['2001-01', '2002-01', '2003-01'],
                              freq='M')
        assert(isinstance(test, TimeSeries))
        assert_equal(test, control)
        assert_equal(test.dates, control.dates)


    def test_missing_values_no_names(self):
        "Make sure that floating point missing values are kept if no names"
        a = "AAA,2010,1,-9\nBBB,2010,2,2"
        dateconv = lambda y, m: Date('M', year=int(y), month=int(m))
        kwargs = dict(freq='M', delimiter=',', dateconverter=dateconv,
                      missing_values= -9,
                      datecols=(1, 2), usecols=(1, 2, 3), names="A")
        test = tsfromtxt(StringIO.StringIO(a), **kwargs)
        assert_equal(test.mask, np.array([(1,), (0,)], dtype=[('A', bool)]))




###############################################################################
#------------------------------------------------------------------------------
if __name__ == "__main__":
    run_module_suite()
