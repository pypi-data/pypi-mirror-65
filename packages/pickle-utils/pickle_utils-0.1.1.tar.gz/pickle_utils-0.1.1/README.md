*NOTE:* You should use `pandas.read_pickle` and `pandas.to_pickle` instead for
`load` and `dump`.

# Available functions:

Use `help(pickle_utils)` in an interactive session for slightly more detailed
docs.

## `load(filename_or_object)`
Load a Pickle file, from a file name or a file-like object. If the argument is a
file name, it must end in ".pkl" or ".pkl.gz". In the second case the file will
be compressed.

Use `pandas.read_pickle` instead.

## `dump(data, filename_or_object)`
Same as before but dump data to disk.

Use `pandas.to_pickle` instead.

## `@memoize(filename, log_level=info)`
Decorator to memoize the output of a function to `filename` with pickle. The
function will be executed only if `filename` does not exist.

