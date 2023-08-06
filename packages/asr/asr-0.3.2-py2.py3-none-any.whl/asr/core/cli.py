from asr.core import read_json
import click
from pathlib import Path
import subprocess


def format(content, indent=0, title=None, pad=2):
    colwidth_c = []
    for row in content:
        if isinstance(row, str):
            continue
        for c, element in enumerate(row):
            nchar = len(element)
            try:
                colwidth_c[c] = max(colwidth_c[c], nchar)
            except IndexError:
                colwidth_c.append(nchar)

    output = ''
    if title:
        output = f'\n{title}\n'
    for row in content:
        out = ' ' * indent
        if isinstance(row, str):
            output += f'{row}'
            continue
        for colw, desc in zip(colwidth_c, row):
            out += f'{desc: <{colw}}' + ' ' * pad
        output += out
        output += '\n'

    return output


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    ...


@cli.command()
@click.option('-s', '--shell', is_flag=True,
              help='Interpret COMMAND as shell command.')
@click.option('-n', '--not-recipe', is_flag=True,
              help='COMMAND is not a recipe.')
@click.option('-z', '--dry-run', is_flag=True,
              help='Show what would happen without doing anything.')
@click.option('-j', '--jobs', type=int,
              help='Run COMMAND in serial on JOBS processes.')
@click.option('-S', '--skip-if-done', is_flag=True,
              help='Skip execution of recipe if done.')
@click.option('--dont-raise', is_flag=True, default=False,
              help='Continue to next folder when encountering error.')
@click.argument('command', nargs=1)
@click.argument('folders', nargs=-1)
@click.pass_context
def run(ctx, shell, not_recipe, dry_run, command, folders, jobs,
        skip_if_done, dont_raise):
    r"""Run recipe, python function or shell command in multiple folders.

    Can run an ASR recipe or a shell command. For example, the syntax
    "asr run recipe" will run the relax recipe in the current folder.

    To run a shell script use the syntax 'asr run --shell "echo Hello!"'.
    This example would run "echo Hello!" in the current folder.

    Provide extra arguments to the recipe using 'asr run "recipe --arg1
    --arg2"'.

    XXX NO Run a recipe in parallel using 'asr run -p NCORES "recipe --arg1"'.

    Run command in multiple folders using "asr run recipe folder1/ folder2/".
    This is also compatible with input arguments to the current command
    through 'asr run "recipe --arg1" folder1/ folder2/'.

    If you dont actually wan't to run the command, i.e., if it is a
    dangerous command, then use the "asr run --dry-run ..." syntax
    where ... could be any of the above commands. For example,
    'asr run --dry-run --shell "echo Hello!" \\*/' would run "echo Hello!"
    in all folders of the current directory.

    Examples
    --------
    Run the relax recipe
    >>> asr run relax

    Run the calculate function in the gs module
    >>> asr run gs@calculate

    Get help for a recipe
    >>> asr run "relax -h"

    Specify an argument
    >>> asr run "relax --ecut 600"

    Run a recipe in parallel with an argument
    >>> asr run -p 2 "relax --ecut 600"

    Run relax recipe in two folders sequentially
    >>> asr run relax folder1/ folder2/

    Run a shell command in this folder
    >>> asr run --shell "ase convert gs.gpw structure.json"

    Run a shell command in "folder1/"
    >>> asr run --shell "ase convert gs.gpw structure.json" folder1/

    Don't actually do anything just show what would be done
    >>> asr run --dry-run --shell "mv str1.json str2.json" folder1/ folder2/

    """
    import subprocess
    from ase.parallel import parprint
    from asr.core import chdir
    from functools import partial

    prt = partial(parprint, flush=True)

    if not folders:
        folders = ['.']
    else:
        prt(f'Number of folders: {len(folders)}')

    nfolders = len(folders)

    if jobs:
        assert jobs <= nfolders, 'Too many jobs and too few folders!'
        processes = []
        for job in range(jobs):
            cmd = 'python3 -m asr run'.split()
            myfolders = folders[job::jobs]
            if skip_if_done:
                cmd.append('--skip-if-done')
            if dont_raise:
                cmd.append('--dont-raise')
            if shell:
                cmd.append('--shell')
            if dry_run:
                cmd.append('--dry-run')
            cmd.append(command)
            cmd.extend(myfolders)
            process = subprocess.Popen(cmd)
            processes.append(process)

        for process in processes:
            returncode = process.wait()
            assert returncode == 0
        return

    # Identify function that should be executed
    if shell:
        command = command.strip()
        if dry_run:
            prt(f'Would run shell command "{command}" '
                f'in {nfolders} folders.')
            return

        for i, folder in enumerate(folders):
            with chdir(Path(folder)):
                prt(f'Running {command} in {folder} ({i + 1}/{nfolders})')
                subprocess.run(command.split())
        return

    # If not shell then we assume that the command is a call
    # to a python module or a recipe
    module, *args = command.split()
    function = None
    if '@' in module:
        module, function = module.split('@')

    if not_recipe:
        assert function, \
            ('If this is not a recipe you have to specify a '
             'specific function to execute.')
    else:
        if not module.startswith('asr.'):
            module = f'asr.{module}'

    import importlib
    mod = importlib.import_module(module)
    if not function:
        function = 'main'
    assert hasattr(mod, function), f'{module}@{function} doesn\'t exist'
    func = getattr(mod, function)

    from asr.core import ASRCommand
    if isinstance(func, ASRCommand):
        is_asr_command = True
    else:
        is_asr_command = False

    import sys
    if dry_run:
        prt(f'Would run {module}@{function} '
            f'in {nfolders} folders.')
        return

    for i, folder in enumerate(folders):
        with chdir(Path(folder)):
            try:
                if skip_if_done and func.done:
                    continue
                prt(f'In folder: {folder} ({i + 1}/{nfolders})')
                if is_asr_command:
                    func.cli(args=args)
                else:
                    sys.argv = [mod.__name__] + args
                    func()
            except click.Abort:
                break
            except Exception as e:
                if not dont_raise:
                    raise
                else:
                    prt(e)
            except SystemExit:
                print('Unexpected error:', sys.exc_info()[0])
                if not dont_raise:
                    raise


