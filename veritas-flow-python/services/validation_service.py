import re

def validar_placa(placa):
    """
    Verifica se a placa está no formato antigo (AAA9999) ou Mercosul (AAA9A99).
    """
    placa = str(placa).strip().upper()
    
    # Padrão Mercosul (ex: ABC1D23) ou Antigo (ex: ABC1234)
    padrao = re.compile(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$')
    
    if padrao.match(placa):
        return True, placa
    return False, "Placa inválida. Utilize o formato ABC1234 ou ABC1D23."

def formata_valor(valor_str):
    """
    Converte string para float.
    """
    try:
        if isinstance(valor_str, str):
            valor = valor_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(valor)
        return float(valor_str)
    except ValueError:
        return 0.0
