
.. _intro:

Introduction to sdss_access
===============================

SDSS Access provides a convenient way of navigating local and remote filesystem paths from the Science Archive Server (SAS).
`sdss_access` uses the SDSS Tree product for all path look-ups.

Path Generation
^^^^^^^^^^^^^^^

You can generate full paths to files easily with `Path.full`::

    # import the path
    from sdss_access import SDSSPath
    path = SDSSPath()

    # generate a file system path
    path.full('mangacube', drpver='v2_3_1', plate='8485', ifu='1901')
    '/Users/Brian/Work/sdss/sas/mangawork/manga/spectro/redux/v2_3_1/8485/stack/manga-8485-1902-LOGCUBE.fits.gz'

Note that this only generates a path. The file may not actually exist locally.  If you want to generate a URL path to the file at 
Utah, you can use `Path.url`::

    # generate a http path to the file
    path.url('mangacube', drpver='v2_3_1', plate='8485', ifu='1901')
    'https://data.sdss.org/sas/mangawork/manga/spectro/redux/v2_3_1/8485/stack/manga-8485-1902-LOGCUBE.fits.gz'


Path Names
^^^^^^^^^^

The syntax for all paths defined in `sdss_access`, for most methods, is ``(name, **kwargs)``.  Each path is defined by a **name** and 
several **keyword arguments**, indicated in the template filepath by **{keyword_name}**.  For example, the path to a MaNGA data cube 
has **name** ``mangacube`` and path keywords, **plate**, **drpver**, and **ifu**, defined in the path 
``$MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-LOGCUBE.fits.gz``.  All paths are defined inside the SDSS 
`tree` product, within the `sdss_paths.ini` file, and available to you as a dictionary, ``path.templates``::

    from sdss_access import SDSSPath
    path = SDSSPath()

    # show the dictionary of available paths
    path.templates

To look up what path names are available, you can use ``path.lookup_names``::

    # look up the available path names
    path.lookup_names()
    ['BOSSLyaDR_cat', ..., 'mangacube', ..., 'xdqso_index']

To look up what keywords are needed for a given path, you can use ``path.lookup_keys``::

    # look up the keyword arguments needed to define a MaNGA cube path
    path.lookup_keys('mangacube')
    ['plate', 'drpver', 'ifu']

The full list of paths can also be found :ref:`here <paths>`.

Downloading Files
^^^^^^^^^^^^^^^^^

You can download files from the SAS and place them in your local SAS.  `sdss_access` expects a local SAS filesystem that mimics
the real SAS at Utah.  If you do not already have a `SAS_BASE_DIR` set, one will be defined in your home directory, as a new `sas`
directory.

sdss_access has four classes designed to facilitate access to SAS data.   

- Access - class that automatically decides between `RsyncAccess` and `CurlAccess` based on the operating system.
- HttpAccess - uses the `urllib` package to download data using a direct http request
- RsyncAccess - uses `rsync` to download data.  Available for Linux and MacOS.  
- CurlAccess - uses `curl` to download data.  This is the only available method for use on Windows machines. 

Using the `HttpAccess` class.

::

    from sdss_access import HttpAccess
    http_access = HttpAccess(verbose=True)

    # set to use remote
    http_access.remote()

    # get the file
    http_access.get('mangacube', drpver='v2_3_1', plate='8485', ifu='1901')

Using the `RsyncAccess` class.  `RsyncAccess` is generally much faster then `HttpAccess` as it spreads multiple file downloads
across multiple continuous rsync download streams.  

::

    # import the rsync class
    from sdss_access import RsyncAccess
    rsync = RsyncAccess()

    # sets a remote mode to the real SAS
    rsync.remote()

    # add all the file(s) you want to download
    # let's download all MPL-6 MaNGA cubes for plate 8485
    rsync.add('mangacube', drpver='v2_3_1', plate='8485', ifu='*')

    # set the stream tasks
    rsync.set_stream()

    # start the download(s)
    rsync.commit()

The default mode of `RsyncAccess` is for collaboration access.  You can also access data from publicly available SDSS data releases, 
by specifying the `public` and `release` keyword arguments on init.

::

    # setup rsync access to download public data from DR14
    rsync = RsyncAccess(public=True, release='dr14')

Using the `CurlAccess` class.  `CurlAccess` behaves exactly the same way as `RsyncAccess`.  After importing and instantiating 
a `CurlAccess` object, all methods and behavior are the same as in the `RsyncAccess` class.   
::

    # import the curl class
    from sdss_access import CurlAccess
    curl = CurlAccess()

Using the `Access` class.  Depending on your operating system, `posix` or not, Access will either create itself using `RsyncAccess` 
or `CurlAccess`, and behave as either object.  Via `Acccess`, Windows machines will always use `CurlAccess`, while Linux or Macs 
will automatically utilize `RsyncAccess`.
::

    # import the access class
    from sdss_access import Access
    access = Access()

    # the access mode is automatically set to rsync. 
    print(access)
    >>> <Access(access_mode="rsync", using="data.sdss.org")>

    # the class now behaves exactly like RsyncAccess. 
    # download a MaNGA cube
    access.remote()
    access.add('mangacube', drpver='v2_3_1', plate='8485', ifu='1901')
    access.set_stream()
    access.commit()

In all all cases, successful `sdss_access` downloads will return a code of 0. Any other number indicates that a problem occurred.  If no verbose message
is displayed, you may need to check the `sdss_access_XX.log` and `sdss_access_XX.err` files within the temporary directory.  

.. _sdss-access-windows:

Notes for Windows Users
^^^^^^^^^^^^^^^^^^^^^^^

`sdss_access` downloads files into a directory defined by the `SAS_BASE_DIR` enviroment variable.  If this path points to another drive other than 
the C drive, make sure that the new drive and paths have full write permissions available to `curl`.  `CurlAccess` may not work properly until correct
permissions are set up in your folder system.

.. _sdss-access-api:

Reference/API
^^^^^^^^^^^^^

.. rubric:: Class

.. autosummary:: sdss_access.path.Path
.. autosummary:: sdss_access.Access
.. autosummary:: sdss_access.HttpAccess
.. autosummary:: sdss_access.RsyncAccess
.. autosummary:: sdss_access.CurlAccess

.. rubric:: Methods

.. autosummary::

    sdss_access.SDSSPath.full
    sdss_access.SDSSPath.url
    sdss_access.SDSSPath.lookup_names
    sdss_access.SDSSPath.lookup_keys
    sdss_access.HttpAccess.remote
    sdss_access.HttpAccess.get
    sdss_access.RsyncAccess.remote
    sdss_access.RsyncAccess.add
    sdss_access.RsyncAccess.set_stream
    sdss_access.RsyncAccess.commit
