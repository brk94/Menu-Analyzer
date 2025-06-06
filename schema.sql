-- Arquivo de esquema do banco de dados para o aplicativo de restaurante.
-- Contém todas as definições de tabela, garantindo a criação apenas se não existirem.

CREATE TABLE IF NOT EXISTS alergenicos (
    id_alergenico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS almoços (
    id_almoços INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255),
    preco FLOAT,
    descricao TEXT,
    detalhes TEXT,
    alergenicos TEXT,
    ingredientes TEXT,
    ingredientes_removiveis TEXT,
    ingredientes_adicionaveis TEXT
);

CREATE TABLE IF NOT EXISTS bebidas (
    id_bebidas INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255),
    preco FLOAT,
    descricao TEXT,
    detalhes TEXT,
    alergenicos TEXT
);

CREATE TABLE IF NOT EXISTS carrinho (
    id_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
    id_item INTEGER,
    tipo_item VARCHAR(20),
    nome_item VARCHAR(255),
    preco_unitario FLOAT,
    quantidade INTEGER,
    ingredientes_removidos TEXT,
    ingredientes_adicionados TEXT
);

CREATE TABLE IF NOT EXISTS doces (
    id_doces INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255),
    preco FLOAT,
    descricao TEXT,
    detalhes TEXT,
    alergenicos TEXT,
    ingredientes TEXT,
    ingredientes_removiveis TEXT,
    ingredientes_adicionaveis TEXT
);

CREATE TABLE IF NOT EXISTS entradas (
    id_entradas INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255),
    preco FLOAT,
    descricao TEXT,
    detalhes TEXT,
    alergenicos TEXT,
    ingredientes TEXT,
    ingredientes_removiveis TEXT,
    ingredientes_adicionaveis TEXT
);

CREATE TABLE IF NOT EXISTS usuarios (
	id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
	nome TEXT UNIQUE,
	email TEXT
);

CREATE TABLE IF NOT EXISTS feedback (
    id_feedback INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100),
    email VARCHAR(100),
    feedback TEXT,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
	id_item	INTEGER PRIMARY KEY AUTOINCREMENT,
	id_pedido INTEGER,
	nome_prato VARCHAR(100),
	categoria VARCHAR(50),
	ingredientes_adicionados TEXT,
	ingredientes_removidos TEXT,
	quantidade INTEGER
);

CREATE TABLE IF NOT EXISTS lanches (
    id_lanches INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255),
    preco FLOAT,
    descricao TEXT,
    detalhes TEXT,
    alergenicos TEXT,
    ingredientes TEXT,
    ingredientes_removiveis TEXT,
    ingredientes_adicionaveis TEXT
);

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    preco_total DECIMAL(10, 2),
    data_hora_compra DATETIME DEFAULT (datetime('now', '-3 hours'))
);

CREATE TABLE IF NOT EXISTS usuarios_alergenicos (
	id_usuario INTEGER,
	id_alergenico INTEGER,
	PRIMARY KEY(id_usuario, id_alergenico),
	FOREIGN KEY(id_alergenico) REFERENCES alergenicos(id_alergenico),
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS veganos (
    id_veganos INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255),
    preco FLOAT,
    descricao TEXT,
    detalhes TEXT,
    alergenicos TEXT,
    ingredientes TEXT,
    ingredientes_removiveis TEXT,
    ingredientes_adicionaveis TEXT
);

-- Inserção de dados na tabela 'alergenicos'

