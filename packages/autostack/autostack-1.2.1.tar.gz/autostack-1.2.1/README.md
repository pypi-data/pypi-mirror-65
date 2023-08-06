![Logo](https://raw.githubusercontent.com/autostack-team/autostack/develop/Logo.png)

<p align="center">
    <a href="https://travis-ci.com/autostack-team/autostack/">
        <img src="https://travis-ci.com/autostack-team/autostack.svg?branch=master"
            alt="Build status"/>
    </a>
    <a href="https://codeclimate.com/github/autostack-team/autostack/test_coverage">
        <img src="https://api.codeclimate.com/v1/badges/4dc7775be0fef62e5492/test_coverage" 
            alt="Code coverage"/>
    </a>
    <a href="https://codeclimate.com/github/autostack-team/autostack/maintainability">
        <img src="https://api.codeclimate.com/v1/badges/4dc7775be0fef62e5492/maintainability" 
            alt="Maintainability"/>
    </a>
    <a href="https://github.com/autostack-team/autostack">
        <img src="https://img.shields.io/github/commit-activity/m/autostack-team/autostack"
            alt="GitHub commit activity"/>
    </a>
    <a href="https://pypi.org/project/autostack/">
        <img src="https://img.shields.io/pypi/dm/autostack"
             alt="PyPI - Downloads"/>
    </a>
    <a href="https://pypi.org/project/autostack/">
        <img src="https://img.shields.io/pypi/v/autostack"
             alt="PyPI"/>
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-orange.svg"
             alt="License"/>
    </a>
    <a href="https://gitter.im/autostack-team/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link">
        <img src="https://badges.gitter.im/autostack-team/community.svg"
             alt="Chat"/>
    </a>
    <a href="https://twitter.com/intent/follow?screen_name=autostackteam">
        <img src="https://img.shields.io/twitter/follow/autostackteam.svg?style=social&logo=twitter"
             alt="Follow on Twitter"/>
    </a>
    <a href="https://www.patreon.com/autostack">
        <img src="https://img.shields.io/badge/Support-Patreon-red?logo=patreon"
             alt="Support on Patreon"/>
    </a>
    <a href="https://instagram.com/retractablebearfist?igshid=7qlm4fol0o50">
        <img src="https://img.shields.io/badge/logo%20by-RBF-purple?logo=instagram"
             alt="Logo designer's instagram"/>
    </a>
</p>

autostack is a command-line debugging tool for Python projects that automatically displays Stack Overflow answers for thrown errors.

What is the first thing you do when a confusing error message is displayed in your terminal window? You search for an answer on Stack Overflow, of course! With autostack, you no longer have to search for answers on Stack Overflow, they are found for you. Gone are the days of scouring the internet for hours to find an answer to your development questions! autostack is here to automate the debugging process and in turn, expedite Python project development.

## Table of Contents

* [Installation](#Installation)
* [Usage](#Usage)
* [Demo](#Demo)
* [Contributing](#Contributing)
* [License](#License)
* [Show&nbsp;your&nbsp;support](#Show-your-support)
* [Authors](#Authors)

## Installation

**1. Clone the repo and use the install script.**

Clone the repo.

```sh
git clone https://github.com/autostack-team/autostack.git
```

Navigate to the project directory, and run the install bash script.

```sh
cd /path/to/project/
chmod +x install.sh
./install.sh 
```

**2. Or just use pip to install.**

```sh
pip3 install autostack
```

## Usage 

In one terminal window, execute "autostack capture" which will capture all errors in the terminal. You can run this command in as many terminal windows as you'd like.

```sh
autostack capture
``` 

In another terminal window, execute "autostack display" to display Stack Overflow posts for all captured errors.

```sh
autostack display
```

To stop running autostack, use the exit command in the terminals that executed "autostack capture". This automatically stops the terminal window displaying Stack Overflow posts for captured errors.

```sh
exit
```

## Demo 

Checkout the demo below!

<p align="center">
    <img src="https://raw.githubusercontent.com/autostack-team/autostack/master/Demo.gif"
        alt="Demo"/>
</p>

## Contributing

For information on how to get started contributing to autostack, see the [contributing guidlines](https://github.com/autostack-team/autostack/blob/master/CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Show your support

Give a ⭐️ if autostack has helped you!

<a href="https://www.patreon.com/autostack">
  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## Authors
* [Elijah Sawyers](https://github.com/elijahsawyers)
* [Benjamin Sanders](https://github.com/BenOSanders)
* [Caleb Werth](https://github.com/cwerth1)
