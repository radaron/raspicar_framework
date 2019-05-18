##################
Raspicar framework
##################

***********
Description
***********

This project provides an easy to use sw framework for the
raspicar_application_ project to update automatically the
dependencies and packages. And also this sw trigger the
application. See more details in the application project documentation.

.. _raspicar_application: https://github.com/radaron/raspicar_application

*******
Modules
*******

===============
package_manager
===============

This module is able to manage python packages to
dynamically update them before running the application
or the framework.
By default the object load the 'config.json' in the
package folder, but there is another option to load
custom config file.

===============
package_updater
===============

This module is able to manage repositories to
dynamically update them before running the application.
By default the object load the 'config.json' in the
package folder, but there is another option to load
custom config file.

************
Architecture
************

.. image:: arch.jpg
   :alt: Missing picture
   :align: center

*******
License
*******

MIT License

Copyright (c) 2019 Aron Radics

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