INSERT INTO alergenicos (nome) VALUES
('Glúten'),
('Lactose'),
('Camarão'),
('Amendoim'),
('Ovos'),
('Soja'),
('Peixe'),
('Frutos do mar'),
('Nozes'),
('Castanhas'),
('Trigo'),
('Leite'),
('Crustáceos'),
('Moluscos'),
('Aipo'),
('Mostarda'),
('Gergelim'),
('Sulfitos'),
('Tremoço'),
('Corantes artificiais'),
('Amêndoas'),
('Castanha-do-pará'),
('Castanha de caju'),
('Pistache'),
('Macadâmia'),
('Noz-pecã'),
('Noz-moscada'),
('Avelã'),
('Pinhão'),
('Salmão'),
('Atum'),
('Bacalhau'),
('Tilápia'),
('Lula'),
('Polvo'),
('Mexilhão'),
('Caranguejo'),
('Lagosta'),
('Caseína'),
('Soro de leite'),
('Manteiga'),
('Queijo'),
('Iogurte'),
('Clara de ovo'),
('Gema de ovo'),
('Albumina'),
('Lecitina de soja'),
('Proteína isolada de soja'),
('Óleo de soja'),
('Benzoato de sódio'),
('Glutamato monossódico (MSG)'),
('Ácido sórbico'),
('Nitrato de sódio'),
('Tartrazina (E102)'),
('BHA (butil-hidroxi-anisol)'),
('BHT (butil-hidroxitolueno)'),
('Centeio'),
('Cevada'),
('Aveia'),
('Kiwi'),
('Morango'),
('Banana'),
('Maçã'),
('Abacaxi'),
('Pêssego'),
('Chocolate'),
('Mel'),
('Carnes vermelhas'),
('Cafeína'),
('Aspartame'),
('Gelatina'),
('Fermento biológico'),
('Vinagre'),
('Álcool etílico'),
('Alho'),
('Cebola');

