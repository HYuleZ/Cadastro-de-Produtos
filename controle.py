from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

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


def gerar_pdf():
    cursor = bd.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CÓDIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF GERADO COM SUCESSO!")


def excluir_dados():
    linha = listar_dados.tableWidget.currentRow()
    listar_dados.tableWidget.removeRow(linha)
    cursor = bd.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))


def editar_dados():
    global numero_id
    linha = listar_dados.tableWidget.currentRow()
    cursor = bd.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][3]))
    numero_id = valor_id


def salvar_dados_editados():
    global numero_id

    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    cursor = bd.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = '{}'".format(codigo, descricao, preco, categoria, numero_id))
    tela_editar.close()
    segunda_tela()

app=QtWidgets.QApplication([])
formulario = uic.loadUi("cadastro-produto.ui")
listar_dados = uic.loadUi("listar-produtos.ui")
tela_editar = uic.loadUi("menu_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(segunda_tela)
listar_dados.pushButton.clicked.connect(gerar_pdf)
listar_dados.pushButton_2.clicked.connect(excluir_dados)
listar_dados.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton_4.clicked.connect(salvar_dados_editados)

formulario.show()
app.exec()