def dfs(graph, visited, now):
    visited.append(now)
    mx = [visited[:]]
    for i in range(len(graph[now])):
        if graph[now][i] not in visited:
            visited = mx[0][:]
            mx.append(dfs(graph, visited, graph[now][i]))
    return max(mx, key=len)

def preproc(list_pairs, elec):            #функция создает список, где индекс - электрод, значение сколько раз встречается в протоколе
    res = {}
    for i, j  in list_pairs:
        if i not in res:
            res[i] = []
        if j not in res:
            res[j] = []
        res[i].append(j)
        res[j].append(i)
    return res

def parse_protokol(protokol_file_name, elec=72):
    with open(protokol_file_name) as f:                     
        protokol = list(map(lambda x: x.split(), f.readlines()))
    del protokol[:elec + 2]

    dictprot = {}
    for i in protokol:                                      
        ab = (int(i[1]), int(i[2]))    
        if ab not in dictprot:
            dictprot[ab] = []
        dictprot[ab].append((int(i[3]), int(i[4])))
    return dictprot

def processing(elec_dict, res = []):
    while not all(not value for value in elec_dict.values()):
        visited = []            #Получить цепь
        now = next((key for key, value in elec_dict.items() if len(value) % 2 != 0),  None) #дописать как выбирать первый 
        chain =  dfs(elec_dict, visited, now)
        res.append(chain)        
        for i in range(len(chain)-1):   #Удалить использованные электроды
            elec_dict[chain[i]].remove(chain[i + 1])
            elec_dict[chain[i + 1]].remove(chain[i])
    return(res)

def greedy_packing(chains_list, chan):
    el = chan + 1 #Для станции с общим электродом электродов на 1 больше, чем каналов
    if len(chains_list[0]) > el:  #Проверка на одно из придуманных ограничений, можно дописать отдельную обработку длинных цепей
        print('Fatal ERROR', alarm)
        
    res = []
    while chains_list != []:
        res.append([])
        j = 0
        while j != len(chains_list): #проход по всем элементам списка
            if len(res[-1]) + len(chains_list[j]) <= el:
                #Можно запомнить пару-склейку цепей для дальнейшего удаления
                res[-1].extend(chains_list[j])
                del chains_list[j]
                j -= 1
                if len(res[-1]) >= el - 1 or chains_list == []: #первая проверка - осталось ли еще 2 и более места, меньше не разместить цепочку, вторая - выход из цикла при пустом списке
                    break
            j += 1
    return res

        
def main_common_electrode(protokol_file_name, elec=72, chan=0):
    dictprot = parse_protokol(protokol_file_name, elec)
    count = 0
    for i in dictprot:
        chains_list = sorted(processing(preproc(dictprot[i], elec), []), key=len, reverse=True)
        a = greedy_packing(chains_list, chan)
        for j in a:
            print(i, ':', j)

filename = input("Укажите расположение файла: ")
electrods =  input("Укажите количество электродов: ")
chan = input("Укажите количество каналов: ")

main_common_electrode(filename, electrods, chan)                          

    
