import os
import fnmatch
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
    parser.add_argument('--dir', type=str, help='Path to the Zotero directory', required=True)

    args = parser.parse_args()

    zotero_directory = args.dir
    pdf_files = find_pdf_files(zotero_directory)
    print(pdf_files)
    
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

        new_location = os.path.join(zotero_directory,  raw_file)
        # copy file to new location
        command = "cp " + file_location + " " + new_location
        os.system(command)

        
        
        combined_file = raw_file + ":" + new_location + ":" + entry.get('file', 'No file location provided').split(':')[-1]
        entry['file'] = combined_file

        print(f"Citation: {citation}")
        print(f"File Location: {file_location}")
        print("-----")
    
    # Write the updated BibTeX back to the file
    with open(bib, 'w') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

