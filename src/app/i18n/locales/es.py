"""
Spanish (es) translations for Magma Bitcoin app.
Traducciones al español para todos los mensajes de la API y la interfaz.
"""

TRANSLATIONS: dict = {

    # -----------------------------------------------------------------------
    # Auth
    # -----------------------------------------------------------------------
    "auth.challenge.issued":        "Desafío emitido correctamente.",
    "auth.challenge.expired":       "El desafío ha caducado. Por favor solicite uno nuevo.",
    "auth.challenge.not_found":     "No se encontró ningún desafío para esta clave pública.",
    "auth.challenge.mismatch":      "El desafío no coincide. Autenticación fallida.",
    "auth.challenge.required":      "Se requiere una cadena de desafío.",
    "auth.pubkey.required":         "Se requiere una clave pública (pubkey).",
    "auth.pubkey.invalid":          "Formato de clave pública inválido. Se esperan 64 caracteres hexadecimales.",
    "auth.success":                 "Autenticación exitosa.",
    "auth.failure":                 "Autenticación fallida. Verifique sus credenciales.",
    "auth.session.created":         "Sesión creada. Ha iniciado sesión correctamente.",
    "auth.session.invalid":         "El token de sesión es inválido o ha caducado.",
    "auth.session.expired":         "Su sesión ha caducado. Por favor inicie sesión nuevamente.",
    "auth.session.revoked":         "Sesión revocada correctamente.",
    "auth.session.not_found":       "Sesión no encontrada.",
    "auth.rate_limited":            "Demasiados intentos de autenticación. Espere {wait_seconds} segundos.",
    "auth.nostr.event.required":    "Se requiere un evento Nostr firmado.",
    "auth.nostr.event.invalid":     "El evento Nostr firmado es inválido.",
    "auth.nostr.pubkey.mismatch":   "La clave pública del evento no coincide con la solicitada.",
    "auth.lnurl.challenge.invalid": "El desafío de autenticación LNURL es inválido.",
    "auth.lnurl.signature.invalid": "La verificación de firma LNURL falló.",
    "auth.permission.denied":       "No tiene permiso para realizar esta acción.",
    "auth.phone.invalid":           "Número de teléfono inválido. Use formato salvadoreño (+503 XXXX-XXXX).",
    "auth.phone.code.sent":         "Código enviado por SMS.",
    "auth.phone.code.invalid":      "Código incorrecto. Intente de nuevo.",
    "auth.phone.code.expired":      "El código ha expirado. Solicite uno nuevo.",

    # -----------------------------------------------------------------------
    # Savings
    # -----------------------------------------------------------------------
    "savings.goal.set":             "Meta de ahorro actualizada correctamente.",
    "savings.goal.not_found":       "No hay meta de ahorro configurada. Configure una para comenzar.",
    "savings.goal.required":        "Se requiere una meta de ahorro para esta acción.",
    "savings.deposit.recorded":     "Depósito de {amount} registrado correctamente.",
    "savings.deposit.invalid_amount": "El monto del depósito debe ser un número positivo.",
    "savings.deposit.not_found":    "Registro de depósito no encontrado.",
    "savings.projection.generated": "Proyección de ahorro generada.",
    "savings.projection.no_data":   "Datos insuficientes para generar una proyección. Realice al menos un depósito.",
    "savings.monthly_target":       "Meta mensual de ahorro",
    "savings.total_saved":          "Total ahorrado",
    "savings.total_btc":            "Total de BTC acumulado",
    "savings.target_years":         "Años objetivo",
    "savings.on_track":             "¡Está en camino de alcanzar su meta!",
    "savings.behind_target":        "Actualmente está por debajo de su meta mensual.",
    "savings.ahead_target":         "Va adelantado respecto a su meta mensual de ahorro.",
    "savings.no_deposits":          "Aún no hay depósitos registrados. ¡Empiece a ahorrar hoy!",

    # -----------------------------------------------------------------------
    # Remittance
    # -----------------------------------------------------------------------
    "remittance.calculation.success": "Cálculo de remesa completado.",
    "remittance.amount.invalid":    "Ingrese un monto de remesa válido.",
    "remittance.currency.invalid":  "Código de moneda inválido. Use un código ISO de 3 letras.",
    "remittance.rate.unavailable":  "El tipo de cambio no está disponible temporalmente. Intente de nuevo en breve.",
    "remittance.fee.breakdown":     "Desglose de comisiones",
    "remittance.recipient.receives": "El destinatario recibe",
    "remittance.sender.pays":       "El remitente paga",
    "remittance.via_bitcoin":       "Vía Bitcoin (instantáneo)",
    "remittance.via_traditional":   "Vía transferencia tradicional (3-5 días hábiles)",
    "remittance.savings_vs_traditional": "Ahorro vs. remesa tradicional",
    "remittance.no_data":           "Los datos de remesa no están disponibles en este momento.",

    # -----------------------------------------------------------------------
    # Pension
    # -----------------------------------------------------------------------
    "pension.projection.generated": "Proyección de pensión generada.",
    "pension.projection.no_data":   "Configure su meta de ahorro para generar una proyección de pensión.",
    "pension.age.required":         "La edad actual es necesaria para el cálculo de pensión.",
    "pension.age.invalid":          "La edad debe estar entre 18 y 80 años.",
    "pension.retirement_age":       "Edad de jubilación objetivo",
    "pension.years_to_retire":      "Años hasta la jubilación",
    "pension.projected_value":      "Valor proyectado del portafolio al jubilarse",
    "pension.monthly_income":       "Ingreso mensual estimado",
    "pension.inflation_adjusted":   "Valor ajustado por inflación",
    "pension.on_track":             "Va en camino hacia una jubilación cómoda.",
    "pension.underfunded":          "Su tasa de ahorro actual puede no alcanzar su meta de jubilación.",
    "pension.increase_savings":     "Considere aumentar su ahorro mensual para alcanzar su meta.",

    # -----------------------------------------------------------------------
    # Market
    # -----------------------------------------------------------------------
    "market.price.unavailable":     "Los datos de precio de Bitcoin no están disponibles temporalmente.",
    "market.price.fetched":         "Precio de mercado obtenido correctamente.",
    "market.fees.unavailable":      "Los datos de comisiones on-chain no están disponibles temporalmente.",
    "market.fees.fetched":          "Estimados de comisiones obtenidos correctamente.",
    "market.history.unavailable":   "El historial de precios no está disponible temporalmente.",
    "market.history.fetched":       "Historial de precios obtenido correctamente.",
    "market.loading":               "Cargando datos de mercado…",
    "market.last_updated":          "Última actualización",

    # -----------------------------------------------------------------------
    # Alerts
    # -----------------------------------------------------------------------
    "alerts.preferences.updated":  "Preferencias de alerta actualizadas.",
    "alerts.preferences.not_found": "No se encontraron preferencias de alerta. Se usarán los valores predeterminados.",
    "alerts.fee.triggered":         "Alerta de comisión Bitcoin: {direction} {level} sat/vB",
    "alerts.price.triggered":       "Alerta de precio Bitcoin: {direction} {price}",
    "alerts.fee.high":              "Las comisiones están ALTAS — actualmente {fee} sat/vB.",
    "alerts.fee.low":               "Las comisiones están BAJAS — actualmente {fee} sat/vB. ¡Buen momento para transaccionar!",
    "alerts.price.above":           "El precio de BTC superó {threshold}.",
    "alerts.price.below":           "El precio de BTC cayó por debajo de {threshold}.",
    "alerts.enabled":               "Las alertas están activadas.",
    "alerts.disabled":              "Las alertas están desactivadas.",

    # -----------------------------------------------------------------------
    # Achievements
    # -----------------------------------------------------------------------
    "achievements.earned":          "¡Logro desbloqueado: {name}!",
    "achievements.none":            "Aún no hay logros. ¡Empiece a ahorrar para ganar su primera medalla!",
    "achievements.all_fetched":     "Logros cargados.",

    # Achievement names
    "achievement.first_deposit.name":       "Primeros Pasos",
    "achievement.first_deposit.desc":       "Realizó su primer depósito de ahorro en Bitcoin.",
    "achievement.hodl_week.name":           "HODLer Semanal",
    "achievement.hodl_week.desc":           "Ahorró de manera consistente durante toda una semana.",
    "achievement.hodl_month.name":          "Apilador Mensual",
    "achievement.hodl_month.desc":          "Mantuvo su hábito de ahorro durante 30 días.",
    "achievement.goal_setter.name":         "Establecedor de Metas",
    "achievement.goal_setter.desc":         "Estableció su primera meta de ahorro.",
    "achievement.diamond_hands.name":       "Manos de Diamante",
    "achievement.diamond_hands.desc":       "Mantuvo su Bitcoin durante una caída del mercado del 10%.",
    "achievement.satoshi_100k.name":        "100K Satoshis",
    "achievement.satoshi_100k.desc":        "Acumuló 100.000 satoshis.",
    "achievement.satoshi_1m.name":          "1M Satoshis",
    "achievement.satoshi_1m.desc":          "Acumuló 1.000.000 de satoshis.",
    "achievement.satoshi_10m.name":         "10M Satoshis",
    "achievement.satoshi_10m.desc":         "Acumuló 10.000.000 de satoshis.",
    "achievement.on_track.name":            "En Camino",
    "achievement.on_track.desc":            "Se mantuvo en línea con su plan de ahorro durante un mes completo.",
    "achievement.nostr_auth.name":          "Nativo Nostr",
    "achievement.nostr_auth.desc":          "Se autenticó usando Nostr (NIP-07).",
    "achievement.streak_7.name":            "Racha de 7 Días",
    "achievement.streak_7.desc":            "Depositó todos los días durante 7 días consecutivos.",
    "achievement.streak_30.name":           "Racha de 30 Días",
    "achievement.streak_30.desc":           "Depositó todos los días durante 30 días consecutivos.",
    "achievement.early_adopter.name":       "Adoptante Temprano",
    "achievement.early_adopter.desc":       "Uno de los primeros 100 usuarios en Magma.",
    "achievement.big_saver.name":           "Gran Ahorrador",
    "achievement.big_saver.desc":           "Ahorró más de $500 en un solo mes.",
    "achievement.lightning_fast.name":      "Rayo Veloz",
    "achievement.lightning_fast.desc":      "Completó un pago en la Red Lightning.",

    # -----------------------------------------------------------------------
    # Notifications
    # -----------------------------------------------------------------------
    "notification.welcome.title":       "¡Bienvenido a Magma!",
    "notification.welcome.body":        "Comience su viaje de ahorro en Bitcoin hoy. Establezca una meta y haga su primer depósito.",
    "notification.deposit.title":       "Depósito Confirmado",
    "notification.deposit.body":        "Su depósito de {amount} ha sido registrado. Ha ahorrado {total} hasta ahora.",
    "notification.achievement.title":   "¡Logro Desbloqueado!",
    "notification.achievement.body":    'Ganó la medalla "{name}". ¡Siga apilando!',
    "notification.goal_reached.title":  "¡Meta de Ahorro Alcanzada!",
    "notification.goal_reached.body":   "¡Felicitaciones! Ha alcanzado su meta de ahorro de {goal}.",
    "notification.price_alert.title":   "Alerta de Precio Bitcoin",
    "notification.price_alert.body":    "BTC ahora está {direction} {threshold}. Precio actual: {price}.",
    "notification.fee_alert.title":     "Alerta de Comisiones",
    "notification.fee_alert.body":      "Las comisiones on-chain ahora están {level}: {fee} sat/vB.",
    "notification.streak.title":        "¡Racha de Ahorro!",
    "notification.streak.body":         "Lleva una racha de {days} días de ahorro. ¡No la rompa!",
    "notification.monthly_summary.title": "Resumen Mensual",
    "notification.monthly_summary.body":  "Este mes ahorró {amount}. Su total ahora es {total}.",

    # -----------------------------------------------------------------------
    # Export
    # -----------------------------------------------------------------------
    "export.generated":             "Exportación generada correctamente.",
    "export.format.pdf":            "Exportar PDF",
    "export.format.csv":            "Exportar CSV",
    "export.format.json":           "Exportar JSON",
    "export.no_data":               "No hay datos disponibles para exportar.",
    "export.savings_report":        "Reporte de Ahorros",
    "export.remittance_report":     "Reporte de Remesas",
    "export.pension_report":        "Reporte de Proyección de Pensión",
    "export.generated_by":          "Generado por Magma",
    "export.generated_on":          "Generado el",
    "export.confidential":          "Confidencial — solo para uso personal.",

    # -----------------------------------------------------------------------
    # Compliance / Admin
    # -----------------------------------------------------------------------
    "compliance.aml.low":           "Transacción de bajo riesgo.",
    "compliance.aml.medium":        "Riesgo medio — se requiere monitoreo.",
    "compliance.aml.high":          "Riesgo alto — se requiere revisión manual.",
    "compliance.aml.critical":      "Riesgo crítico — transacción bloqueada pendiente de revisión.",
    "compliance.ctr.required":      "Se requiere Reporte de Transacción de Divisas para ${amount}.",
    "compliance.sar.drafted":       "Reporte de Actividad Sospechosa redactado.",
    "compliance.alert.pending":     "Alerta de cumplimiento pendiente de revisión.",
    "compliance.alert.resolved":    "Alerta de cumplimiento resuelta.",
    "compliance.sanctioned_address": "Esta dirección está en una lista de sanciones. Transacción bloqueada.",
    "compliance.jurisdiction.sv":   "El Salvador (UAF)",
    "compliance.jurisdiction.us":   "Estados Unidos (FinCEN)",
    "compliance.jurisdiction.eu":   "Unión Europea (ABE)",

    "admin.access.denied":          "Acceso de administrador denegado.",
    "admin.access.not_configured":  "El acceso de administrador no está configurado en este servidor.",
    "admin.action.completed":       "Acción de administrador completada correctamente.",
    "admin.user.banned":            "El usuario {pubkey} ha sido bloqueado.",
    "admin.user.unbanned":          "El bloqueo del usuario {pubkey} ha sido levantado.",
    "admin.maintenance.completed":  "Mantenimiento completado en {elapsed_ms}ms.",
    "admin.config.updated":         "Clave de configuración '{key}' actualizada.",
    "admin.config.blocked":         "La clave de configuración '{key}' no puede modificarse en tiempo de ejecución.",

    # -----------------------------------------------------------------------
    # Errors
    # -----------------------------------------------------------------------
    "error.not_found":              "El recurso solicitado no fue encontrado.",
    "error.bad_request":            "La solicitud está malformada o le faltan campos requeridos.",
    "error.unauthorized":           "Se requiere autenticación.",
    "error.forbidden":              "No tiene permiso para acceder a este recurso.",
    "error.rate_limited":           "Demasiadas solicitudes. Por favor reduzca la frecuencia.",
    "error.internal":               "Ocurrió un error interno del servidor. Por favor intente de nuevo.",
    "error.database":               "Ocurrió un error en la base de datos. Contacte al soporte.",
    "error.validation.string":      "El campo '{field}' debe ser una cadena de texto.",
    "error.validation.number":      "El campo '{field}' debe ser un número.",
    "error.validation.range":       "El campo '{field}' debe estar entre {min} y {max}.",
    "error.validation.required":    "El campo '{field}' es obligatorio.",
    "error.validation.invalid":     "El campo '{field}' tiene un valor inválido.",
    "error.injection.detected":     "Se detectó entrada potencialmente maliciosa en el campo '{field}'.",
    "error.sanitization.failed":    "No se pudo sanitizar la entrada para el campo '{field}'.",
    "error.method.not_allowed":     "El método HTTP no está permitido para este endpoint.",
    "error.payload.too_large":      "El payload de la solicitud supera el tamaño máximo permitido.",
    "error.timeout":                "La solicitud agotó el tiempo de espera. Intente de nuevo.",
    "error.service.unavailable":    "Este servicio no está disponible temporalmente.",
    "error.bitcoin.address":        "Dirección Bitcoin inválida.",
    "error.lightning.invoice":      "Factura de Lightning Network inválida.",
    "error.nostr.pubkey":           "Clave pública Nostr inválida.",
    "error.amount.negative":        "El monto no puede ser negativo.",
    "error.amount.zero":            "El monto no puede ser cero.",
    "error.amount.too_large":       "El monto supera el valor máximo permitido.",
    "error.date.invalid":           "Formato de fecha inválido. Se espera AAAA-MM-DD.",
    "error.currency.invalid":       "Código de moneda inválido.",
    "error.json.invalid":           "Payload JSON inválido.",

    # -----------------------------------------------------------------------
    # Portfolio
    # -----------------------------------------------------------------------
    "portfolio.summary":            "Resumen de Portafolio",
    "portfolio.current_value":      "Valor actual del portafolio",
    "portfolio.total_invested":     "Total invertido",
    "portfolio.unrealized_gain":    "Ganancia/pérdida no realizada",
    "portfolio.return_pct":         "Retorno total",
    "portfolio.btc_price_avg":      "Precio promedio de compra",
    "portfolio.holdings":           "Tenencias",
    "portfolio.no_data":            "No hay datos de portafolio disponibles. Realice su primer depósito para comenzar.",

    # -----------------------------------------------------------------------
    # General UI
    # -----------------------------------------------------------------------
    "general.loading":              "Cargando…",
    "general.saving":               "Guardando…",
    "general.success":              "¡Éxito!",
    "general.error":                "Ocurrió un error.",
    "general.cancel":               "Cancelar",
    "general.confirm":              "Confirmar",
    "general.save":                 "Guardar",
    "general.delete":               "Eliminar",
    "general.edit":                 "Editar",
    "general.view":                 "Ver",
    "general.back":                 "Atrás",
    "general.next":                 "Siguiente",
    "general.previous":             "Anterior",
    "general.close":                "Cerrar",
    "general.search":               "Buscar",
    "general.filter":               "Filtrar",
    "general.sort":                 "Ordenar",
    "general.export":               "Exportar",
    "general.import":               "Importar",
    "general.refresh":              "Actualizar",
    "general.yes":                  "Sí",
    "general.no":                   "No",
    "general.none":                 "Ninguno",
    "general.all":                  "Todo",
    "general.today":                "Hoy",
    "general.yesterday":            "Ayer",
    "general.this_week":            "Esta semana",
    "general.this_month":           "Este mes",
    "general.days_ago":             "hace {n} días",
    "general.hours_ago":            "hace {n} horas",
    "general.minutes_ago":          "hace {n} minutos",
    "general.just_now":             "Justo ahora",
    "general.unknown":              "Desconocido",
    "general.n_a":                  "N/D",

    # -----------------------------------------------------------------------
    # Scoring
    # -----------------------------------------------------------------------
    "scoring.address.required":     "Se requiere una dirección",
    "scoring.address.invalid":      "Formato de dirección Bitcoin inválido: {address}",
    "scoring.analysis.failed":      "Error en el análisis: {error}",
    "scoring.address_query.required": "Se requiere el parámetro de consulta address",

    # -----------------------------------------------------------------------
    # Preferences
    # -----------------------------------------------------------------------
    "preferences.auth.required":    "Se requiere autenticación",
    "preferences.load.failed":      "No se pudieron cargar las preferencias: {error}",
    "preferences.body.empty":       "El cuerpo de la solicitud no puede estar vacío",
    "preferences.fields.invalid":   "No se proporcionaron campos válidos. Aceptados: fee_alert_low, fee_alert_high, alerts_enabled",
    "preferences.update.failed":    "No se pudieron actualizar las preferencias: {error}",
    "preferences.price_usd.required": "Se requiere price_usd",
    "preferences.price_usd.invalid": "price_usd debe ser un número",
    "preferences.direction.required": "Se requiere direction",
    "preferences.alert.created":    "Alerta de precio creada",
    "preferences.alert.add_failed": "No se pudo agregar la alerta: {error}",
    "preferences.alert_id.required": "Se requiere alert_id",
    "preferences.alert.removed":    "Alerta de precio eliminada",
    "preferences.alert.remove_failed": "No se pudo eliminar la alerta: {error}",

    # -----------------------------------------------------------------------
    # Lightning
    # -----------------------------------------------------------------------
    "lightning.overview.failed":    "No se pudo obtener resumen de Lightning: {error}",
    "lightning.compare.failed":     "No se pudo generar la comparación: {error}",
    "lightning.amount.required":    "Se requiere amount_usd (cuerpo o parámetro de consulta)",
    "lightning.amount.invalid":     "amount_usd debe ser un número",
    "lightning.amount.positive":    "amount_usd debe ser positivo",
    "lightning.urgency.invalid":    "urgency debe ser uno de: low, medium, high, instant",
    "lightning.recommend.failed":   "Error en la recomendación: {error}",

    # -----------------------------------------------------------------------
    # Webhooks
    # -----------------------------------------------------------------------
    "webhooks.auth.required":       "Se requiere autenticación",
    "webhooks.url.required":        "Se requiere url",
    "webhooks.events.required":     "events debe ser una lista no vacía",
    "webhooks.events.unsupported":  "Tipo(s) de evento no soportado(s): {events}",
    "webhooks.subscribe.failed":    "Error al crear suscripción: {error}",
    "webhooks.subscribe.success":   "Suscripción creada. Guarde el secreto — no se mostrará de nuevo.",
    "webhooks.sub_id.required":     "Se requiere subscription_id",
    "webhooks.unsubscribe.failed":  "Error al eliminar suscripción: {error}",
    "webhooks.unsubscribe.not_found": "Suscripción no encontrada",
    "webhooks.unsubscribe.success": "Suscripción eliminada",
    "webhooks.list.failed":         "Error al listar suscripciones: {error}",
    "webhooks.update.fields":       "No hay campos válidos para actualizar (url, events, active)",
    "webhooks.update.not_found":    "Suscripción no encontrada",
    "webhooks.update.failed":       "Error en la actualización: {error}",
    "webhooks.test.success":        "Webhook de prueba enviado exitosamente.",
    "webhooks.test.failed":         "Error en el envío del webhook de prueba.",
    "webhooks.test.hint":           "Verifique que la URL sea accesible y retorne un estado 2xx.",

    # -----------------------------------------------------------------------
    # Market
    # -----------------------------------------------------------------------
    "market.days.range":            "days debe estar entre 1 y 365",
    "market.interval.invalid":      "interval debe ser 'daily' o 'hourly'",
    "market.prices.minimum":        "Se necesitan al menos 20 puntos de precio",
    "market.signal_type.required":  "Se requiere signal_type para el modo backtest",
    "market.mode.invalid":          "mode debe ser 'summary', 'score' o 'backtest'",
    "market.no_price_data":         "No hay datos de precio disponibles",

    # -----------------------------------------------------------------------
    # Portfolio
    # -----------------------------------------------------------------------
    "portfolio.amount.positive":    "amount debe ser positivo",
    "portfolio.price.positive":     "price_usd debe ser positivo",
    "portfolio.tx_type.invalid":    "tx_type inválido",
    "portfolio.period.invalid":     "period debe ser 'day', 'week', 'month', 'year' o 'all'",
    "portfolio.assets.required":    "Se requiere la lista de assets",
    "portfolio.assets.mismatch":    "assets y expected_returns deben tener la misma longitud",
    "portfolio.method.invalid":     "method debe ser 'basic', 'min_variance', 'max_sharpe' o 'risk_parity'",
    "portfolio.no_holdings":        "No se encontraron tenencias",
    "portfolio.risk_note":          "Los resultados del stress test muestran el impacto estimado del portafolio bajo cada escenario de mercado predefinido.",
    "portfolio.cost_method.invalid": "method debe ser 'fifo', 'lifo' o 'average'",
    "portfolio.target.required":    "Se requiere target_allocation",

    # -----------------------------------------------------------------------
    # Simulation
    # -----------------------------------------------------------------------
    "simulation.initial.nonneg":    "initial debe ser no negativo",
    "simulation.monthly.nonneg":    "monthly_contribution debe ser no negativo",
    "simulation.years.range":       "years debe estar entre 1 y 50",
    "simulation.amount.positive":   "amount debe ser positivo",
    "simulation.frequency.invalid": "frequency debe ser 'daily', 'weekly' o 'monthly'",
    "simulation.years.range_30":    "years debe estar entre 1 y 30",
    "simulation.prices.required":   "Se requiere la lista de prices",
    "simulation.prices.minimum":    "Se necesitan al menos 20 puntos de precio",
    "simulation.strategy.unknown":  "Estrategia desconocida: {name}",
    "simulation.scenario.required": "Se requiere scenario o custom_scenario para modo single",
    "simulation.mode.invalid":      "mode debe ser 'single', 'stress_test' o 'list'",
    "simulation.price.positive":    "current_price debe ser positivo",
    "simulation.volatility.range":  "volatility debe estar entre 0 y 5",
    "simulation.days.range":        "days debe estar entre 1 y 3650",
    "simulation.age.invalid":       "current_age debe ser menor que retirement_age",
    "simulation.retire.invalid":    "retirement_age debe ser menor que life_expectancy",
    "simulation.portfolio.positive": "portfolio_value debe ser positivo",
    "simulation.withdrawals.positive": "monthly_withdrawals debe ser positivo",

    # -----------------------------------------------------------------------
    # Stats
    # -----------------------------------------------------------------------
    "stats.data.required":          "Campo requerido faltante: data",
    "stats.data.list":              "El campo 'data' debe ser una lista de números.",
    "stats.data.empty":             "El campo 'data' no puede estar vacío.",
    "stats.data.too_large":         "data supera el máximo de {max} puntos.",
    "stats.data.non_numeric":       "data contiene valores no numéricos: {error}",
    "stats.include.list":           "El campo 'include' debe ser una lista de cadenas.",
    "stats.x.required":             "Campo requerido faltante: x",
    "stats.y.required":             "Campo requerido faltante: y",
    "stats.xy.list":                "Los campos 'x' e 'y' deben ser listas.",
    "stats.xy.length":              "x (len={x_len}) e y (len={y_len}) deben tener la misma longitud.",
    "stats.xy.minimum_2":           "Se requieren al menos 2 puntos de datos para correlación.",
    "stats.xy.minimum_3":           "Se requieren al menos 3 puntos de datos para regresión.",
    "stats.xy.too_large":           "Los datos superan {max} puntos.",
    "stats.xy.non_numeric":         "Valores no numéricos: {error}",
    "stats.methods.list":           "El campo 'methods' debe ser una lista.",
    "stats.regression.type_invalid": "Tipo inválido. Use 'linear', 'log_linear' o 'power_law'.",
    "stats.regression.failed":      "Error en la regresión: {error}",

    # -----------------------------------------------------------------------
    # Liquid
    # -----------------------------------------------------------------------
    "liquid.overview.failed":       "No se pudo obtener resumen de Liquid: {error}",
    "liquid.assets.failed":         "No se pudieron obtener los activos Liquid: {error}",
    "liquid.compare.failed":        "No se pudo generar la comparación: {error}",
    "liquid.peg.failed":            "No se pudo obtener información de peg: {error}",
    "liquid.amount.required":       "Se requiere amount_usd",
    "liquid.amount.invalid":        "amount_usd debe ser un número",
    "liquid.amount.positive":       "amount_usd debe ser positivo",
    "liquid.urgency.invalid":       "urgency debe ser uno de: low, medium, high, instant",
    "liquid.privacy.invalid":       "privacy debe ser uno de: normal, high, confidential",
    "liquid.recommend.failed":      "Error en la recomendación: {error}",

    # -----------------------------------------------------------------------
    # Recipients
    # -----------------------------------------------------------------------
    "recipients.auth.required":     "Se requiere autenticación",
    "recipients.body.invalid":      "Cuerpo inválido",
    "recipients.created":           "Destinatario creado",
    "recipients.create.failed":     "Error al crear destinatario: {error}",
    "recipients.list.failed":       "No se pudieron listar destinatarios: {error}",
    "recipients.get.failed":        "Error al consultar destinatario: {error}",
    "recipients.body.empty":        "Cuerpo vacío",
    "recipients.updated":           "Destinatario actualizado",
    "recipients.update.failed":     "Error al actualizar: {error}",
    "recipients.not_found":         "Destinatario no encontrado",
    "recipients.deleted":           "Destinatario eliminado",
    "recipients.delete.failed":     "Error al eliminar: {error}",

    # -----------------------------------------------------------------------
    # Reminders
    # -----------------------------------------------------------------------
    "reminders.auth.required":      "Se requiere autenticación",
    "reminders.body.invalid":       "Cuerpo inválido",
    "reminders.recipient_id.required": "recipient_id requerido (entero)",
    "reminders.created":            "Recordatorio creado",
    "reminders.create.failed":      "Error al crear recordatorio: {error}",
    "reminders.list.failed":        "Error al listar recordatorios: {error}",
    "reminders.body.empty":         "Cuerpo vacío",
    "reminders.updated":            "Recordatorio actualizado",
    "reminders.not_found":          "Recordatorio no encontrado",
    "reminders.deleted":            "Recordatorio eliminado",

    # -----------------------------------------------------------------------
    # Sends
    # -----------------------------------------------------------------------
    "sends.auth.required":          "Se requiere autenticación",
    "sends.body.invalid":           "Cuerpo inválido",
    "sends.recipient_id.required":  "recipient_id requerido (entero)",
    "sends.amount.required":        "amount_usd requerido (numérico)",
    "sends.invoice.failed":         "Error al generar invoice: {error}",

    # -----------------------------------------------------------------------
    # Splits (non-custodial remittance router)
    # -----------------------------------------------------------------------
    "splits.label.required":        "label requerido",
    "splits.profile.not_found":     "Perfil de split no encontrado",
    "splits.rules.required":        "Se requiere una lista de reglas (rules)",
    "splits.profile_id.required":   "profile_id requerido (entero)",
    "splits.amount.required":       "amount_usd requerido (numérico)",
    "splits.build.failed":          "Error al construir split: {error}",

    # -----------------------------------------------------------------------
    # Admin (extra)
    # -----------------------------------------------------------------------
    "admin.target.required":        "Se requiere target_pubkey",
    "admin.user.not_found":         "Usuario no encontrado",
    "admin.token.required":         "Se requiere token para action=revoke",
    "admin.action.unknown":         "Acción desconocida: {action}",
    "admin.key.required":           "Se requiere key para action=set",
    "admin.delete.confirm":         "Establezca confirm='DELETE' para confirmar la eliminación irreversible",

    # -----------------------------------------------------------------------
    # Export (extra)
    # -----------------------------------------------------------------------
    "export.pubkey.invalid":        "Clave pública inválida",
    "export.dates.integer":         "date_from y date_to deben ser enteros",
    "export.year_month.integer":    "year y month deben ser enteros",
    "export.month.range":           "month debe estar entre 1 y 12",
    "export.year.range":            "year fuera de rango válido",
    "export.amount.number":         "amount_usd debe ser un número",
    "export.amount.positive":       "amount_usd debe ser positivo",
    "export.numeric.invalid":       "Parámetro numérico inválido",
    "export.monthly.positive":      "monthly_usd debe ser positivo",
    "export.years.range":           "years debe estar entre 1 y 50",
    "export.report_type.unknown":   "report_type desconocido '{type}'. Valores válidos: savings, statement, remittance, pension",

    # -----------------------------------------------------------------------
    # Locale validation
    # -----------------------------------------------------------------------
    "locale.invalid":               "Idioma inválido. Use 'en' o 'es'.",
}
