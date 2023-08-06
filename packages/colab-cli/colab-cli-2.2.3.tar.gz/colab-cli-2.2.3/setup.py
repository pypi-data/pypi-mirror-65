# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colab_cli', 'colab_cli.utilities']

package_data = \
{'': ['*']}

install_requires = \
['Send2Trash>=1.5.0,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'pydrive>=1.3.1,<2.0.0',
 'typer[all]>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['colab-cli = colab_cli.main:app']}

setup_kwargs = {
    'name': 'colab-cli',
    'version': '2.2.3',
    'description': 'Experience better workflow with google colab, local jupyter notebooks and git',
    'long_description': "# Welcome to colab-cli 👋\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://choosealicense.com/licenses/mit/)\n[![Twitter: aks2899](https://img.shields.io/twitter/follow/aks2899.svg?style=social)](https://twitter.com/aks2899)\n\n> Experience better workflow with google colab, local jupyter notebooks and git\n\nYou can now easily manage working with jupyter notebooks \nand google colab from cli. \n\n# Features \n* 🤠 Upload local jupyter notebook to gdrive from cli\n* 😮 Quick access to jupyter notebooks in gdrive from your cli\n* 🚀 Keeps jupyter notebooks organized in gdrive by creating local file structure in gdrive\n* 🤯 Sync local work on notebooks with gdrive\n* 🥂 Git friendly, pull changes from gdrive and commit to git\n\n### ✨ Demo\n[![demo](https://asciinema.org/a/314749.svg)](https://asciinema.org/a/314749?autoplay=1)\n\n## Install\n\n```sh\npip3 install colab-cli\n```\n\n## Set-up\n\nSTEP-1: \n \nFirst we need to get your client_secrets.json file for \nOAuth2.0 authentication for Drive API,\n\n1. Go to [APIs Console](https://console.developers.google.com/iam-admin/projects) \nand make your own project.\n2. Search for ‘Google Drive API’, select the entry, and click ‘Enable’.\n3. Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.\n4. Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and follow the instructions. Once finished:\n    \n    a. Select ‘Application type’ to be Web application.\n    \n    b. Enter an appropriate name.\n    \n    c. Input http://localhost:8080 for ‘Authorized JavaScript origins’.\n    \n    d. Input http://localhost:8080/ for ‘Authorized redirect URIs’.\n    \n    e. Click ‘Save’.\n    \n5. Click ‘Download JSON’ on the right side of Client ID to \ndownload client_secret_\\<really long ID>.json.\n\n6. Rename the file to “client_secrets.json” and place it in any directory.\n\nSTEP-2: \n\n Go to the local directory with client_secrets.json\n  ```sh\n  colab-cli set-config client_secrets.json\n  ```\nSTEP-3:\n \nNow we need to set the google account user id, goto your browser and see how many google logins you have,\n the count start from zero\n \n for eg. I have 3 login and I use the second one for coding work, so my user id is 1\n  ```sh\n  colab-cli set-auth-user 1\n  ```\n \n🙌 Now You're all set to go\n## Usage\n\n```sh\ncolab-cli --help\n``` \n* List local ipynb\n```sh\ncolab-cli list-nb\n``` \nNOTE : Please work with git repo initialized, else below \ncommands will not work\n\n* Open local ipynb file in google colab for first time\n> Note: It opens the copy of file in gdrive from second time onwards.\n```sh\ncolab-cli open-nb lesson1-pets.ipynb\n``` \n* If you need to get modified ipynb from gdrive local directory use \n```sh\ncolab-cli pull-nb lesson1-pets.ipynb\n``` \n* Made some changes to ipynb locally, push it to gdrive\n```sh\ncolab-cli push-nb lesson1-pets.ipynb\n``` \n* To make a new notebook, you can use\n```sh\ncolab-cli new-nb my_nb.ipynb\n``` \n\n\n## Author\n\n👤 **Akshay Ashok**\n\n* Twitter: [@aks2899](https://twitter.com/aks2899)\n* Github: [@Akshay090](https://github.com/Akshay090)\n* LinkedIn: [@akshay-a](https://linkedin.com/in/akshay-a)\n\n## 🤝 Contributing\n\nContributions, issues and feature requests are welcome!\n\nFeel free to check [issues page](https://github.com/Akshay090/colab-cli/issues). You can also take a look at the [contributing guide](https://github.com/Akshay090/colab-cli/blob/master/CONTRIBUTING.md).\n\n## Show your support\n\nGive a 🌟 if this project helped you!\n\n## 📝 License\n\nCopyright © 2020 [Akshay Ashok](https://github.com/Akshay090).\n\nThis project is [MIT](https://choosealicense.com/licenses/mit/) licensed.\n\n***\n_This README was generated with ❤ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n",
    'author': 'Akshay Ashok',
    'author_email': 'aks28id@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
