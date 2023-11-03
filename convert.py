# pylint: disable=C0103

"""Module providing a command line tool to convert .txt or .md files to .html files."""
import pathlib
import re
import sys
import os
import argparse
import shutil
from tomlkit.toml_file import TOMLFile
from tomlkit.exceptions import UnexpectedCharError
import frontmatter


def print_version():
    """Function prints app version."""
    with open("_version.py", "r", encoding="utf-8") as file:
        print(f"go-go-web {file.read()}")


def remake_til_folder(out):
    """Function removes existing default output folder and recreates it."""
    # delete default output folder
    if os.path.exists(out):
        try:
            shutil.rmtree(out)
            print(f"{out} folder deleted")
        except OSError:
            print(OSError)
            sys.exit(1)

    # create default output folder
    os.makedirs(out)
    print(f"{out} folder created")


def load_config_file(config_file):
    """Function returns contents of TOML config file"""
    try:
        toml = TOMLFile(config_file)
        config_data_doc = toml.read()
        return config_data_doc
    except (FileNotFoundError, UnexpectedCharError) as exception:
        print("Error loading or parsing the config file:", exception)
        sys.exit(1)


def get_html_before_body(filename, css_url, metadata):
    """Function returns the html of the page before and up to the <body>"""
    html = '<!doctype html>\n'
    html += f'<html lang="{metadata["lang"] if "lang" in metadata else "en"}">\n'
    html += '<head>\n'
    html += '\t<meta charset="utf-8">\n'
    html += f'\t<title>{metadata["title"] if "title" in metadata else filename}</title>\n'
    if 'keywords' in metadata:
        html += f'\t<meta name="keywords" content="{metadata["keywords"]}" />\n'
    if 'description' in metadata:
        html += f'\t<meta name="description" content="{metadata["description"]}" />\n'
    html += '\t<meta name="viewport" content="width=device-width, initial-scale=1" />\n'
    if css_url:
        html += f'\t<link rel="stylesheet" href="{css_url}">\n'
    html += '</head>\n'
    html += '<body>\n'
    return html


def get_html_after_body():
    """Function returns the html of the page including and following </body>"""
    html = '</body>\n'
    html += '</html>'
    return html


def convert_to_html(path, output_folder, css_url):
    """Function converts a file to html"""
    # at slash at end of folder path if it is not there
    if output_folder[-1] != "/":
        output_folder += "/"

    # check if output folder is an existing folder
    if not os.path.isdir(output_folder):
        print(
            f"Error: output folder {output_folder} is not an existing folder")
        sys.exit(1)

    # split the root and file ext
    path_tup = os.path.splitext(path)

    # extract the file name and ext
    file_name = path_tup[0]
    file_ext = path_tup[1]
    if file_ext == ".md":
        markdown_to_html(path, file_name, output_folder, css_url)
    elif file_ext == ".txt":
        text_to_html(path, file_name, output_folder, css_url)
    else:
        print(
            f"Error: {path.replace(os.sep, '/')} was not converted. \
                File extension should be .md or .txt")
        sys.exit(1)


def markdown_to_html(path, file_name, output_folder, css_url):
    """Function converts a markdown file to html"""

    # parse file and separate post frontmatter from post content
    post = parse_frontmatter(path)

    # output file name
    output_fname = os.path.basename(file_name) + ".html"

    # use the input file name as the output file name
    output_fpath = output_folder + output_fname

    # flag which signifies if text is inside a code block
    in_code_block = False

    with open(output_fpath, mode='w', encoding="utf-8") as output_file:
        output_file.write(get_html_before_body(
            os.path.basename(file_name), css_url, post.metadata))

        # read each line in post content
        for line in post.content.splitlines():

            # trim the line of whitespace and newline character
            line = line.strip()

            # If text is not inside a code block, must parse styled text
            if not in_code_block:
                # Look for beginning of code block (```)
                result_tup = re.subn(r'^[ ]*```.*$', r'<pre>', line)
                line = result_tup[0]
                num_found = result_tup[1]

                if num_found > 0:
                    in_code_block = True
                else:
                    # Replace *italic* and _italic_ with <em>italic</em>
                    line = re.sub(r'([^*])\*([^*]+)\*', r'\1<em>\2</em>', line)
                    line = re.sub(r'[^_]_([^_]+)_', r'<em>\1</em>', line)

                    # Replace **bold** and __bold__ with <strong>bold</strong>
                    line = re.sub(r'\*\*([^*]+)\*\*',
                                  r'<strong>\1</strong>', line)
                    line = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', line)

                    # Replace --- with <hr />
                    line = re.sub(r'^[ ]*---[-]*[ ]*$', r'<hr />', line)

                    # Replace `text` with <code>text</code>
                    line = re.sub(r'`(.*)`', r'<code>\1</code>', line)

                    # Line is not in code block, so wrap line in paragraph tag
                    line = "<p>" + line + "</p>"
            else:
                # Look for end of code block (```)
                result_tup = re.subn(r'^[ ]*```[`]*[ ]*$', r'</pre>', line)
                line = result_tup[0]
                num_found = result_tup[1]

                if num_found > 0:
                    in_code_block = False

            if line:
                # write the line to the output file
                output_file.write(f'{line}\n')
            else:
                # write an empty line to the output file
                output_file.write('\n')

        output_file.write(get_html_after_body())

    print(f"{path.replace(os.sep, '/')} converted to {output_fpath} successfully!")


