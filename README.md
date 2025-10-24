<h1 align="center">Calcular Comprimento das Vias - Avançado (Plugin QGIS)</h1>

<p align="center">
  <img src="icons/icon.png" alt="Ícone do plugin" width="96" height="96"><br>
  <em>Plugin QGIS para cálculo de comprimento total e por categoria de vias lineares</em>
</p>

<hr>

<h2>Descrição</h2>

<p>
O <strong>Calcular Comprimento das Vias - Avançado</strong> é um plugin desenvolvido para o QGIS com o objetivo de calcular o comprimento total de feições lineares, como ruas, rodovias e trilhas. 
O plugin também permite realizar o cálculo agrupado por categoria do campo <code>highway</code>, adicionar um campo contendo o comprimento individual de cada feição e exportar os resultados em diferentes formatos.
</p>

<hr>

<h2>Funcionalidades</h2>

<ul>
  <li>Seleção de camadas vetoriais com geometria do tipo linha.</li>
  <li>Cálculo do comprimento total geral em quilômetros.</li>
  <li>Cálculo do comprimento total agrupado por categoria <code>highway</code>.</li>
  <li>Criação automática do campo <code>comp_km</code> contendo o comprimento de cada feição.</li>
  <li>Exportação da camada resultante para Shapefile reprojetado (<code>EPSG:31982</code>).</li>
  <li>Exportação dos resultados em formato CSV com total por categoria.</li>
</ul>

<hr>

<h2>Estrutura do Projeto</h2>

<pre>
calcular_comprimento_vias_avancado/
│
├── __init__.py
├── plugin.py
├── interface.py
├── icons/
│   └── icon.png
├── README.md
└── .gitignore
</pre>

<hr>

<h2>Instalação</h2>

<ol>
  <li>Clone ou baixe este repositório no diretório de plugins do QGIS:</li>
  <pre><code>git clone https://github.com/felipe-bertram-ribeiro/Calcular-comprimento-vias.git</code></pre>

  <li>Abra o QGIS.</li>
  <li>No menu, acesse <strong>Complementos → Gerenciar e Instalar Complementos → Instalar a partir de um diretório</strong>.</li>
  <li>Selecione a pasta do plugin e conclua a instalação.</li>
  <li>Ative o plugin na lista de complementos instalados.</li>
</ol>

<hr>

<h2>Modo de Uso</h2>

<ol>
  <li>Carregue no QGIS uma camada vetorial contendo feições lineares.</li>
  <li>Abra o plugin através do menu <strong>Calcular Comprimento das Vias - Avançado</strong>.</li>
  <li>Selecione a camada desejada na interface do plugin.</li>
  <li>Escolha uma das opções disponíveis:
    <ul>
      <li><strong>Calcular Total Geral</strong>: calcula o comprimento total de todas as feições.</li>
      <li><strong>Calcular por Categoria</strong>: realiza o cálculo agrupado por valores do campo <code>highway</code>.</li>
    </ul>
  </li>
  <li>Visualize os resultados na área de texto exibida na janela do plugin.</li>
  <li>Se desejar, utilize as opções para salvar o resultado em Shapefile ou exportar o relatório em CSV.</li>
</ol>

<hr>

<h2>Saídas Geradas</h2>

<ul>
  <li><strong>Campo adicional na camada:</strong> <code>comp_km</code> – comprimento individual de cada feição em quilômetros.</li>
  <li><strong>Arquivo CSV:</strong> tabela contendo as colunas <code>categoria</code> e <code>comprimento_km</code>.</li>
  <li><strong>Shapefile reprojetado:</strong> camada salva no sistema de referência <code>EPSG:31982</code>.</li>
</ul>

<hr>

<h2>Sistema de Coordenadas</h2>

<p>
Os cálculos de comprimento são realizados no sistema de coordenadas <strong>EPSG:31982</strong> (SIRGAS 2000 / UTM Zone 22S). 
Caso a camada original esteja em outro sistema de referência, o plugin realiza automaticamente a transformação de coordenadas para garantir precisão métrica.
</p>

<hr>

<h2>Informações Técnicas</h2>

<ul>
  <li><strong>Nome do Plugin:</strong> Calcular Comprimento das Vias - Avançado</li>
  <li><strong>Versão:</strong> 1.0.0</li>
  <li><strong>Compatibilidade:</strong> QGIS 3.x ou superior</li>
  <li><strong>Campo criado:</strong> <code>comp_km</code></li>
  <li><strong>CRS utilizado:</strong> EPSG:31982</li>
</ul>

<hr>

<h2>Autor e Contato</h2>

<ul>
  <li><strong>Autor:</strong> Felipe Bertram</li>
  <li><strong>E-mail:</strong> felipebertram3014@gmail.com</li>
</ul>

<hr>

<h2>Licença</h2>

<p>
Este projeto é distribuído sob a licença <strong>MIT</strong>. 
É permitida a utilização, modificação e redistribuição do código, desde que seja mantido o devido crédito ao autor original.
</p>
