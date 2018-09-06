# -*- coding: cp1251

class PairList():
    '''
    Класс списка брусов. Используется для ведения списка перспективных брусов L и
    списка брусов глобальных минимумов Lres.
    '''
    def __init__(self, pairList=[]):
        self._pairList = [pair for pair in pairList]


    def __repr__(self):
        return str(self._pairList)
    
    
    def __getitem__(self, idx):
        return self._pairList[idx]
    
    
    def __delitem__(self, idx):
        del self._pairList[idx]
    
    
    def __len__(self):
        return len(self._pairList)
    
    
    def Append(self, box):
        self._pairList.append(box)
        self._pairList.sort(key=lambda x: x[1])
        
        
    def MultiDelete(self, f_wave):
        '''
            Удаляет элементы списка, начиная с fromIdx.
        '''
        newList = []
        for i in range(len(self)):
            if self[i][1] < f_wave:
                newList.append(self[i])
        self._pairList = newList
    
    def PopHead(self):
        '''
        '''
        return self._pairList.pop(0)

