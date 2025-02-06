import pandas as pd
from flask import Flask, request, render_template, jsonify, send_file

app = Flask(__name__)
df = None

def load_file(file):
    global df
    try:
        df = pd.read_csv(file, sep=';')
        return {"success": True, "message": "Archivo cargado correctamente"}
    except Exception as e:
        return {"success": False, "message": f"No se pudo cargar el archivo: {e}"}

def map_multiple_values(value, mapping):
    if pd.isna(value):
        return value
    values = str(value).split(',')
    mapped_values = []
    for v in values:
        try:
            int_v = int(float(v)) 
            mapped_values.append(mapping.get(int_v, v))
        except ValueError:
            mapped_values.append(v)  
    return ', '.join(mapped_values)


municipios = []

def convert_data():
    global df, municipios
    global df
    if df is not None:
        try:
            sex_mapping = {1: 'Hombre', 2: 'Mujer', 3: 'Indeterminado'}
            df['sexo'] = df['sexo'].map(sex_mapping)
            estrato_mapping = {1: 'Bajo-bajo', 2: 'Bajo', 3: 'Medio-bajo', 4: 'Medio', 5: 'Medio-Alto', 6: 'Alto'}
            df['estratoVivienda'] = df['estratoVivienda'].map(estrato_mapping)
            tipovivienda_mapping = {1: 'Casa', 2: 'Casa Indigena', 3: 'Carpa', 4: 'Apartamento', 5: 'Habitacion', 6: 'Contenedor', 7: 'Embarcacion', 8: 'Bagon', 9: 'Refugio Natural', 10: 'Cueva', 11: 'Puente', 12: 'Otro' }
            df['codTipoVivienda'] = df['codTipoVivienda'].map(tipovivienda_mapping)
            materialPredominanteParedes_mapping = {1: 'bloque, ladrillo, piedra, madera pulida', 2: 'bahareque', 4: 'Material prefabricado', 5: 'Madera burda, tabla, tablon', 6: 'guadua, casa, esterilla, otrovegetal', 7: 'zinc, tela, lona, carton, latas, desechos, plastico', 8: 'otro', 9: 'sin parededs'}
            df['materialPredominanteParedes'] = df['materialPredominanteParedes'].map(materialPredominanteParedes_mapping)
            materialPredominantePiso_mapping = {1: 'Alfombra o tapete, marmol, parque, madera pulida y lacada', 2: 'baldosa,vinilo, tableta, ladrillo', 3: 'Cemento, gravilla', 4: 'Madera burda, madera en mal estado, tabla, tablon', 5: 'Tierra o arena', 6: 'otro' }
            df['materialPredominantePiso'] = df['materialPredominantePiso'].map(materialPredominantePiso_mapping)
            materialPredominanteTecho_mapping = {1: 'concreto', 2: 'tejas de barro', 3: 'fibrocemento', 4: 'zinc', 5: 'palma o paja', 6: 'plastico', 7: 'desechos (carton, lata, tela, sacos, etc)', 8: 'otro'}
            df['materialPredominanteTecho'] = df['materialPredominanteTecho'].map(materialPredominanteTecho_mapping)
            hacinamiento_mapping = {1: 'Si', 2: 'No'}
            df['hacinamiento'] = df['hacinamiento'].map(hacinamiento_mapping)
            codRiesgoAccidenteVivienda_mapping = {1: 'objetos cortantes o pulzantes al alcance de los niños', 2: 'Sustancias quimicas al lado de los niños', 3: 'Medicamentos al alcance de los niños', 4: 'Velas, velones, inciensos encendidos en la vivienda', 5: 'Conexiones electricas en mal estado o sobrecargadas', 6: 'Botones, canicas entre objetos pequeños o con piezas que puedan desmontarse, al alcancede los niños', 7: 'Pasillos obstruidos con juguetes, sillas u otros objetos', 8: 'Superficies resbaladisas, suelos con agua, grasas, aceites, entre otros', 9: 'Tanques o recipientes de almacenamiento de agua sin tapa', 10: 'Escaleras sin proteccion', 11: 'Ninguno'}
            df['codRiesgoAccidenteVivienda'] = df['codRiesgoAccidenteVivienda'].apply(lambda x: map_multiple_values(x, codRiesgoAccidenteVivienda_mapping))
            sitiosInteresFacilAccesoVivienda_mapping = {1: 'Medios de transporte:buses, autos, camiones, lanchas, etc', 2: 'Parques, y areas deportivas, centros sociales y/o recreacionales', 3: 'Instituciones educativas', 4: 'Sercicios de salud', 5: 'Ninguno'}
            df['sitiosInteresFacilAccesoVivienda'] = df['sitiosInteresFacilAccesoVivienda'].apply(lambda x: map_multiple_values(x, sitiosInteresFacilAccesoVivienda_mapping))
            fuentesEnergiaCombustibleCocinar_mapping = {1: 'Electricidad', 2: 'Gas natural', 3: 'Gas licuado del petroleo, gas propano', 4: 'Leña, madera o carbon de leña', 5: 'Petroleo, gasolina, kerosen, alcohol', 6: 'Carbon Mineral', 7: 'Materiales de desecho', 8: 'Otro'}
            df['fuentesEnergiaCombustibleCocinar'] = df['fuentesEnergiaCombustibleCocinar'].apply(lambda x: map_multiple_values(x, fuentesEnergiaCombustibleCocinar_mapping))
            observaCriaderosVectores_mapping = {1: 'Si', 2: 'No'}
            df['observaCriaderosVectores'] = df['observaCriaderosVectores'].apply(lambda x: map_multiple_values(x, observaCriaderosVectores_mapping))
            observacionesLugaresCercaVivienda_mapping = {1: 'Cultivos', 2: 'Apriscos', 3: 'Porquerizas', 4: 'Galpones', 5: 'Terrenos baldios', 6: 'Presencia de plagas:roedores, cucarachas, zancudos, moscas, etc', 7: 'Ruido o sonido desagradable', 8: 'Malos olores', 9: 'Sitios satelites de disposicion de excretas', 10: 'Rellenos sanitarios/botaderos', 11: 'Industrias contaminantes; del sector energetico, minero, tranpsorte, construccion, manufacturera, entre otros', 12: 'Contaminacion visual', 13: 'Rio o quebrada', 14: 'Planta de tratamiento de agua residual', 15: 'Extraccion minera', 16: 'Canales de agua lluvia', 17: 'Vias de trafico vehicular', 18: 'Quemas a cielo abierto', 19: 'Otro', 20: 'Ninguno' }
            df['observacionesLugaresCercaVivienda'] = df['observacionesLugaresCercaVivienda'].apply(lambda x: map_multiple_values(x, observacionesLugaresCercaVivienda_mapping))
            actividadEconomicaEnVivienda_mapping = {1: 'Si', 2: 'No'}
            df['actividadEconomicaEnVivienda'] = df['actividadEconomicaEnVivienda'].apply(lambda x: map_multiple_values(x, actividadEconomicaEnVivienda_mapping))
            animalesEnViviendaEntornoInmediato_mapping = {1: 'Perros', 2: 'Gatos', 3: 'Porcinos', 4: 'Bovidos:bufalos, vacas, toros', 5: 'equidos: Asnos, mulas, caballos, burros', 6: 'Ovinos /caprino', 7: 'Aves de produccion', 8: 'Aves ornamentales', 9: 'Peces hornamentales, hamster', 10: 'Cobayos, conejos', 11: 'Animales silvestres', 12: 'Otro', 13: 'Ninguno'}
            df['animalesEnViviendaEntornoInmediato'] = df['animalesEnViviendaEntornoInmediato'].apply(lambda x: map_multiple_values(x, animalesEnViviendaEntornoInmediato_mapping))
            principalFuenteAguaConsumoHumano_mapping = {1: 'Acueducto administrado por empresa prestadora: ESP', 2: 'Agua embotellado o en bolsa', 3: 'Acueducto veredal o comunitario', 4: 'Pila publica', 5: 'Carro tanque', 6: 'Abasto con distribuccion comunitaria', 7: 'Pozo con bomba', 8: 'Pozo sin bomba, aljibe, jaguey o barreno', 9: 'Laguna o jaguey', 10: 'Rio, quebrada, manantial o nacimiento', 11: 'Aguas lluvias', 12: 'Aguatero', 13: 'Otro'}
            df['principalFuenteAguaConsumoHumano'] = df['principalFuenteAguaConsumoHumano'].apply(lambda x: map_multiple_values(x, principalFuenteAguaConsumoHumano_mapping))
            disposicionExcretas_mapping = {1: 'Sanitario conectado al alcantarillado', 2: 'Sanitario y letrina', 3: 'Sanitario conectado a pozo septico', 4: 'Sanitario ecologico seco', 5: 'Sanitario sin conexion', 6: 'Sanitario con disposicion a fuente hidrica', 7: 'Campo abierto', 8: 'Otro'}
            df['disposicionExcretas'] = df['disposicionExcretas'].apply(lambda x: map_multiple_values(x, disposicionExcretas_mapping))
            disposicionAguaResidual_mapping = {1:'Alcantarillado', 2: 'Pozo septico', 3: 'Campo de oxidacion', 4: 'Biofiltro', 5: 'Fuente hidrica', 6: 'Campo abierto', 7: 'Otro'}
            df['disposicionAguaResidual'] = df['disposicionAguaResidual'].apply(lambda x: map_multiple_values(x, disposicionAguaResidual_mapping))
            disposicionResiduosSolidos_mapping = {1: 'Recoleccion por parte del servicio de aseo distrital o municipal', 2: 'Enterramiento', 3: 'Quema a campo abierto', 4: 'Disposicion en fuentes de agua cercana', 5: 'Disposicion a capo abierto', 6: 'Otro'}
            df['disposicionResiduosSolidos'] = df['disposicionResiduosSolidos'].apply(lambda x: map_multiple_values(x, disposicionResiduosSolidos_mapping))
            tipoFamilia_mapping = {1: 'Nuclear biparental', 2: 'Nuclear monoparental', 3: 'Extenso biparental', 4: 'Extenso monoparental', 5: 'Compuesto biparental', 6: 'Compuesto monoparental', 7: 'Otro' }
            df['tipoFamilia'] = df['tipoFamilia'].apply(lambda x: map_multiple_values(x, tipoFamilia_mapping))
            familograma_mapping = {1: 'Biologicos', 2: 'Psicologicos', 3: 'Sociales'}
            df['familograma'] = df['familograma'].apply(lambda x: map_multiple_values(x, familograma_mapping))
            codResultadoAPGAR_mapping = {1: 'Normal: 17-20 puntos', 2: 'Disfucion leve: 13-16 puntos', 3: 'Disfucion moderada: 10-12 puntos', 4: 'Disfucion severa: <=9 puntos' }
            df['codResultadoAPGAR'] = df['codResultadoAPGAR'].apply(lambda x: map_multiple_values(x, codResultadoAPGAR_mapping))
            cuidador_mapping = {1: 'Si', 2: 'No'}
            df['cuidador'] = df['cuidador'].apply(lambda x: map_multiple_values(x, cuidador_mapping))
            escalaZARIT_mapping = {1: 'Ausencia de sobrecarga: <= 46', 2: 'Sobrecarga ligera: 47-55', 3: 'Sobrecarga intensa >=56' }
            df['escalaZARIT'] = df['escalaZARIT'].apply(lambda x: map_multiple_values(x, escalaZARIT_mapping))
            ecomapa_mapping = {1: 'Positivo', 2: 'Tenue', 3: 'Estresante', 4: 'Fluye', 5: 'Intenso' }
            df['ecomapa'] = df['ecomapa'].apply(lambda x: map_multiple_values(x, ecomapa_mapping))
            ninosNinasAdolescentes_mapping = {1: 'Si', 2: 'No' }
            df['ninosNinasAdolescentes'] = df['ninosNinasAdolescentes'].apply(lambda x: map_multiple_values(x, ninosNinasAdolescentes_mapping))
            gestantes_mapping = {1: 'Si', 2: 'No' }
            df['gestantes'] = df['gestantes'].apply(lambda x: map_multiple_values(x, gestantes_mapping))
            adultosMayores_mapping = {1: 'Si', 2: 'No' }
            df['adultosMayores'] = df['adultosMayores'].apply(lambda x: map_multiple_values(x, adultosMayores_mapping))
            victimasConflicto_mapping = {1: 'Si', 2: 'No' }
            df['victimasConflicto'] = df['victimasConflicto'].apply(lambda x: map_multiple_values(x, victimasConflicto_mapping))
            personasDiscapacidad_mapping = {1: 'Si', 2: 'No' }
            df['personasDiscapacidad'] = df['personasDiscapacidad'].apply(lambda x: map_multiple_values(x, personasDiscapacidad_mapping))
            enfermedadesHuerfanas = {1: 'Si', 2: 'No' }
            df['enfermedadesHuerfanas'] = df['enfermedadesHuerfanas'].apply(lambda x: map_multiple_values(x, enfermedadesHuerfanas))
            enfermedadesTransmisibles_mapping = {1: 'TB', 2: 'Lepra', 3: 'Escabiosis, enfermedades infecciosas de la piel u otras', 4: 'Malaria', 5: 'Dengue', 6: 'Chagas', 7: 'Hepatitis A', 8: 'Alguna enfermedad inmunoprevenible, varicela-Parotiditis, otra', 9: 'Otra', 10: 'Ninguna'}
            df['enfermedadesTransmisibles'] = df['enfermedadesTransmisibles'].apply(lambda x: map_multiple_values(x, enfermedadesTransmisibles_mapping))
            sucesosVitalesNormativos_mapping = {1: 'Si', 2: 'No' }
            df['sucesosVitalesNormativos'] = df['sucesosVitalesNormativos'].apply(lambda x: map_multiple_values(x, sucesosVitalesNormativos_mapping))
            enSituacíonVulnerabilidad_mapping = {1: 'Si', 2: 'No' }
            df['enSituacíonVulnerabilidad'] = df['enSituacíonVulnerabilidad'].apply(lambda x: map_multiple_values(x, enSituacíonVulnerabilidad_mapping))
            practicasCuidadoSaludCriticas_mapping = {1: 'Si', 2: 'No' }
            df['practicasCuidadoSaludCriticas'] = df['practicasCuidadoSaludCriticas'].apply(lambda x: map_multiple_values(x, practicasCuidadoSaludCriticas_mapping))
            conAntecedentesDeEnfermedades_mapping = {1: 'Si', 2: 'No' }
            df['conAntecedentesDeEnfermedades'] = df['conAntecedentesDeEnfermedades'].apply(lambda x: map_multiple_values(x, conAntecedentesDeEnfermedades_mapping))
            fuenteAlimientos_mapping = {1: 'Cultiva', 2: 'Cria de animales', 3: 'Caceria', 4: 'Recoleccion de alimentos', 5: 'Trueque o intercambio', 6: 'Compra', 7: 'Asistencia del estado', 8: 'Ayuda humanitaria', 9: 'Otro' }
            df['fuenteAlimientos'] = df['fuenteAlimientos'].apply(lambda x: map_multiple_values(x, fuenteAlimientos_mapping))
            habitosVidaSaludable_mapping = {1: 'Si', 2: 'No' }
            df['habitosVidaSaludable'] = df['habitosVidaSaludable'].apply(lambda x: map_multiple_values(x, habitosVidaSaludable_mapping))
            recSocioemocionalesCuidadoSalud_mapping = {1: 'Si', 2: 'No' }
            df['recSocioemocionalesCuidadoSalud'] = df['recSocioemocionalesCuidadoSalud'].apply(lambda x: map_multiple_values(x, recSocioemocionalesCuidadoSalud_mapping))
            practicasCuidadoEntorno_mapping = {1: 'Si', 2: 'No' }
            df['practicasCuidadoEntorno'] = df['practicasCuidadoEntorno'].apply(lambda x: map_multiple_values(x, practicasCuidadoEntorno_mapping))
            practicasRelacionesSanasConstructivas_mapping = {1: 'Si', 2: 'No' }
            df['practicasRelacionesSanasConstructivas'] = df['practicasRelacionesSanasConstructivas'].apply(lambda x: map_multiple_values(x, practicasRelacionesSanasConstructivas_mapping))
            recursosSocComunPromocionSalud_mapping = {1: 'Si', 2: 'No' }
            df['recursosSocComunPromocionSalud'] = df['recursosSocComunPromocionSalud'].apply(lambda x: map_multiple_values(x, recursosSocComunPromocionSalud_mapping))
            practicasAutonomiaCapFuncionalAdultoMayor_mapping = {1: 'Si', 2: 'No' }
            df['practicasAutonomiaCapFuncionalAdultoMayor'] = df['practicasAutonomiaCapFuncionalAdultoMayor'].apply(lambda x: map_multiple_values(x, practicasAutonomiaCapFuncionalAdultoMayor_mapping))
            practicasPrevencionEnfermedadesParaTodos_mapping = {1: 'Si', 2: 'No' }
            df['practicasPrevencionEnfermedadesParaTodos'] = df['practicasPrevencionEnfermedadesParaTodos'].apply(lambda x: map_multiple_values(x, practicasPrevencionEnfermedadesParaTodos_mapping))
            practicasSaberesAncestrales_mapping = {1: 'Si', 2: 'No' }
            df['practicasSaberesAncestrales'] = df['practicasSaberesAncestrales'].apply(lambda x: map_multiple_values(x, practicasSaberesAncestrales_mapping))
            exigibilidadDerechoSalud_mapping = {1: 'Si', 2: 'No' }
            df['exigibilidadDerechoSalud'] = df['exigibilidadDerechoSalud'].apply(lambda x: map_multiple_values(x, exigibilidadDerechoSalud_mapping))
            rolEnLaFamilia_mapping = {1: 'Jefe de familia', 2: 'Conyuge', 3: 'Hijo', 4: 'Herman@', 5: 'Padre o Madre', 6: 'Otro' }
            df['rolEnLaFamilia'] = df['rolEnLaFamilia'].apply(lambda x: map_multiple_values(x, rolEnLaFamilia_mapping))
            nivelEducativo_mapping = {1: 'Preescolar', 2: 'Basica primaria', 3: 'Basica secundaria', 4: 'Media academica o clasica', 5: 'Media tecnica, bachillerato tecnico', 6: 'Normalista', 7: 'Tenica profesional', 8: 'Tecnologica', 9: 'Profesional', 10: 'Especializacion', 11: 'Maestria', 12: 'Doctorado', 13: 'Ninguno' }
            df['nivelEducativo'] = df['nivelEducativo'].apply(lambda x: map_multiple_values(x, nivelEducativo_mapping))
            regimenSalud_mapping = {1: 'Subsidiado', 2: 'Contributivo', 3: 'Especial', 4: 'Excepcion', 5: 'No afiliado'}
            df['regimenSalud'] = df['regimenSalud'].apply(lambda x: map_multiple_values(x, regimenSalud_mapping))
            pertenenciaGrupoEspecialProteccion_mapping = {1: 'Niñas, niños y adolescentes', 2: 'Gestantes', 3: 'Adulto mayor', 4: 'Condiciones de discapacidad', 5: 'Orientacion sexual diversa', 6: 'Victima de violencia', 7: 'Grupo etnico' }
            df['pertenenciaGrupoEspecialProteccion'] = df['pertenenciaGrupoEspecialProteccion'].apply(lambda x: map_multiple_values(x, pertenenciaGrupoEspecialProteccion_mapping))
            pertenenciaEtnica_mapping = {1: 'Indigena', 2: 'ROM GITANOS', 3: 'Raizal san andres y providencia', 4: 'Palenquero de san basilio de palenque', 5: 'Negr@', 6: 'Afrocolombiano', 7: 'Ninguna de las anteriores'}
            df['pertenenciaEtnica'] = df['pertenenciaEtnica'].apply(lambda x: map_multiple_values(x, pertenenciaEtnica_mapping))
            medicinaTradiconal_mapping = {1: 'Medico tradicional', 2: 'Partera', 3: 'Sabedor de la salud propia', 4: 'No aplica'}
            df['medicinaTradiconal'] = df['medicinaTradiconal'].apply(lambda x: map_multiple_values(x, medicinaTradiconal_mapping))
            codDiscapacidades_mapping = {1: 'Fisica', 2: 'Auditiva', 3: 'Visual', 4: 'Sordoceguera', 5: 'Intelectual', 6: 'Psicosocial, mental', 7: 'Multiple', 8: 'Sin discapacidad' }
            df['codDiscapacidades'] = df['codDiscapacidades'].apply(lambda x: map_multiple_values(x, codDiscapacidades_mapping))
            diagnosticoNutricional_mapping = {1: 'Obesidad', 2: 'Sobrepeso', 3: 'Riesgo de sobrepeso', 4: 'Peso adecuado para la talla', 5: 'Riesgo de desnutricion aguda', 6: 'Desnutricion aguda moderada, mental', 7: 'Desnutricion aguda severa'}
            df['diagnosticoNutricional'] = df['diagnosticoNutricional'].apply(lambda x: map_multiple_values(x, diagnosticoNutricional_mapping))
            condiSaludCronica_mapping = {1: 'Si', 2: 'No'}
            df['condiSaludCronica'] = df['condiSaludCronica'].apply(lambda x: map_multiple_values(x, condiSaludCronica_mapping))
            esquemaAtencionesPromMtto_mapping = {1: 'Si', 2: 'No'}
            df['esquemaAtencionesPromMtto'] = df['esquemaAtencionesPromMtto'].apply(lambda x: map_multiple_values(x, esquemaAtencionesPromMtto_mapping))
            intervencionesPendientes_mapping = {1: 'Valoracion integral para la PYMS', 2: 'Valoracion integral por profesional en odontologia para la PYMS', 3: 'Promocion y apoyo a la lactancia materna', 4: 'Aplicacion de fluor', 5: 'Proflaxis y remocion de placa bacteriana', 6: 'Vacunacion de acuerdo al esquema', 7: 'Fortificacion casera con micronutrientes en polvo', 8: 'Suplementacion con micronutrientes', 9: 'Desparacitacion intestinal antihelmintica', 10: 'Tamizaje para anemia - hemoglobina y hematocrito', 11: 'Planificacion familiar y anticoncepcion', 12: 'Tmizaje de riesgo cardiovascular', 13: 'Tamizaje para ITS', 14: 'Tamizaje para cancer de cuello uterino', 15: 'Tamizaje para cancer de mama', 16: 'Tamizaje para cancer de prostata', 17: 'Tamizaje para cancer de colon y recto', 18: 'Tamizaje para el cuidado preconcepcional', 19: 'Atencion para el cuidado prenatal - controles prentales', 20: 'Preparacion para la materninad y paternidad', 21: 'Interrupcion voluntaria del embarazo', 22: 'Atencion de puerperio', 23: 'Atencion para el seguimiento de recien nacido', 24: 'Educacion para la salud', 25: 'Ninguno' }
            df['intervencionesPendientes'] = df['intervencionesPendientes'].apply(lambda x: map_multiple_values(x, intervencionesPendientes_mapping))
            motivoNoAtencionPromMtto_mapping = {1: 'Lugar de atencion lejano, cerrado o ausencia del profesional de salud', 2: 'Horarios de atencion restringido', 3: 'Largos tiempos de espera', 4: 'No habia disponibilidad de la tecnologia', 5: 'Desconocimiento del derecho a las intervenciones de DTPE', 6: 'Desconocimiento que las intervenciones son gratuitas', 7: 'Persona enferma', 8: 'Persona Hospitalizada', 9: 'Orden medica por enfermedad' }
            df['motivoNoAtencionPromMtto'] = df['motivoNoAtencionPromMtto'].apply(lambda x: map_multiple_values(x, motivoNoAtencionPromMtto_mapping))
            practicaDeportiva_mapping = {1: 'Si', 2: 'No'}
            df['practicaDeportiva'] = df['practicaDeportiva'].apply(lambda x: map_multiple_values(x, practicaDeportiva_mapping))
            menorSeisMeses_mapping = {1: 'Si', 2: 'No'}
            df['menorSeisMeses'] = df['menorSeisMeses'].apply(lambda x: map_multiple_values(x, menorSeisMeses_mapping))
            menorCincoAnios_mapping = {1: 'Si', 2: 'No'}
            df['menorCincoAnios'] = df['menorCincoAnios'].apply(lambda x: map_multiple_values(x, menorCincoAnios_mapping))
            algunaEnfermedad_mapping = {1: 'Si', 2: 'No'}
            df['algunaEnfermedad'] = df['algunaEnfermedad'].apply(lambda x: map_multiple_values(x, algunaEnfermedad_mapping))
            recibeAtencionEnfermedad_mapping = {1: 'Si', 2: 'No'}
            df['recibeAtencionEnfermedad'] = df['recibeAtencionEnfermedad'].apply(lambda x: map_multiple_values(x, recibeAtencionEnfermedad_mapping))
            motivosNoAtencionEnfermedad_mapping = {1: 'Lugar de atencion lejano, cerrado o ausencia del profesional de salud', 2: 'Horarios de atencion restringido', 3: 'Largos tiempos de espera', 4: 'No habia disponibilidad de la tecnologia', 5: 'Desconocimiento del derecho a las intervenciones de DTPE', 6: 'Desconocimiento que las intervenciones son gratuitas', 7: 'Persona enferma', 8: 'Persona Hospitalizada', 9: 'Orden medica por enfermedad', 10: 'Falta de tiempo del cuidador', 11: 'Rechazo de la atencion por tradicion o cultura', 12: 'No afiliado'}
            df['motivosNoAtencionEnfermedad'] = df['motivosNoAtencionEnfermedad'].apply(lambda x: map_multiple_values(x, motivosNoAtencionEnfermedad_mapping))
            def determinar_curso_de_vida(edad):
                if 0 <= edad <= 5:
                   return 'Primera Infancia'
                elif 6 <= edad <= 11:
                   return 'Infancia'
                elif 12 <= edad <= 17:
                   return 'Adolescencia'
                elif 18 <= edad <= 28:
                  return 'Juventud'
                elif 29 <= edad <= 59:
                   return 'Adultez'
                elif 60 <= edad <= 150:
                    return 'Vejez'
                else:
                   return 'No aplica'
                
            df['cursos_de_vida'] = df['edad'].apply(determinar_curso_de_vida)

            def agregar_columnas_adicionales(row):
                if row['cursos_de_vida'] == 'Primera Infancia':
                    row['VALORACION INTEGRAL'] = """Aplica para:
                    - Atencion en salud por medicina general (Ambos sexos)
                    - Atencion integral por especialista en pediatria (Ambos sexos)
                    - Atencion integral por especialista en medicina familiar (Ambos sexos)
                    - Atencion en salud por profesional de enfermeria (Ambos sexos)
                    - Atencion en salud bucal por profesional de odontologia (Ambos sexos)
                    - Atencion por profesional en medicina o de enfermeria para la promocion y apoyo de la lactancia materna (Solo mujeres)
                    - Tamizaje para hemoglobina (Ambos sexos)"""
                    row['PROTECCION ESPECIFICA SALUD BUCAL'] = """Aplica para:
                    - Topicacion de fluor en Barniz (Ambos sexos)
                    - Control de placa dental (Ambos sexos)
                    - Aplicacion de sellantes (Ambos sexos)"""
                    row['PROTECCION ESPECIFICA VACUNACION (SEGUN ESQUEMA PAI)'] = """Aplica para:
                    - Neumococo (Ambos sexos)
                    - Tuberculosis [BCG] (Ambos sexos)
                    - Difteria, Tetanos y Tos ferina [DPT] (Ambos sexos)
                    - Haemophilus Influenza Tipo B, Difteria, Tetanos, Tos ferina y Hepatitis B (Pentavalente) (Ambos sexos)
                    - Poliomielitis (VOP o IVP) (Ambos sexos)
                    - Hepatitis A (Ambos sexos)
                    - Hepatitis B (Ambos sexos)
                    - Fiebre Amarilla (Ambos sexos)
                    - Varicela (Ambos sexos)
                    - Influenza (Ambos sexos)
                    - Rotavirus (Ambos sexos)
                    - Sarampion, Parotiditis y Rubeola [SRP] (Triple Viral) (Ambos sexos)"""
                    row['PROTECCION ESPECIFICA'] = """Aplica para:
                    - Fortificacion casera con micronutrientes en polvo (Ambos sexos)
                    - Suplementacion con micronutrientes (Vitamina A) (Ambos sexos)
                    - Suplementacion con hierro* (Ambos sexos)
                    - Desparasitacion intestinal antihelmíntica (Ambos sexos)"""
                    row['EDUCACION PARA LA SALUD'] = """Aplica para:
                    - Educacion individual (padres o cuidadores) (Ambos sexos)
                    - Educacion dirigida a la familia (Ambos sexos)
                    - Educacion grupal (Ambos sexos)"""

                if row['cursos_de_vida'] == 'Infancia':
                    row['VALORACION INTEGRAL'] = """Aplica para:
                    - Atencion en salud por medicina general (Ambos sexos)
                    - Atencion en salud por especialista en pediatria (Ambos sexos)
                    - Atencion integral por especialista en medicina familiar (Ambos sexos)
                    - Atencion en salud por profesional de enfermeria (Ambos sexos)
                    - Atencion en salud bucal por profesional de odontologia (Ambos sexos)"""
                    row['DETECCION TEMPRANA'] = """Aplica para:
                    - Tamizacion para Anemia (Ambos sexos)"""
                    row['PROTECCION ESPECIFICA'] = """Aplica para:
                    - Topicacion de fluor en barniz (Ambos sexos)
                    - Control de placa dental (Ambos sexos)
                    - Aplicacion de sellantes (Ambos sexos)
                    - Vacunacion (Ambos sexos)"""
                    row['EDUCACION PARA LA SALUD'] = """Aplica para:
                    - Educacion individual (Ambos sexos)
                    - Educacion dirigida a la familia (Ambos sexos)
                    - Educacion grupal (Ambos sexos)"""
                          
                if row['cursos_de_vida'] == 'Adolescencia':
                    row['VALORACION INTEGRAL'] = """Aplica para:
                    - Atencion en salud por medicina general (Ambos sexos)
                    - Atencion integral por especialista en medicina familiar (Ambos sexos)
                    - Atencion en salud por profesional de enfermeria (Ambos sexos)
                    - Atencion en salud bucal por odontologia general (Ambos sexos)"""
                    row['DETECCION TEMPRANA'] = """Aplica para:
                    - Prueba rapida treponemica (Ambos sexos)
                    - Prueba rapida para VIH (Ambos sexos)
                    - Asesoria pre y pos test VIH (Ambos sexos)
                    - Tamizaje para anemia (Ambos sexos)
                    - Prueba de embarazo (Solo Mujeres)"""
                    row['PROTECCION ESPECIFICA'] = """Aplica para:
                    - Atencion en salud por medicina general, medicina familiar, ginecologia o enfermeria para la asesoria en anticoncepcion - Consulta primera vez (Ambos sexos)
                    - Atencion en salud por medicina general, medicina familiar, ginecologia  o enfermeria para la asesoria en anticoncepcion - Control (Ambos sexos)
                    - Insercion de dispositivo intrauterino anticonceptivo [DIU] (Solo Mujeres)
                    - Extraccion de dispositivo anticonceptivo intrauterino [DIU] sod (Solo Mujeres)
                    - Insercion de anticonceptivos subdermicos (Solo Mujeres)
                    - Extraccion  de anticonceptivos subdermicos por incision (Solo Mujeres)
                    - Suministro de anticoncepcion oral ciclo e inyectable (Solo Mujeres)
                    - Suministro de preservativos (Ambos sexos)
                    - Metodo hormonal oral Progestina (Solo  Mujeres)
                    - Implante subdermico de Levonorgestrel o Etonorgestrel (Solo Mujeres)
                    - Inyeccion de Acetato de Medroxiprogesterona (Solo Mujeres)
                    - Topicacion de fluor en barniz (Ambos sexos)
                    - Detartraje supragingival (Ambos sexos)
                    - Aplicacion de sellantes (Ambos sexos)
                    - Vacunacion (Ambos sexos)"""
                    row['EDUCACION PARA LA SALUD'] = """Aplica para:
                    - Educacion individual (Ambos sexos)
                    - Educacion dirigida a la familia (Ambos sexos)
                    - Educacion grupal (Ambos sexos)"""

                if row['cursos_de_vida'] == 'Juventud':
                    row['VALORACION INTEGRAL'] = """Aplica para:
                    - Atencion en salud por medicina general (Ambos sexos)
                    - Atencion integral por especialista en medicina familiar (Ambos sexos)
                    - Atencion en salud bucal por odontologia general (Ambos sexos)"""
                    row['DETECCION TEMPRANA'] = """Aplica para:
                    - Tamizaje de riesgo cardiovascular: glicemia basal, perfil lipidico, creatinina, uro analisis (Ambos sexos)
                    - Prueba rapida treponemica (Ambos sexos)
                    - Prueba rapida para VIH (Ambos sexos)
                    - Asesoria pre y pos test VIH (Ambos sexos)
                    - Prueba rapida para Hepatitis B (Ambos sexos)
                    - Prueba rapida para Hepatitis C (Ambos sexos)
                    - Prueba de embarazo (Solo Mujeres)
                    - Tamizaje de cancer de cuello uterino (citologia) (Solo Mujeres)
                    - Colposcopia (Solo Mujeres)
                    - Biopsia cervicouterina (Solo Mujeres)"""
                    row['PROTECCION ESPECIFICA'] = """Aplica para:
                    - Atencion en salud por medicina general, medicina familiar, ginecologia o enfermeria para la asesoria en anticoncepcion - Consulta primera vez (Ambos sexos)
                    - Atencion en salud por medicina general, medicina familiar, ginecologia  o enfermeria para la asesoria en anticoncepcion - Control (Ambos sexos)
                    - VASECTOMIA SOD (Solo Hombres)
                    - Ablacion u oclusion de trompa de Falopio bilateral por laparoscopia (Solo Mujeres)
                    - Ablacion u oclusion de trompa de Falopio bilateral por laparotomía (Solo Mujeres)
                    - Insercion de dispositivo anticonceptivo intrauterino [DIU] sod (Solo Mujeres)
                    - Extraccion de dispositivo anticonceptivo intrauterino (Solo Mujeres)
                    - anticonceptivo intrauterino[DIU] sod
                    - Insercion de anticonceptivos subdermicos (Solo Mujeres)
                    - Metodo hormonal oral Progestina (Solo Mujeres)
                    - Implante subdermico de Levonorgestrel o Etonorgestrel (Solo Mujeres)
                    - Inyeccion de Acetato de Medroxiprogesterona (Solo Mujeres)
                    - Suministro de preservativos (Ambos sexos)
                    - Profilaxis y remocion de placa bacteriana (Ambos sexos)
                    - Detartraje supragingival (Ambos sexos)
                    - Vacunacion (Ambos sexos)"""
                    row['EDUCACION PARA LA SALUD'] = """Aplica para:
                    - Educacion individual (Ambos sexos)
                    - Educacion dirigida a la familia (Ambos sexos)
                    - Educacion grupal (Ambos sexos)"""

                if row['cursos_de_vida'] == 'Adultez':
                    row['VALORACION INTEGRAL'] = """Aplica para:
                    - Atencion integral por especialista en medicina familiar (Ambos sexos)
                    - Atencion en salud bucal por odontologia general (Ambos sexos)"""
                    row['DETECCION TEMPRANA'] = """Aplica para:
                    - Tamizaje de cancer de cuello uterino (ADN VPH) (Solo Mujeres)
                    - Tecnicas de inspeccion visual con acido acetico y lugol (Solo Mujeres)
                    - Criocauterizacion de cuello uterino (Solo Mujeres)
                    - Colposcopia cervico uterina (Solo Mujeres)
                    - Biopsia cervico uterina (Solo Mujeres)
                    - Mamografia bilateral (Solo Mujeres)
                    - Tamizaje para cancer de mama (valoracion clinica  de la mama) (Solo Mujeres)
                    - Tamizaje para cancer de colon* (Sangre oculta en materia fecal por inmunoquimica) (Ambos sexos)
                    - Colposcopia (Solo Mujeres)
                    - Biopsia de colon (Ambos sexos)
                    - Tamizaje de riesgo cardiovascular y metabolico: glicemia basal, perfil lipidico, creatinina, uro analisis (Ambos sexos)
                    - Prueba rapida treponemica (Ambos sexos)
                    - Prueba rapida para VIH (Ambos sexos)
                    - Asesoria pre y pos test VIH (Ambos sexos)
                    - Prueba rapida para Hepatitis B (Ambos sexos)
                    - Prueba rapida para Hepatitis C (Ambos sexos)
                    - Prueba de embarazo (Solo Mujeres)"""
                    row['PROTECCION ESPECIFICA'] = """Aplica para:
                    - Atencion en salud por medicina general, medicina familiar, ginecologia o enfermeria para la asesoria en anticoncepcion - Consulta primera vez (Ambos sexos)
                    - Atencion en salud por medicina general, medicina familiar, ginecologia  o enfermeria para la asesoria en anticoncepcion - Control (Ambos sexos)
                    - VASECTOMIA SOD (Solo Hombres)
                    - Ablacion u oclusion de trompa de Falopio bilateral por laparoscopia (Solo Mujeres)
                    - Ablacion u oclusion de trompa de Falopio bilateral por laparotomía (Solo Mujeres)
                    - Insercion de dispositivo anticonceptivo intrauterino [DIU] sod (Solo Mujeres)
                    - Extraccion de dispositivo anticonceptivo intrauterino (Solo Mujeres)
                    - Insercion de anticonceptivos subdermicos (Solo Mujeres)
                    - Metodo hormonal oral Progestina (Solo Mujeres)
                    - Implante subdermico de Levonorgestrel o Etonorgestrel (Solo Mujeres)
                    - Inyeccion de Acetato de Medroxiprogesterona (Solo Mujeres)
                    - Suministro de preservativos (Ambos sexos)
                    - Profilaxis y remocion de placa bacteriana (Ambos sexos)
                    - Detartraje supragingival (Ambos sexos)
                    - Vacunacion (Ambos sexos)"""
                    row['EDUCACION PARA LA SALUD'] = """Aplica para:
                    - Educacion individual (Ambos sexos)
                    - Educacion dirigida a la familia (Ambos sexos)
                    - Educacion grupal (Ambos sexos)"""
                    
                if row['cursos_de_vida'] == 'Vejez':
                    row['VALORACION INTEGRAL'] = """Aplica para:
                    - Atencion integral por especialista en medicina general (Ambos sexos)
                    - Atencion integral por especialista en medicina familiar (Ambos sexos)
                    - Atencion en salud bucal por odontologia general (Ambos sexos)"""
                    row['DETECCION TEMPRANA'] = """Aplica para:                    
                    - Tamizaje para cancer de colon* (Sangre oculta en materia fecal por inmunoquimica) (Ambos sexos)
                    - Tecnicas de inspeccion visual con acido acetico y lugol
                    - Criocauterizacion de cuello uterino 
                    - Colposcopia cervico uterina
                    - Biopsia de colon (Ambos sexos)
                    - Mamografia bilateral
                    - Tamizaje de riesgo cardiovascular y metabolico: glicemia basal, perfil lipidico, creatinina, uro analisis (Ambos sexos)
                    - Prueba rapida treponemica (Ambos sexos)
                    - Prueba rapida para VIH (Ambos sexos)
                    - Asesoria pre y pos test VIH (Ambos sexos)
                    - Prueba rapida para Hepatitis B (Ambos sexos)
                    - Prueba rapida para Hepatitis C (Ambos sexos)
                    - Mamografia bilateral (Solo Mujeres)
                    - Tamizaje para cancer de mama (valoracion clinica  de la mama) (Solo Mujeres)
                    - Tamizaje de cancer de cuello uterino (ADN VPH) (Solo Mujeres)
                    - Tecnicas de inspeccion visual con acido acetico y lugol (Solo Mujeres)
                    - Criocauterizacion de cuello uterino (Solo Mujeres)
                    - Colposcopia cervico uterina (Solo Mujeres)
                    - Biopsia cervico uterina (Solo Mujer)"""
                    row['PROTECCION ESPECIFICA'] = """Aplica para:
                    - Atencion en salud por medicina general, medicina familiar, ginecologia o enfermeria para la asesoria en anticoncepcion - Consulta primera vez (Ambos sexos).
                    - Atencion en salud por medicina general, medicina familiar, ginecologia  o enfermeria para la asesoria en anticoncepcion - Control (Ambos sexos).
                    - VASECTOMIA SOD (Solo Hombres)
                    - Suministro de preservativos (Solo Hombres)
                    - Profilaxis y remocion de placa bacteriana (Ambos sexos)
                    - Inyeccion de Acetato de Medroxiprogesterona (Solo Mujeres)
                    - Detartraje supragingival (Ambos sexos)
                    - Vacunacion (Ambos sexos)"""
                    row['EDUCACION PARA LA SALUD'] = """Aplica para:
                    - Educacion individual (Ambos sexos)
                    - Educacion dirigida a la familia (Ambos sexos)
                    - Educacion grupal (Ambos sexos)"""       
                return row
            municipios = df['municipio'].unique().tolist()
            #primer alerta y plan            
            df_alertas_vivienda = df[df['estratoVivienda'].isin(['Bajo-bajo', 'Bajo', 'Medio-Bajo', 'Medio', 'Medio-Alto', 'Alto'])].copy()
            df_alertas_vivienda['EstratoSocioeconomico'] = 'estratoVivienda'
            df_alertas_vivienda['alerta'] = df_alertas_vivienda['estratoVivienda'].map({
            'Bajo-bajo': 'Si responde "Bajo-bajo" se genera la alerta: Riesgo medio (Tiempo de respuesta: 1 a 3 meses)',
            'Bajo': 'Si responde "Bajo" se genera la alerta: Riesgo medio (Tiempo de respuesta: 1 a 3 meses)',
            'Medio-Bajo': 'Si responde "Medio-Bajo" se genera la alerta: Riesgo bajo o sin riesgo (Tiempo de respuesta: 3 a 6 meses)',
            'Medio': 'Si responde "Medio" se genera la alerta: Riesgo bajo o sin riesgo (Tiempo de respuesta: 3 a 6 meses)',
            'Medio-Alto': 'Si responde "Medio-Alto" se genera la alerta: Riesgo bajo o sin riesgo (Tiempo de respuesta: 3 a 6 meses)',
            'Alto': 'Si responde "Alto" se genera la alerta: Riesgo bajo o sin riesgo (Tiempo de respuesta: 3 a 6 meses)'})
            df_alertas_vivienda['plan'] = df_alertas_vivienda['estratoVivienda'].map({
            'Bajo-bajo': 'Realizar talleres de fortalecimiento comunitario para la mejora de condiciones de vivienda.',
            'Bajo': 'Implementar un plan de apoyo técnico para optimizar servicios básicos y saneamiento.',
            'Medio-Bajo': 'Promover campañas educativas sobre hábitos de mantenimiento y cuidado del hogar.',
            'Medio': 'Desarrollar un programa de incentivos para hogares sostenibles.',
            'Medio-Alto': 'Fomentar buenas prácticas en el uso de recursos y ahorro energético.',
            'Alto': 'Difundir información sobre programas de vivienda saludable y sostenibilidad.'})
            df_alertas_vivienda['agrupacion'] = 'INFORMACION GENERAl'

            columnas_seleccionadas = ['primernombre', 'primerApellido', 'nroDocumento', 'fechaNacimiento', 'rolEnLaFamilia', 'cursos_de_vida', 'municipio', 'sexo', 'tipoDocumento', 'ubicacionHogar', 'estratoVivienda', 'codTipoVivienda', 'agrupacion', 'alerta', 'plan']
            # Unión de ambos DataFrames
            df_alertas = pd.concat([df_alertas_vivienda], ignore_index=True)

