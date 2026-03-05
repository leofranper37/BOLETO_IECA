import os


class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'troque-esta-chave-em-producao')
	MAX_PARCELAS = int(os.getenv('MAX_PARCELAS', '10'))
	VALOR_TOTAL = float(os.getenv('VALOR_TOTAL', '400'))
	PIX_CODE = os.getenv(
		'PIX_CODE',
		'CONFIGURE_O_PIX_CODE_NAS_VARIAVEIS_DE_AMBIENTE'
	)
	PIX_KEY = os.getenv('PIX_KEY', '')
	PIX_RECEIVER_NAME = os.getenv('PIX_RECEIVER_NAME', 'IECA')
	PIX_CITY = os.getenv('PIX_CITY', 'ANGRA')
