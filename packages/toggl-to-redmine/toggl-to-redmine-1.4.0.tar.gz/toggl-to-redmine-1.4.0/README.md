# Toggl to Redmine

Essa aplicação é um _fork_ do projeto "Automatic Toggl Import" feito pelo Rodrigo Marques. Seu intuito é oferecer uma versão em linha de comando para o lançamento automatizado de horas do Toggl para o Redmine.

## Instalação

Com o Python instalado, rode o seguinte comando no PowerShell: `pip install --upgrade toggl_to_redmine`.

Após a instalação feita pelo pip, é exibido um _warning_ sobre adicionar o caminho para o executável no _path_. Copie esse caminho, vá até as variáveis de ambiente de sua conta e adicione ao _path_ esse caminho. Basta pesquisar "variáveis de ambiente" no Windows para encontrar a configuração.

Abra uma nova instância do PowerShell e execute `toggl_to_redmine --help`. Se aparecer a mensagem de ajuda, a instalação foi bem sucedida.

## Como Usar

Basta rodar o comando `toggl_to_redmine` que as horas do dia atual registradas no Toggl serão importadas para o Redmine. Na primeira vez, o programa pede os dados de configuração para o usuário, que ficam armazenados em `"$HOME\.config\toggl-to-redmine.txt"`. É possível utilizar opções (`--since`, `--until`) para determinar o lançamento de horas de um intervalo de dias.

## Arquitetura

Todo o código fonte relacionado ao _import_ de horas foi desacoplado da plataforma na qual o usuário está interagindo. No projeto Toggl-to-redmine-core encontra-se toda a lógica da aplicação, enquanto que nesse repositório há a ferramenta CLI que interage com o usuário.

## TODO

* Adicionar _option_ para solicitar _reset_ de configuração?
