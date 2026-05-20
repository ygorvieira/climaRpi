# ClimaRpi 🌤️

Um script em Python extremamente leve e eficiente projetado para rodar em um **Raspberry Pi 3** equipado com **Alpine Linux**. Ele consome dados da API pública do **Open-Meteo** para exibir informações detalhadas sobre o clima atual, previsões diárias e alertas diretamente no terminal.

A escolha do Alpine Linux com Raspberry Pi 3 é perfeita para este projeto, pois o sistema operacional consome pouquíssima memória RAM e processamento, tornando-o ideal para rodar continuamente como um serviço ou tarefa agendada (Cron).

---

## 🚀 Funcionalidades

- **Condições Atuais:** Temperatura, sensação térmica, umidade, pressão atmosférica e velocidade do vento.
- **Previsão do Dia:** Temperaturas mínima e máxima, além do horário exato do nascer e pôr do sol.
- **Alertas Inteligentes:** Avisos automáticos de calor excessivo ($T \ge 35°C$), frio intenso ($T \le 10°C$), umidade muito alta ($\ge 90\%$) ou iminência de chuva.
- **Leveza Extrema:** Sem interface gráfica pesada, comunicação rápida via JSON e baixíssimo consumo de banda.

---

## 🛠️ Requisitos e Instalação no Alpine Linux

O Alpine Linux utiliza o gerenciador de pacotes `apk` e preza por minimalismo. Em vez de instalar o `pip` e compilar bibliotecas na placa ARM (o que pode demorar e consumir muita memória), instalamos a versão empacotada de forma nativa.

### 1. Atualizar os repositórios
Acesse o terminal do seu Raspberry Pi e atualize os índices de pacotes:
```bash
apk update
```

### 2. Instalar o Python 3 e a biblioteca Requests
Instale o interpretador Python e o pacote `py3-requests` diretamente dos repositórios do Alpine:
```bash
apk add python3 py3-requests
```

*(Opcional)* Se você preferir usar Git para gerenciar seu código no Pi:
```bash
apk add git
```

---

## ⚙️ Configuração e Execução

### 1. Clonar ou baixar o script
Certifique-se de que o arquivo `app.py` esteja no diretório de sua escolha no Raspberry Pi.

### 2. Dar permissão de execução ao script
Como o script possui a linha `#!/usr/bin/env python3` no topo, você pode torná-lo diretamente executável:
```bash
chmod +x app.py
```

### 3. Personalizar a localização (Opcional)
Por padrão, o script está configurado para a cidade do **Rio de Janeiro** (`LATITUDE = -22.90` e `LONGITUDE = -43.20`).
Para alterar para a sua região, abra o arquivo `app.py` com o editor de sua preferência (ex: `nano` ou `vi`) e edite as coordenadas nas linhas **7** e **8**:
```python
# Exemplo: São Paulo
LATITUDE = -23.55
LONGITUDE = -46.63
```

### 4. Executar manualmente
Basta executar o arquivo no terminal:
```bash
./app.py
```

---

## ⏱️ Automação (Agendamento com Cron)

Para exibir ou registrar o clima de forma automática a cada hora, você pode usar o `crond`, que já vem instalado e ativo por padrão no Alpine Linux.

### 1. Configurando o Cron
Abra a tabela de tarefas do cron para o usuário atual:
```bash
crontab -e
```

### 2. Adicionar a tarefa
Adicione uma linha ao final do arquivo para rodar o script de hora em hora (por exemplo, redirecionando a saída para um arquivo de log ou exibindo no console do sistema):
```cron
0 * * * * /home/ygorvieira/Projetos/climaRpi/app.py >> /home/ygorvieira/Projetos/climaRpi/clima.log 2>&1
```
> [!NOTE]
> Ajuste o caminho absoluto `/home/ygorvieira/Projetos/climaRpi/app.py` para o local exato onde seu script está armazenado no Raspberry Pi.

---

## ⚠️ Dica Crucial para Alpine OS: Modo Diskless (Run-from-RAM)

Muitas instalações do Alpine Linux em Raspberry Pi utilizam o modo **Diskless** (onde o sistema roda inteiramente na memória RAM para preservar a vida útil do cartão MicroSD contra corrupção de dados).

Se este for o seu caso, qualquer alteração feita no sistema (como a instalação dos pacotes `py3-requests`, novos scripts ou configurações do `crontab`) **será perdida ao reiniciar o Raspberry Pi** se você não salvar o estado.

Para salvar permanentemente suas alterações:
```bash
lbu commit -d
```
Este comando salva a nova configuração e os pacotes instalados no arquivo `.apkovl` no cartão SD, garantindo que o seu monitor de clima continue funcionando perfeitamente mesmo após quedas de energia ou reinicializações.

---

## 📊 Exemplo de Saída no Terminal

```text
==================================================
CLIMA - RIO DE JANEIRO
==================================================

Condição: Parcialmente nublado
Temperatura: 24.5°C
Sensação térmica: 25.1°C
Mínima: 19.8°C
Máxima: 28.2°C

Umidade: 72%
Pressão: 1014.2 hPa

Vento: 12.5 km/h

Nascer do sol: 06:15
Pôr do sol: 17:32

==================================================
```

---
*Desenvolvido com carinho para rodar em hardware de baixo custo e alta eficiência!* 🐧⚡