-- ========= Inserção de dados: almoços =========
INSERT INTO almoços (id_almoços, nome, preco, descricao, detalhes, alergenicos, ingredientes, ingredientes_removiveis, ingredientes_adicionaveis) VALUES
(1, 'Feijoada Completa', 55.0, 'Feijão preto cozido com diversas carnes suínas e bovinas defumadas, acompanhado de arroz, couve refogada, farofa e laranja.', 'Um dos pratos mais emblemáticos da culinária brasileira, a feijoada é uma explosão de sabores e texturas, perfeita para um almoço farto e tradicional.', 'porco', 'feijão preto, carne seca, paio, linguiça calabresa, costelinha de porco, orelha de porco, rabo de porco, arroz, couve, farinha de mandioca, laranja', 'torresmo, paio, linguiça calabresa', 'ovo cozido, banana frita, bisteca'),
(2, 'Moqueca Mista', 62.0, 'Ensopado de peixe branco e camarões cozidos em leite de coco, azeite de dendê, pimentões e tomate, servido com arroz branco e pirão.', 'Um prato rico e saboroso da culinária afro-brasileira, a moqueca combina a suavidade do peixe e do camarão com o aroma marcante do dendê e do leite de coco.', 'peixe, camarão', 'peixe branco, camarão, leite de coco, azeite de dendê, cebola, alho, tomate, pimentões, coentro, arroz, farinha de mandioca', 'pimentões, cebola, tomate', 'coentro picado, pimenta, farofa de dendê'),
(3, 'Baião de Dois', 48.0, 'Arroz cozido com feijão de corda, queijo coalho, carne de sol desfiada, linguiça e nata.', 'Um prato típico do Nordeste brasileiro, o baião de dois é uma combinação reconfortante e cheia de sabor, perfeito para quem aprecia uma culinária regional autêntica.', 'laticínios', 'arroz, feijão de corda, carne de sol, linguiça calabresa, queijo coalho, nata, cebola, alho, coentro, pimenta do reino', 'carne de sol, linguiça, queijo coalho', 'ovo frito, pimenta biquinho, cheiro-verde'),
(4, 'Frango Assado', 39.9, 'Frango inteiro assado com ervas finas e batatas rústicas.', 'Um clássico reconfortante, o frango assado é uma opção simples e deliciosa para o almoço, com a pele crocante e a carne suculenta.', '', 'frango inteiro, batatas, cebola, alho, azeite, sal, pimenta do reino, alecrim, tomilho', 'alecrim, tomilho, batatas', 'cebola assada, cenoura, farofa simples'),
(5, 'Parmegiana de Carne', 52.0, 'Bife à milanesa gratinado com molho de tomate e queijo mussarela, acompanhado de arroz branco e purê de batata.', 'Um dos pratos mais populares no Brasil, a parmegiana combina a crocância da carne empanada com a suculência do molho e a cremosidade do queijo.', 'glúten, laticínios', 'bife, farinha de trigo, ovo, farinha de rosca, óleo para fritar, molho de tomate, queijo mussarela, arroz, batata, leite, manteiga, sal, noz-moscada', 'molho de tomate, queijo mussarela', 'presunto, ervilha, batata frita'),
(6, 'Salmão Grelhado', 58.0, 'Filé de salmão grelhado com molho de maracujá e arroz com brócolis.', 'Uma opção leve e saudável, o salmão grelhado é rico em ômega-3 e o molho de maracujá adiciona um toque agridoce refrescante.', 'peixe', 'filé de salmão, sal, pimenta do reino, azeite, maracujá, açúcar, arroz, brócolis, alho', 'molho de maracujá', 'legumes salteados, purê de mandioquinha, arroz integral'),
(7, 'Risoto Funghi', 45.0, 'Risoto cremoso preparado com arroz arbóreo e diversos tipos de cogumelos frescos.', 'Um prato elegante e saboroso da culinária italiana, o risoto funghi exalta o sabor terroso e a textura aveludada dos cogumelos.', 'laticínios', 'arroz arbóreo, cogumelos frescos, cebola, alho, vinho branco seco, caldo de legumes, manteiga, queijo parmesão ralado, azeite, salsinha, sal, pimenta do reino', 'queijo parmesão, vinho branco', 'azeite trufado, ervas frescas, mais cogumelos'),
(8, 'Macarrão à Bolonhesa', 36.5, 'Espaguete ao molho bolonhesa clássico, preparado com carne moída, tomate e especiarias.', 'Um prato reconfortante e popular em todo o mundo, o espaguete à bolonhesa é uma opção simples e saborosa para o dia a dia.', 'glúten', 'espaguete, carne moída, cebola, alho, cenoura, salsão, azeite, vinho tinto seco, tomate pelado, extrato de tomate, louro, orégano, sal, pimenta do reino', 'carne moída, molho de tomate', 'queijo ralado, manjericão, azeite'),
(9, 'Virado à Paulista', 50.0, 'Arroz, tutu de feijão, bisteca de porco, linguiça, ovo frito, couve refogada e banana frita.', 'Um prato robusto e tradicional da culinária paulista, o virado é uma combinação de sabores e ingredientes que representam a fartura da mesa caipira.', 'porco, ovo', 'arroz, feijão cozido, farinha de mandioca, toucinho, cebola, alho, bisteca de porco, linguiça caipira, ovos, couve, banana, óleo, sal, pimenta do reino', 'bisteca, linguiça, ovo frito', 'torresmo, abóbora cozida, farofa rica'),
(10, 'Escondidinho de Carne Seca', 42.0, 'Purê cremoso de mandioca coberto com carne seca desfiada e refogada com cebola e pimentões, gratinado com queijo.', 'Um prato rústico e saboroso da culinária brasileira, o escondidinho de carne seca combina a cremosidade da mandioca com o sabor marcante da carne seca.', 'laticínios', 'mandioca, leite, manteiga, sal, carne seca dessalgada e desfiada, cebola, alho, pimentões, azeite, queijo mussarela ralado', 'queijo, pimentões', 'azeitona, cheiro-verde, requeijão cremoso');

