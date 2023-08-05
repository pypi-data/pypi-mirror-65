![img](https://img.shields.io/gitlab/pipeline/ymd_h/cpprb.svg)
![img](https://img.shields.io/pypi/v/cpprb.svg)
![img](https://img.shields.io/pypi/l/cpprb.svg)
![img](https://img.shields.io/pypi/status/cpprb.svg)
[![img](https://gitlab.com/ymd_h/cpprb/badges/master/coverage.svg)](https://ymd_h.gitlab.io/cpprb/coverage/)

![img](./site/static/images/favicon.png)


# Overview

cpprb is a python ([CPython](https://github.com/python/cpython/tree/master/Python)) module providing replay buffer classes for
reinforcement learning.

Major target users are researchers and library developers.

You can build your own reinforcement learning algorithms together with
your favorite deep learning library (e.g. [TensorFlow](https://www.tensorflow.org/), [PyTorch](https://pytorch.org/)).

cpprb forcuses speed, flexibility, and memory efficiency.

By utilizing [Cython](https://cython.org/), complicated calculations (e.g. segment tree for
prioritized experience replay) are offloaded onto C++.
(The name cpprb comes from "C++ Replay Buffer".)

In terms of API, initially cpprb referred to [OpenAI Baselines](https://github.com/openai/baselines)'
implementation. In the current version, cpprb has much more
flexibility. Any [NumPy](https://numpy.org/) compatible types of any numbers of values can
be stored (as long as memory capacity is sufficient). For example, you
can store the next action and the next next observation, too.


# Installation

cpprb requires following softwares before installation.

-   C++17 compiler (for installation from source)
    -   [GCC](https://gcc.gnu.org/) (maybe 7.2 and newer)
    -   [Visual Studio](https://visualstudio.microsoft.com/) (2017 Enterprise is fine)
-   Python 3
-   pip

Cuurently, [clang](https://clang.llvm.org/), which is a default Xcode C/C++ compiler at Apple macOS,
cannot compile cpprb.

If you are macOS user, you need to install GCC and set environment values
of `CC` and `CXX` to `g++`, or just use virtual environment (e.g. [Docker](https://www.docker.com/)).

Step by step installation is described [here](https://ymd_h.gitlab.io/cpprb/installation/install_on_macos/).

Additionally, here are user's good feedbacks for installation at [macOS](https://github.com/keiohta/tf2rl/issues/75) and [Ubuntu](https://gitlab.com/ymd_h/cpprb/issues/73).
(Thanks!)


## Install from [PyPI](https://pypi.org/) (Recommended)

The following command installs cpprb together with other dependancies.

    pip install cpprb

Depending on your environment, you might need `sudo` or `--user` flag
for installation.

On supported platflorms (Linux x86-64 and Windows amd64), binary
packages are hosted on PyPI can be used, so that you don't need C++ compiler.

If you have trouble to install from binary, you can fall back to
source installation to passk `--no-binary` option to the above pip command.

Currently, no other platforms, such as macOS, and 32bit or
arm-architectured Linux and Windows, cannot install from binary, and
need to compile by yourself. Please be patient, we will plan to
support wider platforms in future.


## Install from source code

First, download source code manually or clone the repository;

    git clone https://gitlab.com/ymd_h/cpprb.git

Then you can install same way;

    cd cpprb
    pip install .

For this installation, you need to convert extended Python (.pyx) to
C++ (.cpp) during installation, it takes longer time than installation
from PyPI.


# Usage

Here is a simple example for storing standard environment (aka. "obs",
"act", "rew", "next<sub>obs</sub>", and "done").

    from cpprb import ReplayBuffer
    
    buffer_size = 256
    obs_shape = 3
    act_dim = 1
    rb = ReplayBuffer(buffer_size,
    		  env_dict ={"obs": {"shape": obs_shape},
    			     "act": {"shape": act_dim},
    			     "rew": {},
    			     "next_obs": {"shape": obs_shape},
    			     "done": {}})
    
    obs = np.ones(shape=(obs_shape))
    act = np.ones(shape=(act_dim))
    rew = 0
    next_obs = np.ones(shape=(obs_shape))
    done = 0
    
    for i in range(500):
        rb.add(obs=obs,act=act,rew=rew,next_obs=next_obs,done=done)
    
    
    batch_size = 32
    sample = rb.sample(batch_size)
    # sample is a dictionary whose keys are 'obs', 'act', 'rew', 'next_obs', and 'done'

Flexible environment values are defined by `env_dict` when buffer creation.

Since stored values have flexible name, you have to pass to
`ReplayBuffer.add` member by keyword.


# Features

cpprb provides buffer classes for building following algorithms.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Algorithms</th>
<th scope="col" class="org-left">cpprb class</th>
<th scope="col" class="org-left">Paper</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">Experience Replay</td>
<td class="org-left">`ReplayBuffer`</td>
<td class="org-left">[L. J. Lin](https://link.springer.com/article/10.1007/BF00992699)</td>
</tr>


<tr>
<td class="org-left">Prioritized Experience Replay</td>
<td class="org-left">`PrioritizedReplayBuffer`</td>
<td class="org-left">[T. Schaul et. al.](https://arxiv.org/abs/1511.05952)</td>
</tr>


<tr>
<td class="org-left">Multi-step Learning</td>
<td class="org-left">`ReplayBuffer`, `PrioritizedReplayBuffer`</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>

cpprb features and its usage are described at following pages:

-   [Flexible Environment](https://ymd_h.gitlab.io/cpprb/features/flexible_environment/)
-   [Multi-step add](https://ymd_h.gitlab.io/cpprb/features/multistep_add/)
-   [Prioritized Experience Replay](https://ymd_h.gitlab.io/cpprb/features/per/)
-   [Nstep Experience Replay](https://ymd_h.gitlab.io/cpprb/features/nstep/)
-   [Memory Compression](https://ymd_h.gitlab.io/cpprb/features/memory_compression/)


# Contributing to cpprb

Any contribution are very welcome!


## Making Community Larger

Bigger commumity makes development more active and improve cpprb.

-   Star this repository (and/or [GitHub Mirror](https://github.com/yamada-github-account/cpprb))
-   Publish your code using cpprb
-   Share this repository to your friend and/or followers.


## Report Issue

When you have any problems or requests, you can check [issues on GitLab.com](https://gitlab.com/ymd_h/cpprb/issues).
If you still cannot find any information, you can open your own issue.


## Merge Request (Pull Request)

cpprb follows local rules:

-   Branch Name
    -   "HotFix<sub>\*</sub>\*\*" for bug fix
    -   "Feature<sub>\*</sub>\*\*" for new feature implementation
-   docstring
    -   Must for external API
    -   [Numpy Style](https://numpydoc.readthedocs.io/en/latest/format.html)
-   Unit Test
    -   Put test code under "test/" directory
    -   Can test by `python -m unittest <Your Test Code>` command
    -   Continuous Integration on GitLab CI configured by `.gitlab-ci.yaml`
-   Open an issue and associate it to Merge Request

Step by step instruction for beginners is described at [here](https://ymd_h.gitlab.io/cpprb/contributing/merge_request).


# Links


## cpprb sites

-   [Project Site](https://ymd_h.gitlab.io/cpprb/)
    -   [Class Reference](https://ymd_h.gitlab.io/cpprb/api/)
    -   [Unit Test Coverage](https://ymd_h.gitlab.io/cpprb/coverage/)
-   [Main Repository](https://gitlab.com/ymd_h/cpprb)
-   [Github Mirror](https://github.com/yamada-github-account/cpprb)
-   [cpprb on PyPI](https://pypi.org/project/cpprb/)


## cpprb users' repositories

-   **[keiohta/TF2RL](https://github.com/keiohta/tf2rl):** TensorFlow2.0 Reinforcement Learning


# Lisence

cpprb is available under MIT lisence.

