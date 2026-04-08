def predecir_reabastecimiento(stock, precio):
    """
    Simulación de IA avanzada mediante lógica difusa y puntuación de prioridad.
    Calcula la urgencia basada en el valor del inventario y el riesgo de rotura de stock.
    """
    # 1. Calculamos un factor de riesgo (a menos stock, más riesgo)
    # Si el stock es 0, el riesgo es máximo.
    factor_riesgo = max(0, (20 - stock) / 20) 
    
    # 2. Factor de importancia económica (productos caros duelen más si no hay)
    # Normalizamos el precio: productos de más de 500€ se consideran "críticos"
    factor_importancia = min(1.0, precio / 500)
    
    # 3. Cálculo de la Puntuación de Prioridad (0.0 a 1.0)
    prioridad = (factor_riesgo * 0.7) + (factor_importancia * 0.3)

    # 4. Clasificación según la puntuación obtenida
    if prioridad > 0.8:
        return f"CRÍTICO ({int(prioridad*100)}%): Pedido inmediato. Riesgo alto de pérdida de ingresos."
    elif prioridad > 0.5:
        return f"RECOMENDADO ({int(prioridad*100)}%): Planificar reabastecimiento en la próxima ventana."
    elif prioridad > 0.2:
        return "ESTABLE: Monitorizar semanalmente."
    else:
        return "OPTIMO: Stock saludable."