-- ========= Inserção de dados: bebidas =========
INSERT INTO bebidas (id_bebidas, nome, preco, descricao, detalhes, alergenicos) VALUES
(1, 'Cerveja Pilsen', 10.0, 'Cerveja lager clara e refrescante, com notas sutis de malte e lúpulo Saaz.', 'Garrafa 600ml, produzida por uma cervejaria artesanal local, ideal para acompanhar petiscos e pratos leves.', 'glúten'),
(2, 'Vinho Tinto Seco', 28.0, 'Vinho tinto seco e elegante, com aromas de frutas vermelhas maduras e taninos suaves.', 'Garrafa 750ml, safra 2020 da Serra Gaúcha, harmoniza bem com carnes grelhadas e massas com molhos encorpados.', ''),
(3, 'Caipirinha', 18.0, 'Coquetel brasileiro clássico e refrescante, feito com cachaça artesanal, limão Taiti fresco e açúcar demerara.', 'Servido com gelo picado, perfeito para o clima tropical de Recife e para acompanhar frutos do mar.', ''),
(4, 'Suco de Maracujá', 9.0, 'Suco natural de maracujá azedinho e revigorante.', 'Feito com polpa de maracujás selecionados, ideal para refrescar nos dias quentes ou como acompanhamento de pratos agridoces.', ''),
(5, 'Cerveja IPA', 12.0, 'Cerveja India Pale Ale com amargor pronunciado e aromas cítricos e florais de lúpulos americanos.', 'Long neck 355ml, de uma microcervejaria pernambucana, para apreciadores de cervejas intensas.', 'glúten'),
(6, 'Vinho Branco Suave', 25.0, 'Vinho branco levemente adocicado, com notas frutadas de pêssego e melão.', 'Garrafa 750ml, safra 2021 do Vale do São Francisco, excelente para harmonizar com saladas, peixes leves e sobremesas não muito doces.', ''),
(7, 'Moscow Mule', 22.0, 'Coquetel picante e refrescante com vodka premium, ginger beer artesanal e suco de limão fresco.', 'Servido em caneca de cobre com gelo e uma rodela de limão, perfeito para um happy hour animado.', ''),
(8, 'Água Tônica', 7.0, 'Água carbonatada com quinino, levemente amarga e refrescante.', 'Lata 350ml, ideal para misturar em coquetéis ou para beber pura com gelo e limão.', ''),
(9, 'Chopp Pilsen', 8.0, 'Chopp pilsen claro e leve, com colarinho cremoso e sabor maltado suave.', 'Copo 300ml, tirado com maestria, a pedida ideal para um dia de calor em Recife.', 'glúten'),
(10, 'Gin Tônica', 25.0, 'Coquetel clássico e aromático com gin London Dry, água tônica premium e especiarias como zimbro e laranja.', 'Servido em copo alto com gelo e rodelas de laranja e limão, uma opção sofisticada e refrescante.', '');

-- ========= Inserção de dados: doces =========
INSERT INTO doces (id_doces, nome, preco, descricao, detalhes, alergenicos, ingredientes, ingredientes_removiveis, ingredientes_adicionaveis) VALUES
(1, 'Brownie com Nozes', 18.0, 'Brownie de chocolate intenso com nozes picadas.', 'Um clássico irresistível para os amantes de chocolate.', 'glúten, laticínios, nozes', 'chocolate amargo, manteiga, açúcar, ovos, farinha de trigo, nozes picadas', 'nozes', 'calda de chocolate, sorvete, frutas vermelhas'),
(2, 'Cheesecake Frutas Verm.', 22.0, 'Cheesecake cremoso com cobertura de frutas vermelhas frescas.', 'Sobremesa elegante e refrescante.', 'glúten, laticínios', 'cream cheese, açúcar, ovos, biscoito maisena, manteiga, frutas vermelhas', 'frutas vermelhas', 'calda de frutas, chantilly, raspas de limão'),
(3, 'Mousse de Maracujá', 16.0, 'Mousse leve e aerada de maracujá.', 'Sobremesa tropical com toque cítrico.', 'laticínios', 'polpa de maracujá, leite condensado, creme de leite, gelatina incolor', '', 'raspas de limão, sementes de maracujá, calda de maracujá'),
(4, 'Pudim Leite Cond.', 15.0, 'Pudim clássico de leite condensado com calda de caramelo.', 'Sobremesa tradicional e reconfortante.', 'laticínios, ovos', 'leite condensado, leite, ovos, açúcar', '', 'mais calda de caramelo, coco ralado'),
(5, 'Torta de Maçã', 20.0, 'Torta de maçã com canela e massa crocante.', 'Sobremesa caseira e aromática.', 'glúten', 'maçã, farinha de trigo, manteiga, açúcar, canela, limão', '', 'sorvete, chantilly, calda de caramelo'),
(6, 'Brigadeiro Tradicional', 4.5, 'Brigadeiro tradicional de chocolate.', 'O doce mais amado do Brasil.', 'laticínios', 'leite condensado, chocolate em pó, manteiga, granulado', 'granulado', 'chocolate granulado colorido, coco ralado, castanhas picadas'),
(7, 'Beijinho de Coco', 4.0, 'Beijinho cremoso de coco.', 'Doce tradicional com sabor tropical.', 'laticínios', 'leite condensado, coco ralado, manteiga, açúcar', 'coco ralado', 'cravo, coco queimado'),
(8, 'Bolo de Cenoura', 18.0, 'Bolo fofo de cenoura com cobertura de chocolate.', 'Um bolo clássico e delicioso.', 'glúten, laticínios, ovos', 'cenoura, farinha de trigo, ovos, óleo, açúcar, fermento, chocolate em pó, leite, manteiga', '', 'granulado, nozes picadas'),
(9, 'Pavê de Chocolate', 25.0, 'Pavê cremoso de chocolate com biscoito champanhe.', 'Sobremesa em camadas fácil e saborosa.', 'glúten, laticínios, ovos', 'biscoito champanhe, leite, gemas, açúcar, chocolate em pó, amido de milho, creme de leite', '', 'raspas de chocolate, frutas'),
(10, 'Doce de Leite', 12.0, 'Doce de leite cremoso.', 'Um doce simples e delicioso.', 'laticínios', 'leite, açúcar, bicarbonato de sódio', '', 'canela em pó, queijo minas');

