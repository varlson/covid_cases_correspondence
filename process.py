from util import *
from scipy.stats import spearmanr
import matplotlib.pyplot as plt


"""
    sort_by_metric => Ordena os nós da rede de acordo com as metricas
    
    paramentros:
        graph => rede(Igraph)
        metric => metrica(string)
        
"""


def sort_by_metric(graph, metric):
    
    peso = None
    
    if metric == "strength" or "betweenness_w":
        peso = graph.es['weight']
        peso = [0.001 if x <= 0 else x for x in peso]

    
    weighted =[]
    if metric == "strength":
        weighted =  graph.strength(weights=peso)
    else:
        # print(peso)
        weighted =  graph.betweenness(weights=peso)

    
    done =None
    
    if metric == "degree":
        temp =[]
        for x in range(graph.vcount()):
            temp.append([x, graph.degree(x), graph.vs['label'][x], graph.vs['geocode'][x]])
            done =temp
    elif metric == "betweenness":
        done = [[x, graph.betweenness(x), graph.vs['label'][x], graph.vs['geocode'][x]] for x in range(graph.vcount())]
        temp =[]
        for x in range(graph.vcount()):
            temp.append([x, graph.betweenness(x), graph.vs['label'][x], graph.vs['geocode'][x]])
            done =temp
            
    elif metric == "strength":
        temp =[]
        for index, x in enumerate(weighted):
            temp.append([index, x, graph.vs['label'][index], graph.vs['geocode'][index]])
            done =temp
    
    else:
        done = [[index, x, graph.vs['label'][index], graph.vs['geocode'][index]] for index, x in enumerate(weighted)]    
        temp=[]
        for index, x in enumerate(weighted):
            temp.append([index, x, graph.vs['label'][index], graph.vs['geocode'][index]])
            done =temp
            
    done = sorted(done, key=lambda data: data[1], reverse=True)
    return done


def sort_by_metric_costomized(graph, metric, no_in_list):
    peso = None
    
    if metric == "strength" or "betweenness_w":
        peso = graph.es['weight']
        peso = [0.001 if x <= 0 else x for x in peso]

    
    weighted =[]
    if metric == "strength":
        weighted =  graph.strength(weights=peso)
    else:
        # print(peso)
        weighted =  graph.betweenness(weights=peso)

    
    done =None
    
    if metric == "degree":
        temp =[]
        for x in range(graph.vcount()):
            if graph.vs['geocode'][x] not  in no_in_list:
                temp.append([x, graph.degree(x), graph.vs['label'][x], graph.vs['geocode'][x]])
        done =temp
    elif metric == "betweenness":
        
        temp =[]
        for x in range(graph.vcount()):
            if graph.vs['geocode'][x] not  in no_in_list:
                temp.append([x, graph.betweenness(x), graph.vs['label'][x], graph.vs['geocode'][x]])
        done =temp
            
    elif metric == "strength":
        temp =[]
        for index, x in enumerate(weighted):
            if graph.vs['geocode'][index] not  in no_in_list:
                temp.append([index, x, graph.vs['label'][index], graph.vs['geocode'][index]])
        done =temp
    
    else:
        
        temp=[]
        for index, x in enumerate(weighted):
            if graph.vs['geocode'][index] not  in no_in_list:
                temp.append([index, x, graph.vs['label'][index], graph.vs['geocode'][index]])
        done =temp
            
    done = sorted(done, key=lambda data: data[1], reverse=True)
    return done



"""
    correspondence_builder => Estabele a relação entre as apariçoes de casos e nós da rede
    
    Parametros:
        cities => Lista de geocodigos de cidades extraido do DataFrame(pandas) 
        sorted_by_metric => Lista de geocodigos de cidades extraido do graph(igrap) ordenados de acordo com metrica
    
    Retorno:
        Retorna lista de correspondencia 
"""
def correspondence_builder(cities, sorted_by_metric):
    list_of_correspondence=[]
    
    for index, geocode in enumerate(cities):
        
        list_of_correspondence.append(float(counter(index+1, sorted_by_metric, cities)/(index+1)))
        
    return list_of_correspondence






"""
    mapeador function => A função cria e mapea indices de nós de acordo lista de nós ordenados pela metrica,
    criando e retornando assim o coeficiente de spearmman baseados nas listas de indices de cidades e de nós
    
    Paramentros:
        cites => DataFrame(pandas) de cidades com nomes, estados, geocodigos...
        sorted_by_metric => Matrix de nós ordenados pela metrica colunas com (indece de nó, valor de metrica, label, geocode)
        name =>  nome do ficheiro csv para guardar as duas listas
"""



def mapeador(cities, sorted_by_metrics):
    
    net_index=[]
    cid_index=[]
    ausentes=[]
    for index, node in enumerate(sorted_by_metrics):
        try:
            i = list(cities['Geocode']).index(node[3])
            cid_index.append(i)
            net_index.append(index)
        except:
            ausentes.append(node[3])
    
    return spearmanr(cid_index, net_index)



