import pickle 
import os
import time
import numpy as np

class utils:
    @staticmethod
    def get_prob(counts_list, n = 1.5):
        '''
        inputs:
            counts_list: type list, the counts  are arranged from smallest to largest [0,0,1,2,5,...]
            n: describe the propability to choise the element of counts_list,  n>1
        '''
        counts = np.array(counts_list,dtype=np.float32)
        counts[counts==0] = 0.9
        p = 1/(counts**n)
        p = p/sum(p)
        return p
    
    @staticmethod
    def get_idx_list(counts_prob):
        '''
        counts_prob: probability list
        return: index list
        '''
        def idx_pick(counts_prob, _random):
            accumu_prob = 0
            for idx, prob in enumerate(counts_prob):
                accumu_prob += prob
                if accumu_prob >= _random:
                    return idx
        idx = []  
        for i in np.random.rand(len(counts_prob)):
            idx.append(idx_pick(counts_prob, i))
        return idx

    @staticmethod
    def get_idx(idx_list):
        return list(set(idx_list[:15]))
    

class Mynote:

    def __init__(self, userName = ''):
#         import pickle 
#         self.category = category
        self._english = {}
        self._essay = []
        self.fileName = userName+'dict.pkl'
        self.en_read_len, self.es_read_len = 0, 0
        self.get_read_item_en = self.get_read_item('english')
        self.get_read_item_es = self.get_read_item('essay')

        
        
    def english(self, label, content):
        self._english.setdefault(label, [])
        self._english[label].append([content, 0])
        
    def essay(self, content):
        self._essay.append([content, 0])
    
    def get_read_item(self, flag):

        
        if flag == 'english':
            while 1:
                en_sorted_list = sorted(self._english.items(), # _english's data structure is {key, [[val1, count],[val2, 0],...]}
                                        key=lambda x: x[1][0][1], reverse=False) # sorted from small to big of count
                en_sorted_idx =[i[1][0][1] for i in en_sorted_list] # get sorted index
                counts_prob = utils.get_prob(en_sorted_idx, n=2)
                idx_list = utils.get_idx_list(counts_prob)
                idx = utils.get_idx(idx_list)              
#                 print(en_sorted_list,'en_sorted_list')
#                 print(idx)
                self.en_read_len = len(idx)
                for i in idx:
                    key = en_sorted_list[i]
                    yield key[0]
                    
        elif flag == 'essay':
            while 1:
                self._essay.sort(key=lambda x: x[1], reverse=False)
                es_sorted_idx = [i[1] for i in self._essay]

                counts_prob = utils.get_prob(es_sorted_idx, n=2)
                idx_list = utils.get_idx_list(counts_prob)
                idx = utils.get_idx(idx_list)
                print(idx)
                self.es_read_len = len(idx)
                for i in idx:
                    yield i
        else:
            raise ''
                
    def read_eng(self):          
        key = next(self.get_read_item_en)
        self._english[key][0][1] += 1 # count
        return [key, self._english[key]]
    
    def read_essay(self):
        idx = next(self.get_read_item_es)
        self._essay[idx][1] += 1 # count 
        return idx, self._essay[idx]
    
    def save(self):
        with open(self.fileName,'wb') as fo:
            pickle.dump((self._english, self._essay), fo)
            
    def load(self):
        with open(self.fileName,'rb') as fi:
            self._english, self._essay = pickle.load(fi)
            
    def del_en_key(self,key):
        '''delete english related item of dict'''
        del self._english[key]

    def del_es_idx(self,idx):
        del self._essay[idx]

def main():    
    note = Mynote()
    try:
        note.load()
    except:
        print('No dictionary data was imported')
    disp_mode = [' Record ', ' Review ']

    while 1:
        mode = input('进入记录模式press 1, 进入回顾模式press 2, 退出press 0')
        if mode == '1':
            print(f'{disp_mode[0]:*<55}')
            while 1:
                flag = input('记录单词press 1, 记录灵感press 2, 退回press 0 \n')
                if flag == '1':
                    answer = tuple(input('pls input your words follow, separated from","\n').split(','))
                    note.english(answer[0], answer[1])
                elif flag == '2':
                    answer = input('pls input your inspiration here\n')
                    note.essay(answer)
                elif flag == '0':
                    break
                else:
                    print('bad input, try again\n')
        elif mode == '2':
            while 1:

                print(f'{disp_mode[1]:*^55}')
                try:
                    read_idx = eval(input(' English :1, Inspiration :2, back :0'))
                    read_flag = [0, 'English','Inspiration']
                    if read_idx > 2:
                        print('bad input, try again\n')
                        continue
                except:
                    print('bad input, try again\n')
                    continue
                
                
                if read_flag[read_idx] == 'Inspiration': # this episode is stupid
                    es_idx, read_ess = note.read_essay()
                    es_read_len = note.es_read_len
                    while True:
                        es_read_len -= 1
                        print(read_ess[0], f'\t counts {read_ess[1]}')
                        if es_read_len == 0:
                            break
                        _ = input('...')
                        if _ == '0':
                            break
                        if _ == '-1':
                            print(f'delete item {read_ess[0]}')
                            note.del_es_idx(es_idx)
                        es_idx, read_ess = note.read_essay()

                if read_flag[read_idx] == 'English': # stupid too
                    read_eng = note.read_eng()
                    en_read_len = note.en_read_len
                    while True:
                        en_read_len -= 1
                        print(f'{read_eng[0]}')
                        time.sleep(4)
                        print(f'{read_eng[1][0][0]:->50}')
                        if en_read_len == 0:
                            break
                        _ = input('...')
                        if _ == '0':
                            break
                        elif _ == '-1':# del item
                            print(f'delete item {read_eng[0]}')
                            note.del_en_key(read_eng[0])
                        read_eng = note.read_eng()
                elif read_flag[read_idx] ==0:
                    break

        elif mode == '0':
            break
        else:
            print('bad input, try again\n')

    note.save()
            
if __name__ == '__main__':
    main()