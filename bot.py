from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import PySimpleGUI as sg

def interface():
    sg.theme('DarkBlue14')
    layout = [
    [sg.Text('Usuário:'), sg.InputText(size=(20,0),key='usuario'), sg.Text('Senha:'), sg.InputText(size=(20,0),key='senha')],
    [sg.Text('Link Sorteio:'), sg.InputText(size=(20,0),key='link_sorteio'), sg.Text('Nº de Marcações:'), sg.InputText(size=(6,0), key='n_marcacoes')],
    [sg.Text('Tempo de espera entre comentários (segundos):'), sg.InputText(size=(17,0), key='intervalo_comentarios')],
    [sg.Button(('Iniciar'), size=(50,0))]
        ]

    window = sg.Window('Robô Instagram', layout)

    while True:
        event, values = window.read()

        usuario = values['usuario']
        senha = values['senha']
        link_sorteio = values['link_sorteio']
        n_marcacoes = int(values['n_marcacoes'])
        intervalo_comentarios = int(values['intervalo_comentarios'])

        if event == sg.WIN_CLOSED:
            break
        if event == 'Iniciar':
            robo(usuario, senha, link_sorteio, n_marcacoes, intervalo_comentarios)

    window.close()

def robo(usuario, senha, link_sorteio, n_marcacoes, intervalo_comentarios):
    def executar_login():
        navegador.get("https://www.instagram.com")
        time.sleep(3)
        campo_usuario = navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        campo_usuario.click()
        time.sleep(1)
        campo_usuario.send_keys(usuario)
        time.sleep(1)
        campo_senha = navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        campo_senha.click()
        time.sleep(1)
        campo_senha.send_keys(senha)
        time.sleep(1)
        campo_senha.send_keys(Keys.ENTER)
        time.sleep(10)

    def inserir_comentario(comentario,repeticoes,pausa):
        for x in range(repeticoes):
            navegador.get(link_sorteio)
            time.sleep(5)
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
            campo_comentario.send_keys(comentario)
            campo_comentario.send_keys(Keys.ENTER)
            time.sleep(pausa)
            print(x)

    def inserir_comentario_lista(lista_contatos,pausa):
        for contato in lista_contatos:
            navegador.get(link_sorteio)
            time.sleep(5)
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

    def carregar_contatos(arquivo,n_marcacoes):
        contatos = open(arquivo,'r',encoding='UTF-8')
        lista_contatos = contatos.read()
        lista_contatos = lista_contatos.split('\n')
        contatos_formatados=[]
        linha_atual=1
        proxima_linha=-1
        contador=0
        contato_formatado=''   
        for contato in lista_contatos:
            if contato[0:4] == 'Foto':
                proxima_linha=linha_atual+1
            elif proxima_linha == linha_atual:
                contador+=1
                if len(contato_formatado)>0:
                    contato_formatado+='@'+contato+' '
                else:
                    contato_formatado='@'+contato+' '
                    
            if contador == n_marcacoes:
                contatos_formatados.append(contato_formatado)            
                contador=0
                contato_formatado=''
            
            linha_atual+=1 #linha_atual=5
        
        return contatos_formatados

    print(n_marcacoes)

    contatos = carregar_contatos('contatos.txt', n_marcacoes) 
    print(len(contatos),'Contatos carregados.')
    navegador = webdriver.Chrome()
    wait = WebDriverWait(navegador, 10, 1)
    executar_login()
    inserir_comentario_lista(contatos, intervalo_comentarios)

##########CHAMADA
interface()