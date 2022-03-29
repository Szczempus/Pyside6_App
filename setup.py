from cx_Freeze import setup, Executable
import setuptools

setup(
    name="CudApp",
    version="1.0.0",
    options={"build.exe": {
        "packages": ['os', 'sys', 'ctypes', 'PySide2', 'cv2', 'matplotlib.cm', 'deepforest', 'torch', 'math', 'time',
                     'numpy', 'osgeo', 'tifffile', 'numpy', 'PIL', 'shutil','shapely','rasterio'
                     # 'affine', 'aiohttp',
                     # 'aiosignal',
                     # 'albumentations',
                     # 'altgraph',
                     # 'async-timeout',
                     # 'attrs',
                     # 'bottle',
                     # 'bottle-websocket',
                     # 'bzip2',
                     # 'ca-certificates',
                     # 'certifi',
                     # 'cffi',
                     # 'click',
                     # 'click-plugins',
                     # 'cligj',
                     # 'colorama',
                     # 'conda-pack',
                     # 'cx-freeze',
                     # 'cx-logging',
                     # 'eel',
                     # 'fiona',
                     # 'frozenlist',
                     # 'fsspec',
                     # 'gdal',
                     # 'geopandas',
                     # 'gevent',
                     # 'gevent-websocket',
                     #
                     # 'greenlet',
                     #
                     # 'imagecodecs',
                     #
                     # 'imageio',
                     #
                     # 'importlib-metadata',
                     #
                     # 'iopath',
                     #
                     # 'joblib',
                     #
                     # 'libffi',
                     #
                     # 'libzlib',
                     #
                     # 'lief',
                     #
                     # 'multidict',
                     #
                     # 'munch',
                     #
                     # 'networkx',
                     #
                     # 'ninja',
                     #
                     # 'numpy',
                     #
                     # 'opencv-python-headless',
                     #
                     # 'openssl',
                     # 'packaging',
                     # 'pandas',
                     #
                     # 'pefile',
                     # 'pillow',
                     #
                     # 'pip',
                     #
                     # 'progressbar2',
                     #
                     # 'psutil',
                     #
                     # 'pycparser',
                     # 'pydeprecate',
                     # 'pyinstaller',
                     # 'pyinstaller-hooks-contrib',
                     # 'pyparsing',
                     # 'pyproj',
                     # 'pyside2',
                     # 'python',
                     # 'python-utils',
                     # 'python_abi',
                     # 'pytorch-lightning',
                     # 'pytz',
                     # 'pywavelets',
                     # 'pywin32',
                     # 'pywin32-ctypes',
                     # 'qudida',
                     # 'rasterio',
                     # 'rtree',
                     # 'scikit-image',
                     # 'scikit-learn',
                     # 'scipy',
                     # 'setuptools',
                     # 'shapely',
                     # 'shiboken2',
                     # 'six',
                     # 'slidingwindow',
                     # 'snuggs',
                     # 'sqlite',
                     # 'threadpoolctl',
                     # 'tifffile',
                     # 'tk',
                     # 'torch',
                     # 'torchaudio',
                     # 'torchmetrics',
                     #
                     # 'torchvision',
                     #
                     # 'typing-extensions',
                     #
                     # 'ucrt',
                     #
                     # 'vc',
                     # 'vs2015_runtime',
                     #
                     # 'wheel',
                     # 'whichcraft',
                     # 'xmltodict',
                     # 'xz',
                     #
                     # 'yarl',
                     #
                     # 'zope-event',
                     #
                     # 'zope-interface'
                     ],
        'include_msvcr': True,
        'copy_dependent_files': True,
        # 'include_files': [r'C:\anaconda3\envs\groot2.1_deploy\Library\lib']

    }},
    executables=[Executable("main.py", base="Win32GUI")]
)
