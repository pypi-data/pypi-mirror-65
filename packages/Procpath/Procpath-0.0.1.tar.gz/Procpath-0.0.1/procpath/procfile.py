from typing import NamedTuple


__all__ = 'registry',


registry = {}


class Stat(NamedTuple):
    """
    Representation of ``/proc/[pid]/stat``, see ``man proc``.

    Fields are kept up until ``rss``. At the moment, later fields don't
    seem to be useful for the monitoring purposes.
    """

    pid: int
    """The process ID."""

    comm: str
    """
    The filename of the executable. This is visible whether or not the
    executable is swapped out.
    """

    state: str
    """
    One of the following characters, indicating process state:

        R  Running

        S  Sleeping in an interruptible wait

        D  Waiting in uninterruptible disk sleep

        Z  Zombie

        T  Stopped (on a signal) or (before Linux 2.6.33)
           trace stopped

        t  Tracing stop (Linux 2.6.33 onward)

        W  Paging (only before Linux 2.6.0)

        X  Dead (from Linux 2.6.0 onward)

        x  Dead (Linux 2.6.33 to 3.13 only)

        K  Wakekill (Linux 2.6.33 to 3.13 only)

        W  Waking (Linux 2.6.33 to 3.13 only)

        P  Parked (Linux 3.9 to 3.13 only)

    """

    ppid: int
    """The PID of the parent of this process."""

    pgrp: int
    """The process group ID of the process."""

    session: int
    """The session ID of the process."""

    tty_nr: int
    """
    The controlling terminal of the process. (The minor device number
    is contained in the combination of bits 31 to 20 and 7 to 0; the
    major device number is in bits 15 to 8.)
    """

    tpgid: int
    """
    The ID of the foreground process group of the controlling terminal
    of the process.
    """

    flags: int
    """
    The kernel flags word of the process.  For bit meanings, see the
    PF_* defines in the Linux kernel source file include/linux/sched.h.
    Details depend on the kernel version.

    The format for this field was %lu before Linux 2.6.
    """

    minflt: int
    """
    The number of minor faults the process has made
    which have not required loading a memory page from disk.
    """

    cminflt: int
    """
    The number of minor faults that the process's
    waited-for children have made.
    """

    majflt: int
    """
    The number of major faults the process has made
    which have required loading a memory page from disk.
    """

    cmajflt: int
    """
    The number of major faults that the process's
    waited-for children have made.
    """

    utime: int
    """
    Amount of time that this process has been scheduled
    in user mode, measured in clock ticks (divide by
    sysconf(_SC_CLK_TCK)).  This includes guest time,
    guest_time (time spent running a virtual CPU, see
    below), so that applications that are not aware of
    the guest time field do not lose that time from
    their calculations.
    """

    stime: int
    """
    Amount of time that this process has been scheduled
    in kernel mode, measured in clock ticks (divide by
    sysconf(_SC_CLK_TCK)).
    """

    cutime: int
    """
    Amount of time that this process's waited-for children have been
    scheduled in user mode, measured in clock ticks (divide by
    sysconf(_SC_CLK_TCK)). (See also times(2).)  This includes guest
    time, cguest_time (time spent running a virtual CPU, see below).
    """

    cstime: int
    """
    Amount of time that this process's waited-for children have been
    scheduled in kernel mode, measured in clock ticks (divide by
    sysconf(_SC_CLK_TCK)).
    """

    priority: int
    """
    (Explanation for Linux 2.6) For processes running a
    real-time scheduling policy (policy below; see
    sched_setscheduler(2)), this is the negated schedul‐
    ing priority, minus one; that is, a number in the
    range -2 to -100, corresponding to real-time priori‐
    ties 1 to 99.  For processes running under a non-
    real-time scheduling policy, this is the raw nice
    value (setpriority(2)) as represented in the kernel.
    The kernel stores nice values as numbers in the
    range 0 (high) to 39 (low), corresponding to the
    user-visible nice range of -20 to 19.

    Before Linux 2.6, this was a scaled value based on
    the scheduler weighting given to this process.
    """

    nice: int
    """
    The nice value (see setpriority(2)), a value in the
    range 19 (low priority) to -20 (high priority).
    """

    num_threads: int
    """
    Number of threads in this process (since Linux 2.6).
    Before kernel 2.6, this field was hard coded to 0 as
    a placeholder for an earlier removed field.
    """

    itrealvalue: int
    """
    The time in jiffies before the next SIGALRM is sent to the process
    due to an interval timer.  Since kernel 2.6.17, this field is no
    longer maintained, and is hard coded as 0.
    """

    starttime: int
    """
    The time the process started after system boot. In
    kernels before Linux 2.6, this value was expressed
    in jiffies.  Since Linux 2.6, the value is expressed
    in clock ticks (divide by sysconf(_SC_CLK_TCK)).

    The format for this field was %lu before Linux 2.6.
    """

    vsize: int
    """Virtual memory size in bytes."""

    rss: int
    """
    Resident Set Size: number of pages the process has
    in real memory.  This is just the pages which count
    toward text, data, or stack space.  This does not
    include pages which have not been demand-loaded in,
    or which are swapped out.
    """

    @classmethod
    def from_bytes(cls, b):
        pid, _, rest = b.partition(b' (')
        comm, _, rest = rest.rpartition(b') ')
        state, _, rest = rest.partition(b' ')

        fl = len(cls._fields) - 3
        fields = [int(pid), comm.decode(), state.decode()]
        fields.extend(map(int, rest.split(maxsplit=fl)[:fl]))
        return cls(*fields)

