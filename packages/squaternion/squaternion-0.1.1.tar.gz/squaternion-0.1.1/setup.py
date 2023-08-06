# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squaternion']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata']

setup_kwargs = {
    'name': 'squaternion',
    'version': '0.1.1',
    'description': 'Some simple functions for quaternion math',
    'long_description': '# Simple Quaternions (`squaternion`)\n\nGenerally I don\'t need all of the capabilities (or complexity) of `quaternion`\nmath libraries. Basically I just need a way to convert between Euler and\nQuaternion representations and have a nice way to print them out.\n\n## Install\n\n  pip install squaternion\n\n## Usage\n\nThis is all this library does, convert between Euler angles and Quaternions.\nThere are other libraries that do so much more ... but I don\'t need all of that.\n\n```python\nfrom squaternion import euler2quat, quat2euler, Quaternion\n\n# if you know the values you want Quaternion(w, x, y, z), note this is a\n# namedtuple so it is immutable once created\nq = Quaternion(1,0,0,0)\n\n# however you typically don\'t think in 4 dimensions, so create from\n# euler angles euler2quat(roll, pitch, yaw), default is radians, but set\n# degrees true if giving degrees\nq = euler2quat(0, -90, 100, degrees=True)\n\n# can get the euler angles back out in degrees (set to True)\ne = quat2euler(*q, degrees=True)\n```\n\n## References\n\n- [Wikipedia Convert Between Quaternions and Euler Angles](https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles)\n- [Wikipedia Euler Angle Definitions](https://en.wikipedia.org/wiki/Euler_angles#Conventions_2)\n- [Wikipedia Gimbal Lock](https://en.wikipedia.org/wiki/Gimbal_lock)\n\n# MIT License\n\nCopyright (c) 2018 Kevin Walchko\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/squaternion/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
