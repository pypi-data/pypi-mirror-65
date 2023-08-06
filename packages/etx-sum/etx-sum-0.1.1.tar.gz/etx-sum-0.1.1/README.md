# Description

The intention of this Python project is to provide the basic statistics about my trading habbits, based on the data i get from my CFD broker [ETX capital](https://www.etxcapital.com/)


# Installation

## Requirements 

* Python 3.6 or newer


To install the package using pip simply run the following command

      pip3 install etx-sum

# Usage
The usage of this is intended to extremely simple

After you have installed the package see [Installation](#Installation) you simply log into your ETX account download youre trading history, to nice place on you computer.

In ETX this is done like seen on the below screenshot.

![How to get you're trading history ](./static/tradingHistory.png)

when the download completes, you simple run the following command in your terminal.

      etx-sum <path_to_where_you_downloaded_your_trading_history>





# Participate

## building

      python3 setup.py clean --all sdist bdist_wheel 

## Installing locally 

      python3 setup.py clean --all install

## Uploading to pypi

      python3 -m twine upload dist/*

Username: *__\_\_token\_\___*
>For the actual token you need to be part of the project
