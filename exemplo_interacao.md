# Exemplos de Interação com o Agente

## Cenário 1: Consulta de Catálogo, Estoque, Promoções e Regras de Pagamento

```text
C:\Users\Cico\Documents\Desafio Técnico AI Engineer 2026>python main.py
=== Atendimento Empório da Música (Digite 'sair' para encerrar) ===

Você: Oi tudo bem? Quais opções de violões disponíveis vocês têm custando até R$ 1000?

Hugo (Empório da Música): Opa, tudo ótimo por aqui! E com você? Deixa eu dar uma olhadinha aqui no sistema quais violões a gente tem nessa faixa de até R$ 1000 pra você!

-> [Sistema] Executando: get_produtos('5')
-> [Sistema] Executando: get_promocoes('todas')

Hugo (Empório da Música): Olha só, separei as opções que temos aqui por menos de R$ 1000, divididas pelo tipo de corda pra facilitar sua escolha:

**Violões de Nylon (Clássicos):**
- Tagima Memphis AC-39: R$ 429,90
- Rozini RC-104: R$ 459,90
- Yamaha C40: R$ 599,90
- Giannini GN-15: R$ 689,00
- Yamaha C70: R$ 849,00

**Violões de Aço (Folk/Dreadnought):**
- Shelby SN-100: R$ 549,00
- Giannini GF-1R: R$ 579,90
- Yamaha F310: R$ 699,90
- Tagima Dallas Tuner: R$ 749,00
- Tagima Woodstock: R$ 899,00

**7 Cordas:**
- Tagima TW-7 (Aço): R$ 999,00

Eu até vi um Giannini GF-3D que seria uma ótima opção, mas ele está sem estoque no momento. Esses que te passei acima estão todos disponíveis! Algum deles te chamou mais a atenção?

Você: Meu jogador, pesquisei no google e vi o Takamine GD20, quanto tá custando? Tem algum desconto se eu pagar no PIX?

Hugo (Empório da Música): Opa, o Takamine GD20 é uma máquina! Deixa eu ver aqui o preço dele e já aproveito pra conferir como funciona nosso desconto no PIX pra você!

-> [Sistema] Executando: get_promocoes('Takamine GD20')
-> [Sistema] Executando: get_politicas('pagamento')

Hugo (Empório da Música): [02/11/2026 12:42:55] Hugo: Conferi aqui! O Takamine GD20 Dreadnought Natural está saindo por R$ 2.199,00. Eu vi que tinha uma promoção de 12% de desconto (aquela "Oferta Especial"), mas ela já expirou, então o preço agora é o valor normal de tabela.

Mas ó, tem o desconto do PIX sim! Pagando à vista no PIX, você tem 5% de desconto, então ele sai por R$ 2.089,05. Temos 5 unidades dele em estoque.

E aí, o que achou? Quer aproveitar e garantir o seu?
```

---

## Cenário 2: Promoção Expirada, Produto sem Estoque e Consulta de Promoções Ativas

```text
C:\Users\Cico\Documents\Desafio Técnico AI Engineer 2026>python main.py
=== Atendimento Empório da Música (Digite 'sair' para encerrar) ===

Você: Opa! Vi que o violão Giannini GF-3D Sunburst tava com 40% de desconto na Semana do Músico. Quero levar ele!

Hugo (Empório da Música): Show de bola! Esse violão é sensacional mesmo. Deixa eu conferir aqui agora se ainda temos ele em estoque com esse desconto da Semana do Músico pra você!

 -> [Sistema] Executando: get_promocoes('Giannini GF-3D Sunburst')
 -> [Sistema] Executando: get_produtos('5')

Hugo (Empório da Música): Poxa, tenho uma notícia não muito boa. Essa promoção de 40% da Semana do Músico já expirou e, pra completar, o Giannini GF-3D acabou saindo todo do nosso estoque.

Mas não desanima, não! Tenho outras opções bem bacanas por aqui que você pode curtir. Se você gosta desse estilo, tenho o Giannini GF-1R Aço Folk Sunburst por R$ 579,90 ou o Tagima Woodstock Dreadnought Natural por R$ 899,00. Quer que eu te mande mais detalhes de algum deles?

Você: Poxa meu grão duque... Me fala ai pelo menos quais são as promoções que tão funcionando ainda

Hugo (Empório da Música): Poxa, eu sei, é uma pena! Mas relaxa, deixa eu dar uma olhada aqui no sistema o que ainda tá rolando de promoção pra você aproveitar!

 -> [Sistema] Executando: get_promocoes('todas')

Hugo (Empório da Música): Olha, não são tantas quanto a Semana do Músico, mas ainda tem coisa boa rolando! Se liga nessas que estão com desconto agora:

- **Kalani KAL-700T Tenor Natural**: de R$ 359,00 por R$ 323,10 (10% de desconto)
- **Ohana CK-20 Concert Natural**: de R$ 549,00 por R$ 439,20 (20% de desconto)
- **Crafter HT-100 Folk Aço Natural**: de R$ 2.399,00 por R$ 1.967,18 (18% de desconto)
- **Taylor 110e Dreadnought Natural**: de R$ 5.999,00 por R$ 5.519,08 (8% de desconto)

Algum desses chamou sua atenção ou quer que eu procure algo mais específico?
```

