# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d3ploy']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.38,<2.0.0', 'pathspec>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['d3ploy = d3ploy.d3ploy:cli']}

setup_kwargs = {
    'name': 'd3ploy',
    'version': '3.0.5',
    'description': 'Easily deploy to S3 with multiple environment support.',
    'long_description': '# d3ploy\n\nEasily deploy to S3 with multiple environment support. Version 3 supports Python 3.6+.\n\n## Installation & Usage\n\nTo install, run `pip install d3ploy`.\nTo use, run `d3ploy`. Additional arguments may be specified. Run `d3ploy --help` for more information.\n\n## Authentication\n\nYour AWS credentials can be set in a number of ways:\n\n1. In a ".boto" file in your home folder. See [Boto\'s documentation](http://docs.pythonboto.org/en/latest/boto_config_tut.html) for how to create this file.\n2. In a ".aws" file in the folder you\'re running `d3ploy` in. Follows the same format as ".boto".\n3. In the environment variables "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY".\n\n## Configuration options\n\nWhen you run `d3ploy`, it will look in the current directory for a ".d3ploy.json" file that defines the different deploy enviroments and their options. At a minimum, a "default" environment is required and is the environment used if you pass no arguments to `d3ploy`. Additionally, you may pass in a different path for you config file with the `-c` or `--config` options.\n\nTo supress all output, pass `-q` or `--quiet` to the command. Note that there is not a way to set the quiet option in the config file(s).\n\nTo set the number of separate processes to use, pass `-p 10` or `--processess 10` where \'10\' is the number to use. If you do not want to use multiple processes, set this to \'0\'.\n\nYou can add as many environments as needed. Deploy to an environment by passing in its key like `d3ploy staging`. As of version 3.0, environments no longer inherit settings from the default environment. Instead, a separate `defaults` object in the config file can be used to set options across all environments.\n\nThe only required option for any environment is "bucket_name" for the S3 bucket to upload to. Additionally, you may define:\n\n- "local_path" to upload only the contents of a directory under the current one; defaults to "." (current directory)\n- "bucket_path" to upload to a subfolder in the bucket; defaults to "/" (root)\n- "exclude" to specify patterns to not upload\n- "acl" to specify the canned ACL set on each object. See https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl.\n- "delete" to remove files on S3 that are not present in the local directory\n- "charset" to set the charset flag on \'Content-Type\' headers of text files\n- "caches" to set the Cache-Control header for various mimetypes. See below for more.\n- "gitignore" to add all entries in a .gitignore file to the exclude patterns\n- "cloudfront_id" to invalidate all paths in the given CloudFront distribution IDs. Can be a string for one distribution or an array for multiple.\n\n### Example .d3ploy.json\n\n```json\n{\n  "environments": {\n    "default": {\n      "bucket_name": "d3ploy-tests",\n      "local_path": "./tests/files",\n      "bucket_path": "/default/"\n    },\n    "staging": {\n      "bucket_name": "d3ploy-tests",\n      "local_path": "./tests/files",\n      "bucket_path": "/staging/"\n    }\n  },\n  "defaults": {\n    "caches": {\n      "text/javascript": 2592000,\n      "image/gif": 22896000,\n      "image/jpeg": 22896000,\n      "image/png": 22896000,\n      "image/webp": 22896000,\n      "text/*": 2592000,\n      "text/html": 0,\n      "text/plain": 0\n    }\n  }\n}\n```\n\n## Cache-Control Headers\n\nIf you want to set Cache-Control headers on various files, add a `caches` object to your config file like:\n\n```\n"caches": {\n  "text/javascript": 2592000,\n  "image/gif": 22896000,\n  "image/jpeg": 22896000,\n  "image/png": 22896000,\n  "image/webp": 22896000,\n  "text/*": 2592000,\n  "text/html": 0,\n  "text/plain": 0\n}\n```\n\nEach key is the mimetype of the kind of file you want to have cached, with a value that is the seconds the `max-age` flag set to. In the above example, CSS and JavaScript files will be cached for 30 days, images will be cached for 1 year, and html files will not be cached. For more about Cache-Control, read [Leverage Browser Caching](https://developers.google.com/speed/docs/insights/LeverageBrowserCaching). You may use wildcards like `image/*` to apply to all images. If there\'s a more specific match for a particular image type, that will override the wildcard. For example:\n\n```\n"caches": {\n  "image/png": 300,\n  "image/*": 31536000\n}\n```\n\nIn this case JPGs, GIFs and all other images except for PNGs will be cached for 1 year. PNGs, however, will be cached for 5 minutes.\n\n## macOS Notification Center\n\nd3ploy will attempt to alert you via Notification Center when it is completed. To enable this feature run `pip install d3ploy[notifications]`.\n\n## Progress Bar\n\nd3ploy will use the `progressbar2` module if it\'s available to display output. This includes a percentage completed and an ETA. To enable, run `pip install d3ploy[progress]`.\n\n## Caution About Using the gzip Option\n\nAlmost all modern browsers will support files that are served with gzip compression. The notable exception is non-smartphone mobile browsers. If you have significant traffic over those browsers, it is advisable to avoid the gzip option. Additionally, your CDN make offer compression on-the-fly for you; this is the preferred method when available.\n',
    'author': 'dryan',
    'author_email': 'dryan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dryan/d3ploy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
