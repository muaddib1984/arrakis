
# ARRAKIS

Arrakis is a remote DSP processor that connects over an IP Connection (SSH) to a 
local data visualization flowgraph. The focus of this project was to provide a way 
to get a 'horse sense' visualization of wideband spectrum over a low-data rate 
IP connection.

Performance measurements were taken with the iftop application (sudo iftop -i <iface> -P) 
and have shown that at 8 Vectors Per Second, 40MHz of bandwidth can be visualized with
~2.5Mbps.

The Remote DSP and Local Visualization Portions in the diagram 
are contained in ARRAKIS.
The wrapper around the various SDR types are in the STILLSUIT repository
(https://github.com/muaddib1984/stillsuit)

Supported SDR's are:  
 - Ettus Research USRP  
 - LimeSDR  
 - RTL-SDR  


 *** 




    +-------------------------------+        +----------------+
    | REMOTE HOST                   |        |LOCAL HOST      |
    | +---------+    +------------+ |  SSH   |                |
    | |STILLSUIT+--->+SPACE FOLDER+--------->+GUILD NAVIGATOR |
    | |  (SDR)  | ZMQ|    (DSP)   | |  ZMQ   | (VISUALIZATION |
    | +---------+    +------------+ |        | AND CONTROL)   |
    +-------------------------------+        +-----+----------+
           ^               ^                       |
           |               +-----------------------+
           +---------------------------------------+
                           XMLRPC


## DEPENDENCIES:
[GNURadio 3.9+](https://github.com/gnuradio/gnuradio) on both Remote and Local Host Machines  
openssh-server on remote machine
(```apt install openssh-server```)

## DESCRIPTION:
### DATA STREAM
Space Folder uses a ZMQ SUB Block for IQ input and ZMQ PUB Block for FFT vectors out.
    The intended input is the output I/Q from one of the STILLSUIT sources, but could 
    also be any I/Q stream from a GNURadio ZMQ PUB Block that sends complex32 I/Q data.
    The default ports are 5000 for input and 5001 for output.
Guild Navigator uses a ZMQ SUB Block for FFT vector input.
    The default input port is 5001.

### CONTROL
Guild Navigator Controls Space Folder and STILLSUIT parameters with XMLRPC.
    The default ports are 8000 for STILLSUIT and 8001 for Space Folder.

### USAGE:
The default parameters for STILLSUIT, SPACEFOLDER and GUILD NAVIGATOR will work 
    together 'out of the box'. Parameters can be seen using ```'-h'```

**Space Folder Flowgraph:**
![GUI screenshot](https://github.com/muaddib1984/arrakis/blob/main/flowgraph_images/space_folder.png)

#### Space Folder Help Menu:
```
    $ python3 space_folder.py -h

    usage: space_folder.py [-h] [-x CONTROL_IP] [-X CONTROL_PORT] [-s SAMP_RATE] [-z ZMQ_IN_IP] [-o ZMQ_OUT_IP] [-O ZMQ_OUT_PORT]

    remote ingest and decimation for low bw link

    optional arguments:
      -h, --help            show this help message and exit
      -x CONTROL_IP, --control-ip CONTROL_IP
                            Set XMLRPC SERVER IP [default='127.0.0.1']
      -X CONTROL_PORT, --control-port CONTROL_PORT
                            Set XMLRPC SERVER PORT [default=8001]
      -s SAMP_RATE, --samp-rate SAMP_RATE
                            Set SAMPLE RATE [default='20.0M']
      -z ZMQ_IN_IP, --zmq-in-ip ZMQ_IN_IP
                            Set ZMQ IN IP ADDR [default='127.0.0.1']
      -o ZMQ_OUT_IP, --zmq-out-ip ZMQ_OUT_IP
                            Set ZMQ OUT IP ADDR [default='127.0.0.1']
      -O ZMQ_OUT_PORT, --zmq-out-port ZMQ_OUT_PORT
                            Set ZMQ OUT IP PORT [default='5001']
```

**Guild Navigator Flowgraph:**
![GUI screenshot](https://github.com/muaddib1984/arrakis/blob/main/flowgraph_images/guild_navigator.png)

### Guild Navigator Help Menu:
```
    $ python3 guild_navigator.py -h
    
    usage: guild_navigator.py [-h] [-x CONTROL_IP] [-X CONTROL_PORT] [-b RF_BW] [-f RF_FREQ] [-g RF_GAIN] [-s SAMP_RATE] [-z ZMQ_IN_IP]

    remote visualizatin for space folder application

    optional arguments:
      -h, --help            show this help message and exit
      -x CONTROL_IP, --control-ip CONTROL_IP
                            Set XMLRPC SERVER IP [default='127.0.0.1']
      -X CONTROL_PORT, --control-port CONTROL_PORT
                            Set XMLRPC SERVER PORT [default=8002]
      -b RF_BW, --rf-bw RF_BW
                            Set RF BANDWITDH [default='10.0M']
      -f RF_FREQ, --rf-freq RF_FREQ
                            Set RF FREQUENCY [default='750.0M']
      -g RF_GAIN, --rf-gain RF_GAIN
                            Set RF GAIN [default='50.0']
      -s SAMP_RATE, --samp-rate SAMP_RATE
                            Set SAMPLE RATE [default='20.0M']
      -z ZMQ_IN_IP, --zmq-in-ip ZMQ_IN_IP
                            Set ZMQ IN IP ADDR [default='127.0.0.1']
```

## RUNNING:
From your local host, establish an ssh tunnel with port forwarding:  
```ssh -L 5001:localhost:5001 -L 8000:localhost:8000 -L 8001:localhost:8001 <remoteuser>@<remoteipaddress>```

On your remote host, start the appropriate STILLSUIT source for your SDR 
(or comparable I/Q source) and start Space Folder.

On your Local Host, start Guild Navigator.

You will see the spectrum for the default 20MHz (works with UHD/LimeSDR/siggen)
![GUI screenshot](https://github.com/muaddib1984/arrakis/blob/main/flowgraph_images/arrakis_spectrum.png)

#### **NOTE:**
Space Folder and Guild Navigator are configured for wideband visualization and have
a default sampling rate of 20Msps. If you are using an RTLSDR, change the Sample Rate
for Space Folder and Guild Navigator from the command line using:   
```./space_folder -s 2e6```  
```./guild_navigator.py -s 2e6```

The STILLSUIT source for RTLSDR is set by default to 2Msps.

## Future Work:
Replace Guild Navigator with a Web-Based GUI Interface that supports visualization
and control in the same way. This would remove the need for GNURadio to be
installed on the local host and could potentially allow for multiple users to
view the spectrum at once.

## Credits:
Space Folder's DSP function was largely inspired by Ham2Mon by madengr.
https://github.com/madengr/ham2mon 
