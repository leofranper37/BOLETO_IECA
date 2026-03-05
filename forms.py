from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class BoletoForm(FlaskForm):
	nome = StringField('Nome', validators=[DataRequired()])
	num_pessoas = IntegerField('Número de Pessoas', default=1)
	parcelas = IntegerField('Parcelas', default=1)
	concorda = BooleanField('Concordo com as regras', validators=[DataRequired()])
