#! python3
import sys, webbrowser, bs4, requests, os, smtplib, sys
from tqdm import tqdm

#------------------------------------------------------------
#Alunos: Bruno H Raiher, Eric M Rocha
#Data: 26-05-2019
#Progama gera lista com os 20 melhores
#filmes do imdb com ordenação pelas
#colunas e baixa capa dos filmes
#------------------------------------------------------------

#------------------------------------------------------------
#..:declara as variaveis e as listas:..
#------------------------------------------------------------
start = 1
nomes = []
anos = []
ratings = []
metascores = []
votos = []
list_url_filme = []
                                    
print("Relação de filmes do IMDB.")
print("Buscando dados dos filmes...")
print("Aguarde...")
#for para buscar 2000 filmes.
for i in tqdm(range(start, 2001)):
   #url do site concatenado com o valor  incial da pagina
   url = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,short&release_date=2017,2017&sort=num_votes,desc&count=1&start='+ str(i)
   res = requests.get(url)
   res.raise_for_status()
   soup = bs4.BeautifulSoup(res.text, 'html.parser')
   
   #------------------------------------------------------------
   #..:busca os dados na pagina(Nome, ano, rating, metascore, votos):..
   #------------------------------------------------------------

   #captura o titulo do filme
   filme_nome = soup.select('h3.lister-item-header > a:nth-of-type(1)')
   #condição para inserir dado na lista caso não haja dado
   if (len(filme_nome) == 0):
        filme_nome.append("ND") 
        list_url_filme.append("ND") 
   else:
        for index, item in enumerate(filme_nome, start=0): 
      #insere o nome do filme  
            nome = item.contents[0]
            nome = nome.replace (":","")
            nomes.append(nome)
      #insere o link da imagem
            list_url_filme.append(filme_nome[index].get('href')) 

      
   #captura o ano do filme
   filme_ano = soup.select('h3.lister-item-header > span:nth-of-type(2)')
   if (len(filme_ano) == 0):
        anos.append("1900") 
   else:
        for index, item in enumerate(filme_ano, start=0):
               anos.append(item.contents[0])


   #captura o rating do filme
   filme_rating = soup.select('div.ratings-imdb-rating > strong')
   if (len(filme_ano) == 0):
        ratings.append("ND") 
   else:
        for index, item in enumerate(filme_rating, start=0):   
      #insere na lista todos as Classificações dos filmes
             ratings.append(item.contents[0])


   #captura o metascore do filme
   filme_metascore = soup.select('div.ratings-metascore > span.metascore')
   if (len(filme_metascore) == 0):
        metascores.append("ND") 
   else:
        for index, item in enumerate(filme_metascore, start=0):   
      #insere na lista todos os metascore dos filmes
            metascores.append(item.contents[0]) 
      

   #captura os votos do filme
   filme_voto = soup.select('p.sort-num_votes-visible > span:nth-of-type(2)')
   if (len(filme_voto) == 0):
        votos.append("ND") 
   else:
        for index, item in enumerate(filme_voto, start=0): 
            #insere na lista todos os votos dos filmes
            votos.append(item.contents[0]) 

   
#------------------------------------------------------------------------------------------------------------------
#..:Criará uma lista com os dados requeridos, para depois ordena-los:..
#------------------------------------------------------------------------------------------------------------------

print("Dados encontrados.")
filmes =[]
for i in range(0,len(nomes)):
       #gera uma lista com os dados dos filmes
    filmes += [(nomes[i] , anos[i] , ratings[i] , votos[i] , metascores[i] , list_url_filme[i])]

print("Encontrado: "+ str(len(filmes)) + " filmes")

print("Como você deseja ordenar a lista de filmes?")
aux = int(input("1 = Nome, 2 = Ano, 3 = Classificação, 4 = Votos, 5 = Metascore "))
#enquanto o valor for incorreto a execução continua
while aux > 5 or aux < 1:
    print("1 = Nome, 2 = Ano, 3 = Classificação, 4 = Votos, 5 = Metascore ")
    aux = int(input('Valor incorreto! Informe novamente um valor: '))
   
ordena = int(input("Ordenar de forma Crecsente ou Descresente? 1 = Crescente , 2 = Decrecente "))
while ordena > 2 or ordena < 1:
    ordena = int(input("Valor incorreto! Informe novamente um valor: "))
if(ordena == 1):
    ordenacao = False
else: 
    ordenacao = True

def segundo(elem):
   #Cria a função para ordenar os filmes conforme o parâmetro passado pelo usuário. O elemento define a coluna que será ordenada.
    return elem[aux-1]
#ordena os filmes conforme os parametros do usuario
filmes.sort(key=segundo, reverse = ordenacao)

#------------------------------------------------------------
#..:Gera os arquivos:..
#------------------------------------------------------------
print("Gerando arquivo com os 20 melhores")
print("Aguarde...")

#cria o arquivo de ranking dos 20 melhores 
arquivo = open('ranking.txt','w')

#cria a pasta se não existir para salvar as capas dos filmes
os.makedirs('fotos', exist_ok=True) 

try:
      #escreve o cabeçalho do  arquivo
   arquivo.write('{:20}   {:20}{:20}{:50}{:20}{:10}'.format('#' ,"imdb","metascore","filme","votos","ano")) #formata para ser semelhante a uma tabela
   arquivo.write("\n")  

   for index in tqdm(range(0, 20)): #um for para trazer apenas os 20 primeiros
      if(filmes[index][4] == "ND"):
             del filmes[index]
         #formata os dados das listas para exibir de forma de uma tabela
      arquivo.write('{:20}   {:20}{:20}{:50}{:20}{:20}'.format(str(index+1),filmes[index][2] ,filmes[index][4],filmes[index][0],filmes[index][3],filmes[index][1]))
      arquivo.write("\n")  
         #coloca o inicio do link, pois o href vem essa parte
      url_filme = "https://www.imdb.com" + filmes[index][5]
         #abre o link da pagina do filme
      img = requests.get(url_filme)
      img.raise_for_status()
      soup_img = bs4.BeautifulSoup(img.text, 'html.parser')
         
         #localiza o elemento da capa do filme
      capa_filme_elemento = soup_img.select('div.poster > a >img')
         #obtem a url da imagem da capa do filme
      capa_filme_url = capa_filme_elemento[0].get('src')
         #abre o link da capa do filme
      capa_filme = requests.get(capa_filme_url)
         #cria o arquivo jpg com nome do filme na pasta fotos
      try:
         #remove o caracteres que podem dar erro ao ser utilizado no nome do arquivo jpg
         nome = filmes[index][0]
         nome = nome.replace ("/","")
         nome = nome.replace ("|","")
         nome = nome.replace ("?","")
         nome = nome.replace (":","")
         nome = nome.replace ("“","")
         nome = nome.replace ("<","")
         nome = nome.replace (">","")
         nome = nome.replace ("!","")
         nome = nome.replace ("*","")
         imageFile = open(os.path.join('fotos', os.path.basename(nome +".jpg")), 'wb')
            #pega por chunk's os dados da imagem da url aberta
         for chunk in capa_filme.iter_content(100000):
               #grava os dados dentro da imagem
            imageFile.write(chunk)
            #finaliza a imagem
         imageFile.close()
      except:
         print(' A capa do filme não foi gerada!')
         #fecha o arquivo
   arquivo.close()
   print("Arquivo ranking.txt gerado com sucesso!")
except:
   print("Arquivo ranking.txt não pode ser gerado!")