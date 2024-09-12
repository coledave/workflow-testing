#!/bin/bash

# container runs as root which is different to the overall action, as
# such we need to tell git we're okay with this.
git config --global --add safe.directory /github/workspace

matrix=$(/matrix-strategy-path.py "$1" "$2" 2>&1)
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "$matrix" >&2
    exit $exit_code
fi

echo "matrix=${matrix}" >> $GITHUB_OUTPUT
