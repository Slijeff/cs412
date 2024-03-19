from collections import Counter, defaultdict

def ord_prefixspan(filename, minsup):
    class Database:
        def __init__(self, filename=None, minsup=1, seqs=[]):
            self.seqs = seqs
            self.minsup = minsup
            if filename:
                with open(filename, 'r') as f:
                    for line in f:
                        self.seqs.append(line.replace("\n","").replace(" ", "").split(",")[1][1:-1])
        
        def scan(self, prevseq: str):
            tmp = [Counter(set(s)) for s in self.seqs]
            total = defaultdict(int)
            for t in tmp:
                for k, v in t.items():
                    total[k] += v
            total = {(prevseq + k) : v for k,v in total.items() if v >= self.minsup}
            return total
        
        def projection(self, exclude: str):
            projected = [s[s.find(exclude)+1:] for s in self.seqs if s.find(exclude) != -1]
            # self.seqs = projected
            return Database(None, self.minsup, projected)
    
    
    freq_sequences = defaultdict(int) # default initialization
    
    def prefixspan(database: Database, prevseq: str):
        res = database.scan(prevseq)
        for k, v in res.items():
            freq_sequences[k] += v
            newdb = database.projection(k[-1])
            prefixspan(newdb, k)

    db = Database(filename, minsup)
    prefixspan(db, "")
    del db
    return dict(freq_sequences)
    

# if __name__ == "__main__":
#     res = ord_prefixspan("validation.txt", 2 )
#     print(res)
#     print(len(res))
#     print("ecb" in res)
