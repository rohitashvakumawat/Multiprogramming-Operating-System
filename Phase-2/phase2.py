import random

M = [['\0' for _ in range(4)] for _ in range(300)]  # memory
IR = ['\0' for _ in range(4)]  # instruction register
IC = 0  # instruction counter
R = ['\0' for _ in range(4)]  # general purpose register
C = False  # toggle register
PTR = 0  # page table register
buffer = [' ' for _ in range(40)]  #
EM = 0  # error message
SI = 0  # system interrupt
TI = 0  # time interrupt
PI = 0  # page interrupt
RA = 0
VA = 0  # real and virtual address
all_pages = [0] * 30
file1 = None
file2 = None
count = 0
PTE = 0  # page table entry
pgnum = 0  # page number
error_occurred = False
valid = 0
term = 0
dataerr = 0

class ProcessControlBlock:
    def __init__(self):
        self.jobid = 0
        self.ttl = 0  # time limit
        self.ttc = 0  # time counter incremented only after execution of instruction
        self.tll = 0  # line limit
        self.llc = 0  # line limit counter

pcb = ProcessControlBlock()

def read():
    global buffer
    buffer = [' ' for _ in range(40)]
    buffer = file1.readline().strip()
    if buffer.startswith('$END'):
        terminate(1)
        return

    print(buffer[0:4])
    i = RA
    stop = i + 9
    k = 0
    for _ in range(i, stop + 1):
        for j in range(4):
            M[i][j] = buffer[k]
            k += 1
            print(f'M[{i}][{j}]={M[i][j]}')
    print()

def write():
    global pcb
    pcb.llc += 1
    if pcb.llc > pcb.tll:
        terminate(2)
        return

    i = RA
    stop = i + 9
    for i in range(RA, stop + 1):
        for j in range(4):
            if M[i][j] == '\0':
                continue
            else:
                file2.write(M[i][j])
    file2.write("\n")

def terminate(EM):
    global term
    file2.write("\n\n")
    file2.write(f"Job Id : {pcb.jobid}\n")
    if EM == 0:
        file2.write("Program executed successfully\n")
        file2.write("No Error\n")
    elif EM == 1:
        file2.write("Error Occurred\n")
        file2.write("Out of Data\n")
    elif EM == 2:
        file2.write("Error Occurred\n")
        file2.write("Line Limit Exceeded\n")
    elif EM == 3:
        file2.write("Error Occurred\n")
        file2.write("Time Limit Exceeded\n")
    elif EM == 4:
        file2.write("Error Occurred\n")
        file2.write("Operation Code Error\n")
    elif EM == 5:
        file2.write("Error Occurred\n")
        file2.write("Operand Error\n")
    elif EM == 6:
        file2.write("Error Occurred\n")
        file2.write("Invalid Page Fault\n")

    file2.write(f"IC : {IC}\n")
    file2.write("IR :")
    file2.write(''.join(IR))
    file2.write("\n")
    file2.write(f"SI : {SI}\n")
    file2.write(f"PI : {PI}\n")
    file2.write(f"TI : {TI}\n")
    file2.write(f"TLL : {pcb.tll}\n")
    file2.write(f"TTC : {pcb.ttc}\n")
    file2.write(f"LLC : {pcb.llc}\n")
    file2.write(f"TTL : {pcb.ttl}\n")
    file2.write("\n\n")
    term = 1

