# LeapMotionGestures - UFPel
#### Thainan Remboski, William Dalmorra, Marilton de Aguiar

Códigos desenvolvidos na intenção de desenvolver um algoritmo para reconhecimento de gestos estáticos utilizando como interface o Leap Motion. Até o momento possui um programa principal chamado GestureRecognition, capaz de identificar em tempo real os gestos previamente ensinados para o algoritmo. Para geração de um novo gesto existe o programa GestureRecord, que imprime diversas informações úteis sobre o posicionamento da mão durante o gesto. A saída desse programa necessita ser tratada antes de ser utilizada como entrada para o GestureRecognition. Além disso, foi desenvolvido um outro programa chamado gesture_classification onde divide um conjunto de amostras entre amostras de trainamento e amostras de teste para o algoritmo SVM de classificação.

Próximos passos:
 - Encontrar quais features são mais importantes para classificação dos gestos pela SVM.
 - Definir uma extensão padrão para gestos estático no Leap Motion a partir das features definidas acima.

Este trabalho faz parte do projeto LIKI, que é um trabalho em parceria entre a UFPel e o IFSul - Campus Pelotas.

Contato:
	Thainan Remboski - tbremboski@inf.ufpel.edu.br
	William Dalmorra - wddsouza@inf.ufpel.edu.br
	Marilton de Aguiar - marilton@inf.ufpel.edu.br
