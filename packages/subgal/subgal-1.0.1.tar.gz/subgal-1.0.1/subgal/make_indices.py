#!/usr/bin/env python3

import sys
import os
import json
import collections
from string import Template

DEFAULT_BASE_URL = "http://localhost:8080/"

__doc__ = """Usage: subgal make-indices [options] [-v ...] <correlations.json>
       subgal make-indices --help

Options:
-h, --help                       This help
-i, --index-root=<path>          Where the index_....html files will be created
                                 [DEFAULT: .]
-v, --verbosity                  Number of v's is level of verbosity
                                 (No -v results in silence, -vvvv is
                                 super verbose)
-b, --base-url=<url>             All images and indices will have <url> at the beginning
                                 [DEFAULT: {1}]
""".format(sys.argv[0], DEFAULT_BASE_URL)


from docopt import docopt


def vprint(given_verbosity, verbosity, string):
  if given_verbosity <= verbosity:
    print(string)


def directories_to_original_filenames(correlation):
  to_return = collections.defaultdict(list)
  for original_filename in correlation.keys():
    directory = os.path.dirname(original_filename)
    to_return[directory].append(original_filename)
  return to_return


def create_main_index(main_index_filename, index_filenames):
  individual_index_links = ""
  for index_filename in index_filenames:

    # Don't show index_ or .html
    individual_index_links += f'<li><a class="myButton" href="{index_filename}">{os.path.splitext(index_filename)[0][6:]}</a></li>\n'

  import pkg_resources
  main_index_template = pkg_resources.resource_stream("subgal", "templates/main_index_template.html")
  main_index_template = Template(main_index_template.read().decode('utf-8'))

  with open(main_index_filename, 'w') as f:
    f.write(main_index_template.substitute({'individual_index_links': individual_index_links}))


def create_index(index_filename, directory, correlations, verbosity=0,
    thumb_key="300x300", big_key="1000x1000", main_index_filename="index.html"):
  v = verbosity
  vprint(1, v, f"Creating {index_filename}")

  image_anchors = ""
  for original_filename in correlations:
    if os.path.dirname(original_filename) == directory:
      vprint(2, v, f"  {original_filename}")
      basename = os.path.basename(original_filename)

      # Here's where there are choices  I'm mapping one thumbnail to
      # another because originals are always so big
      try:
        thumb = correlations[original_filename][thumb_key]
        big = correlations[original_filename][big_key]
      except KeyError as e:
        message = f"Either {thumb_key} or {big_key} doesn't exist " \
            + f"for {original_filename}"
        vprint(1, v, message)
        raise ValueError(message)

      image_anchors += f'<a href="{big}" data-ngthumb="{thumb}" data-ngdesc="">{basename}</a>'

  import pkg_resources
  individual_index_template = pkg_resources.resource_stream("subgal", "templates/individual_index_template.html")
  individual_index_template = Template(individual_index_template.read().decode('utf-8'))

  with open(index_filename, 'w') as f:
    f.write(individual_index_template.substitute({
      'image_anchors': image_anchors,
      'directory': directory,
      'main_index_filename': main_index_filename
    }))


def main(argv):
  args = docopt(__doc__, argv=argv)

  base_url = args['--base-url']
  index_root = args['--index-root']
  json_filename = args['<correlations.json>']
  verbosity = args['--verbosity']
  v = verbosity

  with open(json_filename) as f:
    correlations = json.load(f)

  dtoof = directories_to_original_filenames(correlations)

  index_filenames = []
  for directory in dtoof.keys():
    index_filename = "index_" + directory.replace(os.path.sep, "__") + ".html"
    index_filenames.append(index_filename)
    try:
      create_index(index_filename, directory, correlations,
          verbosity=verbosity)
    except ValueError as e:
      vprint(1, v, "Missing some thumbs")
  create_main_index(os.path.join(index_root, "index.html"), index_filenames)


if __name__ == "__main__":
  main(sys.argv)
