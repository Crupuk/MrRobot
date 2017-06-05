from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
import time
import datetime
import sys

PASTA_PADRAO = "C:\\leonardo\\projs\\robot"
CASA = "Avenida Jornalista Henrique Cordeiro, Barra da Tijuca, Rio de Janeiro"
TRABALHO = "Avenida Augusto Severo, 84 - Glória, Rio de Janeiro - RJ, Brasil"

class Waze():

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.browser.get("https://www.waze.com/pt-BR/livemap")

    def fillForm(self,periodo):
        try:
            print("\nPreenchendo  Formulário...")
            campoOrigem = self.browser.find_element_by_xpath("//div[@id='origin']/div/span/input[1]")
            campoOrigem.clear()
            
            if(periodo=="manha"):
                campoOrigem.send_keys(CASA)
            else:
                campoOrigem.send_keys(TRABALHO)
            
            time.sleep(1)
            campoOrigem.send_keys(Keys.DOWN)
            campoOrigem.send_keys(Keys.ENTER)
            time.sleep(1)
            
            #O Waze não aceita clicar na lupa. Faz-se necessario selecionar com o mouse ou teclado
            campoDestino = self.browser.find_element_by_xpath("//div[@id='destination']/div/span/input[1]")
            campoDestino.clear()

            if(periodo=="manha"):
                campoDestino.send_keys(TRABALHO)
            else:
                campoDestino.send_keys(CASA)

            time.sleep(1)
            campoDestino.send_keys(Keys.DOWN)
            campoDestino.send_keys(Keys.ENTER)
        except:
            pass

class Maps:
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.browser.get("https://www.google.com.br/maps/@-22.9949984,-43.2742303,14z/data=!5m1!1e1")
    

def setPeriodicidade():
        horaatual =  time.gmtime().tm_hour - 3
        if(6<=horaatual<10 or 15<=horaatual<=20):
                return(15)
        elif(10<=horaatual<15):
                return(45)
        else:
                return(60)

def determinaPeriodo():
    horaatual = time.gmtime().tm_hour - 3
    if(0<horaatual<10):
        return("manha")
    else:
        return("tarde")

def salvarScreenshot(browser, nome):
        today = datetime.date.today()
        os.chdir(PASTA_PADRAO)
        os.makedirs(str(today), exist_ok=True)
        os.chdir(str(today))

        browser.browser.refresh()
        if(isinstance(browser,Waze)):
            browser.fillForm(determinaPeriodo())
        time.sleep(5)
        if(isinstance(browser,Waze)):nome = "Waze-"+nome
        browser.browser.save_screenshot(str(nome))
      
        print("\nSalvando arquivo:%s ..."%nome)

def getNomeArquivo():
        now = datetime.datetime.now()
        return("Barra "+str(now.hour)+"-"+str(now.minute)+"-"+str(now.second)+".png")

def contagemRegressiva(tempo):
    for i in range(tempo, 0,-1):
            sys.stdout.write("\rPróximo monitoramento em {0} seg".format(i))
            sys.stdout.flush()
            time.sleep(1)

if __name__ == "__main__":
        try:
            waze = Waze()
            #maps = Maps()
            print("Pressione CTRL+C para interromber o monitoramento...")            
            
            while(True):
                #salvarScreenshot(maps, getNomeArquivo())
                salvarScreenshot(waze,getNomeArquivo())
                periodicidade = setPeriodicidade()
                contagemRegressiva(periodicidade*60)
        except KeyboardInterrupt:
            print("Bye")
        except Exception as e:
            print("[-]ERRO -"+str(e))