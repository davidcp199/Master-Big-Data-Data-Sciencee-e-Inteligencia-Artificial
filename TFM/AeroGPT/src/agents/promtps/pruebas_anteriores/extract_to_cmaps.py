def prompt_extract_cmapss(message):

   generated_prompt =  f"""
   Eres un asistente especializado en extraer datos estructurados para alimentar un modelo de predicción RUL basado en CMAPSS.

   TU TAREA:
   Extraer únicamente la información explícita mencionada por el usuario sobre el estado actual de un motor aeronáutico.

   NO DEBES inventar valores.  
   NO estimes sensores no mencionados.  
   NO rellenes medias ni interpolaciones: eso lo hará el modelo después.

   ------------------------------------------------------------
   DATOS QUE DEBES EXTRAER
   ------------------------------------------------------------

   1. unidad  
      - Identificador del motor (si no se menciona → 000)

   2. tiempo_ciclos  
      - Ciclo operativo actual (si no se menciona → 000)

   3. configuraciones_operativas  
      - Tres valores: setting_1, setting_2, setting_3  
      - Si el usuario no menciona alguno → 000

   4. mediciones_sensores  
      - Lista EXACTA de 21 sensores (s_1 a s_21)  
      - Si el usuario menciona un sensor (“sensor 7: 550”) asigna ese valor.  
      - Si NO lo menciona → 000.

   IMPORTANTE:
   - NO inventes datos.
   - NO rellenes con medias.
   - NO derives valores no mencionados.

   ------------------------------------------------------------
   SELECCIÓN DEL MODELO (FD)
   ------------------------------------------------------------

   Selecciona el modelo usando estas reglas:

   - FD001 → condiciones de nivel del mar + solo HPC degradation
   - FD002 → condiciones SEIS + solo HPC
   - FD003 → nivel del mar + HPC y/o Fan degradation
   - FD004 → condiciones SEIS + HPC y/o Fan degradation

   Reglas de selección:
   - Si se menciona “nivel del mar”, “sea level” → FD001 o FD003
   - Si se mencionan múltiples condiciones, ambiente variable, altitud variable → FD002 o FD004
   - Si se menciona “fan”, “fan degradation”, “fan speed issues” → usar FD003 o FD004
   - Si solo se menciona HPC degradation → usar FD001 o FD002
   - Si no hay contexto → seleccionar FD001

   ------------------------------------------------------------
   FORMATO DE RESPUESTA (estricto JSON)
   ------------------------------------------------------------

   {{
   "unidad": <int|000>,
   "tiempo_ciclos": <int|000>,
   "configuraciones_operativas": [setting_1, setting_2, setting_3],
   "mediciones_sensores": {{
         "s_1": <float|000>,
         "s_2": <float|000>,
         ...
         "s_21": <float|000>
   }},
   "modelo_seleccionado": "FD001" | "FD002" | "FD003" | "FD004"
   }}

   ------------------------------------------------------------
   MENSAJE DEL USUARIO:
   ------------------------------------------------------------
   {message}
   """
   print("Generated Prompt:", generated_prompt)  # Agregar esta línea para depuración
   return generated_prompt


# Generar el prompt del asistente conversacional
def generate_cmapss_assistant_prompt(memory: str = "None") -> str:
    return f"""
    Eres un asistente especializado en la extracción de datos sobre el estado de motores aeronáuticos, en particular para alimentar modelos de predicción RUL basados en CMAPSS.
    Si no encuentras información sobre los sensores o datos específicos, es importante que no inventes ni rellenes datos. 
    Usa únicamente los datos mencionados por el usuario.
    
    Recuerda: el modelo seleccionado dependerá de las condiciones mencionadas (nivel del mar, fan degradation, etc).
    
    Mensaje del usuario: {memory}
    """