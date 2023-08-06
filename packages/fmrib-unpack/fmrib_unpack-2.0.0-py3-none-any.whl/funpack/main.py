#!/usr/bin/env python
#
# main.py - funpack entry point
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the ``funpack`` entry point. """


import multiprocessing     as mp
import functools           as ft
import os.path             as op
import                        sys
import                        logging
import                        warnings
import                        datetime
import                        calendar

import pandas              as pd
import pandas.api.types    as pdtypes

import funpack
import funpack.util        as util
import funpack.icd10       as icd10
import funpack.config      as config
import funpack.custom      as custom
import funpack.dryrun      as dryrun
import funpack.cleaning    as cleaning
import funpack.importing   as importing
import funpack.exporting   as exporting
import funpack.hierarchy   as hierarchy
import funpack.processing  as processing
import funpack.loadtables  as loadtables


log = logging.getLogger(__name__)


def main(argv=None):
    """``funpack`` entry point. """

    # Make sure built in plugins are
    # registered, as they are queried
    # in the command-line help. Set
    # logging to critical until we've
    # parsed command-line args.
    logging.getLogger().setLevel(logging.CRITICAL)
    custom.registerBuiltIns()

    args, argv = config.parseArgsWithConfigFile(argv)
    date = datetime.date.today()

    # Now that args are passed,
    # we can set up logging properly.
    configLogging(args)

    log.info('funpack %s', funpack.__version__)
    log.info('Date: %s (%s)', date.today(), calendar.day_name[date.weekday()])
    log.info('Command-line arguments %s', ' '.join(argv))
    log.debug('Running with the following options')
    for name, val in args.__dict__.items():
        if val is not None:
            val = str(val)
            if len(val) <= 30: log.debug('  %s: %s',    name, val)
            else:              log.debug('  %s: %s...', name, val[:30])

    # Load any custom plugins
    # that have been specified.
    if args.plugin_file is not None:
        for p in args.plugin_file:
            custom.loadPluginFile(p)

    # default output format inferred
    # from output filename or, failing
    # that, tsv
    if args.format is None:
        fmt = op.splitext(args.outfile)[1].lower().strip('.')
        if fmt in ('h5', 'hdf'):
            fmt = 'hdf5'
        if not custom.exists('exporter', fmt):
            fmt = 'tsv'
        args.format = fmt

    # error if any loaders/formats are
    # invalid (we can only perform this
    # check after plugins have been
    # loaded)
    if args.loader is not None:
        for f, l in args.loader.items():
            if not custom.exists('loader', l):
                raise ValueError('Unknown loader {} [{}]'.format(l, f))
    if not custom.exists('exporter', args.format):
        raise ValueError('Unknown output format {}'.format(args.format))
    if args.date_format is not None and \
       not custom.exists('formatter', args.date_format):
        raise ValueError('Unknown date format {}'.format(args.date_format))
    if args.time_format is not None and \
       not custom.exists('formatter', args.time_format):
        raise ValueError('Unknown time format {}'.format(args.time_format))
    if args.var_format is not None:
        for v, f in args.var_format.items():
            if not custom.exists('formatter', f):
                raise ValueError('Unknown formatter {} [{}]'.format(f, v))

    if args.num_jobs > 1:
        log.debug('Running up to %i jobs in parallel', args.num_jobs)
        mgr = mp.Manager()

        # We need to initialise icd10
        # before the worker processes
        # are created, so its state is
        # shared by all processes.
        icd10.initialise(mgr)

        pool = mp.Pool(args.num_jobs)

    else:
        pool = None
        mgr  = None

    try:
        with util.timed(None, log, fmt='Total time: %s (%+iMB)'):

            dtable, unknowns, uncategorised, drop = doImport(args, pool, mgr)

            if args.dry_run:
                dryrun.doDryRun(dtable, unknowns, uncategorised, drop, args)
            else:
                doCleanAndProcess(  dtable, args)
                doFormat(           dtable, args)
                doUnknownsExport(   dtable, args, unknowns, uncategorised)
                doExport(           dtable, args)
                doICD10Export(              args)
                doDescriptionExport(dtable, args)
                doSummaryExport(    dtable, args)

    finally:
        # shutdown the pool gracefully
        if pool is not None:
            pool.close()
            pool.join()
            pool = None

    return 0


def doImport(args, pool, mgr):
    """Data import stage.

    :arg args: :class:`argparse.Namespace` object containing command line
               arguments
    :arg pool: :class:`multiprocessing.Pool` object for parallelisation (may
               be ``None``)
    :arg mgr:  :class:`multiprocessing.Manager` object for parallelisation (may
               be ``None``)

    :returns:  A tuple containing:

                - A :class:`.DataTable` containing the data
                - A sequence of :class:`.Column` objects representing the
                  unknown columns.
                - A sequence of :class:`.Column` objects representing columns
                  which are uncategorised, and have no processing or cleaning
                  rules specified on them.
                - A list of :class:`.Column` objects that were not loaded from
                  each input file.
    """

    with util.timed('Table import', log):
        vartable, proctable, cattable, unknowns, uncategorised = \
            loadtables.loadTables(
                args.infile,
                args.variable_file,
                args.datacoding_file,
                args.type_file,
                args.processing_file,
                args.category_file,
                noBuiltins=args.no_builtins,
                naValues=args.na_values,
                childValues=args.child_values,
                recoding=args.recoding,
                clean=args.clean,
                typeClean=args.type_clean,
                globalClean=args.global_clean,
                skipProcessing=args.skip_processing,
                prependProcess=args.prepend_process,
                appendProcess=args.append_process,
                sniffers=args.loader,
                indexes=args.index)

    subjects, exprs = args.subject
    variables       = args.variable
    categories      = args.category
    columns         = args.column

    # Import data
    with util.timed('Data import', log):
        dtable, drop = importing.importData(
            datafiles=args.infile,
            vartable=vartable,
            proctable=proctable,
            cattable=cattable,
            variables=variables,
            colnames=columns,
            categories=categories,
            subjects=subjects,
            subjectExprs=exprs,
            exclude=args.exclude,
            encoding=args.encoding,
            indexes=args.index,
            trustTypes=args.trust_types,
            mergeAxis=args.merge_axis,
            mergeStrategy=args.merge_strategy,
            indexVisits=args.index_visits,
            loaders=args.loader,
            pool=pool,
            mgr=mgr,
            dryrun=args.dry_run)

    # Filter unknown/uncategorised
    # column lists to only contain
    # those that were loaded
    allcols       = dtable.dataColumns
    unknowns      = [c for c in unknowns      if c in allcols]
    uncategorised = [c for c in uncategorised if c in allcols]

    # if it appears that we're doing
    # a full run on a large data set,
    # emit warnings about unknown/
    # uncategorised variables.
    bigrun = any((args.variable_file   is not None,
                  args.datacoding_file is not None,
                  args.processing_file is not None,
                  args.category_file   is not None))

    if bigrun:
        for u in unknowns:
            log.warning('Variable %s [file %s, column %s, assigned '
                        'variable ID %s] is unknown.',
                        u.name, u.datafile, u.index, u.vid)
        for u in uncategorised:
            log.warning('Variable %s [file %s, column %s, assigned '
                        'variable ID %s] is uncategorised and does not '
                        'have any cleaning or processing rules set.',
                        u.name, u.datafile, u.index, u.vid)

    return dtable, unknowns, uncategorised, drop


def doCleanAndProcess(dtable, args):
    """Data cleaning and processing stage.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    :arg pool:   :class:`multiprocessing.Pool` object for parallelisation (may
                 be ``None``)
    """

    # Clean data (it times each step individually)
    cleaning.cleanData(
        dtable,
        skipNAInsertion=args.skip_insertna,
        skipCleanFuncs=args.skip_clean_funcs,
        skipChildValues=args.skip_childvalues,
        skipRecoding=args.skip_recoding)

    # Process data
    with util.timed('Data processing', log):
        processing.processData(dtable)


def doFormat(dtable, args):
    """Data formatting stage. This is called just prior to :func:`doExport`.

    It applies any variable-specific formatting that has been specified, and
    also formats date/time columns.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    """

    vartable   = dtable.vartable
    dateFormat = args.date_format
    timeFormat = args.time_format
    formatters = args.var_format

    # We format columns in parallel - build
    # a list of arguments to pass to the
    # exporting.formatColumn function.
    fmtargs = []
    fmtfunc = ft.partial(exporting.formatColumn,
                         dateFormat=dateFormat,
                         timeFormat=timeFormat,
                         formatters=formatters)

    # We format all date/time columns, and
    # any for which a custom formatter or
    # a fill value has been provided.
    for col in dtable.dataColumns:

        vid    = col.vid
        name   = col.name
        series = dtable[:, name]

        if vid in vartable.index: vtype = vartable['Type'][vid]
        else:                     vtype = None

        if any((vid   in formatters,
                name  in formatters,
                vtype in (util.CTYPES.date, util.CTYPES.time),
                pdtypes.is_datetime64_any_dtype(series),
                col.fillval is not None)):
            fmtargs.append((col, dtable.subtable([col])))

    # Format each column in parallel - each
    # exporting.formatColumn call returns a
    # subtable that can then be merged back
    # in to the main table.
    with dtable.pool() as pool:
        results = pool.starmap(fmtfunc, fmtargs)

    for subtable in results:
        dtable.merge(subtable)


def doExport(dtable, args):
    """Data export stage.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    """

    # List of data tables and file names
    # for export (we may split the dtable
    # up into two)
    dtables = []

    # Suppress/separate out non-
    # numeric columns if requested
    if args.suppress_non_numerics or args.write_non_numerics:

        # identify numeric/non-
        # numeric columns
        ncols  = []
        nncols = []
        for col in dtable.dataColumns:
            series = dtable[:, col.name]
            if pdtypes.is_numeric_dtype(series): ncols .append(col)
            else:                                nncols.append(col)

        # if suppress, only numeric
        # columns are saved to main
        # output file
        if args.suppress_non_numerics:
            dtables.append((dtable.subtable(ncols), args.outfile))
        else:
            dtables.append((dtable, args.outfile))

        # if write, non-numeric columns
        # are saved to an auxillary file
        if args.write_non_numerics:
            dtables.append((dtable.subtable(nncols), args.non_numerics_file))

    # only one output file
    else:
        dtables.append((dtable, args.outfile))

    # If not parallelising, we export the
    # entire file in one go. Because what's
    # the point in chunked export if we're
    # not parallelising across chunks?
    if args.num_jobs <= 1:
        args.num_rows = len(dtable)

    with util.timed('Data export', log):
        for dtable, outfile in dtables:
            exporting.exportData(
                dtable,
                outfile,

                # General export options
                fileFormat=args.format,
                numRows=args.num_rows,

                # TSV options
                sep=args.tsv_sep,
                missingValues=args.tsv_missing_values,

                # HDF5 options
                key=args.hdf5_key,
                style=args.hdf5_style)


def doICD10Export(args):
    """If a ``--icd10_map_file`` has been specified, the ICD10 codes present
    in the data (and their converted values) are saved out to the file.
    """
    if args.icd10_map_file is None:
        return

    with util.timed('ICD10 mapping export', log):
        try:
            ihier = hierarchy.getHierarchyFilePath(name='icd10')
            ihier = hierarchy.loadHierarchyFile(ihier)
            icd10.saveCodes(args.icd10_map_file, ihier)

        except Exception as e:
            log.warning('Failed to export ICD10 mappings: {}'.format(e),
                        exc_info=True)


def doDescriptionExport(dtable, args):
    """If a ``--description_file`` has been specified, a description for every
    column is saved out to the file.
    """
    if args.description_file is None:
        return

    with util.timed('Description export', log):
        cols = dtable.dataColumns

        try:
            with open(args.description_file, 'wt') as f:
                for col in cols:
                    desc = generateDescription(dtable, col)
                    f.write('{}\t{}\n'.format(col.name, desc))

        except Exception as e:
            log.warning('Failed to export descriptions: {}'.format(e),
                        exc_info=True)


def generateDescription(dtable, col):
    """Called by :func:`doDescriptionExport`. Generates and returns a
    suitable description for the given column.

    :arg dtable: :class:`.Datatable` instance
    :arg col:    :class:`.Column` instance
    """
    vartable = dtable.vartable
    desc     = vartable.loc[col.vid, 'Description']

    if pd.isna(desc) or (desc == col.name):
        desc = 'n/a'

    # If metadata has been added to the column,
    # we add it to the description. See the
    # binariseCategorical processing function
    # for an example of this.
    if col.metadata is not None:
        suffix = ' ({})'.format(col.metadata)
    else:
        suffix = ' ({}.{})'.format(col.visit, col.instance)

    return '{}{}'.format(desc, suffix)


def doUnknownsExport(dtable, args, unknowns, uncategorised):
    """If the ``--unknown_vars_file`` argument was used, the unknown/
    unprocessed columns are saved out to a file.

    :arg dtable:        :class:`.DataTable` containing the data
    :arg args:          :class:`argparse.Namespace` object containing command
                        line arguments
    :arg unknowns:      List of :class:`.Column` objects representing the
                        unknown columns.
    :arg uncategorised: A sequence of :class:`.Column` objects representing
                        columns which are uncategorised, and have no processing
                        or cleaning rules specified on them.
    """

    if args.unknown_vars_file is None:
        return

    if len(unknowns) + len(uncategorised) == 0:
        return

    # Save unknown/uncategorised
    # vars list to file columns:
    #  - name      - column name
    #  - file      - originating input file
    #  - class     - unknown or uncategorised
    #  - exported  - whether column passed processing and was exported
    allcols     = list(dtable.dataColumns)
    allunknowns = list(unknowns + uncategorised)

    names       = [u.name            for u in allunknowns]
    files       = [u.datafile        for u in allunknowns]
    classes     = ['unknown'         for u in unknowns] + \
                  ['uncategorised'   for u in uncategorised]
    exported    = [int(u in allcols) for u in allunknowns]
    rows        = ['{}\t{}\t{}\t{}'.format(n, f, c, e)
                   for n, f, c, e in zip(names, files, classes, exported)]

    log.debug('Saving unknown/uncategorised variables to %s',
              args.unknown_vars_file)

    try:
        with open(args.unknown_vars_file, 'wt') as f:
            f.write('name\tfile\tclass\texported\n')
            f.write('\n'.join(rows))

    except Exception as e:
        log.warning('Error saving unknown variables to {}: '
                    '{}'.format(args.unknown_vars_file, e),
                    exc_info=True)


def doSummaryExport(dtable, args):
    """If a ``--summary_file`` has been specified, a summary of the cleaning
    steps that have been applied to each variable are saved out to the file.
    """
    if args.summary_file is None:
        return

    vartable = dtable.vartable
    vids     = sorted(dtable.variables)[1:]
    sumdf    = pd.DataFrame(columns=['ID', 'NAValues',
                                     'RawLevels', 'NewLevels',
                                     'ParentValues', 'ChildValues',
                                     'Clean', 'Flags']).set_index('ID')

    with util.timed('Summary export', log):
        for vid in vids:
            sumdf.at[vid, 'NAValues']     = vartable.at[vid, 'NAValues']
            sumdf.at[vid, 'RawLevels']    = vartable.at[vid, 'RawLevels']
            sumdf.at[vid, 'NewLevels']    = vartable.at[vid, 'NewLevels']
            sumdf.at[vid, 'ParentValues'] = vartable.at[vid, 'ParentValues']
            sumdf.at[vid, 'ChildValues']  = vartable.at[vid, 'ChildValues']

            clean = vartable.at[vid, 'Clean']
            if pd.notna(clean):
                sumdf.at[vid, 'Clean'] = list(clean.values())

            flagstr  = []
            cols     = dtable.columns(vid)
            colflags = {c : dtable.getFlags(c) for c in cols}
            flags    = set.union(*colflags.values())

            for flag in flags:
                if all([flag in colflags[c] for c in cols]):
                    flagstr.append(flag)
                else:
                    names = [c.name for c in cols if flag in colflags[c]]
                    flagstr.append('{} [{}]'.format(flag, ', '.join(names)))

            sumdf.at[vid, 'Flags'] = ';'.join(flagstr)

        sumdf.to_csv(args.summary_file, sep='\t')


def configLogging(args):
    """Configures ``funpack`` logging.

    :arg args: ``argparse.Namespace`` object containing parsed command line
               arguments.
    """

    # Custom log handler which
    # colours messages
    class LogHandler(logging.StreamHandler):

        def emit(self, record):

            levelno = record.levelno

            if   levelno >= logging.WARNING:  colour = '\x1b[31;1m'
            elif levelno >= logging.INFO:     colour = '\x1b[39;1m'
            elif levelno >= logging.DEBUG:    colour = '\x1b[90;1m'
            else:                             colour = ''

            # Reset terminal attributes
            # after each message.
            record.msg = '{}{}\x1b[0m'.format(colour, record.msg)

            return super(LogHandler, self).emit(record)

    logger = logging.getLogger('funpack')
    fmt    = logging.Formatter('%(asctime)s '
                               '%(levelname)8.8s '
                               '%(filename)20.20s '
                               '%(lineno)4d: '
                               '%(funcName)-15.15s - '
                               '%(message)s',
                               '%H:%M:%S')

    if args.log_file is None: handler = LogHandler()
    else:                     handler = logging.FileHandler(args.log_file)

    handler.setFormatter(fmt)
    logger.addHandler(handler)

    # configure verbosity
    if   args.quiet:      loglevel = logging.CRITICAL
    elif args.noisy == 0: loglevel = logging.INFO
    else:                 loglevel = logging.DEBUG

    logging.getLogger('funpack').setLevel(loglevel)

    if args.quiet or args.noisy < 3:
        warnings.filterwarnings('ignore',  module='pandas')
        warnings.filterwarnings('ignore',  module='numpy')
        warnings.filterwarnings('ignore',  module='tables')

    if args.noisy == 1:
        makequiet = ['funpack.expression',
                     'funpack.custom',
                     'funpack.cleaning_functions',
                     'funpack.processing_functions']
    elif args.noisy == 2:
        makequiet = ['funpack.expression',
                     'funpack.custom']
    else:
        makequiet = []

    for mod in makequiet:
        logging.getLogger(mod).setLevel(logging.INFO)


if __name__ == '__main__':
    sys.exit(main())
