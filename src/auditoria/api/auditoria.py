import seedwork.presentacion.api as api
import json
from seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session, Response, abort
from modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacionDTOJson
from modulos.auditoria.aplicacion.comandos.crear_regulacion import CrearRegulacion
from modulos.auditoria.aplicacion.queries.obtener_regulacion import ObtenerRegulacion
from modulos.auditoria.aplicacion.queries.obtener_todas_regulacion import ObtenerTodasRegulacion
from seedwork.aplicacion.comandos import ejecutar_commando
from seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('auditoria', '/auditoria')

@bp.route('/regulacion', methods=('POST',))
def regulacion_usando_comando():
    try:
        session['uow_metodo'] = 'pulsar'
        regulacion_dict = request.json

        map_regulacion = MapeadorRegulacionDTOJson()
        regulacion_dto = map_regulacion.externo_a_dto(regulacion_dict)
        comando = CrearRegulacion(regulacion_dto.id,
                                  regulacion_dto.nombre, 
                                  regulacion_dto.region,
                                  regulacion_dto.payload,
                                  regulacion_dto.fecha_actualizacion,
                                  regulacion_dto.requisitos)
        ejecutar_commando(comando)
        print("==================TERMINA============================")
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    
@bp.route('/regulacion/<id>', methods=('GET',))
def dar_regulacion_usando_query(id=None):
    if id:
        print("==========ENTRA ENDOPINT CONSULTAR REGULACION ============")
        query_resultado = ejecutar_query(ObtenerRegulacion(id))
        map_regulacion = MapeadorRegulacionDTOJson()
        if not query_resultado.resultado:
          abort(404, description="No se encontró la regulación solicitada")
        
        return map_regulacion.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]

@bp.route('/regulacion', methods=('GET',))
def dar_todas_regulaciones_usando_query():
        print("==========ENTRA ENDOPINT CONSULTAR TODAS ============")   
        query_resultado = ejecutar_query(ObtenerTodasRegulacion())
        map_regulacion = MapeadorRegulacionDTOJson()
        print("==========CASO TERMINA============") 
        if not query_resultado.resultado:
         return {}
        return [map_regulacion.dto_a_externo(data_source)  for data_source in query_resultado.resultado]
        
@bp.route('/health', methods=('GET',))
def ping():
    return "pong"
        
    