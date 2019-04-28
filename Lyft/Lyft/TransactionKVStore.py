from VersionedKVStore import KVStore

class TransactionKVStore(object):
    """description of class"""

    def reset(self):
        self.kvStore = KVStore()
        self.operationsStack = []
        self.currentBlock = []

    def processLine(self, line):
        if line == 'BLOCK':
            if self.currentBlock:
                self.operationsStack.append(self.currentBlock)
                self.currentBlock = []
        elif line == 'COMMIT':
            for command in self.currentBlock:
                self.kvStore.processLine(command)

            if self.operationsStack:
                self.currentBlock = self.operationsStack.pop()
            else:
                self.currentBlock = []
        elif line == 'ROLLBACK':
            if self.operationsStack:
                self.currentBlock = self.operationsStack.pop()
            else:
                self.currentBlock = []
        else:
            self.currentBlock.append(line)

    def processFile(self, input_file, output_file):
        self.reset()

        with open(input_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.processLine(line.rstrip('\n'))

        with open(output_file, 'w') as f:
            f.write(self.kvStore.serialize())

if __name__ == '__main__':
    input_files = [ './transactions1.txt', './transactions2.txt' ]

    transactionStore = TransactionKVStore()
    for input_file in input_files:
        output_file = input_file.replace('.txt', '_done.txt')
        transactionStore.processFile(input_file, output_file)