-- ========= Inserção de dados: entradas =========
INSERT INTO entradas (id_entradas, nome, preco, descricao, detalhes, alergenicos, ingredientes, ingredientes_removiveis, ingredientes_adicionaveis) VALUES
(1, 'Ceviche de Tilápia', 38.5, 'Tilápia fresca marinada no limão com cebola roxa, coentro e pimenta dedo-de-moça.', 'O ceviche é um prato tradicionalmente atribuído ao Peru, mas sua fama se espalhou por toda América Latina. Esta iguaria é uma verdadeira celebração de sabores cítricos e frescor, combinando peixe cru marinado com ingredientes aromáticos. No Brasil, ganhou versões adaptadas, valorizando peixes locais e temperos regionais.', 'peixe', 'tilápia, limão, cebola roxa, coentro, pimenta dedo-de-moça, sal', 'coentro, cebola roxa, pimenta dedo-de-moça', 'milho crocante, chips de batata doce, cubos de manga'),
(2, 'Bruschetta Italiana', 24.9, 'Pão artesanal crocante coberto com tomate fresco, manjericão e azeite extra virgem.', 'Originária da Itália, mais precisamente da região da Toscana, a bruschetta era, no início, uma forma simples dos agricultores aproveitarem o pão amanhecido. Hoje, transformou-se em uma das entradas mais famosas do mundo, trazendo em cada mordida a rusticidade e o frescor dos ingredientes italianos.', 'glúten', 'pão italiano, tomate, manjericão, azeite extra virgem, alho, sal', 'tomate, manjericão, azeite', 'presunto parma, queijo burrata, azeitonas'),
(3, 'Tartar de Salmão', 49.9, 'Cubos de salmão fresco temperados com azeite trufado, limão siciliano e cebolinha.', 'O tartar tem suas raízes na culinária francesa, sendo inicialmente preparado com carne bovina. Com o tempo, a técnica se expandiu para peixes como o salmão, combinando a textura macia do peixe cru com temperos que realçam sua delicadeza. Hoje é um ícone da gastronomia contemporânea.', 'peixe', 'salmão fresco, azeite trufado, limão siciliano, cebolinha, sal, pimenta do reino', 'cebolinha, limão siciliano, azeite trufado', 'abacate, ovas de peixe, chips de batata'),
(4, 'Salada Caprese', 28.5, 'Mussarela de búfala, tomate fresco e manjericão regados com azeite de oliva.', 'Inspirada nas cores da bandeira italiana — verde, branco e vermelho —, a Caprese nasceu na Ilha de Capri como um prato leve e refrescante, perfeito para o verão mediterrâneo. Seu minimalismo destaca a importância da qualidade dos ingredientes.', 'laticínios', 'mussarela de búfala, tomate, manjericão, azeite de oliva, sal, pimenta do reino', 'manjericão, tomate, azeite de oliva', 'pesto de manjericão, azeitonas pretas, nozes'),
(5, 'Guacamole com Nachos', 34.0, 'Creme de abacate temperado com tomate, cebola e coentro, servido com nachos crocantes.', 'O guacamole remonta aos tempos dos astecas, na antiga Mesoamérica. Considerado um alimento sagrado, o abacate era um símbolo de fertilidade. Hoje, o guacamole é um dos maiores representantes da culinária mexicana, conhecido pelo seu frescor e equilíbrio de sabores.', '', 'abacate, tomate, cebola, coentro, limão, sal, pimenta, nachos', 'coentro, tomate, cebola', 'jalapeño, sour cream, queijo cheddar'),
(6, 'Dadinho de Tapioca', 23.9, 'Quadradinhos crocantes de tapioca com queijo coalho, acompanhados de melaço.', 'Inventado por acaso em um restaurante em São Paulo, o dadinho de tapioca rapidamente conquistou o paladar brasileiro. A combinação da crocância externa com o interior macio e o toque adocicado do melaço cria uma experiência única, homenageando ingredientes típicos do Nordeste.', 'laticínios', 'tapioca granulada, queijo coalho, leite, manteiga, sal, melaço de cana', 'queijo coalho, sal', 'melado de cana, geleia de pimenta, ervas frescas'),
(7, 'Camarão Empanado', 42.0, 'Camarões empanados crocantes, servidos com molho tártaro.', 'A tradição de empanar e fritar frutos do mar é antiga, originária das técnicas japonesas do tempurá, mas amplamente adaptada na gastronomia costeira brasileira. O camarão empanado traz o sabor do litoral em cada mordida.', 'camarão, glúten', 'camarão, farinha de trigo, ovo, farinha panko, óleo para fritar, sal, pimenta do reino, molho tártaro', 'camarão, farinha panko, temperos', 'limão siciliano, molho agridoce, pimenta dedo-de-moça'),
(8, 'Carpaccio de Carne', 39.9, 'Finas fatias de carne crua com rúcula, parmesão e molho especial.', 'Criado em Veneza na década de 1950, o carpaccio foi uma inovação gastronômica em homenagem ao pintor Vittore Carpaccio. Este prato sofisticado rapidamente virou sinônimo de elegância, trazendo frescor e leveza ao paladar.', 'carne, queijo', 'carne bovina, rúcula, queijo parmesão, azeite extra virgem, suco de limão, mostarda dijon, sal, pimenta do reino', 'rúcula, queijo parmesão, molho de mostarda', 'azeitonas pretas, alcaparras, lascas de parmesão'),
(9, 'Mini Pastéis de Queijo', 19.9, 'Pequenos pastéis de massa crocante recheados com queijo minas.', 'Pastéis chegaram ao Brasil através dos imigrantes chineses, adaptando-se rapidamente à cultura brasileira. Hoje, são indispensáveis em feiras e bares, carregando a essência do nosso jeito descontraído de comer.', 'glúten, laticínios', 'massa de pastel, queijo minas, óleo para fritar, sal', 'massa do pastel, queijo minas', 'pimenta biquinho, molho de pimenta, requeijão cremoso'),
(10, 'Tábua de Frios', 45.9, 'Seleção de queijos, embutidos e frutas secas.', 'As tábuas de frios surgiram da tradição europeia de conservar carnes e queijos para o inverno. Hoje, são sinônimo de confraternização, harmonizando sabores variados em apresentações generosas.', 'laticínios', 'queijo gouda, queijo brie, salame, presunto cozido, azeitonas, uvas passas, damasco seco, castanhas', 'queijos, embutidos, frutas secas', 'castanhas, geleia de damasco, azeitonas verdes');

