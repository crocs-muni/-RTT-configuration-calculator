# RTT Configuration Calculator
Configuration Calculator is a tool for automated creation of battery configuration
files for the [Randomness Testing Toolkit](https://github.com/crocs-muni/randomness-testing-toolkit) (RTT).
It supports all batteries used in the RTT except the TestU01 BigCrush Battery.

## Installation
No installation is needed. \
This project requires Python 3.5.2 or higher interpreter.

## Usage
To run this tool, execute the `confic_calc.py` script with desired arguments. Exactly one of the `-f` (path to file the
user will test) or `-s` (size of the file the user will test) arguments
must be specified. The battery configuration will be stored in `config.json` file (path to different file may
be given as one of the arguments). The battery configuration file may be directly used with RTT.

```bash
usage: RTT Configuration calculator. [-h] (-f DATA_FILE | -s SIZE)
                                     [-c CONFIG_FILE] [-i]
                                     [--dieharder-buffer DIEHARDER_BUFFER]
                                     [--nist-stream-size NIST_STREAM_SIZE]
                                     [--tu01-buffer TU01_BUFFER]
                                     [--tu01-bit-nb TU01_BIT_NB]
```

## Battery configurations
The battery configuration is created so that as many as possible data from the tested file are used without
_file rewind_.

Some test are marked as with __variable__ size. That means that each run of the test consumes slightly
different amount of data. This may lead to _file rewinds_, therefore these test use size buffers to prevent them.
The buffer size may be changed, but do so on your own risk.

### NIST STS
The NIST STS battery requires to set the _stream size_ argument. The default value used
by the Configuration Calculator is 1,000,000. The user may change this argument, but lower values will break 
recommendations for some tests.

### TestU01 Rabbit, Alphabit and BlockAlphabit
The TestU01 Rabbit, Alphabit and BlockAlphabit batteries require to set the _bit_nb_ argument. The default value
used by the Configuration Calculator is 52,428,800. The user may change this value, but lower value will
cause some tests from the Rabbit battery to be omitted from the execution.

