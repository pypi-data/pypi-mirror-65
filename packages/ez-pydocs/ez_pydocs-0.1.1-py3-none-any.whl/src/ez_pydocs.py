"""
A nice tool to generate docs for all python utilities that we create.
"""
import argparse
import fnmatch
import os
import re
import subprocess


def generate_markdown(modules):
    """
    Generate the documentation output in markdown
    """
    create_doc_cmd = ["pydocmd", "simple", *modules]
    process = subprocess.Popen(
        create_doc_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # Wait for the process to finish.
    exit_status = process.wait()

    # Exit status > 0 == Error
    if exit_status:
        err_msg = process.stderr.read()
        print("Couldn't successfully create the documentation file.")
        print(err_msg)
        raise SystemExit

    # Obtain the markdown string.
    docs = process.stdout.read().decode("utf-8")

    return docs


def write_md_file(path_to_dir: str, markdown: str):
    """
    Write the doc contents to the file.
    """
    # Write the documentation into it's respesctive
    # file.
    with open(f"{path_to_dir}/docs.md", "w+") as output_file:
        output_file.write(markdown)

def parse_args():
    """
    Create the argument parser and return the parsed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "directory",
        type=str,
        help="The directory to traverse. Ideally should be in the same directory as your README.md",
    )

    return parser.parse_args()

def main():
    """
    Walk through the directories of our python project and start
    documenting all of the code.
    """

    args = parse_args()

    if not os.path.exists(f"{os.getcwd()}/{args.directory}"):
        print("The entered directory doesn't exist. Exiting the program.")
        raise SystemExit

    md_for_readme = ["## Documentation"]
    for root, dirs, files in os.walk(f"./{args.directory}"):
        registered_modules = []
        found_a_file = False
        module_root = re.sub("/", ".", re.sub(r"\./", "", root))

        # Iterate through all of the files and add python modules to the list of
        # modules to be documented
        for file in files:
            if fnmatch.fnmatch(file, "*.py"):
                found_a_file = True
                file_without_extension = re.sub("\.py", "", file)
                module_to_generate = f"{module_root}{file_without_extension}++"
                registered_modules.append(module_to_generate)

        if found_a_file:
            print(f"Creating documentation for {root}")
            docs = generate_markdown(registered_modules)
            write_md_file(root, docs)
            path_as_md_link = f"* [{module_root}]({root}docs.md)"
            md_for_readme.append(path_as_md_link)
        else:
            print(f"No python files found in {root}.")

    print("\n---COPY & PASTE IN README---")
    for line in md_for_readme:
        print(line)

if __name__ == "__main__":
    main()