-- ========= Inserção de dados: lanches =========
INSERT INTO lanches (id_lanches, nome, preco, descricao, detalhes, alergenicos, ingredientes, ingredientes_removiveis, ingredientes_adicionaveis) VALUES
(1, 'Hambúrguer Clássico', 28.0, 'Pão brioche, hambúrguer de carne bovina, queijo cheddar, alface, tomate e maionese.', 'Um clássico amado por todos, perfeito para qualquer hora.', 'glúten, laticínios', 'pão brioche, hambúrguer de carne bovina, queijo cheddar, alface, tomate, maionese', 'tomate, alface, maionese', 'cebola caramelizada, bacon, ovo'),
(2, 'X-Salada', 30.5, 'Pão de hambúrguer, hambúrguer de carne, queijo mussarela, presunto, alface, tomate e molho especial.', 'Um lanche completo e saboroso com ingredientes frescos.', 'glúten, laticínios', 'pão de hambúrguer, hambúrguer de carne, queijo mussarela, presunto, alface, tomate, molho especial', 'tomate, alface, presunto', 'ovo, bacon, milho'),
(3, 'Sanduíche de Frango', 26.0, 'Pão integral, peito de frango desfiado, requeijão light, cenoura ralada e rúcula.', 'Opção leve e saudável para um lanche rápido.', 'glúten, laticínios', 'pão integral, peito de frango desfiado, requeijão light, cenoura ralada, rúcula', 'rúcula, cenoura ralada, requeijão light', 'queijo branco, tomate seco, azeitona'),
(4, 'Tostex Misto', 18.0, 'Pão de forma, queijo mussarela e presunto tostados.', 'Um clássico simples e delicioso para um lanche rápido.', 'glúten, laticínios', 'pão de forma, queijo mussarela, presunto', 'presunto', 'tomate, orégano'),
(5, 'Beirute de Rosbife', 35.0, 'Pão sírio, rosbife fatiado, queijo prato, tomate, alface e molho de mostarda.', 'Um sanduíche robusto e cheio de sabor.', 'glúten, laticínios', 'pão sírio, rosbife fatiado, queijo prato, tomate, alface, molho de mostarda', 'tomate, alface, molho de mostarda', 'cebola caramelizada, picles, ovo cozido'),
(6, 'Wrap Vegano', 32.0, 'Wrap integral, pasta de grão de bico, abobrinha grelhada, pimentão, tomate e espinafre.', 'Opção vegana nutritiva e saborosa.', 'glúten', 'wrap integral, pasta de grão de bico, abobrinha grelhada, pimentão, tomate, espinafre', 'tomate, pimentão', 'cogumelos, azeitona, guacamole'),
(7, 'Cachorro Quente', 22.0, 'Pão de cachorro quente, salsicha, mostarda, ketchup e maionese.', 'Um clássico popular e saboroso.', 'glúten', 'pão de cachorro quente, salsicha, mostarda, ketchup, maionese', 'mostarda, ketchup, maionese', 'vinagrete, purê de batata, queijo ralado'),
(8, 'Misto Quente', 20.0, 'Pão francês, queijo mussarela e presunto na chapa.', 'Um lanche simples e rápido para qualquer momento.', 'glúten, laticínios', 'pão francês, queijo mussarela, presunto', 'presunto', 'tomate, orégano'),
(9, 'Sanduíche de Atum', 27.0, 'Pão de forma integral, atum em conserva, maionese light, cebola picada e alface.', 'Opção leve e rica em ômega-3.', 'glúten, peixe', 'pão de forma integral, atum em conserva, maionese light, cebola picada, alface', 'cebola picada, alface, maionese light', 'tomate, azeitona, ovo cozido'),
(10, 'Crepe de Queijo', 25.0, 'Massa de crepe, queijo mussarela e orégano.', 'Um lanche rápido e saboroso com recheio simples.', 'glúten, laticínios', 'massa de crepe, queijo mussarela, orégano', 'orégano', 'presunto, frango desfiado, tomate');

