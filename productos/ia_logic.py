def predecir_reabastecimiento(stock, precio):
    # Simulamos una IA: Si el stock es bajo y el precio es asequible, 
    # la IA recomienda comprar mucho.
    if stock < 20 and precio < 100:
        return "RECOMENDADO: Comprar lote grande (Alta demanda prevista)"
    elif stock < 10:
        return "URGENTE: Reponer unidades mínimas"
    else:
        return "ESTABLE: No se requiere acción"