# InfraMonitor

InfraMonitor é um projeto em **Python** para monitorar recursos de um sistema Linux. Ele nasceu como um estudo prático de **DevOps**, automação e observabilidade, e foi pensado também como peça de portfólio para quem está buscando uma vaga de estágio na área.

> **Status do projeto:** Em desenvolvimento

---

## Sobre

A ideia aqui é simples: coletar dados úteis do servidor, organizar essas informações e deixá-las prontas para análise no terminal, em logs e em relatórios.

O projeto já consegue trabalhar com:

- CPU
- Memória RAM
- Disco
- Alertas automáticos
- Relatórios em JSON e CSV
- Rede
- Processos em execução
- Bateria (quando disponível)
- Informações do sistema operacional

O foco é mostrar uma base sólida de engenharia, com código organizado, testes e uma estrutura que faz sentido para um cenário de servidor Linux.

---

## Tecnologias utilizadas

- Python 3.11+
- psutil
- Git
- GitHub

---

## Estrutura atual

```
InfraMonitor/
│
├── src/
│   ├── main.py
│   ├── monitor.py
│   ├── collectors.py
│   ├── alerts.py
│   ├── reports.py
│   ├── logger.py
│   ├── config.py
│   └── utils.py
│
├── tests/
├── config.json
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/InfraMonitor.git
```

### 2. Entre na pasta

```bash
cd InfraMonitor
```

### 3. Crie um ambiente virtual, se quiser isolar a instalação

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute

```bash
python src/main.py
```

### 6. Ajuste a configuração

O comportamento do projeto é definido pelo arquivo [config.json](config.json), na raiz do repositório. Ali você pode ajustar intervalo de coleta, limites de alerta, diretório de logs e diretório de relatórios.

Campos principais:

- `intervalo_coleta_segundos`
- `alertas.cpu.warning` e `alertas.cpu.critical`
- `alertas.memoria.warning` e `alertas.memoria.critical`
- `alertas.disco.warning` e `alertas.disco.critical`
- `logs.diretorio`, `logs.arquivo`, `logs.nivel`, `logs.max_bytes`, `logs.backup_count`
- `relatorios.diretorio`

---

## O que esse projeto mostra

- Coleta e tratamento de métricas de sistema
- Estrutura voltada para Linux
- Alertas automáticos com limites configuráveis
- Geração de logs estruturados
- Exportação de relatórios em JSON e CSV
- Testes automatizados com `pytest`

---

## Objetivos do projeto

Este projeto foi pensado para o meu portfólio com foco em vagas de estágio DevOps. Ele ajuda a demonstrar interesse prático em:

- Linux
- Infraestrutura
- DevOps
- Automação
- Observabilidade
- Python

---

## Alertas automáticos

O agente gera alertas quando CPU, memória RAM ou disco ultrapassam os limites definidos em [config.json](config.json).

Se o arquivo não estiver disponível, o projeto continua funcionando com os valores padrão.

---

## Relatórios

O projeto também exporta os registros coletados em JSON e CSV, sem alterar o fluxo de coleta.

### Estrutura dos relatórios

- JSON: mantém os registros completos.
- CSV: organiza os dados em formato tabular.

### Diretório padrão

Os relatórios são gravados no diretório definido em `relatorios.diretorio`.

---

## Roadmap

Próximas melhorias que fazem sentido para evoluir o projeto:

- [ ] Melhor compatibilidade com Linux
- [ ] Exportação de relatórios (JSON/CSV)
- [ ] Monitoramento contínuo
- [ ] Alertas de uso de recursos
- [ ] Dockerização da aplicação
- [ ] Testes automatizados

---

## Contribuição

O projeto está aberto para melhorias e serve como base de estudo. Sugestões são bem-vindas.

---

## Licença

Este projeto está licenciado sob a licença MIT.

---

## Autor

**William Lopes Matias**

Estudante de Bacharelado Interdisciplinar em Ciência e Tecnologia

Focado em Linux • Infraestrutura • DevOps • Automação