-- ========= Inserção de dados: veganos =========
INSERT INTO veganos (id_veganos, nome, preco, descricao, detalhes, alergenicos, ingredientes, ingredientes_removiveis, ingredientes_adicionaveis) VALUES
(1, 'Bruschetta Vegana', 26.5, 'Pão italiano tostado com tomate fresco marinado, manjericão e azeite.', 'Entrada clássica em versão vegana, leve e saborosa.', 'glúten', 'pão italiano, tomate, manjericão, azeite extra virgem, alho, sal', 'tomate, manjericão, azeite', 'azeitonas, rúcula, pesto vegano'),
(2, 'Wrap Falafel Vegano', 34.0, 'Wrap integral com bolinhos de grão de bico fritos, tahine, pepino e tomate.', 'Lanche nutritivo e saboroso inspirado na culinária do Oriente Médio.', 'glúten, gergelim', 'wrap integral, falafel, tahine, pepino, tomate, alface', 'pepino, tomate, alface', 'picles, cebola roxa, hortelã, molho picante vegano'),
(3, 'Moqueca de Cogumelos', 58.0, 'Ensopado de cogumelos frescos com leite de coco, azeite de dendê, pimentões e tomate, servido com arroz.', 'Almoço vegano rico e aromático, com a textura carnuda dos cogumelos.', '', 'cogumelos, leite de coco, azeite de dendê, pimentões, tomate, cebola, alho, coentro, arroz', 'pimentões, cebola, tomate', 'tofu defumado, castanhas, farofa de dendê vegana'),
(4, 'Hambúrguer Vegano', 32.0, 'Pão vegano, hambúrguer de grão de bico, queijo vegano, alface e tomate.', 'Lanche clássico em versão totalmente vegetal.', 'glúten', 'pão vegano, hambúrguer de grão de bico, queijo vegano, alface, tomate, maionese vegana', 'tomate, alface, maionese vegana', 'cebola caramelizada, cogumelos salteados, abacate'),
(5, 'Salada de Quinoa Vegana', 40.0, 'Quinoa cozida com legumes frescos, ervas, tofu grelhado e molho cítrico.', 'Almoço leve e nutritivo, cheio de vitaminas e proteínas vegetais.', '', 'quinoa, tofu, pepino, tomate cereja, abobrinha, cenoura, salsinha, hortelã, azeite, limão, sal', 'pepino, tomate cereja', 'grão de bico assado, semente de girassol, abacate'),
(6, 'Torta de Chocolate Vegana', 28.0, 'Fatia de torta cremosa de chocolate amargo com base de castanhas.', 'Doce vegano decadente e delicioso, perfeito para finalizar a refeição.', 'nozes', 'chocolate amargo vegano, leite de coco, tâmaras, castanhas, cacau em pó', '', 'frutas vermelhas, coco ralado, calda de chocolate vegana'),
(7, 'Curry de Grão de Bico', 45.0, 'Curry cremoso de grão de bico com leite de coco, especiarias e arroz basmati.', 'Almoço vegano aromático e reconfortante, inspirado na culinária indiana.', '', 'grão de bico, leite de coco, cebola, alho, gengibre, curry em pó, cominho, coentro, tomate, espinafre, arroz basmati', 'espinafre, tomate', 'tofu firme, lentilha, pimenta fresca'),
(8, 'Sanduíche de Abacate', 29.0, 'Pão integral com pasta de abacate, tomate seco, rúcula e brotos.', 'Lanche vegano fresco e nutritivo.', 'glúten', 'pão integral, abacate, tomate seco, rúcula, brotos, limão, sal', 'rúcula, brotos', 'pepino, azeitona, pasta de amendoim'),
(9, 'Sopa de Lentilha Vegana', 38.0, 'Sopa nutritiva de lentilha com legumes e ervas aromáticas.', 'Entrada ou almoço vegano reconfortante e cheio de fibras.', '', 'lentilha, cenoura, batata, cebola, alho, salsão, tomate, louro, tomilho, azeite, sal', 'salsão, tomate', 'espinafre, coentro fresco, pão integral'),
(10, 'Cookie Vegano', 12.0, 'Cookie crocante e saboroso feito com aveia, gotas de chocolate vegano e nozes.', 'Doce vegano perfeito para um lanche rápido.', 'glúten, nozes', 'aveia, farinha de trigo, açúcar mascavo, óleo vegetal, gotas de chocolate vegano, nozes, fermento, sal', '', 'frutas secas, sementes, canela');

-- Fim do schema.