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


OBS2: Tambem deve-se instalar a biblioteca skimage, do scikit:

1. Instale as dependencias:

sudo apt-get install python-matplotlib python-numpy python-pil python-scipy

sudo apt-get install build-essential cython

2. Pelo pip, rode o comando:

sudo pip install -U scikit-image

3. Caso o comando acima de erro, apontando falha no pacote freetype:

sudo apt-get install libfreetype6-dev

4. Rode o comando, pelo Pip, novamente:

sudo pip install -U scikit-image

5. Caso houver problemas durante a instalação do scikit-kit referentes ao pacote Pillow, recomenda-se instalar as dependências do pacote Pillow:

sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev