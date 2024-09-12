#!/usr/bin/env python3

import argparse
import yaml
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Filter stacks based on changed files.")
    parser.add_argument("yaml_data", help="YAML string or path to a YAML file defining the matrix strategy.")
    parser.add_argument("changed_files_command", help="Command to fetch the list of changed files.")

    args = parser.parse_args()

    try:
        with open(args.yaml_data, "r") as f:
            yaml_data = f.read()
    except FileNotFoundError:
        yaml_data = args.yaml_data

    matrix_strategy = matrix_strategy_from_yaml(yaml_data)
    changed_files_list = changed_files(args.changed_files_command)
    matrix = generate_matrix(matrix_strategy, changed_files_list)

    print(matrix)


def changed_files(cmd: str) -> list[str]:
    """Execute the provided command and returns the list of changed files."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode("utf-8").splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr.decode('utf-8')}")
        sys.exit(1)


def matrix_strategy_from_yaml(data: str) -> dict[str, list[str]]:
    """Parse the YAML string into a matrix to match against."""
    try:
        return yaml.safe_load(data)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)


def generate_matrix(matrix_strategy: dict[str, list[str]], changed_files: list[str]) -> list[str]:
    """Filters the given matrix against each of the paths"""
    return [
        stack
        for stack, patterns in matrix_strategy.items()
        if any(pattern_match(pattern, changed_files) for pattern in patterns)
    ]


def pattern_match(pattern: str, changed_files: list[str]) -> bool:
    match pattern:
        case p if p.endswith("**"):
            return pattern_match_greedy(pattern, changed_files)
        case _:
            return pattern_match_exact(pattern, changed_files)


def pattern_match_exact(pattern: str, changed_files: list[str]) -> bool:
    return pattern in changed_files


def pattern_match_greedy(pattern: str, changed_files: list[str]) -> bool:
    return any(changed_file.startswith(pattern[:-2]) for changed_file in changed_files)


if __name__ == "__main__":
    main()