# Selección de columnas
            df_alertas = df_alertas[columnas_seleccionadas]
            df_alertas.to_csv('Alertas_Familiares.csv', sep=';', index=False, encoding='utf-8-sig')
            df_alertas.to_csv('Alertas_Familiares.csv', sep=';', index=False)
            return {"success": True, "message": "Archivo convertido correctamente"}
        except Exception as e:
            return {"success": False, "message": f"No se pudo convertir el archivo: {e}"}

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    result = load_file(file)
    return jsonify(result)

@app.route('/convert', methods=['POST'])
def convert():
    result = convert_data()
    return jsonify(result)

@app.route('/municipios', methods=['GET'])
def get_municipios():
    global municipios
    return jsonify(municipios)

@app.route('/download', methods=['GET'])
def download_file():
    global df
    municipio = request.args.get('municipio')
    if df is not None:
        if municipio:
            df_filtered = df[df['municipio'] == municipio]
        else:
            df_filtered = df

        file_path = 'Resultado_Datos_Convertidos.csv'
        df_filtered.to_csv(file_path, sep=';', index=False, encoding='utf-8-sig')
        return send_file(file_path, as_attachment=True)
    else:
        return {"success": False, "message": "No hay datos para guardar"}

    
@app.route('/download_alertas', methods=['GET'])
def download_alertas():
    global df
    municipio = request.args.get('municipio')
    
    if df is not None:
        if municipio:
            df_filtered = df[df['municipio'] == municipio]
        else:
            df_filtered = df
        file_path = 'Alertas_Familiares.csv'
        
        try:
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return {"success": False, "message": f"No se pudo descargar el archivo de alertas: {e}"}
    else:
        return {"success": False, "message": "No hay datos para generar alertas"}


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)