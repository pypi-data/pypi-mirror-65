# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gyakujinton', 'gyakujinton.Shape', 'gyakujinton.Window']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.2,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'scikit-image>=0.16.2,<0.17.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['gyakujinton = gyakujinton.cli:cli']}

setup_kwargs = {
    'name': 'gyakujinton',
    'version': '0.3.3',
    'description': '',
    'long_description': '# Gyaku Jinton\n\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/gyakujinton)](https://pypi.python.org/pypi/gyakujinton/)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/mamerisawesome/gyakujinton/graphs/commit-activity)\n[![Awesome Badges](https://img.shields.io/badge/badges-awesome-green.svg)](https://github.com/Naereen/badges)\n\nOpenCV wrapper to handle shapes and images.\n\n## Installation\n\nJust execute the command below and do the jutsus below!\n\n```bash\npip install gyakujinton\n```\n\n## Pre-requisites\n\n* Python 3.6.1 or higher\n* OpenCV\n\nI suggest to check OpenCV\'s [tutorials](https://docs.opencv.org/master/da/df6/tutorial_py_table_of_contents_setup.htmlv) on installation to help you.\n\n## Programmatic\n\n### Drawing a polygon on image\n\nGiven an image path, by identifying points in the image, you can draw line based on given point.\n\nIf `color` is added as argument, it will also draw those lines by that color. The color is in RGB format.\n\nIf `output_path` is not defined, the application will create an application window with the modified image.\n\n```python\nfrom gyakujinton import draw_on_image\ndraw_on_image(\n    image_path="/path/to/file.filetype",\n    output_path="/path/to/output-file.filetype",  #optional\n    points=[[INT, INT], ..., [INT, INT]],  # points on a 2D plane\n    color=(0, 0, 0)  # in RGB; optional\n)\n```\n\n### Distorting an image\n\nGiven an image path, this image will be the basis for distortion. The distortion will be from mimimum distortion of 10% to a maximum distortion of 40%. This number is identified in randomly.\n\nA `patch` parameter can be defined to focus on an area in an image. This will "crop" the image based on the input patch. This patch should be a rectangle for a proper distortion to take place.\n\nIf `output_path` is not defined, the application will create an application window with the modified image.\n\n```python\nfrom gyakujinton import skew_image\nskew_image(\n    image_path="/path/to/file.filetype",\n    output_path="/path/to/output-file.filetype",  #optional\n    patch=[[INT, INT], ..., [INT, INT]],  # points on a 2D plane\n)\n```\n\n> Note: The window that will be created will not consider alpha values. As such, to see transparency it is recommended to save the file in PNG format.\n\n## Command-line Interface\n\nThe application also allows executions through the CLI.\n\n### Drawing a polygon on image (CLI)\n\nThe example below gets the image based on the path given and will draw a polygon based on the input points.\n\n```bash\ngyakujinton draw_on_image /path/to/file.filetype --points 100,100 200,100 200,200 100,200\n```\n\nWe can also define an output path by adding the argument `-o` or `--output_path` followed by the file path.\n\n```bash\ngyakujinton draw_on_image /path/to/file.filetype --points 100,100 200,100 200,200 100,200 --output_path /path/to/output-file.filetype\n```\n\n### Distorting an image (CLI)\n\nA proof-of-concept is created within the application to distort the skew the input image.\n\n```bash\ngyakujinton distory /path/to/file.filetype --patch 10,10 10,400 400,400 400,10\n```\n\nSimilar to previous functions, an output path can be set to write the image into a file.\n\n> Note: The window that will be created will not consider alpha values. As such, to see transparency it is recommended to save the file in PNG format.\n\n## Sample\n\nTo test out the application, we\'ll be using an [image by Samantha Gades](https://unsplash.com/photos/BlIhVfXbi9s) taken from Unsplash. We have this beautiful and simple original image.\n\n![Original Image](https://raw.githubusercontent.com/mamerisawesome/gyakujinton/master/sample/samantha-gades-unsplash.jpg)\n\nWe can draw a polygon near the clock by doing the following in the command-line:\n\n```bash\ngyakujinton draw_on_image sample/samantha-gades-unsplash.jpg --points 150,150 150,250 250,250 250,150\n```\n\n![Modified Image](https://raw.githubusercontent.com/mamerisawesome/gyakujinton/master/sample/output.jpg)\n\nAgain, we are not restricted with the polygon that we want to create. It all depends on where we put the points and how they are ordered when lines are to be drawn.\n\n```bash\ngyakujinton draw_on_image sample/samantha-gades-unsplash.jpg --points 100,100 100,150 180,200 250,150 250,100 180,50 -o output-2.jpg\n```\n\n![Modified Image 2](https://raw.githubusercontent.com/mamerisawesome/gyakujinton/master/sample/output-2.jpg)\n\nWe can also test out the created function for image distortion.\n\n```bash\ngyakujinton distort sample/samantha-gades-unsplash.jpg --patch 10,10 10,400 400,400 400,10 -o output.distort.jpg\n```\n\n![Modified Image 3](https://raw.githubusercontent.com/mamerisawesome/gyakujinton/master/sample/output.distort.png)\n\n## Name Inspiration\n\n![Ohnoki\'s Dust Release](https://vignette.wikia.nocookie.net/naruto/images/2/20/Dust_Release.png/revision/latest/scale-to-width-down/1000?cb=20150123214535)\n\n> Source: naruto.fandom.com/wiki\n\nWhen thinking of a name for the app, the first thing that came into mind is Ohnoki\'s [Particle Style (or Dust Release) Atomic Dismantling Jutsu](https://naruto.fandom.com/wiki/Dust_Release:_Detachment_of_the_Primitive_World_Technique) from [Naruto](https://www.viz.com/naruto) which is a technique that has a sphere in the center contained by a geometric object. In the series, dust release is called `Jinton` which was chosen due to how amazed I am on the shapes happening.\n\nNow, with the points above, the technique is used to dismantle atoms to dust. `Gyaku` (or reverse as taught to me by [Google Translate](https://translate.google.com/?gs_lcp=CgZwc3ktYWIQAzIICCEQFhAdEB46BQgAEIMBOgIIADoECAAQCjoFCAAQxAI6CAgAEBYQChAeOgYIABAWEB46BAghEApQ8ghYqDFgxjJoAnAAeACAAZ4BiAG7HpIBBDAuMzGYAQCgAQGqAQdnd3Mtd2l6&uact=5&um=1&ie=UTF-8&hl=en&client=tw-ob#auto/ja/reverse)) was added to signify making of shapes and images rather than dismantling them.\n\nHence, the app name `Gyaku Jinton`.\n\n## Author\n\nAlmer Mendoza\n',
    'author': 'Almer Mendoza',
    'author_email': 'atmalmer23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mamerisawesome/gyakujinton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
