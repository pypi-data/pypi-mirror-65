#!/usr/bin/env python
#
# exporting_tsv.py - Export data to a TSV file.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides the :func:`exportTSV` and :func:`exportCSV` functions,
which export the data contained in a :class:`.DataTable` to a TSV or CSV file.
"""


import functools as ft
import os.path   as op
import              os
import              logging

import numpy as np

from . import util
from . import custom


log = logging.getLogger(__name__)


NUM_ROWS = 10000
"""Default number of rows to export at a time by :func:`exportTSV` - the
default value for its ``numRows`` argument.
"""


@custom.exporter('csv')
def exportCSV(dtable, outfile, **kwargs):
    """Export data to a CSV-style file.

    This function is identical to the :func:`exportTSV`, except that the
    default value for the `sep`` argument is a ``','`` instead of a ``'\t'``.
    """

    sep = kwargs.pop('sep', None)
    if sep is None:
        sep = ','

    exportTSV(dtable, outfile, sep=sep, **kwargs)


@custom.exporter('tsv')
def exportTSV(dtable,
              outfile,
              sep=None,
              missingValues=None,
              numRows=None,
              **kwargs):
    """Export data to a TSV-style file.

    This may be parallelised by row - chunks of ``numRows`` rows will be
    saved to separate temporary output files in parallel, and then concatenated
    afterwards to produce the final output file.

    :arg dtable:         :class:`.DataTable` containing the data

    :arg outfile:        File to output to

    :arg sep:            Separator character to use. Defaults to ``'\\t'``

    :arg missingValues:  String to use for missing/NA values. Defaults to the
                         empty string.

    :arg numRows:        Number of rows to write at a time. Defaults to
                         :attr:`NUM_ROWS`.
    """

    if sep           is None: sep           = '\t'
    if missingValues is None: missingValues = ''
    if numRows       is None: numRows       = NUM_ROWS

    # We're going to output each chunk of
    # subjects to a separate file (in
    # parallel), and then cat the files
    # together afterwards
    index      = dtable.index
    nchunks    = int(np.ceil(len(index) / numRows))
    idxchunks  = [index[i:i + numRows] for i in
                  range(0, len(index), numRows)]
    subtables  = [dtable.subtable(rows=c) for c in idxchunks]
    outfiles   = ['{}_{}'.format(outfile, i) for i in range(nchunks)]

    # write each chunk in parallel
    args = zip(subtables,
               outfiles,
               [True] + [False] * (nchunks - 1),
               range(nchunks))
    func = ft.partial(writeDataFrame,
                      sep=sep,
                      missingValues=missingValues)

    with dtable.pool() as pool:
        pool.starmap(func, args)

    # concatenate the chunks to
    # form the final output file
    if len(outfiles) == 1:
        os.rename(outfiles[0], outfile)
    else:
        util.cat(outfiles, outfile)

    # remove intermediate files
    for f in outfiles:
        if f is not None and op.exists(f):
            os.remove(f)


def writeDataFrame(dtable,
                   outfile,
                   header,
                   chunki,
                   sep,
                   missingValues):
    """Writes all of the data in ``dtable`` to ``outfile``.

    Called by :func:`exportTSV` to output one chunk of data.

    :arg dtable:         :class:`.DataTable` containing the data

    :arg outfile:        File to output to

    :arg header:         If ``True``, write the header row (column names).

    :arg chunki:         Chunk index (used for logging)

    :arg sep:            Separator character to use.

    :arg missingValues:  String to use for missing/NA values.
    """

    columns = dtable.dataColumns
    towrite = dtable[:, :]

    log.info('Writing %u columns and %u rows [chunk %u] to %s ...',
             len(columns), len(dtable), chunki, outfile)

    if header: idcol = towrite.index.name
    else:      idcol = None

    towrite.to_csv(outfile,
                   sep=sep,
                   na_rep=missingValues,
                   header=header,
                   index_label=idcol)
