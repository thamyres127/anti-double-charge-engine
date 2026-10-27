import json
import uuid
from datetime import datetime

# Simulação do Banco de Dados Legado (Clientes que já cancelaram o serviço)
DB_CONTRATOS_CANCELADOS = {
    "CLI_7701": {"nome": "Carlos Eduardo Santos", "data_cancelamento": "2026-08-14"},
    "CLI_7702": {"nome": "Mariana Souza Oliveira", "data_cancelamento": "2026-09-02"},
    "CLI_7703": {"nome": "Roberto Azevedo Lima", "data_cancelamento": "2026-09-20"}
}

class AntiDoubleChargeEngine:
    def __init__(self):
        # Ledger de Chaves de Idempotência para checagem mecânica e travas rápidas
        self.idempotency_ledger = set()

    def processar_faturamento_batch(self, payload_transacao):
        """
        Executa a validação transacional e impede a duplicidade de faturamento
        de contas canceladas ou requisições duplicadas.
        """
        id_cliente = payload_transacao.get("client_id")
        chave_idempotencia = payload_transacao.get("idempotency_key")
        valor = payload_transacao.get("valor")
        
        print(f"\n[LOG - {datetime.now().strftime('%H:%M:%S')}] Analisando transação {chave_idempotencia}...")

        # PASSO 1: Bloqueio por Idempotência Mecânica (Prevenção de clique duplo / duplicidade de rede)
        if chave_idempotencia in self.idempotency_ledger:
            print(f"  [ALERTA DE DUPLICIDADE]: Chave {chave_idempotencia} já processada. Transação rejeitada automaticamente.")
            return {"status": "REJEITADA", "motivo": "Duplicidade de Faturamento Detectada (Idempotência Ativa)"}

        # Registrar a chave no ledger para travar tentativas seguintes na mesma janela de tempo
        self.idempotency_ledger.add(chave_idempotencia)

        # PASSO 2: Varredura de Segurança no Cadastro Legado (Prevenção de cobrança pós-cancelamento)
        if id_cliente in DB_CONTRATOS_CANCELADOS:
            info_cliente = DB_CONTRATOS_CANCELADOS[id_cliente]
            print(f"  [ANOMALIA DETECTADA]: Cliente {info_cliente['nome']} tentou ser faturado em R$ {valor:.2f}.")
            print(f"  [AÇÃO]: Bloqueando cobrança indevida. Contrato foi encerrado em {info_cliente['data_cancelamento']}.")
            return {"status": "EXPURGADA", "motivo": f"Cobrança Indevida Retida: Contrato cancelado em {info_cliente['data_cancelamento']}"}

        # Se passar pelas travas, a transação legítima é aprovada
        print(f"  [SUCESSO]: Transação de R$ {valor:.2f} aprovada e conciliada no Ledger.")
        return {"status": "SUCESSO", "motivo": "Transação legítima processada"}

# --- EXECUTANDO A SIMULAÇÃO BANCÁRIA QUE O RECRUTADOR VAI VER NO CONSOLE ---
if __name__ == "__main__":
    engine = AntiDoubleChargeEngine()
    
    # 1. Simulando a Anomalia Crítica: Sistema antigo tentando cobrar cliente que já cancelou
    print("--- CASO 1: Tentativa de Cobrança Pós-Cancelamento ---")
    cobranca_indevida = {
        "client_id": "CLI_7701",
        "idempotency_key": str(uuid.uuid4()),
        "valor": 249.90
    }
    engine.processar_faturamento_batch(cobranca_indevida)

    # 2. Simulando Instabilidade de Rede: Envio duplicado da mesma transação legítima
    print("\n--- CASO 2: Tentativa de Faturamento Duplicado (Clique Duplo) ---")
    chave_unica = str(uuid.uuid4())
    transacao_original = {"client_id": "CLI_9999", "idempotency_key": chave_unica, "valor": 50.00}
    transacao_duplicada = {"client_id": "CLI_9999", "idempotency_key": chave_unica, "valor": 50.00}
    
    engine.processar_faturamento_batch(transacao_original)  # Primeira tentativa passa
    engine.processar_faturamento_batch(transacao_duplicada)  # Segunda tentativa é barrada pela trava mecânica
