import re
import unicodedata


def _normalize_text(value: str) -> str:
    raw = (value or '').strip().upper()
    normalized = unicodedata.normalize('NFD', raw)
    without_accents = ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')
    return re.sub(r'[^A-Z0-9 .\-]', '', without_accents)


def _field(field_id: str, content: str) -> str:
    return f'{field_id}{len(content):02d}{content}'


def _crc16_ccitt(payload: str) -> str:
    polynomial = 0x1021
    crc = 0xFFFF
    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
    return f'{crc:04X}'


def gerar_pix_copia_e_cola(
    chave_pix: str,
    nome_recebedor: str,
    cidade: str,
    valor: float,
    txid: str = '***',
    descricao: str = ''
) -> str:
    chave = (chave_pix or '').strip()
    if not chave:
        raise ValueError('Chave PIX não informada.')

    nome_limpo = _normalize_text(nome_recebedor)[:25] or 'RECEBEDOR'
    cidade_limpa = _normalize_text(cidade)[:15] or 'CIDADE'
    txid_limpo = _normalize_text(txid)[:25] or '***'
    descricao_limpa = (descricao or '').strip()[:99]
    valor_formatado = f'{float(valor):.2f}'

    gui = _field('00', 'BR.GOV.BCB.PIX')
    chave_field = _field('01', chave)
    merchant_account = gui + chave_field
    if descricao_limpa:
        merchant_account += _field('02', descricao_limpa)

    payload_sem_crc = (
        _field('00', '01')
        + _field('26', merchant_account)
        + _field('52', '0000')
        + _field('53', '986')
        + _field('54', valor_formatado)
        + _field('58', 'BR')
        + _field('59', nome_limpo)
        + _field('60', cidade_limpa)
        + _field('62', _field('05', txid_limpo))
        + '6304'
    )
    crc = _crc16_ccitt(payload_sem_crc)
    return payload_sem_crc + crc