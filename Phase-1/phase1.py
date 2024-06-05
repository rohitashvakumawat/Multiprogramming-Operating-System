class OS:
    def __init__(self):
        self.M = [[' ' for _ in range(4)] for _ in range(100)]
        self.IR = ['\0'] * 4
        self.R = ['\0'] * 4
        self.IC = 0
        self.SI = 0
        self.C = False
        self.buffer = ['\0'] * 40
        self.infile = None
        self.outfile = None

    def init(self):
        for i in range(100):
            for j in range(4):
                self.M[i][j] = ' '
        self.IR = ['\0'] * 4
        self.R = ['\0'] * 4
        self.C = False

    def MOS(self):
        if self.SI == 1:
            self.buffer = ['\0'] * 40
            line = self.infile.readline()
            self.buffer[:len(line)] = list(line)[:40]
            k = 0
            i = int(self.IR[2]) * 10
            
            for l in range(10):
                for j in range(4):
                    if k < len(self.buffer):
                        self.M[i][j] = self.buffer[k]
                        k += 1
                if k == 40:
                    break
                i += 1
            for i in range(100):
                print(f"M[{i}]\t{''.join(self.M[i])}")
        elif self.SI == 2:
            self.buffer = ['\0'] * 40
            k = 0
            i = int(self.IR[2]) * 10
            for l in range(10):
                for j in range(4):
                    if k < len(self.buffer):
                        self.buffer[k] = self.M[i][j]
                        self.outfile.write(self.buffer[k])
                        k += 1
                if k == 40:
                    break
                i += 1
            for i in range(100):
                print(f"M[{i}]\t{''.join(self.M[i])}")
            self.outfile.write("\n")
        elif self.SI == 3:
            self.outfile.write("\n\n")

    def Execute(self):
        while True:
            self.IR = self.M[self.IC]
            self.IC += 1
            if self.IR[0] == 'G' and self.IR[1] == 'D':
                self.SI = 1
                self.MOS()
            elif self.IR[0] == 'P' and self.IR[1] == 'D':
                self.SI = 2
                self.MOS()
            elif self.IR[0] == 'H':
                self.SI = 3
                self.MOS()
                break
            elif self.IR[0] == 'L' and self.IR[1] == 'R':
                i = int(self.IR[2]) * 10 + int(self.IR[3])
                self.R = self.M[i]
            elif self.IR[0] == 'S' and self.IR[1] == 'R':
                i = int(self.IR[2]) * 10 + int(self.IR[3])
                self.M[i] = self.R
            elif self.IR[0] == 'C' and self.IR[1] == 'R':
                i = int(self.IR[2]) * 10 + int(self.IR[3])
                if self.M[i] == self.R:
                    self.C = True
            elif self.IR[0] == 'B' and self.IR[1] == 'T':
                if self.C:
                    i = int(self.IR[2]) * 10 + int(self.IR[3])
                    self.IC = i

    def LOAD(self):
        print("Reading Data...")
        x = 0
        while True:
            line = self.infile.readline()
            if not line:
                break
            self.buffer = list(line)[:40]
            print(''.join(self.buffer))
            if self.buffer[:4] == list('$AMJ'):
                self.init()
            elif self.buffer[:4] == list('$DTA'):
                self.IC = 0
                self.Execute()
            elif self.buffer[:4] == list('$END'):
                continue
            else:
                k = 0
                for x in range(x, 100):
                    for j in range(4):
                        if k < len(self.buffer):
                            self.M[x][j] = self.buffer[k]
                        k += 1
                    if k >= len(self.buffer) or self.buffer[k] == ' ' or self.buffer[k] == '\n':
                        break
        self.infile.close()
        self.outfile.close()

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