def text_to_html(path, file_name, output_folder, css_url):
    """Function converts a txt file to html"""
    output_fname = os.path.basename(file_name) + ".html"

    # use the input file name as the output file name
    output_fpath = output_folder + output_fname

    # open input and output files
    with open(path, mode='r', encoding="utf-8") as input_file, \
            open(output_fpath, mode='w', encoding="utf-8") as output_file:

        output_file.write(get_html_before_body(
            os.path.basename(file_name), css_url, {}))

        # read each line in input file
        for line in input_file:

            # trim the line of whitespace and newline character
            line = line.strip()

            if line:
                # wrap line in paragraph tag
                line = "<p>" + line + "</p>"

                # write the line to the output file
                output_file.write(f'{line}\n')
            else:
                # write an empty line to the output file
                output_file.write('\n')

        output_file.write(get_html_after_body())

    print(f"{path.replace(os.sep, '/')} converted to {output_fpath} successfully!")


def get_default_output_dir():
    """Function returns default output dir specified in _output_dir.py"""
    try:
        with open("_output_dir.py", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(1)


def parse_config(config_file):
    """Function parses config file to return options"""
    # Load and parse the TOML configuration file
    config = load_config_file(config_file)
    return {
        "output": config["output"] if "output" in config else get_default_output_dir(),
        "stylesheet": config["stylesheet"] if "stylesheet" in config else ""
    }


def parse_cmdline(output_dir, css_url):
    """Function parses command-line arguments to return options"""
    return {
        "output": str(output_dir) if output_dir else get_default_output_dir(),
        "stylesheet": css_url if css_url else ""
    }


def parse_frontmatter(input_file):
    """Function parses .md file to return object with frontmatter and content separated"""
    with open(input_file, mode='r', encoding="utf-8"):
        post = frontmatter.load(input_file)
    return post


# only triggered when we call this .py file and not during imports
if __name__ == '__main__':
    def formatter(prog):
        """Function parses command line arguments"""
        return argparse.HelpFormatter(prog, max_help_position=52)
    parser = argparse.ArgumentParser(
        formatter_class=formatter, description="convert txt or md file or folder of files to html")
    parser.add_argument("-v", "--version", action="store_true",
                        help="display the app version")
    parser.add_argument("-o", "--output", type=pathlib.Path,
                        help="specify output directory")
    parser.add_argument("-s", "--stylesheet", type=str,
                        help="specify url for CSS stylesheet")
    parser.add_argument("fname", nargs='?', type=pathlib.Path,
                        help="the input file or folder path")
    parser.add_argument("-c", "--config", type=str, help="specify config file")
    args = parser.parse_args()

    if args.version:
        print_version()
    else:
        if args.fname:
            # get input file path from user input
            input_file_path = str(args.fname)

            # get options from either config file or command line args
            if args.config:
                options = parse_config(args.config)
            else:
                options = parse_cmdline(args.output, args.stylesheet)

            # remove and recreate default output folder
            try:
                remake_til_folder(options["output"])
            except FileNotFoundError:
                print(
                    f"{FileNotFoundError}\n_output_dir.py contains an invalid path")
                sys.exit()

            # check if the input file or folder path EXISTS
            if os.path.isfile(input_file_path):
                # convert file to html
                convert_to_html(input_file_path,
                                options["output"], options["stylesheet"])
            elif os.path.isdir(input_file_path):
                # get each item in the folder
                for item in os.listdir(input_file_path):
                    # get the file path
                    file_path = os.path.join(input_file_path, item)

                    # check if item is a file
                    if os.path.isfile(file_path):
                        # convert file to html
                        convert_to_html(
                            file_path, options["output"], options["stylesheet"])
            else:
                print(f"Error: File {input_file_path} does not exist\n")
                parser.print_help()
                sys.exit(1)
        else:
            print("Error: no file or folder name specified")
            parser.print_help()
            sys.exit(1)
