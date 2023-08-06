# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fingertip',
 'fingertip.plugins',
 'fingertip.plugins.backend',
 'fingertip.plugins.os',
 'fingertip.plugins.self_test',
 'fingertip.util']

package_data = \
{'': ['*']}

install_requires = \
['CacheControl>=0.12.6,<0.13.0',
 'GitPython>=3.1.0,<4.0.0',
 'cloudpickle>=1.3.0,<2.0.0',
 'colorlog>=4.1.0,<5.0.0',
 'fasteners>=0.15,<0.16',
 'lockfile>=0.12.2,<0.13.0',
 'paramiko>=2.7.1,<3.0.0',
 'pexpect>=4.8.0,<5.0.0',
 'pyxdg>=0.26,<0.27',
 'requests-mock>=1.7.0,<2.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['fingertip = fingertip.main:main']}

setup_kwargs = {
    'name': 'fingertip',
    'version': '0.2.0',
    'description': 'Control VMs, containers and other machines with Python, leverage live snapshots',
    'long_description': '`fingertip`\n-----------\n\nThis program/library aims to be a way to:\n\n* fire up VMs and containers in mere seconds using live VM snapshots\n* uniformly control machines from Python by writing small and neat functions\n  transforming them\n* compose and transparently cache the results of these functions\n* build cool apps that exploit live VM snapshots and checkpoints\n* control other types of machines that are not local VMs\n\nAll while striving to be intentionally underengineered\nand imposing as few limits as possible.\nIf you look at it and think that it does nothing in the laziest way possible,\nthat\'s it.\n\nIt\'s currently in alpha stage.\n\n# Teaser\n\nSome examples of executing it from your shell:\n\n``` bash\n$ fingertip os.fedora + ssh  # install Fedora and SSH into it\n$ fingertip os.alpine + console  # install Alpine, access serial console\n$ fingertip os.alpine + ansible package --state=present --name=patch + ssh\n$ fingertip backend.podman-criu + os.alpine + console  # containers!\n```\n\nAn example of Python usage and writing your own steps:\n\n``` python\nimport fingertip\n\ndef main(m=None, alias=\'itself\'):\n    m = m or fingertip.build(\'os.fedora\')\n    m = m.apply(\'ansible\', \'lineinfile\', path=\'/etc/hosts\',\n                line=f\'127.0.0.1 {alias}\')\n    with m:\n        assert \'1 received\' in m(f\'ping -c1 {alias}\').out\n    return m\n```\n\nPut in `fingertip/plugins/demo.py`,\nthis can be now be used in pipelines:\n```\n$ fingertip demo\n$ fingertip os.fedora + demo me\n$ fingertip os.alpine + demo --alias=myself + ssh\n```\n\n## Installation\n\nRefer to [INSTALL.md](INSTALL.md).\n\n\n### Shell usage\n\nIf you have installed fingertip, invoke it as `fingertip`.\n\nIf you\'re running from a checkout, use `python3 <path to checkout>` instead\nor make an alias.\n\nIf you\'re using a containerized version, invoke `fingertip-containerized`\n(and hope for the best).\n\nSo,\n\n``` bash\n$ fingertip os.fedora + ssh\n```\n\nYou should observe Fedora installation starting up, then shutting down,\ncompressing an image, booting up again and, finally,\ngiving you interactive control over the machine over SSH.\n\nInvoke the same command again, and it should do nearly nothing, as\nthe downloads and the installation are already cached\nin `~/.cache/fingertip`.\nEnjoy fresh clean VMs brought up in mere seconds.\nFeel like they\'re already at your fingertips.\nControl them from console or from Python.\n\n\n## Python usage\n\nLet\'s see how manipulating machines can look like\n(`fingertip/plugins/self_test/greeting.py`):\n\n``` python\ndef make_greeting(m, greeting=\'Hello!\'):                      # take a machine\n    with m:                                                   # start if needed\n        m.console.sendline(f"echo \'{greeting}\' > .greeting")  # type a command\n        m.console.expect_exact(m.prompt)                      # wait for prompt\n    return m                                                  # cache result\n\n\n@fingertip.transient                                          # don\'t lock/save\ndef main(m, greeting=\'Hello!\'):                               # take a machine\n    m = m.apply(make_greeting, greeting=greeting)             # use cached step\n    with m:                                                   # start if needed\n        assert m(\'cat .greeting\').out.strip() == greeting     # execute command\n                                                              # do not save\n```\n\n\nThese are regular Python functions, nothing fancy.\nEven this `@fingertip.transient` thing is an optimization-only hint.\nYou can just pass them `fingertip.build(\'fedora\')` and that\'ll work.\n\nHere\'s what can happen inside such a function:\n\n* It accepts a machine as the first argument\n  (which may be already spun up or not, you don\'t know).\n* It inspects it and applies more functions if it wants to,\n  (extra steps applied through `.apply` are cached / reused if it\'s possible).\n* Should any custom steps or changes be applied,\n  the machine must be first spun up using a `with` block (`with m as m`).\n  All modifications to the machine must happen inside that block,\n  or risk being silently undone!\n* Return the machine if the result should be cached and used for the next steps.\n  Not returning one can and usually will undo all the changes you\'ve made.\n  If you don\'t intend to save the result, don\'t return m;\n  additionally, decorate the function with `@fingertip.transient`\n  or at least use `.transient()` with `with`,\n  so that fingertip can apply performance optimizations and be even faster.\n\nThe first function in the chain (or the one used in `fingertip.build`)\nwill not get a machine as the first argument.\nTo write a universal function, just use:\n``` python\ndef func(m=None):\n    m = m or fingertip.build(\'fedora\')\n    ...\n```\n\n\n## Disclaimer\n\nDue to what exactly I cache and the early stage of development,\nempty your `~/.cache/fingertip/machines` often, at least after each update.\n\n``` bash\n$ fingertip cleanup machines all\n```\n\nSome days the whole `~/.cache/fingertip` has to go.\n\n``` bash\n$ fingertip cleanup all\n```\n',
    'author': 'Alexander Sosedkin',
    'author_email': 'asosedki@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/t184256/fingertip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
