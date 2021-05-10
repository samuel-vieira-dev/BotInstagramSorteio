from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time

navegador = webdriver.Chrome()
wait  = WebDriverWait(navegador, 10, 1)

def executar_login():    
    navegador.get("https://instagram.com")
    time.sleep(1)
    campo_usuario = navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    campo_usuario.click()
    time.sleep(2)
    campo_usuario.send_keys('samuelvvieira')
    campo_usuario.send_keys(Keys.TAB + 'samuel1100' + Keys.TAB + Keys.TAB + Keys.ENTER)
    time.sleep(5)

def inserir_comentario(comentario, repeticoes, pausa):
    for x in range(repeticoes):
        navegador.get("https://www.instagram.com/p/COY2MyXFOLl/")
        time.sleep(3)
        campo_comentario = wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH,'//div[@class="RxpZH"]')
            )
        )
        campo_comentario.click()
        campo_comentario = wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH,'//textarea[@placeholder="Adicione um comentário..."]')
            )
        )
        campo_comentario.send_keys(comentario + Keys.ENTER)
        time.sleep(pausa)
        print(x)

def inserir_comentario_lista(lista_contatos,pausa):
    for contato in lista_contatos:
        navegador.get('https://www.instagram.com/p/COY2MyXFOLl/')
        time.sleep(2)
        campo_comentario = wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH,'//div[@class="RxpZH"]')
            )
        )
        campo_comentario.click()
        campo_comentario = wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH,'//textarea[@placeholder="Adicione um comentário..."]')
            )
        )
        campo_comentario.send_keys(contato)
        botao_publicar = wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH,'//button[@type="submit"]')
            )
        )
        botao_publicar.click()
        time.sleep(pausa)

def carregar_contatos(arquivo):
    contatos = open(arquivo,'r', encoding='UTF-8')
    lista_contatos = contatos.read()
    lista_contatos = lista_contatos.split('\n')
    contatos_formatados=[]
    linha_atual = 1
    proxima_linha = -1
    for contato in lista_contatos:
        if contato[0:4] == 'Foto':
            proxima_linha = linha_atual + 1
        elif proxima_linha == linha_atual:
            contatos_formatados.append('@' + contato)

        linha_atual+=1

    return contatos_formatados

contatos = carregar_contatos('contatos.txt')
print(len(contatos), 'Usuários existentes na lista.')

executar_login()
inserir_comentario_lista(contatos, 5)