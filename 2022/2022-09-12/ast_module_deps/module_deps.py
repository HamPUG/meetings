import argparse
import ast
from ast import Import, ImportFrom
import os
import re
import traceback


BLACKLISTED_DIRS = ["__pycache__", "venv"]


def module_name(root_dir, src_file):
    """
    Generates a module name from the source file relative to the root dir.

    :param root_dir: the root dir to use
    :type root_dir: str
    :param src_file: the source file to create the module name for
    :type src_file: str
    :return: the module name
    :rtype: str
    """
    result = src_file.replace(".py", "").replace(root_dir, "")
    result = result.replace("/", ".").replace("\\", ".")
    if result.startswith("."):
        result = result[1:]
    if result.endswith(".__init__"):
        result = result.replace(".__init__", "")

    return result


def add_dep(deps, module, dependent_module, include=None, exclude=None):
    """
    Adds the dependency relationship.

    :param deps: the dictionary of modules and modules that reference it (set)
    :type deps: dict
    :param module: the module that got referenced
    :type module: str
    :param dependent_module: the module that references it
    :type dependent_module: str
    :param include: the regexp for module names to include, includes all if None
    :type include: str
    :param exclude: the regexp for module names to exclude, excludes none if None
    :type exclude: str
    """
    if module not in deps:
        deps[module] = set()
    if include is not None:
        if re.match(include, module) is None:
            return
        if re.match(include, dependent_module) is None:
            return
    if exclude is not None:
        if re.match(exclude, module) is not None:
            return
        if re.match(exclude, dependent_module) is not None:
            return
    deps[module].add(dependent_module)


def analyze_file(root_dir, src_file, deps, include=None, exclude=None, verbose=False):
    """
    Analyzes the specified source file.

    :param root_dir: the root directory to analyze (to determine module names)
    :type root_dir: str
    :param src_file: the python file to analyze
    :type src_file: str
    :param deps: the dictionary of modules and modules that reference it (set)
    :type deps: dict
    :param include: the regexp for module names to include, includes all if None
    :type include: str
    :param exclude: the regexp for module names to exclude, excludes none if None
    :type exclude: str
    :param verbose: whether to output debugging information
    :type verbose: bool
    """
    if verbose:
        print("Parsing: %s" % src_file)
    with open(src_file, "r") as fp:
        lines = fp.readlines()

    module = module_name(root_dir, src_file)
    tree = ast.parse("".join(lines))
    for i in tree.body:
        if isinstance(i, Import):
            for name in i.names:
                add_dep(deps, name.name, module, include=include, exclude=exclude)
        elif isinstance(i, ImportFrom):
            add_dep(deps, i.module, module, include=include, exclude=exclude)


def analyze_dir(root_dir, src_dir, deps, include=None, exclude=None, verbose=False):
    """
    Analyzes the specified directory.

    :param root_dir: the root directory to analyze (to determine module names)
    :type root_dir: str
    :param src_dir: the directory to analyze
    :type src_dir: str
    :param deps: the dictionary of modules and modules that reference it (set)
    :type deps: dict
    :param include: the regexp for module names to include, includes all if None
    :type include: str
    :param exclude: the regexp for module names to exclude, excludes none if None
    :type exclude: str
    :param verbose: whether to output debugging information
    :type verbose: bool
    """
    if verbose:
        print("Analyzing: %s" % src_dir)

    for f in os.listdir(src_dir):
        path = os.path.join(src_dir, f)
        if os.path.isdir(path):
            if f in BLACKLISTED_DIRS:
                continue
            analyze_dir(root_dir, path, deps, include=include, exclude=exclude, verbose=verbose)
        elif f.endswith(".py"):
            analyze_file(root_dir, path, deps, include=include, exclude=exclude, verbose=verbose)


def generate(src_dir, output, include=None, exclude=None, verbose=False):
    """
    Generates the module dependencies for the specified source directory and outputs them
    in the specified dot graph file.

    :param src_dir: the directory with the code to analyze
    :type src_dir: str
    :param output: the file to store the dot graph in
    :type output: str
    :param include: the regexp for module names to include, includes all if None
    :type include: str
    :param exclude: the regexp for module names to exclude, excludes none if None
    :type exclude: str
    :param verbose: whether to output debugging information
    :type verbose: bool
    """
    if verbose:
        print("Starting...")

    deps = dict()
    analyze_dir(src_dir, src_dir, deps, include=include, exclude=exclude, verbose=verbose)

    if len(deps) == 0:
        print("No dependencies determined, skipping graph generation!")
        return

    if verbose:
        print("Generating graph...")
    graph = "digraph {\n"
    for module in deps:
        dep_modules = deps[module]
        for dep_module in dep_modules:
            graph += "  \"%s\" -> \"%s\";\n" % (dep_module, module)
    graph += "}\n"

    if verbose:
        print("Writing graph to: %s" % output)
    with open(output, "w") as fp:
        fp.write(graph)

    if verbose:
        print("Finished!")


def main(args=None):
    """
    Uses either the provided command-line arguments or the system ones
    to generate the statistics.

    :param args: the arguments to use instead of system ones
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description='Generates a module dependency from a source code tree in dot notation.')
    parser.add_argument("-s", "--src_dir", metavar="DIR", required=True, help="the source code tree to analyze.")
    parser.add_argument("-o", "--output", metavar="FILE", required=True, help="the dot graph file to store the dependencies in.")
    parser.add_argument("-i", "--include", metavar="REGEXP", required=False, help="the regexp for module names to include.")
    parser.add_argument("-e", "--exclude", metavar="REGEXP", required=False, help="the regexp for module names to exclude.")
    parser.add_argument("-v", "--verbose", action="store_true", help="whether to output some debugging information.")
    parsed = parser.parse_args(args=args)
    generate(parsed.src_dir, parsed.output, include=parsed.include, exclude=parsed.exclude, verbose=parsed.verbose)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.
    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
