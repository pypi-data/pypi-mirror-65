### TODO Before 0.1.0 release


* Update CHANGELOG
* Fix all links in `README` once the paper is on arXiv (all links in badges in particular)
* Update the README of the bitbucket repo to signal that development has moved to github


### DONE items before 0.1.0
* Check that `libffa.so` is really being rebuilt on pip install: YES, gcc commands appear when running pip install in verbose mode, libffa.so has different md5sum on ozstar
* On OzStar, the pipeline raises an error "_tkinter.TclError: couldn't connect to display "localhost:15.0" when generating candidate plots. Placing `matplotlib.use('Agg')` at the top of pipeline.py does not fix it due to importing order (the console_scripts entry point design means that riptide is always imported first, and that causes matplotlib backend to be set before reacing the first line of pipeline.py). `plt.switch_backend('Agg')` fixes the problem. An alternative would be running the pipeline with a command such as `MPLBACKEND=Agg rffa <args>`
* Remove `h5py` from dependencies
* Force interpolation = 'nearest' when calling imshow() because recent versions of matplotlib use 'antialiased' by default now
* Propagate code version to data products
* Expose `load_json` and `save_json`, or create classmethods to save/load file
* Following the numpy.fft interface: provide `ffa1`, `ffa2` and `ffafreq` functions.
* Improve candidate plots
* Comment `config.yml` template(s)
* Place config templates in a `config` subdir
* Implement DM sinb max
* Bugfix: 'skycoord' attribute should be allowed to be None
* Add log-level parameter to `pipeline.py`
* Add candidate filters
* Move `remove_harmonics` param to `candidate_filters` section
* Update the signal generation function so that the amplitude represents the true signal to noise
* Review `setup.py` in detail, in particular the module URL
* Update `README`
* Grep any important TODOs and FIXMEs and fix them
* Make sure `Candidate` class interface is good because we ain't changing that one lightly once released
* Test extensively on other machines (OzStar)
* Docstrings

### What's next
* Refactor `Periodogram` class, `ffa_search()` should probably not return a search plan if it is a member of pgram itself
* Documentation and readthedocs page
* Validate `config.yml` on pipeline init
* Unit tests
* Travis CI or equivalent
* Output *actual* duty cycle and also best phase of candidates in the C code, and propagate it
* Library of known pulsar test data sets