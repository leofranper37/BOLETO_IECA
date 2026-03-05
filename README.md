# Gerador de Boleto IECA

Aplicação Flask para gerar boletos em PDF com parcelamento e download imediato.

## Rodar localmente

1. Ative o ambiente virtual.
2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Execute:

```bash
python app.py
```

4. Acesse: `http://localhost:5001`

## Variáveis de ambiente

- `SECRET_KEY`: chave de segurança do Flask.
- `PIX_CODE`: código PIX completo (copia e cola) já pronto.
- `PIX_KEY`: chave PIX (email/celular/CPF/CNPJ). Se preencher esta chave, o sistema gera o PIX automaticamente.
- `PIX_RECEIVER_NAME`: nome do recebedor no PIX (ex: `IECA`).
- `PIX_CITY`: cidade do recebedor no PIX (ex: `ANGRA`).
- `VALOR_TOTAL`: valor total (ex: `400`).
- `MAX_PARCELAS`: limite de parcelas (ex: `10`).
- `PORT`: porta usada em produção (plataforma define automaticamente).

## Publicar e gerar link público (Render)

### 1) Subir para o GitHub

No terminal, dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "Projeto pronto para deploy"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

### 2) Publicar no Render

1. Suba o projeto para um repositório GitHub.
2. Entre em [https://render.com](https://render.com) e clique em **New +** > **Web Service**.
3. Conecte o repositório.
4. Configure:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
5. Em **Environment Variables**, adicione:
   - `SECRET_KEY`
   - `PIX_KEY` (recomendado)
   - `PIX_RECEIVER_NAME`
   - `PIX_CITY`
   - `VALOR_TOTAL`
   - `MAX_PARCELAS`
6. Clique em **Create Web Service**.

Ao finalizar o deploy, o Render gera uma URL pública (ex.: `https://seu-app.onrender.com`) para você compartilhar com as pessoas.

### Compartilhar link com outras pessoas

Depois do deploy no Render ficar como **Live**, copie a URL do serviço e envie para as pessoas.
Exemplo: `https://seu-app.onrender.com`
