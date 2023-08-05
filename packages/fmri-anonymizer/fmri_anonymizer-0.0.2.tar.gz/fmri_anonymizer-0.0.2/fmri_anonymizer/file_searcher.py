import os
# from ttictoc import TicToc


def walk_through(parent, *file_types):
    """
    Function that filters out all the file types that are in some parent folder and its sub-folders.
    :param parent: Root path that contains multiple sub-folders and files.
    :param file_types: A list of all of the file types that can be discovered inside of the whole tree structure in
    the parent folder.
    :return: A sorted list of all the files found in the parent.
    """
    files_detected = set()
    if os.path.isdir(parent):
        for root, dirs, files in os.walk(parent):
            for file_ in files:
                if file_.endswith(tuple(file_types)) or (os.path.splitext(file_)[-1] == '' and not file_.startswith('.')):
                    files_detected.add(os.path.join(root, file_))
        return sorted(files_detected)


'''
def main(argv=None):
    t = TicToc()
    t.tic()
    parent = "/Users/hugoanda/Documents/Job_Documentation/Scans_Participants"
    file_type = ".dcm"
    outcome = walk_through(parent=parent, file_type=file_type)
    t.toc()
    print(outcome)
    print(f"Number of files found: {len(outcome)}")
    print(f"Elapsed time for the function is {t.elapsed:.6f}s")


if __name__ == "__main__":
    main()
'''
