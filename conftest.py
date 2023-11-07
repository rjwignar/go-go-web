"""Module contains fixtures, helper functions, global variables for pytest"""
import os
import pytest


class Helpers:
    @staticmethod
    def new_file(directory, file_name, file_contents):
        """Creates new file and returns the path"""
        # Create temporary input txt file
        file_path = directory.join(file_name)
        # Write contents to file
        with open(str(file_path), mode="w", encoding="utf-8") as file:
            file.write(file_contents)
        return str(file_path)

    @staticmethod
    def file_contents(file_path):
        """Returns file contents"""
        with open(str(file_path), "r", encoding="utf-8") as file:
            return file.read()


# Global variables
def pytest_configure():
    """Defines pytest global variables"""
    pytest.simple_txt_contents = 'Hello\n'
    pytest.simple_md_contents = 'Hello\n' \
        '---\n' \
        '**Bold**\n' \
        '*Italics*\n'

    pytest.simple_html_from_txt = '<!doctype html>\n' \
        '<html lang="en">\n' \
        '<head>\n' \
        '\t<meta charset="utf-8">\n' \
        '\t<title>test</title>\n' \
        '\t<meta name="viewport" content="width=device-width, initial-scale=1" />\n' \
        '</head>\n' \
        '<body>\n' \
        '<p>Hello</p>\n' \
        '</body>\n' \
        '</html>'

    pytest.simple_html_with_stylesheet = '<!doctype html>\n' \
        '<html lang="en">\n' \
        '<head>\n' \
        '\t<meta charset="utf-8">\n' \
        '\t<title>test</title>\n' \
        '\t<meta name="viewport" content="width=device-width, initial-scale=1" />\n' \
        '\t<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tufte-css/1.8.0/tufte.min.css">\n' \
        '</head>\n' \
        '<body>\n' \
        '<p>Hello</p>\n' \
        '</body>\n' \
        '</html>'

    pytest.simple_html_from_md = '<!doctype html>\n' \
        '<html lang="en">\n' \
        '<head>\n' \
        '\t<meta charset="utf-8">\n' \
        '\t<title>markdown</title>\n' \
        '\t<meta name="viewport" content="width=device-width, initial-scale=1" />\n' \
        '</head>\n' \
        '<body>\n' \
        '<p>Hello</p>\n' \
        '<p><hr /></p>\n' \
        '<p><strong>Bold</strong></p>\n' \
        '<p>*Italics*</p>\n' \
        '</body>\n' \
        '</html>'


@pytest.fixture
def cleanup_cwd():
    """Cleanup code to revert the CWD back to original value"""
    # Startup code
    old_cwd = os.getcwd()   # Save the old CWD
    yield
    # Cleanup code
    os.chdir(old_cwd)   # Change CWD back


@pytest.fixture
def cleanup_output(request):
    """Cleanup code to remove output file"""
    yield
    # Cleanup code
    for file_path in request.param:
        if os.path.exists(file_path):
            os.remove(file_path)


@pytest.fixture
def helpers():
    return Helpers
