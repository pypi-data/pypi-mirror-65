EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:example
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L example U1
U 1 1 5A486404
P 4650 2700
F 0 "U1" H 4850 2950 60  0000 L CNN
F 1 "example" H 4850 2850 60  0000 L CNN
F 2 "" H 4650 2700 60  0001 C CNN
F 3 "" H 4650 2700 60  0001 C CNN
	1    4650 2700
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG01
U 1 1 5A486451
P 3900 2500
F 0 "#FLG01" H 3900 2575 50  0001 C CNN
F 1 "PWR_FLAG" H 3900 2650 50  0000 C CNN
F 2 "" H 3900 2500 50  0001 C CNN
F 3 "" H 3900 2500 50  0001 C CNN
	1    3900 2500
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 5A486467
P 4300 2500
F 0 "#FLG02" H 4300 2575 50  0001 C CNN
F 1 "PWR_FLAG" H 4300 2650 50  0000 C CNN
F 2 "" H 4300 2500 50  0001 C CNN
F 3 "" H 4300 2500 50  0001 C CNN
	1    4300 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 2500 3900 3000
Wire Wire Line
	3900 3000 4650 3000
Wire Wire Line
	4650 2900 4300 2900
Wire Wire Line
	4300 2900 4300 2500
Wire Wire Line
	4650 2700 4300 2700
Connection ~ 4300 2700
NoConn ~ 4650 2800
$EndSCHEMATC