def read_stat(b, *, dictcls=dict, **kwargs):
    return dictcls(zip(Stat._fields, Stat.from_bytes(b)))

read_stat.schema = Stat
read_stat.empty = Stat(*[None] * len(Stat._fields))._asdict()
registry['stat'] = read_stat


def read_cmdline(b, **kwargs):
    return b.replace(b'\x00', b' ').strip().decode()

read_cmdline.schema = 'cmdline'
read_cmdline.empty = None
registry['cmdline'] = read_cmdline


class Io(NamedTuple):
    """
    Representation of ``/proc/[pid]/io``.

    See https://www.kernel.org/doc/Documentation/filesystems/proc.txt.
    """

    rchar: int
    """
    I/O counter: chars read.

    The number of bytes which this task has caused to be read from
    storage. This is simply the sum of bytes which this process passed
    to read() and pread(). It includes things like tty IO and it is
    unaffected by whether or not actual physical disk IO was required
    (the read might have been satisfied from pagecache).
    """

    wchar: int
    """
    I/O counter: chars written.

    The number of bytes which this task has caused, or shall cause to
    be written to disk. Similar caveats apply here as with rchar.
    """

    syscr: int
    """
    I/O counter: read syscalls.

    Attempt to count the number of read I/O operations, i.e. syscalls
    like read() and pread().
    """

    syscw: int
    """
    I/O counter: write syscalls.

    Attempt to count the number of write I/O operations, i.e. syscalls
    like write() and pwrite().
    """

    read_bytes: int
    """
    I/O counter: bytes read.

    Attempt to count the number of bytes which this process really did
    cause to be fetched from the storage layer. Done at the
    submit_bio() level, so it is accurate for block-backed filesystems.
    """

    write_bytes: int
    """
    I/O counter: bytes written.

    Attempt to count the number of bytes which this process caused to
    be sent to the storage layer. This is done at page-dirtying time.
    """

    cancelled_write_bytes: int
    """
    The big inaccuracy here is truncate. If a process writes 1MB to a
    file and then deletes the file, it will in fact perform no
    writeout. But it will have been accounted as having caused 1MB of
    write. In other words: The number of bytes which this process
    caused to not happen, by truncating pagecache. A task can cause
    "negative" IO too. If this task truncates some dirty pagecache,
    some IO which another task has been accounted for (in its
    write_bytes) will not be happening. We _could_ just subtract that
    from the truncating task's write_bytes, but there is information
    loss in doing that.
    """

    @classmethod
    def from_bytes(cls, b):
        pairs = [l.decode().split(': ', 1) for l in b.splitlines()]
        d = {k: int(v) for k, v in pairs if k in cls._field_set}
        return cls(**d)

Io._field_set = set(Io._fields)

def read_io(b, *, dictcls=dict, **kwargs):
    return dictcls(zip(Io._fields, Io.from_bytes(b)))

read_io.schema = Io
read_io.empty = Io(*[None] * len(Io._fields))._asdict()
registry['io'] = read_io
