# Simple Quaternions (`squaternion`)

[![Actions Status](https://github.com/MomsFriendlyRobotCompany/squaternion/workflows/CheckPackage/badge.svg)](https://github.com/MomsFriendlyRobotCompany/squaternion/actions)
![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/squaternion)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/squaternion)
![PyPI](https://img.shields.io/pypi/v/squaternion)

Generally I don't need all of the capabilities (or complexity) of `quaternion`
math libraries. Basically I just need a way to convert between Euler and
Quaternion representations and have a nice way to print them out.

## Install

  pip install squaternion

## Usage

This is all this library does, convert between Euler angles and Quaternions.
There are other libraries that do so much more ... but I don't need all of that.

```python
from squaternion import euler2quat, quat2euler, Quaternion

# if you know the values you want Quaternion(w, x, y, z), note this is a
# namedtuple so it is immutable once created
q = Quaternion(1,0,0,0)

# however you typically don't think in 4 dimensions, so create from
# euler angles euler2quat(roll, pitch, yaw), default is radians, but set
# degrees true if giving degrees
q = euler2quat(0, -90, 100, degrees=True)

# can get the euler angles back out in degrees (set to True)
e = quat2euler(*q, degrees=True)
```

## References

- [Wikipedia Convert Between Quaternions and Euler Angles](https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles)
- [Wikipedia Euler Angle Definitions](https://en.wikipedia.org/wiki/Euler_angles#Conventions_2)
- [Wikipedia Gimbal Lock](https://en.wikipedia.org/wiki/Gimbal_lock)

# MIT License

Copyright (c) 2018 Kevin Walchko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
