

from fpdf import FPDF
import os
from datetime import datetime, timedelta
import re
import uuid

from pix_utils import gerar_pix_copia_e_cola


def gerar_pdf(
	nome,
	valor_total,
	parcelas,
	pix_code,
	pasta_destino,
	data_primeiro_vencimento=None,
	pix_key='',
	pix_receiver_name='IECA',
	pix_city='ANGRA'
):
	pdf = FPDF()
	valor_parcela = float(valor_total) / int(parcelas)
	os.makedirs(pasta_destino, exist_ok=True)
	qrcode_disponivel = True
	try:
		import qrcode
	except Exception:
		qrcode_disponivel = False
	if not data_primeiro_vencimento:
		data_primeiro_vencimento = datetime.today()
	else:
		data_primeiro_vencimento = datetime.strptime(data_primeiro_vencimento, "%d/%m/%Y")

	nome_base = (nome or "boleto").strip()
	nome_base = re.sub(r"\s+", "_", nome_base)
	nome_base = re.sub(r"[^A-Za-z0-9_\-]", "", nome_base)
	if not nome_base:
		nome_base = "boleto"
	sufixo_unico = uuid.uuid4().hex[:8]

	for i in range(int(parcelas)):
		if pix_code and pix_code != 'CONFIGURE_O_PIX_CODE_NAS_VARIAVEIS_DE_AMBIENTE':
			pix_payload = pix_code
		else:
			pix_payload = gerar_pix_copia_e_cola(
				chave_pix=pix_key,
				nome_recebedor=pix_receiver_name,
				cidade=pix_city,
				valor=valor_parcela,
				txid=f'PARC{i+1:03d}'
			)

		pdf.add_page()
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 12, 'Boleto Retiro Espiritual 2027 - IECA', ln=True, align='C')
		pdf.ln(4)
		pdf.set_font('Arial', '', 12)
		pdf.cell(0, 10, f'Nome: {nome}', ln=True)
		pdf.cell(0, 10, f'Parcela: {i+1} de {parcelas}', ln=True)
		pdf.cell(0, 10, f'Valor da Parcela: R$ {valor_parcela:.2f}', ln=True)
		data_venc = data_primeiro_vencimento + timedelta(days=30*i)
		pdf.cell(0, 10, f'Vencimento: {data_venc.strftime("%d/%m/%Y")}', ln=True)
		pdf.cell(0, 10, 'Banco: Bradesco (237)', ln=True)
		pdf.cell(0, 10, 'Agência: 0459-6 Conta: 35369-8', ln=True)
		pdf.cell(0, 10, 'CNPJ: 29830783/0001-12', ln=True)
		pdf.ln(4)
		pdf.set_font('Arial', 'B', 12)
		pdf.cell(0, 10, 'PIX:', ln=True)
		pdf.set_font('Arial', '', 11)
		pdf.multi_cell(0, 8, pix_payload)
		if qrcode_disponivel:
			# Gerar QR Code do PIX
			qr_img = qrcode.make(pix_payload)
			qr_path = os.path.join(pasta_destino, f"pix_qr_{sufixo_unico}_{i}.png")
			qr_img.save(qr_path)
			pdf.image(qr_path, x=pdf.get_x()+60, y=pdf.get_y(), w=50, h=50)
			pdf.ln(55)
		else:
			pdf.ln(10)
			pdf.set_font('Arial', 'I', 10)
			pdf.cell(0, 8, 'QR Code indisponivel neste ambiente. Use o codigo PIX acima.', ln=True)
		pdf.set_font('Arial', 'I', 10)
		pdf.multi_cell(0, 7, 'Mensagem:\nOlá, este boleto refere-se ao Retiro Espiritual 2027 da IECA.\nRegras: Valor total pode ser parcelado em até 10x. Não pode atrasar mais de 3 parcelas, senão o boleto será cancelado e o valor devolvido. O pagamento pode ser feito via Pix (QR Code acima) ou depósito bancário.')
		# Remove QR temporário
		if qrcode_disponivel:
			try:
				os.remove(qr_path)
			except Exception:
				pass

	filename = f"boleto_{nome_base}_{sufixo_unico}.pdf"
	caminho = os.path.join(pasta_destino, filename)
	pdf.output(caminho)
	return filename
