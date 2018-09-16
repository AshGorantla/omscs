import sys
from collections import OrderedDict
import re


r = re.compile('([a-zA-z]+)([0-9\-]+)')


def split_line(line):
    [node, vector_str] = line.split(':')
    return node, vector_str.split(',')


def parse_entry(entry):
    m = r.match(entry)
    return m.group(1), int(m.group(2))


def read_file(file):
    results = OrderedDict()
    with open(file, 'r') as f:
        lines = f.read()
        iterations = lines.split('-----\n')
        if '' in iterations:
            iterations.remove('')
        final_iteration = iterations[-1]
        for line in final_iteration.split('\n'):
            if line != '':
                print(line)
                (node, vector_entries) = split_line(line)
                results[node] = dict(parse_entry(entry) for entry in vector_entries)

    return results


def compare(actual, expected):
    errors = []

    if list(actual.keys()) != list(expected.keys()):
        errors.append('List of nodes did not match or were not in the expected order, expected %s but got %s' %
                      (','.join(actual.keys()), ','.join(expected.keys())))
        return errors

    for node, expected_vector in expected.iteritems():
        actual_vector = actual[node]
        unexpected_keys = set(actual_vector.keys()).difference(set(expected_vector.keys()))
        if len(unexpected_keys) > 0:
            errors.append('For node %s entries for the following nodes appeared unexpectedly in the distance vector: %s' %
                          (','.join(unexpected_keys), node))
        for vector_node, expected_distance in expected_vector.iteritems():
            actual_distance = actual_vector.get(vector_node)
            if actual_distance is None:
                errors.append('For node %s no distance was output for node %s, should have been %d' %
                              (node, vector_node, expected_distance))
            elif expected_distance != actual_distance:
                errors.append('For node %s the distance for node %s was %d but should have been %d' %
                              (node, vector_node, actual_distance, expected_distance))

    return errors


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Syntax:"
        print "    python check_output.py <log_file> <expected_final_output_file>"
        exit(1)

    log_file = sys.argv[1]
    expected_output_file = sys.argv[2]

    actual = read_file(log_file)
    expected = read_file(expected_output_file)
    errors = compare(actual, expected)
    if len(errors) > 0:
        print errors
        exit(1)
    else:
        print 'Output matches!'
