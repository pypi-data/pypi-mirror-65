"""
pickup.py
=========
Module for fruit to allow adding fruit configurations to the global fruit workspace.
"""

import os
import fruit.modules.console as console
from typing import List

DOT_FRUITPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.fruitpath")

def load_fruit_env() -> List[str]:
  """
  Load the environment variable `fruitpath` and parse it into an array of strings.
  The environment variable has to be separated via ';'.

  Returns
  -------
  List[str]:
    List of pathes added by the user. For invalid environment variables an empty array will be added.
  """
  try:
    with open(DOT_FRUITPATH, 'r') as fp:
      pathlist = fp.readlines()
    return pathlist
  except Exception as exc:
    console.error(f"The environmental variable FRUITPATH cannot be loaded!")
    console.error(f"Reason {str(exc)}")
    return []

def save_fruit_env(paths: List[str]) -> None:
  """
  Save the environmental variable FRUITPATH from the list of pathes. The saved variable will
  be a  ';' separated list.

  Parameters
  ----------
  paths : List[str]
      List of pathes
  """
  try:
    with open(DOT_FRUITPATH, 'w') as fp:
      fp.writelines(paths)
  except Exception as exc:
    console.error("The environmental variable FRUITPATH cannot be modified!")
    console.error(f"Reason: {str(exc)}")

def pickup_path(path: str):
  """
  Add a new path to the FRUITPATH environmental variable for global fruit configurations.

  Parameters
  ----------
  path : str
      New path to add. May be relative or absolute path
  """
  abspath = os.path.abspath(path)
  pathlist = load_fruit_env()

  if abspath not in pathlist:
    pathlist.append(abspath)
    console.echo(f"{abspath} was picked up!")
  else:
    console.warning(f"The path {abspath} is already picked up!")

  save_fruit_env(pathlist)

def drop_path(path: str):
  """
  Remove an already 'picked-up' path from the global FRUITPATH.

  Parameters
  ----------
  path : str
      Path to remove. May be relative or absolute
  """
  abspath = os.path.abspath(path)
  pathlist = load_fruit_env()

  try:
    pathlist.remove(abspath)
    save_fruit_env(pathlist)
    console.echo(f"{abspath} was dropped!")
  except Exception as exc:
    console.error(f"The path {abspath} cannot be removed!")
    console.error(f"Reason: {str(exc)}")