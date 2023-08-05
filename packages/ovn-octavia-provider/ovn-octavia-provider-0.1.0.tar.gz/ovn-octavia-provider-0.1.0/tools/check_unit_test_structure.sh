#!/usr/bin/env bash

# This script identifies the unit test modules that do not correspond
# directly with a module in the code tree.  See TESTING.rst for the
# intended structure.

repo_path=$(cd "$(dirname "$0")/.." && pwd)
base_test_path=ovn_octavia_provider/tests/unit
test_path=$repo_path/$base_test_path

test_files=$(find ${test_path} -iname 'test_*.py')

ignore_regexes=(
    # Exceptional cases that should be skipped can be added here
    # EXAMPLE: "^objects/test_objects.py$"
)

error_count=0
ignore_count=0
total_count=0
for test_file in ${test_files[@]}; do
    relative_path=${test_file#$test_path/}
    expected_path=$(dirname $repo_path/ovn_octavia_provider/$relative_path)
    test_filename=$(basename "$test_file")
    expected_filename=${test_filename#test_}
    # Module filename (e.g. foo/bar.py -> foo/test_bar.py)
    filename=$expected_path/$expected_filename
    # Package dir (e.g. foo/ -> test_foo.py)
    package_dir=${filename%.py}
    if [ ! -f "$filename" ] && [ ! -d "$package_dir" ]; then
        for ignore_regex in ${ignore_regexes[@]}; do
            if [[ "$relative_path" =~ $ignore_regex ]]; then
                ignore_count=$((ignore_count + 1))
                continue 2
            fi
        done
        echo "Unexpected test file: $base_test_path/$relative_path"
        error_count=$((error_count + 1))
    fi
    total_count=$((total_count + 1))
done

if [ "$ignore_count" -ne 0 ]; then
    echo "$ignore_count unmatched test modules were ignored"
fi

if [ "$error_count" -eq 0 ]; then
    echo 'Success!  All test modules match targets in the code tree.'
    exit 0
else
    echo "Failure! $error_count of $total_count test modules do not match targets in the code tree."
    exit 1
fi
