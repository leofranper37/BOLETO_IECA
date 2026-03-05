import os
import traceback
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
			pix_code = (current_app.config.get('PIX_CODE', '') or '').strip()
			pix_key = (current_app.config.get('PIX_KEY', '') or '').strip()
			pix_receiver_name = (current_app.config.get('PIX_RECEIVER_NAME', '') or 'IECA').strip()
			pix_city = (current_app.config.get('PIX_CITY', '') or 'ANGRA').strip()
			if (not pix_code or pix_code == 'CONFIGURE_O_PIX_CODE_NAS_VARIAVEIS_DE_AMBIENTE') and not pix_key:
				return render_template(
					'form.html',
					erro='Configure PIX_CODE ou PIX_KEY nas variáveis de ambiente do servidor.'
				)

			pdf_dir = os.path.join(current_app.root_path, 'static', 'pdfs')
			try:
				filename = gerar_pdf(
					nome=nome,
					valor_total=valor_total,
					parcelas=parcelas,
					pix_code=pix_code,
					pix_key=pix_key,
					pix_receiver_name=pix_receiver_name,
					pix_city=pix_city,
					pasta_destino=pdf_dir,
					data_primeiro_vencimento=None,
				)
				return render_template('boleto_gerado.html', filename=filename)
			except Exception:
				traceback.print_exc()
				return render_template(
					'form.html',
					erro='Nao foi possivel gerar o boleto agora. Tente novamente em instantes.'
				)

		return render_template('form.html')
