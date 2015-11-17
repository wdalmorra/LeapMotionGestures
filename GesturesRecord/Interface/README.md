Antes de tudo eh necessario criar uma variavel de ambiente chamada 'LEAP_HOME' com o valor do path ate o SDK, por exemplo '/home/user/Leap/LeapSDK/'. (Nao esquecer de fechar o terminal e abrir de novo ou rodar 'source ~/.bashrc')

Depois disso, eh necessario iniciar o Leap Motion: em outro terminal rodar o comando 'sudo leapd'.
Por ultimo, inicializar o MongoDB: 'sudo service mongod start'.

Se tudo ocorrer como planejado, so rodar o main: 'python2 main.py'.



OBS: Para quem nao tem o MongoDB instalado e funcionando no Ubuntu 15.04:

1. Adicione o repositorio do debian:

echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

2. Update no apt-get e instala o MongoDB:

sudo apt-get update

sudo apt-get install -y mongodb-org

3. Por ultimo, instalar o PyMongo (tambem eh possivel instalar pelo pip):

sudo apt-get install python-pymongo