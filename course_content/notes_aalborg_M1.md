## Module 1

### Session 1
Online introduction: Welcome & course overview (MP))
Online interaction with Polls, and Q&As on the videos (MP, SL, JS)
Online discussion: Strengths and weaknesses, challenges and opportunities of consequential LCA? (BW, SL; JS)

#### Lecture 1: Attributional vs. Consequential

#### Lecture 2: ISO14040/44 - A standard for consequential LCA

#### Lecture 3: How to reflect physical and monetary causalities in LCA

#### Lecture 4: Temporal errors

#### Lecture 5: Non-intuitive results

### Session 2
Online interaction with Polls, and Q&As on the videos (BW, SL)
Online group exercise: checking the case studies, status, roundtable and potential consequential elements (MP)
Online discussion: Communicating consequential models (SL, MP, JS)

#### Lecture 6: Comparability Algorithm
**Functional unit:** 
* interchangable, substitutable by consumer 
**Step 1: Identify market segmentation**
* market segmentation - geographical, temporal, customer -> niches (inside segments) 
* No segmentation when supply substitution is possible 
* eg. food - ultimately substitutable, -> meals/snacks, breakfast/lunch/dinner, home/restaurant -> further niches
**Step 2: Identify the obligatory product properties**
* functionality, quality, costs -> quantitative description of what? how well? how long? 
* data comes from businesses, govt., 
* Legislation/standards > evidence from market history > market surveys 
* Quantitative techniques: cross-price elasticities, similarity/convergence of price over time, causal relations in price series 
**Step 3: Quantify the functional unit** 
* best to define it by the function of the product -> seating support for > 7 years, not 'chair' 
* therefore, 'how?' and 'how long?' are also addressed 
* Does the size matter? Not for small changes,(maybe set FU to the av. yearly consumption)  but could have effects if large. 
* For big decisions (non-linear consequences): FU should have the same size as the expected outcome of the decision 

#### Lecture 7: Linking algorithm: composing a consumption mix
* How do we link the different unit processes together to represent a product system
* Guidance in ISO 14049: supplementary processes are those involved when switching product systems
* Need to know: 
1. do volumes fluctuate in time?
2. are any suppliers constrained?
3. which unconstrained suppliers have the lowest production costs?

**How to identify marginal unconstrained suppliers?**
* Demand ++ -> modern competitive suppliers
* Demand -- -> old uncompetitive suppliers
* BUT: difference between increase/decrease must be relative to the replacement rate of capital. (only below that will old tech be taken out of the market)
e.g., demand for gas -2%pa. but cap replacement reate is -3.3%pa, so new technology is still needed

**Composition**
* In increasing demand: only the modern tech is supplying new demand - only looking at what is changing
* In decreasing demand: only the old tech is changing, as it's the least competitive
* Constrained market: fulfilled by someone else giving up their supply (the marginal consumer) They could be seen as the supplying technology?
*QUESTION: by-product is not always so clearly defined, how to determine this?*
*By-products can never be affected by a change in demand: they are excluded from consequential market mixes*
* Partially constrained market: some will come from normal supplier, some from reduction in demand from marginal consumer

**How is this incorporated in ecoInvent?**
* technology constraints: classification as old, new, etc
* constrained markets: modelled as a reduction in consumption of the marginal consumer
* by-product constraints: only reference products can be unconstrained and thus be part of a consumption mix

### Lecture 8: How to identify the determining product in a system of co-production
*reference product: change in demand leads to change in supply*
**Combined production: eg. oil refinery, amounts of co-products can be varied**
* Joint production: eg. soy oil/meal, amounts are fixed -> determining products must be identified depending on the existence of alternative production routes
* Type 1: only one joint product w/o alternative production route
* Type 2: all joint products have alternative production routes -> determining product selected based on costs/revenues/market-trends
* ---- normalised market trend: divide trend by output ratio
* ---- when both revenues are needed for the activity to change, the one with the lowest NMT will impose the constraint on the others
* Type 3: more than one joint product has no alternative production route -> both will be determining products
* ---- e.g. slaughterhouse: most products don't have an alternative (ex. leather, bone meal)
* ---- increase in demand for mince leads to increase in production of determining products, reduction in demand from other consumers, surplus by-products -> substitition, surplus cuts taken up by other consumers
** there is a decision tree in the slides **

### Lecture 9: The co-product algorithm
*QUESTION: HOW TO DEAL WITH NON-FREE MARKETS? e.g. milk production*
*QUESTION: CHANGES IN DEMAND -> assumption that there is a change in consumption pattern, determined by price? but prices don't change so quickly, or might be inelastic...*
*procedure for substutution*
** SUBSTITUTION IS THE ONLY ALGORITHM THAT MAINTAINS MASS, ELEMENT, MONETARY BALANCES ** 
** SYSTEM EXPANSION? 
1. **combined or joint production?**
* can co-products be varied independently?
* if not, they can be subdivided according to physical causalities
2. for joint production: what is the determining product? 
3. is the determining product fully utilised?
e.g. increase in demand for calves does not cause increase in milk production
e.g. sheep production in EI: determining product determined by production aims -> meat is negative input flow for a fleece sheep
3. (b) if the dependent co-product is not fully utilised? we are just avoiding the waste treatment that would have happened.  
 
### Lecture 10: Errors in background databases
*"required algorithims are implemented reasonably  well in EI"*
**PROBLEMS IN EI**
1. user interface makes it difficult to follow the modelling of negative physical flows
2. mass balancing in not implemented in a wat that allows the use of this to identify errors in the modelling "big problem for consequential LCA"
3. manually induced errors in the modelling still appear: eg. manure emissions are still part of crop production instead for animals

**GENERAL PROBLEMS**
1. aggregation errors regarding: space, product, time. an average production mix will conclude information from the past.
* solutions? differentiated data, maybe also a correction factor could be developed based on learning curves...
2. often very big differences in ei CON vs ei APOS
*CAUSES*
* marginal suppliers very different from the averages 
* speciality products: (example about waste carbon paper) 
* multiple determining products 
* by-products from treatment activities 
* determining products heavily influenced by by-products 

** WHY CON. IS BETTER...**
* includes displacement of other activities 
* eg. Si + HCl -> SiH4 (1kg)+ SiCl4(15kg) but in att. all of the burdens are given to the SiH4 

*Three situations where con. is essential*
1. when the marginal suppliers have much more/less impact than the average
2. when analysing the use of by-products 
3. when analysing the use of determining products from  activities with significant amounts of other co-products 

## Module 2 - 
