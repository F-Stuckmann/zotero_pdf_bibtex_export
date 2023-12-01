import os
import fnmatch
import shlex
import bibtexparser


def find_pdf_files(directory):
    pdf_files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.pdf'):
            pdf_files.append(os.path.join(root, filename))
    return pdf_files
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', type=str, help='Path to the exported Zotero directory', required=True)
    parser.add_argument("--zotero", help="Path to the Zotero directory", required=True)

    args = parser.parse_args()

    zotero_directory = args.dir
    base_directory = args.zotero
    global_pdf_files = find_pdf_files(base_directory)
    
    # find .bib file in zotero_directory load .bib file
    files = [os.path.join(zotero_directory, f) for f in os.listdir(zotero_directory) if os.path.isfile(os.path.join(zotero_directory, f)) and f.endswith('.bib')]
    bib = files[0]
    print(bib)
    with open(bib) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)

    for entry in bib_database.entries:
        # Extracting the citation (formatted as an example, adjust as needed)
        citation = f"{entry.get('author')}, {entry.get('title')}, {entry.get('journal')}, {entry.get('year')}"

        file_id = entry.get("ID")
        # raw filename
        raw_file = file_id + '.pdf'
        
        # Extracting the file location
        file_location = os.path.join(zotero_directory, entry.get('file', 'No file location provided').split(':')[1])
        if ".pdf" not in file_location:
            found = False
            # search in global zotero library
            r = [i for i in entry.get('file', 'No file location provided').split(":") if ".pdf" in i][0]
            if ";" in r:
                r = r.split(";")[1]
            base_file = os.path.basename(r)
            for f in global_pdf_files:
                if base_file == os.path.basename(f):
                    file_location = f
                    found = True
                    break
            if not found:
                raise Exception("File not found {ID} {base_file} - is the default zotero repository provided?".format(ID=file_id, base_file=base_file))

        new_location = os.path.join(zotero_directory,  raw_file)
        # copy file to new location
        command = "cp '" + file_location + "' " + new_location
        # Split the command into parts
        # command_parts = shlex.split(command)

        # # Reconstruct the command with each part safely quoted
        # sanitized_command = ' '.join(shlex.quote(part) for part in command_parts)
        os.system(command)

        
        
        combined_file = raw_file + ":" + new_location + ":" + entry.get('file', 'No file location provided').split(':')[-1]
        entry['file'] = combined_file
    
    # Write the updated BibTeX back to the file
    with open(bib, 'w') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

