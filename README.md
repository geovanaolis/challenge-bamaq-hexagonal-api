# Desafio BAMAQ Capital - API de Análise de Crédito

Este projeto é uma API desenvolvida para o desafio técnico da BAMAQ Capital. O objetivo é simular um fluxo de recebimento de solicitações, avaliação assíncrona por mensageria e consulta rápida de status, utilizando a **Arquitetura Hexagonal (Ports and Adapters)**.

## 🚀 Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI** (Web Framework)
- **MySQL** (Banco de Dados Relacional principal)
- **Redis** (Cache de acesso ultrarrápido)
- **Apache Kafka** (Mensageria / Event-Driven)
- **SQLAlchemy** (ORM)
- **Pytest** (Testes Automatizados)
- **Docker & Docker Compose** (Infraestrutura)

## 🏗️ Arquitetura Hexagonal

O projeto foi dividido separando a regra de negócio da infraestrutura tecnológica:
- **Domain:** Entidades puras e regras de negócio (`RequestEntity`, `RequestStatus`). Não possui dependência de banco de dados ou frameworks web.
- **Infrastructure:** Adaptadores que se comunicam com o mundo externo (MySQL via SQLAlchemy, produtor do Kafka, etc).
- **Application/API:** Onde o FastAPI recebe as requisições (`main.py`) e orquestra a chamada entre o domínio e a infraestrutura.
- **Worker:** Consumidor Kafka desacoplado (`worker.py`) responsável por ler eventos, processar regras e atualizar MySQL e Redis.

---

## ⚙️ Como executar o projeto

### 1. Pré-requisitos
Você precisará ter instalado na sua máquina:
- [Python 3.12](https://www.python.org/downloads/)
- [Docker e Docker Compose](https://www.docker.com/)

### 2. Subindo a Infraestrutura (Banco, Cache e Mensageria)
Na raiz do projeto, suba os containers do MySQL, Redis, Zookeeper e Kafka:
```bash
docker-compose up -d
```

### 3. Configurando o Ambiente Python
Crie e ative um ambiente virtual, e instale as dependências:
```bash
python -m venv venv
source venv/Scripts/activate  # No Linux/Mac use: source venv/bin/activate
pip install -r requirements.txt
```

### 4. Rodando a API
Com o ambiente ativado, inicie o servidor da aplicação:
```bash
uvicorn src.main:app --reload
```
A API estará disponível em: `http://localhost:8000`. 
Você pode acessar a documentação interativa (Swagger) em: **`http://localhost:8000/docs`**

### 5. Rodando o Worker (Processador em 2º plano)
Abra um **novo terminal**, ative o ambiente virtual e inicie o consumidor do Kafka:
```bash
source venv/Scripts/activate
python worker.py
```

---

## 🧪 Como testar

### Pelo Swagger (Interface)
1. Acesse `http://localhost:8000/docs`.
2. Faça um `POST` na rota `/requests` passando um `customer_id` (string) e um `value` (float). Você receberá um ID e o status `PENDING`.
3. O terminal do Worker avisará que processou a mensagem e atualizou o status (Se `value <= 10000`: `APPROVED`, senão `MANUAL_REVIEW`).
4. Faça um `GET` na rota `/requests/{id}` usando o ID gerado. Ele retornará o status avaliado direto do Cache (Redis).

### Testes Automatizados (Pytest)
Para rodar os testes de domínio que validam a criação e regras das entidades, rode no terminal:
```bash
pytest
```