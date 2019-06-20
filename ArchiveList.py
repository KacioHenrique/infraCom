#as solicitações que o cliente vai fazer ao servidor
#a class do servidor pode usar esse objeto como resposta ao cliente 
class ArchiveList:
    def __init__(self):
        self.movies = ["toy story","toy story 2","toy story 3", "toy story 4"]
    
    def getAllArchives(self):
        return self.movies
        
    def solictArchive(self,name):
        for movie in self.movies:
            if name == movie:
                return movie + ".mp4"
        
        return "empy"
        

    

test = ArchiveList()

print(test.getAllArchives())
print(test.solictArchive("toy story 5"))
