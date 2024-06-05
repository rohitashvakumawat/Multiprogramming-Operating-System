# Multiprogramming-Operating-System

# Phase 1 Implementation of a Simple Operating System

This project simulates a basic operating system capable of loading, interpreting, and executing a series of instructions from an input file. The primary components include memory management, instruction handling, and input/output operations.

## Class `OS`

The `OS` class models the simple operating system. Here's a breakdown of its components and functionality:

### Attributes

- `M`: Memory, represented as a 100x4 grid.
- `IR`: Instruction Register, a list of 4 characters.
- `R`: General Purpose Register, a list of 4 characters.
- `IC`: Instruction Counter, an integer.
- `SI`: Service Interrupt, an integer.
- `C`: Condition Code, a boolean.
- `buffer`: A buffer for handling input/output operations, a list of 40 characters.
- `infile`: Input file object.
- `outfile`: Output file object.

### Methods

#### `__init__(self)`

Initializes the attributes with default values.

#### `init(self)`

Resets the memory (`M`), instruction register (`IR`), general-purpose register (`R`), and condition code (`C`).

#### `MOS(self)`

Handles different types of service interrupts:
- **SI = 1**: Reads a line from the input file into memory.
- **SI = 2**: Writes a line from memory to the output file.
- **SI = 3**: Writes two newline characters to the output file.

#### `Execute(self)`

Executes instructions based on the contents of memory:
- **GD**: Get Data (input).
- **PD**: Put Data (output).
- **H**: Halt execution.
- **LR**: Load Register from memory.
- **SR**: Store Register into memory.
- **CR**: Compare Register with memory.
- **BT**: Branch on True (condition code).

#### `LOAD(self)`

Reads the input file line by line and processes control cards (`$AMJ`, `$DTA`, `$END`):
- **$AMJ**: Start of a new job, initialize the system.
- **$DTA**: Data card, begin executing instructions.
- **$END**: End of the job, continue reading.

### Main Function

The `main()` function initializes the `OS` object, opens the input and output files, and starts the loading process.

## Usage

1. Ensure the input file path is correctly set in the `main()` function.
2. Run the script to process the input file and produce an output file.

```python
def main():
    os = OS()
    os.infile = open("E:\VIT\SY2\OS\Phase 1\input.txt", "r")
    os.outfile = open("E:\VIT\SY2\OS\Phase 1\output.txt", "w")
    if not os.infile:
        print("Failure")
    else:
        print("File Exist")
    os.LOAD()

if __name__ == "__main__":
    main()
```

# Phase 2 Implementation of a Simple Operating System

This project extends the simple operating system simulation to handle memory management with paging, instruction execution, and error handling. It simulates a basic OS that can load, interpret, and execute instructions from an input file while managing memory using a paging mechanism.

## Components

### Global Variables and Constants

- `M`: Memory, a 300x4 grid.
- `IR`: Instruction Register, a list of 4 characters.
- `IC`: Instruction Counter, an integer.
- `R`: General Purpose Register, a list of 4 characters.
- `C`: Condition Code, a boolean.
- `PTR`: Page Table Register, an integer.
- `buffer`: A buffer for handling input/output operations, a list of 40 characters.
- `EM`: Error Message code.
- `SI`: Service Interrupt code.
- `TI`: Time Interrupt code.
- `PI`: Page Interrupt code.
- `RA`: Real Address.
- `VA`: Virtual Address.
- `all_pages`: Track allocated pages, a list of 30 integers.
- `file1`: Input file object.
- `file2`: Output file object.
- `count`: Counter for allocated pages.
- `PTE`: Page Table Entry.
- `pgnum`: Page Number.
- `error_occurred`: Error flag.
- `valid`: Validity flag for page faults.
- `term`: Termination flag.
- `dataerr`: Data error flag.

### Class `ProcessControlBlock`

Represents the PCB with job control information.

#### Attributes

- `jobid`: Job ID.
- `ttl`: Time limit.
- `ttc`: Time counter.
- `tll`: Line limit.
- `llc`: Line counter.

### Functions

#### `read()`

Reads data from the input file into memory.

#### `write()`

Writes data from memory to the output file.

#### `terminate(EM)`

Handles termination and writes termination information to the output file.

#### `mos(PI)`

Handles various system interrupts and performs necessary operations based on the interrupt codes.

#### `read_file()`

Initializes the input and output file processing.

#### `allocate()`

Allocates a page in memory.

#### `load()`

Loads jobs and instructions from the input file into memory.

#### `simulation()`

Simulates instruction execution and increments the time counter.

#### `start_execution()`

Starts the execution of instructions by fetching and decoding them.

#### `address_map(VA)`

Maps virtual addresses to real addresses.

#### `init()`

Initializes the system by resetting memory and registers.

## Usage

1. Ensure the input file path is correctly set in the `read_file()` function.
2. Run the script to process the input file and produce an output file.

```python
def read_file():
    global file1, file2, pcb
    file1 = open("E:\VIT\SY2\OS\Phase 2\input.txt", "r")
    file2 = open("E:\VIT\SY2\OS\Phase 2\output.txt", "w")
    load()
    file1.close()
    file2.close()
```