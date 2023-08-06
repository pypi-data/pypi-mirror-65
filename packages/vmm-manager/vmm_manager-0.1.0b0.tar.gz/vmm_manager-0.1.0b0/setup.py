# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vmm_manager',
 'vmm_manager.entidade',
 'vmm_manager.infra',
 'vmm_manager.parser',
 'vmm_manager.scvmm',
 'vmm_manager.util']

package_data = \
{'': ['*'], 'vmm_manager': ['includes/*', 'includes/ps_templates/*']}

install_requires = \
['configargparse>=1.1,<2.0',
 'jinja2>=2.11,<3.0',
 'paramiko>=2.7,<3.0',
 'pytz>=2019,<2020',
 'ruamel.yaml>=0.16,<0.17',
 'tqdm>=4.43,<5.0',
 'yamale>=2.0,<3.0',
 'yamlable>=1.0,<2.0']

entry_points = \
{'console_scripts': ['vmm_manager = vmm_manager.vmm_manager:main']}

setup_kwargs = {
    'name': 'vmm-manager',
    'version': '0.1.0b0',
    'description': 'Management of resources on System Center Virtual Machine Manager (SCVMM) in a declarative way.',
    'long_description': '# vmm-manager\n\nScript python que gerencia recursos no System Center Virtual Machine Manager (SCVMM), de forma declarativa, com base em um arquivo de configuração YAML.\n\n![License](https://img.shields.io/github/license/MP-ES/vmm_manager.svg)\n![Tests](https://github.com/MP-ES/vmm_manager/workflows/Tests/badge.svg)\n![Release](https://github.com/MP-ES/vmm_manager/workflows/Release/badge.svg)\n![Python](https://img.shields.io/pypi/pyversions/vmm-manager.svg)\n![PyPI](http://img.shields.io/pypi/v/vmm-manager.svg)\n\n## Pré-requisitos\n\nÉ necessário ter uma máquina Windows, que servirá como ponto de acesso ao SCVMM, com as seguintes ferramentas:\n\n- OpenSSH\n- Módulo PowerShell do SCVMM (**virtualmachinemanager**), geralmente instalado junto com o Console do Virtual Machine Manager (VMM)\n  \nNessa máquina, também é necessário executar o comando PowerShell `set-executionpolicy unrestricted`, com poderes administrativos.\n\n## Instalação\n\n```shell\npip install -U vmm-manager\n```\n\n## Uso\n\nPara consultar as funções e os parâmetros disponíveis, utilize o comando:\n\n```shell\nvmm_manager -h\n```\n\n### Exemplo de arquivo de inventário\n\n```yaml\nagrupamento: vmm_manager_test\nnuvem: "developer"\nimagem_padrao: "vm_linux"\nqtde_cpu_padrao: 1\nqtde_ram_mb_padrao: 512\nredes_padrao:\n  - nome: "vlan1"\nvms:\n  - nome: VMM_TEST1\n    descricao: "Test VM"\n    redes:\n      - nome: "vlan1"\n      - nome: "vlan2"\n    regiao: A\n  - nome: VMM_TEST2\n    regiao: B\n  - nome: VMM_TEST3\n```\n\n## Desenvolvimento\n\n### Instalação e configuração do python-poetry\n\nExecute os comandos a seguir:\n\n```shell\n# instalar o poetry\ncurl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\necho \'source $HOME/.poetry/env\' >>~/.bashrc\n\n# Configurar autocomplete\n# Bash\npoetry completions bash | sudo tee /etc/bash_completion.d/poetry.bash-completion\n```\n\n### Variáveis de ambiente\n\nDefina as variáveis de ambiente de acordo com as instruções do arquivo **.env.default**. Você pode criar um arquivo **.env** e executar o comando `export $(cat .env | xargs)` para defini-las antes da execução do script.\n\n### Como executar\n\n```shell\n# Carregando envs (opcional)\nexport $(cat .env | xargs)\n\n# Instalando dependências\npoetry install --no-root\n\n# Executando script\npoetry run python -m vmm_manager -h\n```\n\n### Comandos úteis para DEV\n\n```shell\n# Habilitar shell\npoetry shell\n\n# Incluir uma dependência\npoetry add <pacote> [--dev]\n\n# Executar lint\npylint tests/* vmm_manager/*\n\n# Executar testes\npython -m pytest -v\n```\n\n## Referências\n\n- [Virtual Machine Manager](https://docs.microsoft.com/en-us/powershell/module/virtualmachinemanager/?view=systemcenter-ps-2019)\n- [Python-Poetry](https://python-poetry.org/)\n',
    'author': 'Estevão Costa',
    'author_email': 'ecosta@mpes.mp.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MP-ES/vmm_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
