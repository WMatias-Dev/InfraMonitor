# InfraMonitor

InfraMonitor é uma ferramenta de monitoramento de recursos do sistema desenvolvida em **Python**, com foco em ambientes **Linux**. O projeto foi criado para consolidar conhecimentos em administração de sistemas, monitoramento, automação e desenvolvimento de aplicações para infraestrutura.

> **Status do projeto:** 🚧 Em desenvolvimento

---

## 📖 Sobre

O objetivo do InfraMonitor é fornecer uma interface simples para visualizar informações do sistema operacional diretamente pelo terminal.

Atualmente, o projeto permite consultar informações de:

- 🖥️ CPU
- 💾 Memória RAM
- 💿 Disco
- 🌐 Rede
- 📋 Processos em execução
- 🔋 Bateria (quando disponível)
- ⚙️ Informações do sistema operacional

O projeto está sendo desenvolvido de forma incremental, seguindo boas práticas de organização de código e versionamento.

---

## 🚀 Tecnologias utilizadas

- Python 3.11+
- psutil
- Platform (biblioteca padrão)
- Git
- GitHub

---

## 📂 Estrutura do projeto

```
InfraMonitor/
│
├── src/
│   ├── main.py
│   ├── monitor.py
│   └── utils.py
│
├── tests/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/InfraMonitor.git
```

### 2. Entre na pasta

```bash
cd InfraMonitor
```

### 3. Crie um ambiente virtual (opcional, mas recomendado)

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

---

## 📌 Funcionalidades atuais

- Consulta de utilização da CPU
- Consulta de memória RAM
- Informações sobre discos
- Estatísticas de rede
- Listagem de processos
- Informações do sistema operacional
- Informações da bateria (quando disponível)

---

## 🎯 Objetivos do projeto

Este projeto faz parte do meu portfólio de estudos voltado para:

- Linux
- Infraestrutura
- DevOps
- Automação
- Observabilidade
- Python

---

## 📅 Roadmap

Próximas melhorias planejadas:

- [ ] Melhor compatibilidade com Linux
- [ ] Sistema de logs
- [ ] Exportação de relatórios (JSON/CSV)
- [ ] Monitoramento contínuo
- [ ] Alertas de uso de recursos
- [ ] Dockerização da aplicação
- [ ] Testes automatizados

---

## 🤝 Contribuição

Este é um projeto de estudos e aprendizado. Sugestões de melhorias são bem-vindas.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT.

---

## 👨‍💻 Autor

**William Lopes Matias**

Estudante de Bacharelado Interdisciplinar em Ciência e Tecnologia

Focado em Linux • Infraestrutura • DevOps • Automação