/* Descrição:
 * Criação da tabela de Ocorrências;
 *
 * Autor: Matheus Lima
 * Data: 22/08/2025
 */

-- Tabela
DROP TABLE IF EXISTS public.tb_ocorrencia CASCADE;

CREATE TABLE public.tb_ocorrencia (
    id UUID NOT NULL,
    titulo VARCHAR(120) NOT NULL,
    descricao TEXT NULL,
    prioridade VARCHAR(10) NOT NULL CHECK (prioridade IN ('BAIXA','MEDIA','ALTA')),
    status VARCHAR(15) NOT NULL CHECK (status IN ('ABERTA','EM_ANDAMENTO','RESOLVIDA','CANCELADA')),
    email_responsavel VARCHAR(255) NOT NULL,
    tags TEXT[] DEFAULT '{}',
    data_abertura TIMESTAMP NOT NULL DEFAULT NOW(),
    data_atualizacao TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

-- Índices
CREATE INDEX idx_tb_ocorrencia_titulo ON public.tb_ocorrencia (titulo);
CREATE INDEX idx_tb_ocorrencia_status ON public.tb_ocorrencia (status);
CREATE INDEX idx_tb_ocorrencia_prioridade ON public.tb_ocorrencia (prioridade);

-- Comentários
COMMENT ON TABLE public.tb_ocorrencia IS 'Tabela de Ocorrências reportadas';
COMMENT ON COLUMN public.tb_ocorrencia.id IS 'Chave única da ocorrência (UUID)';
COMMENT ON COLUMN public.tb_ocorrencia.titulo IS 'Título da ocorrência (5–120 caracteres)';
COMMENT ON COLUMN public.tb_ocorrencia.descricao IS 'Descrição detalhada da ocorrência';
COMMENT ON COLUMN public.tb_ocorrencia.prioridade IS 'Prioridade: BAIXA, MEDIA ou ALTA';
COMMENT ON COLUMN public.tb_ocorrencia.status IS 'Status: ABERTA, EM_ANDAMENTO, RESOLVIDA, CANCELADA';
COMMENT ON COLUMN public.tb_ocorrencia.email_responsavel IS 'E-mail do responsável';
COMMENT ON COLUMN public.tb_ocorrencia.tags IS 'Lista de tags relacionadas';
COMMENT ON COLUMN public.tb_ocorrencia.data_abertura IS 'Data de abertura da ocorrência';
COMMENT ON COLUMN public.tb_ocorrencia.data_atualizacao IS 'Data da última modificação da ocorrência';

-- Permissões
ALTER TABLE public.tb_ocorrencia OWNER TO incidents_user;
GRANT ALL ON TABLE public.tb_ocorrencia TO incidents_user;