def mos(PI):
    global pgnum, count, valid
    count = 0
    if PI == 3 and TI == 0:
        if valid == 1:
            print("Valid Page Fault: ")
            pgnum = allocate()
            print(f"\nAllocated Page for Logical Page {PTE % 10}: {pgnum}")
            M[PTE][0] = chr(pgnum // 10 + 48)
            M[PTE][1] = chr(pgnum % 10 + 48)
            print("Page Table")
            for x in range(10):
                print(f"M[{PTR + x}]={M[PTR + x][0]}{M[PTR + x][1]}")
            count += 1
            PI = 0
            print(f"IC: {IC}")
    elif PI == 2 and TI == 0:  
        terminate(5)
    elif SI == 1 and TI == 0:  
        read()
    elif SI == 2 and TI == 0:  
        write()
    elif SI == 3 and TI == 0:  
        terminate(0)
    elif PI == 1 and TI == 0:  
        terminate(4)
    elif SI == 1 and TI == 2:  
        terminate(3)
    elif SI == 2 and TI == 2:
        write()
        terminate(3)
    elif SI == 3 and TI == 2:
        terminate(0)
    elif PI == 1 and TI == 2:
        terminate(3)
        terminate(4)  
    elif PI == 2 and TI == 2:
        terminate(3)
        terminate(5)  

def read_file():
    global file1, file2, pcb
    file1 = open("E:\VIT\SY2\OS\Phase 2\input.txt", "r")
    file2 = open("E:\VIT\SY2\OS\Phase 2\output.txt", "w")
    load()
    file1.close()
    file2.close()

def allocate():  
    while True:
        pagenum = random.randint(0, 29)
        if all_pages[pagenum] == 0:
            all_pages[pagenum] = 1
            return pagenum

def load():
    global pcb, dataerr
    m = 0
    count = 0
    while True:
        buffer = file1.readline().strip()
        if buffer.startswith('$AMJ'):
            init()
            pcb.jobid = int(buffer[4:8])
            pcb.ttl = int(buffer[8:12])
            pcb.tll = int(buffer[12:16])
            PTR = allocate() * 10
            print(f"\nAllocated Page is for Page Table: {PTR // 10}")
            print("Job ID :", pcb.jobid)
            print("Time Limit :", pcb.ttl)
            print("Line Limit :", pcb.tll)
            print("Time Counter :", pcb.ttc)
            print("Line Counter :", pcb.llc)
            continue
        elif buffer.startswith('$DTA'):
            print("Started Execution")
            start_execution()
            if dataerr == 1:
                m = 0
                count = 0
                dataerr = 0
            continue
        elif buffer.startswith('$END'):
            m = 0
            count = 0
            continue
        else:
            PTE = allocate()
            print(f"\nAllocated Page for Page {count}: {PTE}")
            M[PTR + count][0] = chr(PTE // 10 + 48)
            M[PTR + count][1] = chr(PTE % 10 + 48)
            count += 1
            k = 0
            m = PTE * 10
            stop = m + 10
            for _ in range(m, stop):
                for j in range(4):
                    if k < len(buffer):
                        M[m][j] = buffer[k]
                        k += 1
        for x in range(300):
            print(f"M[{x}]: {''.join(M[x])}")

def simulation():
    global pcb
    if IR[0] == 'G' and IR[1] == 'D':
        pcb.ttc += 2
    elif IR[0] == 'P' and IR[1] == 'D':
        pcb.ttc += 1
    elif IR[0] == 'H':
        pcb.ttc += 1
    elif IR[0] == 'L' and IR[1] == 'R':
        pcb.ttc += 1
    elif IR[0] == 'S' and IR[1] == 'R':
        pcb.ttc += 2
    elif IR[0] == 'C' and IR[1] == 'R':
        pcb.ttc += 1
    elif IR[0] == 'B' and IR[1] == 'T':
        pcb.ttc += 1

    if pcb.ttc > pcb.ttl:
        TI = 2
        mos(PI)

def start_execution():
    global IC, term, PI
    IC = 0
    while True:
        term = 0
        RA = address_map(IC)
        if PI != 0:
            break
        for i in range(4):  
            IR[i] = M[RA][i]
        if M[RA][0] != 'H' and not M[RA][2].isdigit() or not M[RA][3].isdigit():
            PI = 2
            mos(PI)

        IC += 1

        if IR[0] == 'G' and IR[1] == 'D':  
            simulation()
            SI = 1
            valid = 1
            if M[RA][2].isdigit():
                VA = int(M[RA][2:])
                RA = address_map(VA)

            mos(PI)
        elif IR[0] == 'P' and IR[1] == 'D':  
            simulation()
            SI = 2
            valid = 0
            if M[RA][2].isdigit():
                VA = int(M[RA][2:])
                RA = address_map(VA)

            mos(PI)
        elif IR[0] == 'H':
            simulation()
            SI = 3
            valid = 0
            mos(PI)
            return
        elif IR[0] == 'L' and IR[1] == 'R':
            simulation()
            valid = 0
            if M[RA][2].isdigit():
                VA = int(M[RA][2:])
                RA = address_map(VA)

            for j in range(4):
                R[j] = M[RA][j]
        elif IR[0] == 'S' and IR[1] == 'R':
            simulation()
            valid = 1
            if M[RA][2].isdigit():
                VA = int(M[RA][2:])
                RA = address_map(VA)

            for j in range(4):
                M[RA][j] = R[j]
        elif IR[0] == 'C' and IR[1] == 'R':
            simulation()
            valid = 0
            if M[RA][2].isdigit():
                VA = int(M[RA][2:])
                RA = address_map(VA)

            s1 = ''.join(M[RA])
            s2 = ''.join(R)
            if s1 == s2:
                C = True
            else:
                C = False
        elif IR[0] == 'B' and IR[1] == 'T':
            simulation()
            valid = 0
            if M[RA][2].isdigit():
                VA = int(M[RA][2:])
                RA = address_map(VA)
            if C:
                IC = int(''.join(IR[2:]))
        else:
            PI = 1
            SI = 0
            mos(PI)
        if term == 1:
            return

def address_map(VA):
    global pgnum
    if 0 <= VA < 100:
        PTE = PTR + (VA // 10)
        if M[PTE][0] == '\0':
            PI = 3
            mos(PI)
        else:
            RA = int(''.join(M[PTE]).replace('\x00', ''))
            if 0 <= RA < 300:
                return RA
            else:
                PI = 2
                mos(PI)
    else:
        PI = 2
        mos(PI)
    return pgnum * 10

def init():
    global M, IR, R, C, pcb, PTR, all_pages
    M = [['\0' for _ in range(4)] for _ in range(300)]
    IR = ['\0' for _ in range(4)]
    R = ['\0' for _ in range(4)]
    C = False
    pcb.llc = 0
    pcb.ttc = 0
    all_pages = [0] * 30

read_file()
