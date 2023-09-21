import re
import sys
import os

# prints the app version
def print_version():
    """Function printing app version."""
    with open("_version.py", "r", encoding="utf-8") as file:
        print("go-go-web " + file.read())


# prints the app help message
def print_help():
    """Function printing usage message."""
    print("Usage: convert.py -i <txt_filename> or <folder_containing_txt_files>  [-o <output_dir>] [-s <css_url>]\n")
    print("Options:")
    print("  -i, --input\t\tInput directory or .txt file\t" + "[string] [required]".rjust(24))
    print("  -o, --output\t\tSpecify output directory\t" + "[string] [default: \"\"]".rjust(24))
    print("  -s, --stylesheet\tSpecify url for CSS stylesheet \t" + "[string] [default: \"\"]".rjust(24))
    print("  -h, --help\t\tPrint this help message\t\t" + "[boolean]".rjust(24))
    print("  -v, --version\t\tPrint version number\t\t" + "[boolean]".rjust(24))
    sys.exit()

# takes an input file path for a .txt file, and outputs an .html file
def convert_txt_md_html(path, output_folder, css_url):
    """Function converting one txt file to html"""

    # at slash at end of folder path if it is not there
    if output_folder[-1] != "/":
        output_folder += "/"

    # check if output folder is an existing folder
    if not os.path.isdir(output_folder):
        print("Error: output folder " + output_folder + " is not an existing folder")
        return

    # split the root and file ext
    path_tup = os.path.splitext(path)

    # extract the file name and ext
    file_name = path_tup[0]
    file_ext = path_tup[1]
    
    # check if input file has a valid extension
    if file_ext in ( ".txt" ,".md"):
        title = os.path.basename(file_name)
        output_fname = title + ".html"

        # use the input file name as the output file name
        output_fpath = output_folder + output_fname

        # open input and output files
        with open(path, mode='r', encoding="utf-8") as input_file, open(output_fpath, mode='w', encoding="utf-8") as output_file:

            # write html head
            output_file.write('<!doctype html>\n')
            output_file.write('<html lang="en">\n')
            output_file.write('<head>\n')
            output_file.write('\t<meta charset="utf-8">\n')
            output_file.write(f'\t<title>{title}</title>\n')
            output_file.write('\t<meta name="viewport" content="width=device-width, initial-scale=1">\n')
            if css_url:
                output_file.write(f'\t<link rel="stylesheet" href="{css_url}">\n')
            output_file.write('</head>\n')

            # write html body
            output_file.write('<body>\n')

            # read each line in input file
            for line in input_file:

                # trim the line of whitespace and newline character
                line = line.strip()

                if file_ext == ".md" :
                    # Replace *italic* and _italic_ with <em>italic</em>
                    line = re.sub(r'[^*]\*([^*]+)\*', r'<em>\1</em>', line)
                    line = re.sub(r'[^_]_([^_]+)_', r'<em>\1</em>', line)

                    # Replace **bold** and __bold__ with <strong>bold</strong>
                    line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
                    line = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', line)
    
                if line:
                    # check if line is empty string
                    # write the line to the output file wrapped in the paragraph tag
                    output_file.write(f'<p>{line}</p>\n')
                else:
                    # write an empty line to the output file
                    output_file.write(f'\n')


            # write closing tags
            output_file.write(f'</body>\n')
            output_file.write(f'</html>')
        
        print(path.replace(os.sep, '/') + " converted to " + output_fpath + " successfully!")
    else:
        print("Error: " + path.replace(os.sep, '/') + " was not converted. File extension should be .txt")


# only triggered when we call this .py file and not during imports
if __name__ == '__main__':

    # get list of all arguments user typed in command line after calling this .py file with "python convert.py"
    args = sys.argv[1:]

    # check if user specified any arguments
    if args:
        option_name = args[0]

        if option_name == "-v" or option_name == "--version":
            print_version()
        elif option_name == "-h" or option_name == "--help":
            print_help()
        elif option_name == "-i" or option_name == "--input":

            # default output folder path and css url
            output_folder = "til"
            css_url = None

            # delete default output folder
            if os.path.exists(output_folder):
                for f in os.listdir(output_folder):
                    os.remove(os.path.join(output_folder, f))
                os.rmdir(output_folder)
                print(output_folder + " folder deleted")

            # create default output folder
            os.makedirs(output_folder)
            print(output_folder + " folder created")



            file_names = args[1:]

            # check if use provided file name or folder name argument
            if file_names:

                # get the first file name argument provided by the user
                path = file_names[0]

                # get succeeding arguments to check if user specified an output directory or stylesheet
                args = file_names[1:]
                
                i = 0
                max_input_options = 2

                while args and i < max_input_options:
                    option_name = args[0]

                    if option_name == "-o" or option_name == "--output":
                        # get output path specified by user in succeeding argument
                        output_args = args[1:]

                        if output_args:
                            # set the output_folder
                            output_folder = output_args[0]
                        else:
                            print("Missing required argument: <output_dir>")
                            print_help()

                    elif option_name == "-s" or option_name == "--stylesheet":
                        # get file path of stylesheet specified by user in succeeding argument
                        css_args = args[1:]

                        if css_args:
                            # set the css file path
                            css_url = css_args[0]
                        else:
                            print("Missing required argument: <css_url>")
                            print_help()
                    else:
                        print("Invalid option: " + option_name)
                        print_help()
                    
                    # read the next option
                    args = args[2:]

                # check if the path given is for existing file, existing folder, or non-existent
                if os.path.isfile(path):
                    convert_txt_md_html(path, output_folder, css_url)
                elif os.path.isdir(path): 
                    # get each item in the folder
                    for item in os.listdir(path):

                        # get the file path
                        file_path = os.path.join(path, item)

                        # check if item is a file
                        if os.path.isfile(file_path):
                            convert_txt_md_html(file_path, output_folder, css_url)

                else:  
                    print("Error: file cannot be found")
            else:
                print("Missing required argument: <txt_filename> or <folder_containing_txt_files>")
                print_help()
        else:
            print("Invalid option: " + option_name)
            print_help()
    else:
        print()
        print_help()