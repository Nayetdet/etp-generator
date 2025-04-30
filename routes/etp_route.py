from flask import Blueprint, Response, request, jsonify
from services.etp_service import EtpService

etp_bp = Blueprint('ETP', __name__, url_prefix = '/etp')

@etp_bp.route('/<id>', methods = ['GET'])
def get(id):
    etp = EtpService.get(id)
    if etp:
        return jsonify(etp), 200
    return Response(status = 404)

@etp_bp.route('/', methods = ['POST'])
def create():
    data = request.json
    etp = EtpService.create(
        tipo_contratacao = data.get('tipo_contratacao'),
        titulo = data.get('titulo'),
        problema = data.get('problema'),
        orgao = data.get('orgao'),
        setor_requisitante = data.get('setor_requisitante'),
        quantidade = data.get('quantidade'),
        unidade_medida = data.get('unidade_medida'),
        orcamento_estimado = data.get('orcamento_estimado'),
        impacto_ambiental = data.get('impacto_ambiental'),
        responsaveis = data.get('responsaveis'),
        pca_inclusao = data.get('pca_inclusao'),
        pca_referencia = data.get('pca_referencia')
    )

    if etp:
        return jsonify(etp), 201
    return jsonify({'error': 'Could not generate ETP'}), 500

@etp_bp.route('/<id>', methods = ['DELETE'])
def delete(id):
    if EtpService.delete(id):
        return Response(status = 204)
    return Response(status = 404)