""" list_of_coord =>lista de tuplas de coordenadas x e y 
    label => lista de labels de legenda dos plots
    name => node do arquivo plot
"""
def graphPloter(list_of_coord, labels, name, o_path): 
    plt.clf()
    for index, coord in enumerate(list_of_coord):
        x = coord[0]
        y = coord[1]
        sper = coord[2]
        corr = "{:.8f}".format(sper[0])
        pval = "{:.8f}".format(sper[1])
        plt.plot(x, y, label=labels[index]+' sp: '+corr+' pv: '+pval, marker="1")
    
    plt.legend()
    plt.title(name)
    dirMaker(o_path)
    plt.savefig(o_path+'/'+name+'.png')



def indexFilter(geocodes, graph):
    index=0
    list_of_index=[]
    
    for geo in graph.vs['geocode']:
        if geo in geocodes:
            list_of_index.append(index)
            index+=1
    return list_of_index




def filter(network, city_cases, name):
    
    length = network.vcount()
    geocode =[]
    datas =[]
    utps=[]
    ausente=[]
    cidades=[]
    

    
    for i, geo in enumerate(network.vs['geocode']):
        try:
            index = list(city_cases['Geocode']).index(geo)
            geocode.append(geo)
            cidades.append(network.vs['label'][i])
        except:
            ausente.append(geo)            
    
    
    print(f'len net: {network.vcount()}')
    print(f'len cidades: {len(cidades)}')
    
    df = {}
    # df['Datas'] = datas
    df['Cidades'] = cidades
    # df['Estados'] = estados
    df['Geocode'] = geocode
    # if isAereal:
    #     df['UTP'] = utps
    df = pd.DataFrame(df)
    _path = 'Filtrados'
    dirMaker(_path)
    
    pd.DataFrame({'Ausentes':ausente}).to_csv(_path+'/ausentes_terrestrial.csv', index=False)
    df.to_csv(_path+'/'+name+'.csv')
    
    


def extractor(dataFrame, graph, full_path, name): # This function extract datas from big big data file    
    
    g_geocode = [float(x) for x in graph.vs['geocode']]
    df_geocode = [float(x) for x in list(dataFrame['ibgeID'])]
    
    
    geocode = []
    cities = []
    states =[]
    ausentes =[]
    
    
    for geoc in g_geocode:
        
        if geoc in df_geocode:
            i = df_geocode.index(geoc)
            geocode.append(geoc)
            cities.append(dataFrame['city'][i])
            states.append(dataFrame['state'][i])
        else:
            ausentes.append(geoc)
    df ={}
    
    df['Cidades'] = cities
    df['Estados'] = states
    df['Geocode'] = geocode
    
    df = pd.DataFrame(df)
    dirMaker(full_path)
    df.to_csv(full_path+'/'+name+'.csv', index=False)
    pd.DataFrame({
        'Ausentes':ausentes
    }).to_csv(full_path+name+'_ausentes.csv', index=False)
        


''' -------------------------------------NORTH OF BRAZIL PROCESSOR--------------------------------
'''


def northBrazil_extractor(dataFrame, netwwork, output_path):
    NORTH_START_GEO=[12, 16, 13, 17, 14, 11, 15]
    
    df_geocodes = list(dataFrame['Geocode'])
    cities=[]
    ausentes =[]
    geocode=[]
    for geocod in netwwork.vs['geocode']:
        
        state_geo = int(str(int(geocod))[:2])
        if state_geo in NORTH_START_GEO:
            try:
                index = df_geocodes.index(geocod)
                cities.append(dataFrame['Cidades'][index])
                geocode.append(df_geocodes[index])
            except:
                ausentes.append(geocod)
        else:
            ausentes.append(geocod)
       
    
    df={}
    df['Cidades'] =cities
    df['Geocode'] = geocode
        
    df = pd.DataFrame(df)
    df.to_csv(output_path+'.csv', index=False)
    pd.DataFrame({
        'Ausentes': ausentes
    }).to_csv(output_path+'_ausentes.csv', index=False)


''' -------------------------------------AMAZONAS STATES--------------------------------
'''


def amazonas_extractor(dataFrame, netwwork, output_path):
    
    df_geocodes = list(dataFrame['Geocode'])
    cities=[]
    ausentes =[]
    geocode=[]
    for geocod in netwwork.vs['geocode']:
        
        state_geo = int(str(int(geocod))[:2])
        if state_geo ==13:
            try:
                index = df_geocodes.index(geocod)
                cities.append(dataFrame['Cidades'][index])
                geocode.append(df_geocodes[index])
            except:
                ausentes.append(geocod)
       
    
    df={}
    df['Cidades'] =cities
    df['Geocode'] = geocode
        
    df = pd.DataFrame(df)
    df.to_csv(output_path+'.csv', index=False)

    pd.DataFrame({
        'Ausentes': ausentes
    }).to_csv(output_path+'_ausentes.csv', index=False)





def processed_data_exporter(x_axis, y_axis,o_path, name):
    dirMaker(o_path)
    pd.DataFrame({
        'X_axis': x_axis,
        'Y_axis': y_axis
    }).to_csv(o_path+'/'+name+'.csv')