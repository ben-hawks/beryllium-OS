# Ljinux
A "linux" written in python, for CircuitPython powered microcontrollers.  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a><br />
![neofetch](https://github.com/bill88t/ljinux/blob/main/other/screenshots/boot.gif)<br />
<b>Important notes:</b><br />
This project is still <b>in it's early developement</b>!<br />
This project is <b>NOT</b> a linux distribution.<br />
This project is <b>NOT</b> compatible with any linux code / binaries.<br />

<b><i>We also now have a [discord](https://discord.gg/V8AejwGpCv) server!<br />
If you need support or want to hang out, feel free to join in!</i></b><br />

We also work with [Github Discussions](https://github.com/bill88t/ljinux/discussions).<br />

Table of Contents
=================
* [Prerequisites](#prerequisites-and-optional-hardware)
* [Installation / updating](#installation--updating)
* [Packages](#packages)
* [Connection](#connection)
* [Directory structure](#directory-structure)
* [Manual](#a-complete-ljinux-manual-is-available)
* [Useful resources](#useful-resources-that-helped-with-the-development-of-this-project)

## Prerequisites and optional hardware

Runs on circuitpython <code>8.1.X</code>, <code>8.2.X</code> and <code>9.0.0-alpha-X</code>.<br />
At the moment the supported boards are:<br />

 - Raspberry Pi Pico<br />
 - Raspberry Pi Pico W<br />
 - Waveshare RP2040-Zero<br />
 - Adafruit KB2040<br />
 - Waveshare ESP32-S2-Pico<br />
 - Adafruit Feather ESP32-S2<br />
 - Adafruit Feather ESP32-S3 TFT<br />
 - Pimoroni Pico Lipo (16mb)<br />
 - Pimoroni Pico Lipo (4mb)<br />
 - Wemos Lolin S2 Mini<br />
 - Seeed XIAO nRF52840 (Sense)<br />
 - DFRobot Beetle ESP32-C3<br />
 - M5Stack Timer Camera X<br />
 - WeAct ESP32-C6<br />
 - Firebeetle 2 ESP32-S3<br />

But it can probably run on many more.<br />
<br />
The currently stable supported MCU's are: <code>ESP32</code>, <code>ESP32-S2</code>, <code>ESP32-S3</code>, <code>ESP32-C3</code>, <code>ESP32-C6</code>, <code>RP2040</code>, <code>nRF52840</code>.<br />
The currently unsupported CircuitPython-compatible MCU families are: <code>SAMD21</code>, <code>SAMD51</code>, <code>litex</code>, <code>mimxrt10xx</code>, <code>efr32</code>, <code>stm</code>, <code>unix</code>.<br />
The MCU's that are currently unsupported are so because I either can't get my hands on a decent board with them or they don't have enough ram for ljinux.<br />
<br />
The only real limiting factor should be ram, as about 70k (usable under circuitpython) are needed.<br />
<i>(If you have gotten it running on an unsupported board, feel free to pr)</i><br />

## Installation / Updating

Note: Installation using scripts, from windows is unsupported.<br />
If you are windows user, this project **really** isn't for you.<br />
Don't even try from wsl.<br />

1) Install a supported CircuitPython version onto the board.<br />
    Detailed instructions regarding CircuitPython can be found [here](https://learn.adafruit.com/welcome-to-circuitpython).<br />
2) Download the latest ljinux release for your board and extract it onto it.<br />
    Or even better, if you wish to use the latest and greatest, clone this repository and from within the "source" folder, run <code>make install</code> with your board mounted.<br />
    DO NOT run with <code>-j</code>!!!<br />
    This command will automatically update the system files if they already exist.<br />
    To only update the wanna-be kernel run <code>make</code> instead.<br />
    If you plan on loading the files remotely (via web/ble workflow), run <code>make \*your board.board_id\* install</code> instead (DO NOT run with <code>-j</code>).<br />
    The files for you to copy will be created inside <code>source/build_\*your board.board_id\*</code>.<br />
3) *(Optional)* Copy over the packages you wish to install with jpkg, or install drivers with make.<br />
    More info regarding packages in [Packages](#packages)
4) Eject & powercycle the board<br />
    When it's plugged back in, you can connect to it via serial.<br />
    (You can use putty to connect to the board on Windows, Tio or GNU/Screen on Linux or MacOS)<br />
<b>IMPORTANT NOTE: To make the board appear again as a usb drive on the host, run the ljinux command </b><code>devmode</code><br />

## Packages
Some of ljinux's features are not bundled with this install.<br />
You will have to install them seperately through the jpkg package manager.<br />
<br />
You can find ljinux packages in the [jpkg github topic](https://github.com/topics/jpkg).<br />
<br />
<b>Recommended packages:</b><br />
<br />
Farland, the ljinux display manager: https://github.com/bill88t/ljinux-farland <br />
SSD1306 display support: https://github.com/bill88t/ljinux-ssd1306 <br />
RubberDucky script support: https://github.com/bill88t/ljinux-ducky <br />
Hashutils, md5 / sha commands: https://github.com/bill88t/ljinux-hashutils <br />

## Connection

To connect to the board it's recommended to use Putty for Windows and Tio for Linux/MacOS.<br /><br />

For Putty, select connection type to be Serial, select the port to be COM<b>X</b> where <b>X</b> is the number of the serial port allocated by the board and set the speed/baudrate to 115200.<br />
(You can find which com port is allocated from within the Device Manager, it usually is COM3 or COM4)<br />(The baudrate may differ for your board, do not explicitly stick to 115200)<br /><br />

For Tio, if you are on linux, you need to be in the <code>dialout</code> or <code>uucp</code> user group and to connect, run: <code>tio /dev/ttyACM0</code>
<br />If you are on a Mac instead, run: <code>ls /dev/tty.usb*</code> to find the device name, and connect to it by running: <code>tio /dev/tty.usb\<Device name here\></code><br />
To disconnect, press <code>Ctrl</code> + <code>t</code>, <code>q</code>.<br />
To be added to the <code>dialout</code> group, run <code>sudo usermod -a -G dialout \<your username here\></code> and restart.<br />

## Directory structure

<ul>
<li><code>LjinuxRoot</code>, the root filesystem for ljinux. It should be copied as is to the board.</li>
<li><code>rootfilesystem</code>, the files needed in the root of the board. These should also be copied as is.</li>
<li><code>scripts</code>, the files needed for compilation, and installation to a board. They should not be copied over,</li>
<li><code>source</code>, the source files for ljinux and co. They should be compiled into .mpy files and put in /lib of the board.</li>
<li><code>packages</code>, ljinux featured packages and preinstalled software, coming soon.</li>
<li><code>other</code>, miscellaneous files</li>
</ul>

## A complete Ljinux manual is available

 https://github.com/bill88t/ljinux/blob/main/Manual.txt<br />
 <br />

## Additional screenshots
![less](https://github.com/bill88t/ljinux/blob/main/other/screenshots/less.png)
![iwctl](https://github.com/bill88t/ljinux/blob/main/other/screenshots/iwctl.png)

## Useful resources that helped with the development of this project
 https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797<br />
 https://en.wikipedia.org/wiki/ANSI_escape_code<br />
 https://github.com/todbot/circuitpython-tricks<br />
