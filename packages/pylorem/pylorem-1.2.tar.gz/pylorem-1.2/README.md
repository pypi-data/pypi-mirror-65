## Pylorem - A Python lorem ipsum generator

![Python package](https://github.com/Julian-Nash/pylorem/workflows/Python%20package/badge.svg?branch=master)

Generate random words, sentences and paragraphs, useful for placeholder or dummy text.

#### installation

```shell script
pip install pylorem
```

### usage

Importing

```pycon
>>> from pylorem import LoremIpsum
```

Generate a random word

```pycon
>>> LoremIpsum.word()
'Omnino'
>>> LoremIpsum.word()
'Leno'
>>> LoremIpsum.word()
'Opera'
>>> LoremIpsum.word()
'Aliquot'
>>> LoremIpsum.word()
'Dissimulo'
```

Generate a string of `n` words

```pycon
>>> LoremIpsum.words(4)
'Mando refectorium termes quercus'
>>> LoremIpsum.words(8)
'Induco alioquin mortuus eum eloquens concupiscentia utorutiusus habeohabuihabitum'
>>> LoremIpsum.words(12)
'Aequitasequitas sodalitas vel indutiae infectus proeo nuncquidem passer adstringo vorax concupiscentia xiphias'
```

Generate a sentence

```pycon
>>> LoremIpsum.sentence()
'Contingo praesumopresumo praegravopregravo illeillaillud odio ruoruirutum reluctor anser discedodiscessum hosteshostium redemptor nequeo scelestus absconditus calculus.'
```

Generate a string of `n` sentences

```pycon
>>> LoremIpsum.sentences(3)
'Persevero pactum proluoproluprolutum depereo conitor pravitas iacio genus subiungo iuxta refero impudens repletus juventus propter scriptor ait. Patientia aegrus arceo tyrannus furor partim thalassinus denuntio accuso praestantiaprestantia commissum infrainferiusinfimus milia expletus meretrixmeretricis affligeniensis,haffligeniensis consido culpo stillicidium tenax ait notarius bellus. Claudeo subsequor iucunditas creptio improvidus infectus pestifere vulturvolturvulturiusvolturius textortextrix moneo iusiuris sacculus lascivio obstinatus alteralteraalterum compositus.'
```

Generate a paragraph

```pycon
>>> LoremIpsum.paragraph()
'Suffragium decimus sui lesciense,monasteryof superfluo dissimulo peragro quapropter ultra arbitroarbitror occidooccidioccasum promulgatio desparatus in pollicitus elementum. praeponoprepono comiter expugno inveteratus superbia efficio nimis lacero habeohabuihabitum pupula speculum hortusortus templovium repens labo deorsum erepo labellum. infindoinfidiinfissum utorutiusus exigo interrogatio te queritor requiro labrusca infligoinflixiinflictum adulatio aro obstinatus iudico etsi saturo altus humilis adfero malepeiuspessime proprie sic quare iumentum ponspontis. prenda apparatus relinquo satura munusmuneris ego textus teres curtus pretium incito cupiditas sufficio canto illudoillusiillusum sano didicerat. canonicus plector legatarius expletio dito falsus cicuta quanti exigo provisor cras inquis cunae immunda commodo labefacto importo largior comminor praevenio,prevenio coepipresincipio nisi infit pestifere. intendo exesto pluitpluvit comprobo verbum salvus infrainferiusinfimus illis amiculum infeliciter furtim perniciosus impendium aliquando iusiurandumiurisiurandietc pluma hoienses priores,um adficio brevis censura. quem utorutiusus everto evito gravis repletus patefacio civis timidus novem prorsus umquam vel prosperitas cunae comprovincialis princeps nisi temeritas doleo.'
```

Generate `n` paragraphs

```pycon
>>> LoremIpsum.paragraphs(3)
'Quadruplator quiesquietis viriliter stipes aliquando angustus facilis penus,us proluoproluprolutum excuso asporto nuntio vomica lacrimo furtificus coniecto obsequium. Navisnavis neco lacto impleo reliquum mendosus admiror despecto castellandum creta servio absconditus pulex pictoratus epulo summissusfromsummitto defigo. Civitas infirmo siquidem cerno arguo non lamnialamminalamna eloquens proloquor ergo cruentus tardus pertingo cibus facunditas centum niveus gandavum effectus resumoresumpsi,resumptum postea.\n\nCurtus extremus tubineus ferrum ingravesco provectus nescio aliialii claudoclausus praequam/prequam expelloexpuliexpulsum moleste concupisco aestivusestivus praetereopretereo obvius quaesoqueso quasso illa ritus infinitus puteus. Pessimus postulo spolium ageragri praecedoprecedo turpis nihilum amissio/amissus arcus quamplures adduco temptatio perfero assentator umquam cena corbeiam carmen corturiacum. Asper instituo erogo reliquum seditio supersum fugio unus pius proximus navisnavis perimoperemiperemptum anser sto,steti,statum hos. Siquidem si vulgivagus obligatus iocoiocor suadeo cruxcrucis arguo membrana subvenio puto antepono leno exsto perniciosus ianua textilis sanctimonia insolita statua quamplures succurro dulcedo. Morior pevela promutuus factum furtumtheft,robbery/furta ploro vultus incorruptus reddo acidus exitiabilisexitialisexitosus frugalitas angulus perduco precipio bardus necdumnequedum purgo devoveo specus ademptio articulus. Stabulaus talus praesto horum pecco medicus cunae phitonicum querulus sacrificum spes compater iratus voro queribundus asvesniis solsolis creatura.\n\nAtqui inflectoinflexiinflectum insania mitesco oro horum infitialis filius pulchritudopulchritudinis rememdium queribundus recordatio muto anser canto exturbo licet efficio opportunus priorprius digrediordigredidigressus thymum devito. Profero matermatris illarum promulgatio volosibivelle persisto illud lenimentus matera,mairia populus eatenus sub pulchellus repens persolvo contingo blesense impleo jugiter exerceo inferus creber utilis exponoexposuiexpositum. Luctus contego nonnullus nivellensem miror innotesco nequam peto illaturos longe prevenire repetitio mandatum supero cunctus subito quatenus/quatinus. Commoneo inveteratus perspicuus iudicium ruoruirutum comperte medius prenda reus argumentum de expers defigo demonstro subjunctive arbitroarbitror depulso sanctusrodoenus reperio iucunditas acquiro frater super.'
```
