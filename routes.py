import os
from flask import current_app, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from gerar_pdf import gerar_pdf


def init_routes(app):
	@app.route('/download_pdf/<filename>')
	def download_pdf(filename):
		pdf_dir = os.path.join(current_app.root_path, 'static', 'pdfs')
		safe_filename = secure_filename(filename)
		return send_from_directory(pdf_dir, safe_filename, as_attachment=True)

	@app.route('/', methods=['GET', 'POST'])
	def index():
		if request.method == 'POST':
			nome = (request.form.get('nome') or '').strip()
			parcelas_raw = request.form.get('parcelas') or '1'
			concorda = request.form.get('concorda')

			if not nome:
				return render_template('form.html', erro='Informe o nome do solicitante.')

			if not concorda:
				return render_template('form.html', erro='É necessário concordar com as regras para continuar.')

			try:
				parcelas = int(parcelas_raw)
			except ValueError:
				return render_template('form.html', erro='Número de parcelas inválido.')

			max_parcelas = int(current_app.config.get('MAX_PARCELAS', 10))
			if parcelas < 1 or parcelas > max_parcelas:
				return render_template(
					'form.html',
					erro=f'Número de parcelas deve estar entre 1 e {max_parcelas}.'
				)

			valor_total = float(current_app.config.get('VALOR_TOTAL', 400.0))
			pix_code = current_app.config.get('PIX_CODE', '')
			if not pix_code:
				return render_template('form.html', erro='Configuração de PIX não encontrada no servidor.')

			pdf_dir = os.path.join(current_app.root_path, 'static', 'pdfs')
			filename = gerar_pdf(
				nome=nome,
				valor_total=valor_total,
				parcelas=parcelas,
				pix_code=pix_code,
				pasta_destino=pdf_dir,
				data_primeiro_vencimento=None,
			)
			return render_template('boleto_gerado.html', filename=filename)

		return render_template('form.html')
