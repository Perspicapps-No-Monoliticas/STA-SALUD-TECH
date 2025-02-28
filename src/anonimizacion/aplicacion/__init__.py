from pydispatch import dispatcher

from src.aplicacion.pipeline import PipelineAnonimizacion


dispatcher.connect(PipelineAnonimizacion.handle_tokenizado_realizado, signal='TokenizadoDominio')
dispatcher.connect(PipelineAnonimizacion.handle_anonimizado_por_script_realizado, signal='AnonimizadoScriptDominio')
dispatcher.connect(PipelineAnonimizacion.handle_anonimizado_por_modelo_realizado, signal='AnonimizadoModeloDominio')
