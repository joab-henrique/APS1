# APS - Testes Automatizados

Testes pro Scholarship Eligibility Evaluator (`codigo_original.py`), feitos com pytest, mais análise de mutação com mutmut. O código original não foi mexido, só os testes.

## setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest "mutmut==2.4.4"
```

(tem que fixar a versão 2.4.4 do mutmut, a 3.x que o pip instala por padrão usa outro esquema de configuração e não funciona com o `setup.cfg` daqui)

## rodar os testes

```bash
pytest -v
```

## rodar a análise de mutação

```bash
mutmut run
mutmut results     # lista quem sobreviveu
mutmut show <id>   # mostra o diff de um mutante
mutmut html        # gera relatório em ./html
```

Os relatórios já gerados estão em `mutation-reports/initial` e `mutation-reports/final` — é só abrir o `index.html` de cada um.

## arquivos

- `codigo_original.py` - sistema-base, sem alteração
- `conftest.py` - vazio, só pra o pytest achar o `codigo_original.py` na raiz
- `tests/test_scholarship.py` - os testes
- `setup.cfg` - config do mutmut
- `RELATORIO.md` - o relatório da atividade
