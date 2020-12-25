#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 20:07:52 2020

@author: Carlos Meijide García
"""
# tentamos como primeira aproximacion recuperar os datos directamente do NCBI
# selenium e unha biblioteca que fai scraping pasando directamente por chrome 
# tras chamalo cun driver

# e preciso facer dous pasos antes da primeira execucion
# 1 pip install selenium
# 2 meter o arquivo chromedriver en C:\Windows ou para linux en anaconda3/bin
# eu anexo o correspondente a version 86 de chrome windows pero se houbera fallos
# simplemente descargar a version que pida a terminal de Python na mensaxe de erro
# https://sites.google.com/a/chromium.org/chromedriver/downloads

# agora xa se pode executar todo o codigo 

# EN CASO DE NON FUNCIONAR O METODO AUTOMATICO: tan so pegar o fragmento de adn
# e a solucion coñecida nos seus respectivos arquivos, e cambiar a auto=0

auto=0

if auto==0 :
    f = open("adn.txt", "r")
    txt2=f.read()
    f.close()
    f = open("solucion.txt", "r")
    sol=f.read()
    f.close()
    
else :
    # direccion NCBI da secuencia de interese
    url = "https://www.ncbi.nlm.nih.gov/nuccore/NM_207618.2"
    
    from bs4 import BeautifulSoup
    from selenium import webdriver as wd
    
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    
    # creamos navegador fake 
    options = wd.ChromeOptions()
    options.add_argument('headless')
    browser = wd.Chrome(chrome_options=options)
    
    # abrimos url para que cargue
    browser.get(url)
    
    # resulta que a informacion que nos interesa no NCBI
    # carga a posteriori da plantilla
    # temos enton que insistir ata que apareza o que queremos
    delay = 3 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'NM_207618.2_481')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
        
    # recuperamos html
    html = browser.page_source
    
    # facemos parse
    soup = BeautifulSoup(html, 'html.parser')
    
    # e comprobamos que conseguimos a paxina
    rows = soup.find_all('div',{'class': 'sequence'})
    for row in rows:          # Print all occurrences
        print(row.get_text())
        
    # e obtemos o corpo da web
    txt=row.text
    
    ##### limpamos a cadea de mRNA 
    txt2=txt[txt.find("ORIGIN"):]
    txt2=txt2[txt2.find("1"):]
    
    # recuperamos e limpamos a solucion do NCBI
    sol=txt[txt.find('translation="'):]
    sol=sol[sol.find('M'):sol.find('"\n')]

##### formateamos (e aqui onde se salta en caso de problemas co selenium)
strand=txt2.translate({ord(i): None for i in '0123456789\t\n// '})
solucion=sol.translate({ord(i): None for i in '\n '})

#cambiamos ADN a ARN (T->U) 
arn1=strand.replace("t", "u")

# e poñemola en maiusculo
arn=arn1.upper()

# obtemos a taboa de codons https://gist.github.com/stepjue/b2e957215f4e5121fa14
import urllib.request

code = 'https://gist.githubusercontent.com/stepjue/b2e957215f4e5121fa14/raw/fa13ee5332b14924af1f5cde4074b1c9aaa9e183/rna_codons.py'

response = urllib.request.urlopen(code)
data = response.read()
temp=data.decode("utf-8") 
taboa=temp[temp.find("codons"):(temp.find("}")+1)]

exec(taboa)

# e gardamola
cod=codons

# start en metionina
key_list = list(cod.keys()) 
val_list = list(cod.values()) 

# para iso buscamos que codon a codifica
M=key_list[val_list.index('M')]

# e buscamolo
sec=arn[arn.find(M):]

# comezamos a traducir de tres en tres bases nitroxenadas ate dar 
# cun dos codons stop
c=cod[sec[0:3]]
i=0

proteina=""

while c!="Stop" :
      proteina += c
      i+=3
      c=cod[sec[i:i+3]]
      
# exportamos finalmente o computado
if proteina==solucion:
  print("A transcricion foi exitosa, ver resultado en transcricion.txt")
  g = open("transcricion.txt", "w")
  g.write("Transcricion exitosa \n")
  g.write(proteina)
  g.close()
else :
  print("A transcricion foi defectuosa, ver ambos resultados en transcricion.txt ")
  g = open("transcricion.txt", "w")
  g.write("Transcricion defectuosa \n")
  g.close()
  g = open("transcricion.txt", "a")
  g.write("NCBI: \n")
  g.write(solucion)
  g.write("\n")
  g.write("A nosa transcricion: \n")
  g.write(proteina)
  g.close()





      
      
      
    


    


