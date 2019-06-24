from PIL import Image
class Imagem:
    def __init__(self,path):
        self.file = Image.open(path)
        
    def hasImagem(self):
        if self.file is None:
            return False 
        else:
            return True
            
    def getImagem(self):
        if self.hasImagem():
            return self.file
            
    
    
    
    
test = Imagem("serverArchives/toy_story.jpg")
print(test.getImagem())