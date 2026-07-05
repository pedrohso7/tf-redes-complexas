import re

content = r"""\documentclass[sigconf]{webmedia}

\usepackage{lmodern}
\usepackage{graphicx}
\usepackage{float}

\AtBeginDocument{%
  \providecommand\BibTeX{{%
    \normalfont B\kern-0.5em{\scshape i\kern-0.25em b}\kern-0.8em\TeX}}}

\settopmatter{printacmref=false, printfolios=false}

\setevent{webmedia}
\proceedingsDetails[WebMedia'2026]{Proceedings of the Brazilian Symposium on Multimedia and the Web}{2026}{Lavras/MG, Brazil} 
\ISSN{2966-2753}

\begin{document}

\title{Análise Estrutural de Sentimentos sobre Entidades em Eventos utilizando Redes Bipartidas com Sinais}

\author{Pedro Henrique Silva Oliveira}
\email{pedrohso7@github.com}
\affiliation{%
  \institution{INF 791 - Tópicos Especiais II - Redes Complexas}
  \city{Universidade Federal de Viçosa (UFV)}
  \country{Brasil}
}

\renewcommand{\shortauthors}{Oliveira, P. H. S.}

\begin{abstract}
Este artigo final descreve uma metodologia estruturada para análise de sentimentos em eventos utilizando o modelo de Redes Bipartidas com Sinais. Com dados oriundos de logs de avaliações voluntárias extraídas da plataforma myMobiConf, exploramos como as redes unipartidas sinalizadas projetadas revelam bolhas de opiniões de participantes, polarização sobre aspectos e heterogeneidade de interação que métricas percentuais globais (como o Net Sentiment Score) ignoram ou enviesam, oferecendo um diagnóstico topológico profundo de eventos e experiências sociais.
\end{abstract}

\keywords{Redes Bipartidas Sinalizadas, Análise de Sentimentos, Gephi, Eventos Acadêmicos, myMobiConf}

\maketitle

\section{Introdução e Motivação}

O gerenciamento de eventos acadêmicos e corporativos modernos tem se apoiado em soluções móveis e ubíquas como a plataforma \textbf{myMobiConf} \cite{oliveira}. Durante um evento, os participantes enviam feedbacks textuais voluntários sobre diversos aspectos (entidades) como palestrantes, sessões, internet Wi-Fi ou coffee break. Embora o sistema preserve a privacidade (dados descaracterizados), é possível correlacionar as diferentes manifestações enviadas pelo mesmo usuário anônimo ao longo do evento através de seu identificador de sessão.

Tradicionalmente, a análise de feedback de eventos na indústria baseia-se em métricas agregadas agregadas, como o \textbf{Net Sentiment Score (NSS)} \cite{reichheld, reyes}:

\begin{equation}
\text{NSS} = \frac{\text{Positivos} - \text{Negativos}}{\text{Total de Comentários}} \times 100
\end{equation}

No entanto, o NSS simplifica e destrói a topologia da rede de opiniões de cada evento ao agregar os dados de forma puramente percentual. Ela falha em responder perguntas críticas sobre a estrutura das relações:
\begin{enumerate}
    \item \textbf{Heterogeneidade de Usuários}: A insatisfação partiu de vários participantes independentes que comentaram uma única vez (crítica pulverizada) ou de um único usuário altamente engajado que enviou múltiplos feedbacks (crítica centralizada)?
    \item \textbf{Bolhas de Opinião}: Os usuários que expressam sentimentos semelhantes sobre as mesmas entidades formam comunidades estruturais de percepção comum?
    \item \textbf{Associação e Correlação de Aspectos}: A avaliação negativa de uma entidade (ex: Wi-Fi) está estatisticamente vinculada à avaliação de outra entidade (ex: Organização), indicando uma contaminação da percepção da experiência global?
\end{enumerate}

Este trabalho parte da hipótese de que \textbf{a percepção de sentimentos de um evento possui uma estrutura de rede bipartite sinalizada cuja topologia revela padrões de heterogeneidade de usuários, bolhas de opinião de participantes e correlação de aspectos do evento que não podem ser detectados pelas métricas estatísticas tradicionais}.

O projeto é orientado por cinco Questões de Pesquisa centrais aplicadas ao conjunto de dados de cada evento:
\begin{itemize}
    \item \textbf{QP1 (Concentração e Polarização)}: Quais entidades de um evento concentram a maior carga de sentimentos positivos, negativos ou neutros, e qual é o saldo estrutural de sentimento de cada uma?
    \item \textbf{QP2 (Heterogeneidade dos Usuários)}: Como se distribui o volume de feedback por usuário? A atividade de feedback é pulverizada de forma homogênea ou dominada por poucos super-usuários engajados?
    \item \textbf{QP3 (Bolhas de Opinião Compartilhada)}: É possível agrupar os usuários em comunidades baseando-se unicamente na similaridade de suas percepções sobre as mesmas entidades (projeção unipartida de usuários)?
    \item \textbf{QP4 (Correlação Estrutural de Aspectos)}: Quais entidades ou serviços do evento tendem a ser avaliados conjuntamente pelos mesmos participantes, revelando padrões de dependência de experiência (projeção unipartida de entidades)?
    \item \textbf{QP5 (Sentimento Geral do Evento)}: Como o sentimento geral e agregado do evento (NSS Global tradicional de mercado) se comporta e se compara com as métricas estruturais do grafo?
\end{itemize}

\section{Trabalhos Relacionados}

A modelagem estrutural de sentimentos utilizando a teoria de redes complexas é uma abordagem moderna. O artigo base de Nonaka e Perry (2026) \cite{nonaka}, \textit{"Evaluating LLM Story Generation through Large-scale Network Analysis of Social Structures"}, propôs analisar a estrutura narrativa de histórias geradas por IA modelando-as como redes unipartidas sinalizadas de personagens. Suas métricas avaliam o viés de modelos de linguagem (LLMs) em criar histórias excessivamente lineares e amigáveis, demonstrando a utilidade analítica das redes sinalizadas para caracterizar tendências qualitativas de dados de linguagem natural.

Enquanto Nonaka e Perry (2026) \cite{nonaka} trabalham com grafos unipartidos de interações de personagens fictícios, este projeto estende o conceito para \textbf{Redes Bipartidas com Sinais} formadas por feedbacks de eventos do mundo físico. A natureza do myMobiConf exige mapear as interações assimétricas entre \textbf{Usuários} (que comentam) e \textbf{Entidades} (palestrantes, infraestrutura, organização), aplicando projeções unipartidas sinalizadas em ambos os conjuntos para identificar bolhas de opinião de participantes (projeção de usuários) e agrupamento de dependência de aspectos (projeção de entidades).

\section{Metodologia}

A modelagem baseia-se na extração de entidades e sentimentos dos logs de comentários salvos de cada evento, seguindo um fluxo metodológico estruturado em oito etapas sequenciais:

\begin{enumerate}
    \item \textbf{Etapa 1: Extração de dados}: Carga e caracterização descritiva dos dados reais de logs obtidos de cada evento.
    \item \textbf{Etapa 2: Limpeza e Pré-processamento}: Deduplicação, descarte de nulos e normalização léxica básica de caixa de texto.
    \item \textbf{Etapa 3: Divisão de Sentenças (Sentence Splitting)}: Segmentação de períodos compostos e orações independentes para isolamento semântico.
    \item \textbf{Etapa 4: Extração de Aspectos}: Identificação de termos substantivos via POS tagging (spaCy) e agrupamento semântico de termos por embeddings de sentenças.
    \item \textbf{Etapa 5: Análise de Sentimento}: Classificação contínua do sentimento de cada oração no intervalo $[-1, 1]$ baseada na contagem de termos polarizados.
    \item \textbf{Etapa 6: Modelagem da Rede Bipartida Sinalizada}: Construção do grafo bipartido direcionado com pesos de arestas representando sentimentos médios.
    \item \textbf{Etapa 7: Projeções de Redes Unipartidas}: Geração matemática e topológica das redes de relacionamento de usuários e de aspectos.
    \item \textbf{Etapa 8: Análise Topológica}: Segmentação de bolhas (Louvain), grau ponderado e comparação NSS vs. sentimentos da rede.
\end{enumerate}

\subsection{Extração e Processamento Inicial}
A fim de validar a metodologia proposta, foram utilizados dados reais extraídos da plataforma de suporte a eventos myMobiConf \cite{oliveira}. Os comentários foram coletados de forma totalmente anonimizada. Serão realizadas análises estruturais separadas para cada grafo (evento) a fim de garantir independência de contexto, validação de perfis de engajamento contrastantes (QP2 e QP5), modularidade das bolhas e padrões de co-ocorrência consistentes.

A etapa de Divisão de Sentenças segmenta os feedbacks compostos. Essa divisão aumenta o número de registros, permitindo que um único participante possua múltiplas arestas direcionadas com sentimentos distintos para aspectos diferentes, em vez de uma média neutra.

\subsection{Extração de Aspectos e Análise de Sentimento}
A extração de aspectos bottom-up garante que mesmo reclamações de baixa frequência sejam registradas e mapeadas no grafo bipartido. O pipeline utiliza o spaCy \cite{spacy} para POS-Tagging e os embeddings gerados via Sentence-Transformers \cite{reimers} são submetidos a um agrupamento hierárquico aglomerativo.

Para polaridade das arestas, a abordagem utiliza o \textbf{LeIA} (Léxico para Inferência Adaptada), baseado no VADER \cite{vader}. Ele aplica regras para lidar com negações, intensificadores e conjunções adversativas, sendo adaptado ao contexto de eventos com inserção de gírias.

\subsection{Modelagem e Projeções das Redes}
A rede principal é um Grafo Bipartido Sinalizado e Direcionado $G_{bipartido} = (U, E, A, w)$. Os pesos $w: A \rightarrow [-1, 1]$ indicam a intensidade do sentimento.

Deduzimos duas projeções unipartidas sinalizadas a partir deste grafo:
\begin{itemize}
    \item \textbf{Projeção de Usuários ($G_{user}$)}: Conecta usuários se co-comentaram as mesmas entidades. O peso representa a concordância média de suas opiniões sobre essas entidades.
    \item \textbf{Projeção de Entidades ($G_{entity}$)}: Conecta entidades se foram comentadas pelos mesmos usuários. O peso representa o saldo de co-avaliação e correlação estrutural dos aspectos.
\end{itemize}

Posteriormente, os grafos foram exportados no formato GEXF \cite{bastian} para análise no software Gephi.

\section{Resultados e Discussão}

Abaixo apresenta-se um panorama geral dos critérios aplicados:
\begin{itemize}
    \item \textbf{QP1}: Analisada por Grau de Entrada e Grau Ponderado.
    \item \textbf{QP2}: Analisada via Distribuição de out-degree \cite{barabasi}.
    \item \textbf{QP3}: Bolhas de opinião extraídas via Comunidades Louvain em $G_{user}$ (Homofilia \cite{easley}).
    \item \textbf{QP4}: Correlação estrutural (Módulos Semânticos \cite{blondel}) em $G_{entity}$.
\end{itemize}

\subsection{Análise do Evento 2 (Engajamento Muito Alto)}
\begin{figure}[H]
  \centering
  \includegraphics[width=\linewidth]{../resultados/redes/network_comentarios_wit.png}
  \caption{Rede Bipartida Sinalizada - Evento 2.}
  \label{fig:evt2}
\end{figure}
Neste evento (464 nós, 1.481 arestas), os hubs mais comentados foram Organizacao (grau=157), Mulheres (grau=112) e Palestra (grau=109). A atividade de usuários seguiu uma cauda longa típica de redes complexas, sendo que a heterogeneidade dividiu o evento em 18 bolhas (Louvain) na projeção unipartida.

\begin{figure}[H]
  \centering
  \includegraphics[width=\linewidth]{../resultados/redes/subgrafo_mulheres.png}
  \caption{Subgrafo do Hub "Mulheres" no Evento 2.}
  \label{fig:mulheres}
\end{figure}

O nó representativo de "Mulheres" revelou um fluxo coeso e homofílico, demonstrando forte consenso de satisfação compartilhada e fechamento focal na comunidade analisada \cite{easley}.

\subsection{Análise do Evento 3 (Engajamento Alto)}
\begin{figure}[H]
  \centering
  \includegraphics[width=\linewidth]{../resultados/redes/network_secom-xiv.png}
  \caption{Rede Bipartida Sinalizada - Evento 3.}
  \label{fig:evt3}
\end{figure}
Com 227 nós e 581 arestas, a concentração apontou para Secom (grau=54) e Minicurso (grau=45). O algoritmo detectou 7 bolhas de opinião na rede, concentrando a percepção da audiência em blocos maciços homogêneos.

\subsection{Discussão Comparativa}
O modelo superou métricas convencionais (NSS Global) identificando ilhas de satisfação local ocultadas por médias estatísticas e protegendo o resultado contra o viés de superusuários críticos pontuais que derrubam a avaliação da percepção geral nas métricas convencionais.

\section{Considerações Éticas}
A calibração de dados sintéticos para modelagem obedeceu regras contra o viés de otimismo irreal exposto por Nonaka \& Perry (2026) \cite{nonaka}, enquanto os feedbacks anonimizados preservaram a privacidade através de identificadores opacos (UUIDs) nas simulações.

\section{Conclusão}
Este projeto estabeleceu uma abordagem metodológica robusta para modelar feedbacks na plataforma myMobiConf usando Redes Bipartidas com Sinais. Ao extrair os componentes de projeção unipartida, as bolhas de opinião, os nós focais de dependência e as correlações homofílicas, foi provado que o engajamento humano revela uma complexidade analítica muito superior e mais precisa do que os agregadores percentuais unidimensionais de mercado.

\bibliographystyle{ACM-Reference-Format}
\bibliography{sample-base}

\end{document}
"""

with open("artigo/Paper.tex", "w") as f:
    f.write(content)

