from seedwork.aplicacion.dto import Mapeador as AppMap
from seedwork.dominio.repositorios import Mapeador as RepMap
from modulos.auditoria.dominio.entidades import Regulacion
from .dto import RegulacionDTO

class MapeadorRegulacionDTOJson(AppMap):
   
    def externo_a_dto(self, externo: dict) -> RegulacionDTO:
        regulacion_dto = RegulacionDTO(externo.get('id'), externo.get('nombre'), externo.get('region'), externo.get('payload'))    

        return regulacion_dto

    def dto_a_externo(self, dto: RegulacionDTO) -> dict:
        if isinstance(dto, list):  # Si es una lista, convertir cada elemento
          return [self.dto_a_externo(item) for item in dto]
        else:   
          return dto.__dict__

class MapeadorRegulacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Regulacion.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(codigo=None, descripcion=None, obligatorio=None, fecha_actualizacion=None, fecha_creacion=None)
        
        return dict(
                    codigo=locacion.codigo,
                    descripcion=locacion.descripcion,
                    obligatorio=locacion.obligatorio,
                    fecha_actualizacion=locacion.fecha_actualizacion.strftime(self._FORMATO_FECHA),
                    fecha_creacion=locacion.fecha_creacion.strftime(self._FORMATO_FECHA)
        )
        

    def entidad_a_dto(self, entidad: Regulacion) -> RegulacionDTO:
        _id = str(entidad.id)
        nombre= str(entidad.nombre)
        region= str(entidad.region)
        payload= str(entidad.payload)
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)        
        
        return RegulacionDTO(_id, nombre, region, payload, fecha_creacion, fecha_actualizacion)

    def dto_a_entidad(self, dto: RegulacionDTO) -> Regulacion:
        if not dto:
            return None
        if isinstance(dto, list): 
          return [self.dto_a_entidad(item) for item in dto]
        
        regulacion = Regulacion()
        regulacion._id = dto.id
        regulacion.nombre = dto.nombre
        regulacion.region = dto.region
        regulacion.payload = dto.payload
        return regulacion



