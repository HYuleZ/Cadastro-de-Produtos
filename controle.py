from PyQt5 import uic,QtWidgets
import mysql.connector

bd = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria = ""

    print("Código:",linha1)
    print("Descrição:",linha2)
    print("Preço:",linha3)

    if formulario.radioButton.isChecked() :
        print("Categoria: Informática")
        categoria = "Informatica"
    elif formulario.radioButton_2.isChecked() :
        print("Categoria: Alimentos")
        categoria = "Alimentos"
    elif formulario.radioButton_3.isChecked() :
        print("Categoria: Eletrônicos")
        categoria = "Eletronicos"
    else:
        print("Nenhuma categoria foi selecionada...") 
        categoria = ""

    cursor = bd.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3),categoria)
    cursor.execute(comando_SQL, dados)
    bd.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def segunda_tela():
    listar_dados.show()

    cursor = bd.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    # print(dados_lidos)
    listar_dados.tableWidget.setRowCount(len(dados_lidos))
    listar_dados.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            listar_dados.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app=QtWidgets.QApplication([])
formulario=uic.loadUi("cadastro-produto.ui")
listar_dados=uic.loadUi("listar-produtos.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(segunda_tela)

formulario.show()
app.exec()