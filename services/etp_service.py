from config import Config
from repositories.etp_repository import EtpRepository
from openai import OpenAI
import json

class EtpService:
    
    @staticmethod
    def get(id):
        etp = EtpRepository.get(id)
        return etp if etp else None

    @staticmethod
    def create(
        tipo_contratacao: str,
        titulo: str,
        problema: str,
        orgao: str,
        setor_requisitante: str,
        quantidade: int,
        unidade_medida: str,
        orcamento_estimado: float,
        impacto_ambiental: str,
        responsaveis: list[str],
        pca_inclusao: bool,
        pca_referencia: str  
    ):
        prompt = f'''
            Você é um especialista em contratações públicas e redação de Estudos Técnicos Preliminares (ETP).  
            Gere um ETP completo em formato JSON STRICT seguindo rigorosamente as especificações abaixo.

            # PARÂMETROS DE ENTRADA:
            - tipo_contratacao: "{tipo_contratacao}"
            - titulo: "{titulo}"
            - problema: "{problema}"
            - orgao: "{orgao}"
            - setor_requisitante: "{setor_requisitante}"
            - quantidade: {quantidade}
            - unidade_medida: "{unidade_medida}"
            - orcamento_estimado: {orcamento_estimado:.2f}
            - impacto_ambiental: "{impacto_ambiental}"
            - responsaveis: {responsaveis}
            - pca_inclusao: {pca_inclusao}
            - pca_referencia: "{pca_referencia}"

            # MODELO DE SAÍDA (EXEMPLO VÁLIDO):
            {{
                "metadados": {{
                    "versao": "1.0",
                    "data_elaboracao": "2023-11-15",
                    "orgao": "Secretaria Municipal de Saúde",
                    "responsaveis": ["Dr. João Silva","Dra. Maria Oliveira"]
                }},
                "identificacao": {{
                    "titulo": "Aquisição de Medicamentos Oncológicos",
                    "tipo_contratacao": "Pregão Eletrônico",
                    "codigo_pca": "PCA-2023-0456",
                    "setor_requisitante": "Oncologia"
                }},
                "conteudo": {{
                    "descricao_necessidade": {{
                        "problema": "Falta de medicamentos para tratamento de câncer",
                        "impacto_administrativo": "Interrupção de tratamentos",
                        "alinhamento_estrategico": "Plano Municipal de Saúde 2021-2024"
                    }},
                    "requisitos_contratacao": {{
                        "especificacoes_tecnicas": ["Medicamentos com registro na ANVISA"],
                        "sustentabilidade": ["Embalagens recicláveis"],
                        "normativas_aplicaveis": ["Lei 8.666/93"]
                    }},
                    "quantificacao": {{
                        "quantidade": 1500,
                        "unidade_medida": "caixas",
                        "memoria_calculo": "Baseado em demanda histórica"
                    }},
                    "alternativas": {{
                        "opcoes_analisadas": [
                            {{
                                "descricao": "Compra direta",
                                "vantagens": ["Agilidade"],
                                "desvantagens": ["Maior custo"]
                            }}
                        ],
                        "solucao_recomendada": "Pregão Eletrônico"
                    }},
                    "orcamento": {{
                    "valor_estimado": 1250000.00,
                    "composicao_valor": [
                        {{
                            "item": "Caixa de medicamento X",
                            "valor_unitario": 850.00,
                            "fonte_referencia": "SIGA Brasil"
                        }}
                    ],
                    "parcelamento": "3 parcelas",
                    "justificativa": "Valores de mercado"
                    }},
                    "viabilidade": {{
                        "conclusao": "Viável",
                        "condicionantes": ["Liberação de verba"]
                    }}
                }}
            }}

            # REGRAS ABSOLUTAS:
            1. ESTRUTURA FIXA: Mantenha exatamente esta estrutura JSON, mesmo que alguns campos sejam "não aplicável"
            2. TIPOS DE DADOS:
            - Strings: sempre entre aspas duplas
            - Números: decimais com 2 casas para valores monetários
            - Arrays: sempre inicializados, mesmo que vazios []
            3. FORMATAÇÃO:
            - Indentação: 2 espaços
            - Datas: ISO 8601 (YYYY-MM-DD)
            - Escape de caracteres especiais: \\", \\n, etc.
            4. VALORES PADRÃO:
            - Campos string vazios: ""
            - Valores desconhecidos: "não aplicável"
            - Arrays sem itens: []
            5. VALIDAÇÃO:
            - O JSON deve ser parseável por json.loads() sem erros
            - Não pode conter vírgulas finais
            - Não pode conter comentários

            # INSTRUÇÕES DE EXECUÇÃO:
            1. Analise os parâmetros fornecidos
            2. Preencha TODOS os campos mantendo a estrutura exata do modelo
            3. Garanta que o JSON é válido antes de retornar
            4. Retorne APENAS o JSON, sem markdown ou comentários

            O JSON deve começar com "{{" e terminar com "}}" sem texto adicional.
            '''.strip()
        
        try:
            client = OpenAI(api_key = Config.OPENAI_KEY)
            response = client.chat.completions.create(
                model = 'gpt-4o-mini',
                response_format = {'type': 'json_object'},
                messages = [{'role': 'user', 'content': prompt}]
            )

            data = response.choices[0].message.content
            return EtpRepository.create(json.loads(data))
        except Exception:
            return None

    @staticmethod
    def delete(id):
        return EtpRepository.delete(id)
