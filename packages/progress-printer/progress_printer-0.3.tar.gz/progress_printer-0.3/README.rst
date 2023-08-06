progress_printer
-----

The progress_printer package provides an easy way to output the progress and estimated finish time for a for loop.

To use, do:
	>>> import progress_printer as pp
	>>> t0 = datetime.datetime.now()
	>>> for i, list_item in enumerate(list):
    >>>     pp.ProgressStatus(i, len(list), t0)
