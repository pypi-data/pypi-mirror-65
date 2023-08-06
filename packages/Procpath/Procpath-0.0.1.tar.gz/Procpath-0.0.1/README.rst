********
Procpath
********
Procpath is a process tree analysis workbench.

.. sourcecode::

    $ procpath query --help
    usage: procpath query [-h] [-f FILE_LIST] [-d DELIMITER] [-i INDENT] [query]

    positional arguments:
      query                 JSONPath expression, for example this query returns
                            PIDs for process subtree including the given root's:
                            $..children[?(@.stat.pid == 2610)]..pid

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE_LIST, --file-list FILE_LIST
                            PID proc files to read. By default: stat,cmdline.
                            Available: stat,cmdline,io.
      -d DELIMITER, --delimiter DELIMITER
                            Join query result using given delimiter
      -i INDENT, --indent INDENT
                            Format result JSON using given indent number

.. sourcecode::

    $ procpath record --help
    usage: procpath record [-h] [-f FILE_LIST] [-e ENVIRONMENT] [-i INTERVAL]
                           [-r RECNUM] [-v REEVALNUM] -d DATABASE_FILE
                           [query]

    positional arguments:
      query                 JSONPath expression, for example this query returns a
                            node including its subtree for given PID:
                            $..children[?(@.stat.pid == 2610)]

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE_LIST, --file-list FILE_LIST
                            PID proc files to read. By default: stat,cmdline.
                            Available: stat,cmdline,io.
      -e ENVIRONMENT, --environment ENVIRONMENT
                            Commands to evaluate in the shell and template the
                            query, like VAR=date
      -i INTERVAL, --interval INTERVAL
                            Interval in second between each recording, 10 by
                            default.
      -r RECNUM, --recnum RECNUM
                            Number of recordings to take at --interval seconds
                            apart. If not specified, recordings will be taken
                            indefinitely.
      -v REEVALNUM, --reevalnum REEVALNUM
                            Number of recordings after which environment must be
                            re-evaluate. It's useful when you expect it to change
                            in while recordings are taken.
      -d DATABASE_FILE, --database-file DATABASE_FILE
                            Path to the recording database file