@cli.command(name='list')
@click.argument('search', required=False)
def asrlist(search):
    """List and search for recipes.

    If SEARCH is specified: list only recipes containing SEARCH in their
    description.
    """
    from asr.core import get_recipes
    recipes = get_recipes()
    recipes.sort(key=lambda x: x.name)
    panel = [['Name', 'Description'],
             ['----', '-----------']]

    for recipe in recipes:
        longhelp = recipe._main.__doc__
        if not longhelp:
            longhelp = ''

        shorthelp, *_ = longhelp.split('\n')

        if search and (search not in longhelp
                       and search not in recipe.name):
            continue
        status = [recipe.name[4:], shorthelp]
        panel += [status]
    panel += ['\n']

    print(format(panel))


@cli.command()
@click.argument('name')
@click.option('--show/--dont-show', default=True, is_flag=True,
              help='Show generated figures')
def results(name, show):
    """Show results for a specific recipe.

    Generate and save figures relating to recipe with NAME. Examples
    of valid names are asr.bandstructure, asr.gs etc.

    """
    from matplotlib import pyplot as plt
    from asr.core import get_recipe_from_name
    from asr.core.material import (get_material_from_folder,
                                   get_webpanels_from_material,
                                   make_panel_figures)
    recipe = get_recipe_from_name(name)

    if recipe.webpanel is None:
        print('{recipe.name} does not have any results to present!')
        return

    assert Path(f"results-{recipe.name}.json").is_file(), \
        'No results file for {recipe.name}, so I cannot show the results!'

    material = get_material_from_folder('.')
    panels = get_webpanels_from_material(material, recipe)
    make_panel_figures(material, panels)
    if show:
        plt.show()


@cli.command()
@click.argument('recipe')
@click.argument('hashes', required=False, nargs=-1, metavar='[HASH]...')
def find(recipe, hashes):
    """Find result files.

    Find all results files belonging to RECIPE. Optionally, filter
    these according to a certain ranges of Git hashes (requires having
    Git installed). Valid recipe names are asr.bandstructure etc.

    Find all results files calculated with a checkout of ASR that is
    an ancestor of HASH (including HASH): "asr find asr.bandstructure
    HASH".

    Find all results files calculated with a checkout of ASR that is
    an ancestor of HASH2 but not HASH1: "asr find asr.bandstructure
    HASH1..HASH2" (not including HASH1).

    Find all results files that are calculated with a checkout of ASR
    that is an ancestor of HASH1 or HASH2: "asr find asr.bandstructure
    HASH1 HASH2".

    This is basically a wrapper around Git's rev-list command and all
    hashes are forwarded to this command. For example, we can use the
    special HASH^ to refer to the parent of HASH.

    """
    from os import walk

    if not is_asr_initialized():
        initialize_asr_configuration_dir()

    recipe_results_file = f"results-{recipe}.json"

    if hashes:
        hashes = list(hashes)
        check_git()

    matching_files = []
    for root, dirs, files in walk(".", followlinks=False):

        if recipe_results_file in set(files):
            matching_files.append(str(Path(root) / recipe_results_file))

    if hashes:
        rev_list = get_git_rev_list(hashes)
        matching_files = list(
            filter(lambda x: extract_hash_from_file(x) in rev_list,
                   matching_files)
        )

    if matching_files:
        print("\n".join(matching_files))


def extract_hash_from_file(filename):
    """Extract the ASR hash from an ASR results file."""
    results = read_json(filename)
    try:
        version = results['__versions__']['asr']
    except KeyError:
        version = None
    except Exception:
        print(f"Problem when extration asr git hash from {filename}")
        raise

    if version and '-' in version:
        return version.split('-')[1]


def check_git():
    """Check that Git is installed."""
    proc = subprocess.Popen(['git'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    assert not err, f"{err}\nProblem with your Git installation."


def get_git_rev_list(hashes, home=None):
    """Get Git rev list from HASH1 to HASH2."""
    cfgdir = get_config_dir(home=home)

    git_repo = 'https://gitlab.com/mortengjerding/asr.git'
    if not (cfgdir / 'asr').is_dir():
        subprocess.check_output(['git', 'clone', git_repo],
                                cwd=cfgdir)

    asrdir = cfgdir / "asr"
    subprocess.check_output(['git', 'pull'],
                            cwd=asrdir)
    out = subprocess.check_output(['git', 'rev-list'] + hashes,
                                  cwd=asrdir)
    return set(out.decode("utf-8").strip("\n").split("\n"))


def is_asr_initialized(home=None):
    """Determine if ASR is initialized."""
    cfgdir = get_config_dir(home=home)
    return (cfgdir).is_dir()


def initialize_asr_configuration_dir(home=None):
    """Construct ASR configuration dir."""
    cfgdir = get_config_dir(home=home)
    cfgdir.mkdir()


def get_config_dir(home=None):
    """Get path to ASR configuration dir."""
    if home is None:
        home = Path.home()
    return home / '.asr'
