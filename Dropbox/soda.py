import collections

class BuySoda:
    def __init__(self, soda_packagings):
        self.packs = sorted(list(set(soda_packagings)))
        # ways[n]: list or sodas that sum to n, in order of package size ASC
        self.ways = collections.defaultdict(list)
        self.ways[0] = [ [] ]
        
    def ways_to_buy(self, N):
        if not self.packs or N < 1:
            return []
        
        if N in self.ways:
            return self.ways[N]
        
        for n in range(1, N + 1):
            if n in self.ways:
                continue
                
            for pack_n in self.packs:
                if pack_n > n:
                    break
                    
                count = 1
                
                while pack_n * count <= n:
                    for way in self.ways[n - pack_n * count]:
                        # Dedup: Append sodas in ASC order
                        if way and pack_n <= way[-1]:
                            continue
                            
                        self.ways[n].append(way + [ pack_n ] * count)
                        
                    count += 1
                
        return self.ways[N]

soda = [ 1, 2, 6, 12, 24 ]
test = BuySoda(soda)
#print(test.ways_to_buy(1))
#print(test.ways_to_buy(2))
#print(test.ways_to_buy(6))
#print(test.ways_to_buy(12))
#print(test.ways_to_buy(24))
print(test.ways_to_buy(30))
