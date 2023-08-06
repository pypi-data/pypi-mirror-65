# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['displayarray',
 'displayarray.effects',
 'displayarray.frame',
 'displayarray.window']

package_data = \
{'': ['*']}

install_requires = \
['docopt==0.6.2',
 'localpubsub==0.0.4',
 'numpy==1.16.1',
 'opencv_python',
 'pyzmq==18.1.0']

entry_points = \
{'console_scripts': ['displayarray = displayarray.__main__:main']}

setup_kwargs = {
    'name': 'displayarray',
    'version': '0.7.5',
    'description': 'Tool for displaying numpy arrays.',
    'long_description': 'displayarray\n============\n\nA library for displaying arrays as video in Python.\n\nDisplay arrays while updating them\n----------------------------------\n\n.. figure:: https://i.imgur.com/UEt6iR6.gif\n   :alt: \n\n::\n\n    from displayarray import display\n    import numpy as np\n\n    arr = np.random.normal(0.5, 0.1, (100, 100, 3))\n\n    with display(arr) as d:\n        while d:\n            arr[:] += np.random.normal(0.001, 0.0005, (100, 100, 3))\n            arr %= 1.0\n\nRun functions on 60fps webcam or video input\n--------------------------------------------\n\n|image0|\n\n(Video Source: https://www.youtube.com/watch?v=WgXQ59rg0GM)\n\n::\n\n    from displayarray import display\n    import math as m\n\n    def forest_color(arr):\n        forest_color.i += 1\n        arr[..., 0] = (m.sin(forest_color.i*(2*m.pi)*4/360)*255 + arr[..., 0]) % 255\n        arr[..., 1] = (m.sin((forest_color.i * (2 * m.pi) * 5 + 45) / 360) * 255 + arr[..., 1]) % 255\n        arr[..., 2] = (m.cos(forest_color.i*(2*m.pi)*3/360)*255 + arr[..., 2]) % 255\n\n    forest_color.i = 0\n\n    display("fractal test.mp4", callbacks=forest_color, blocking=True, fps_limit=120)\n\nDisplay tensors as they\'re running through TensorFlow or PyTorch\n----------------------------------------------------------------\n\n.. figure:: https://i.imgur.com/TejCpIP.png\n   :alt: \n\n::\n\n    # see test_display_tensorflow in test_simple_apy for full code.\n\n    ...\n\n    autoencoder.compile(loss="mse", optimizer="adam")\n\n    while displayer:\n        grab = tf.convert_to_tensor(\n            displayer.FRAME_DICT["fractal test.mp4frame"][np.newaxis, ...].astype(np.float32)\n            / 255.0\n        )\n        grab_noise = tf.convert_to_tensor(\n            (((displayer.FRAME_DICT["fractal test.mp4frame"][np.newaxis, ...].astype(\n                np.float32) + np.random.uniform(0, 255, grab.shape)) / 2) % 255)\n            / 255.0\n        )\n        displayer.update((grab_noise.numpy()[0] * 255.0).astype(np.uint8), "uid for grab noise")\n        autoencoder.fit(grab_noise, grab, steps_per_epoch=1, epochs=1)\n        output_image = autoencoder.predict(grab, steps=1)\n        displayer.update((output_image[0] * 255.0).astype(np.uint8), "uid for autoencoder output")\n\nHandle input events\n-------------------\n\nMouse events captured whenever the mouse moves over the window:\n\n::\n\n    event:0\n    x,y:133,387\n    flags:0\n    param:None\n\nCode:\n\n::\n\n    from displayarray.input import mouse_loop\n    from displayarray import display\n\n    @mouse_loop\n    def print_mouse_thread(mouse_event):\n        print(mouse_event)\n\n    display("fractal test.mp4", blocking=True)\n\nInstallation\n------------\n\ndisplayarray is distributed on `PyPI <https://pypi.org>`__ as a\nuniversal wheel in Python 3.6+ and PyPy.\n\n::\n\n    $ pip install displayarray\n\nUsage\n-----\n\nAPI has been generated `here <https://simleek.github.io/displayarray/index.html>`_.\n\nSee tests and examples for example usage.\n\nLicense\n-------\n\ndisplayarray is distributed under the terms of both\n\n-  `MIT License <https://choosealicense.com/licenses/mit>`__\n-  `Apache License, Version\n   2.0 <https://choosealicense.com/licenses/apache-2.0>`__\n\nat your option.\n\n.. |image0| image:: https://thumbs.gfycat.com/AbsoluteEarnestEelelephant-size_restricted.gif\n   :target: https://gfycat.com/absoluteearnesteelelephant\n',
    'author': 'SimLeek',
    'author_email': 'simulator.leek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simleek/displayarray',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