---

## Cenário 3: Consulta de Status de Pedido e Política de Devolução/Frete

```text
C:\Users\Cico\Documents\Desafio Técnico AI Engineer 2026>python main.py
=== Atendimento Empório da Música (Digite 'sair' para encerrar) ===

Você: Salve meu comensal, minha esposa fez um pedido no nome da Letícia Gonçalves Rocha, queria saber se já chegou e qual o status.

Hugo (Empório da Música): Salve! Tudo certo por aqui. Deixa eu dar uma olhadinha no sistema agora mesmo pra ver o status desse pedido da Letícia pra você!

 -> [Sistema] Executando: get_pedidos('Letícia Gonçalves Rocha')

Hugo (Empório da Música): Consegui conferir aqui! O pedido da Letícia, referente ao Shelby SU-21S Soprano Sunburst, já consta como entregue no sistema. Dá uma conferida aí se já chegou certinho para vocês!

Você: Conferi aqui, tva na caixa do correio, mas me arrependi da minha compra, posso devolver meu pedido? Quem paga o frete?

Hugo (Empório da Música): Poxa, entendi. Sem problemas! Deixa eu conferir aqui rapidinho como funciona nossa política de devolução e quem arca com o frete nesse caso, só um minutinho.

 -> [Sistema] Executando: get_politicas('trocas')
 -> [Sistema] Executando: get_politicas('frete')

Hugo (Empório da Música): Pode sim, sem problemas! Como a compra foi online, você tem o direito de arrependimento e pode solicitar a devolução em até 7 dias corridos após o recebimento, sem precisar de uma justificativa. 

Só tem um detalhe importante: o instrumento precisa estar na embalagem original, sem nenhum sinal de uso e com todos os manuais e acessórios que acompanham ele, beleza? 

E pode ficar tranquilo quanto ao frete: nesse caso de arrependimento, o custo da devolução é por nossa conta! Assim que o processo for feito, o reembolso é realizada na mesma forma de pagamento que você usou, em até 10 dias úteis. Se quiser seguir com isso, é só me avisar!
```

---

## Cenário 4: Consulta de Frete para Campo Grande (Região Metropolitana)

```text
C:\Users\Cico\Documents\Desafio Técnico AI Engineer 2026>python main.py
=== Atendimento Empório da Música (Digite 'sair' para encerrar) ===

Você: Meu Almirante, eu moro aqui em Campo Grande mesmo, se eu comprar um ukulele de 350 reais quanto fica o frete e em quanto tempo chega?

Hugo (Empório da Música): Opa, tudo certo! Como você é aqui de Campo Grande, deve ser rapidinho. Deixa eu conferir aqui as nossas políticas de frete e entrega pra te passar o valor certinho, beleza?

 -> [Sistema] Executando: get_politicas('frete')

Hugo (Empório da Música): Vi aqui que, como você é de Campo Grande, a gente faz a entrega por motoboy próprio. Como o valor do ukulele é abaixo de R$ 500,00, a taxa de frete fica fixa em R$ 35,00.

Sobre o prazo, é bem rapidinho: chega para você em 1 a 3 dias úteis! Quer aproveitar e já garantir o seu?
```

---

## Cenário 5: Pergunta sobre Acessórios (Fora do Escopo) e Pergunta Fora do Contexto da Loja

```text
C:\Users\Cico\Documents\Desafio Técnico AI Engineer 2026>python main.py
=== Atendimento Empório da Música (Digite 'sair' para encerrar) ===

Você: Vocês têm encordoamento de aço Elixir, palhetas e cabo P10 pra vender?

Hugo (Empório da Música): Opa! Deixa eu conferir aqui se temos esses encordoamentos, palhetas e cabos no nosso estoque pra você!

 -> [Sistema] Executando: get_politicas('sobre')
 -> [Sistema] Executando: get_promocoes('Elixir')

Hugo (Empório da Música): Olhei aqui no sistema e, cara, infelizmente a gente não trabalha com esses itens. A Empório da Música é focada exclusivamente em instrumentos musicais, então não comercializamos acessórios como encordoamentos, palhetas ou cabos. Sinto muito não conseguir te ajudar com isso agora!

Você: Ah meu comendador entendi, mas e uma receita de bolo de cenoura firme vc consegue me mandar agr?

Hugo (Empório da Música): Kkkkkk, aí você me pegou! Eu entendo de nota musical, mas de culinária eu tô mais pra desafinado. Se fosse um solo de guitarra eu te mandava, mas bolo de cenoura eu não sei fazer não! 😂 Mas se precisar de algum instrumento pra acompanhar o lanche, é só falar!
```