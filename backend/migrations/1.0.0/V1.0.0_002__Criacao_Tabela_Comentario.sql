/* Descrição:
 * Criação da tabela de Comentários;
 *
 * Autor: Matheus Lima
 * Data: 22/08/2025
 */

-- Tabela
DROP TABLE IF EXISTS public.tb_comentario CASCADE;

CREATE TABLE public.tb_comentario (
    id UUID NOT NULL,
    ocorrencia_id UUID NOT NULL,
    autor VARCHAR(120) NOT NULL,
    mensagem TEXT NOT NULL,
    data_criacao TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT tb_comentario_ocorrencia_fk FOREIGN KEY (ocorrencia_id)
        REFERENCES public.tb_ocorrencia (id)
        ON DELETE CASCADE
);

-- Comentários
COMMENT ON TABLE public.tb_comentario IS 'Tabela de comentários vinculados a ocorrências';
COMMENT ON COLUMN public.tb_comentario.id IS 'Chave única do comentário (UUID)';
COMMENT ON COLUMN public.tb_comentario.ocorrencia_id IS 'Chave da ocorrência relacionada';
COMMENT ON COLUMN public.tb_comentario.autor IS 'Autor do comentário';
COMMENT ON COLUMN public.tb_comentario.mensagem IS 'Texto do comentário';
COMMENT ON COLUMN public.tb_comentario.data_criacao IS 'Data de criação do comentário';

-- Permissões
ALTER TABLE public.tb_comentario OWNER TO incidents_user;
GRANT ALL ON TABLE public.tb_comentario TO incidents_user;
