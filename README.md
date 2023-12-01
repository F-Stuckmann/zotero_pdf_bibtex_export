# Zotero PDF Export

If you want to upload your Zotero library to overleaf, it is convinient to have all the pdf files in a single directory and the name should be the reference you use in Latex.
Simply provide the export path of zotero and this directory will create the following structure:

```
Library.bib
LATEX_REFERENCE_1.pdf
LATEX_REFERENCE_2.pdf
```

In your latex document the references are as follows:
```
\cite{LATEX_REFERENCE_1}
```