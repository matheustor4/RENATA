from random import random;
import matplotlib.pyplot as plt;
import math; 

class RbdBlock():
        def __init__(self, avail, name, parallelBlocks=0, blockAvailability=0):
                self.avail = avail;
                self.name = name;
                self.parallelBlocks = 0;
                self.blockAvailability = 0;
        
        def calculateAvail(self, parallelBlocks):
            self.parallelBlocks = parallelBlocks;
            self.blockAvailability = float(1 - (1-self.avail)**parallelBlocks);
            #return self.blockAvailability; 
        

class Individuo():
        def __init__(self, blocks, target, geracao=0):
            self.blocks = blocks;
            self.notaAvaliacao = 0;
            self.geracao = geracao;
            self.cromossomo = [];
            self.target = target;
            self.selected = False;
            self.sumBlocks = 0; 
            self.resultModel = 0;
            
            for i in range(len(blocks)):
                 self.cromossomo.append(round(random() * 10));
                 
                
             
        def avaliacao(self):
            resultAvailModel = 1;
            
            for i in range(len(self.blocks)):
               self.blocks[i].calculateAvail(self.cromossomo[i]);
               resultAvailModel = resultAvailModel * blocks[i].blockAvailability;
               self.resultModel = resultAvailModel;
  
          
            diff = abs(self.target - resultAvailModel);
            if math.isclose(diff, 0, abs_tol=1e-07):
                self.notaAvaliacao = 10;
                self.selected = True;
            elif math.isclose(diff, 0, abs_tol=1e-03):
                self.notaAvaliacao = 8;
                self.selected = False;
            elif math.isclose(diff, 0, abs_tol=1e-01):
                self.notaAvaliacao = 5;
                self.selected = False;
            else:
                self.notaAvaliacao = 1;
                self.selected = False;
            
            for i in range(len(self.cromossomo)):
                self.sumBlocks += self.cromossomo[i];
                        
            
        def crossover(self, outroIndividuo):
            corte = round(random() * len(self.cromossomo));
            filho1 = outroIndividuo.cromossomo[0:corte] + self.cromossomo[corte::];
            filho2 = self.cromossomo[0:corte] + outroIndividuo.cromossomo[corte::];
            
            filhos = [Individuo(self.blocks, self.target, self.geracao + 1), Individuo(self.blocks, self.target, self.geracao + 1)];
            
            filhos[0].cromossomo = filho1;
            filhos[1].cromossomo = filho2;
                                  
            return filhos;
        
        def mutacao(self, taxaMutacao):
            for i in range(len(self.cromossomo)):
                if random() < taxaMutacao:
                    self.cromossomo[i] = round(random() * 10);
                    
            return self;
                
class AlgoritmoGenetico():
    def __init__(self, tamanhoPopulacao):
        self.tamanhoPopulacao = tamanhoPopulacao;
        self.populacao = [];
        self.geracao = 0;
        self.melhorSolucao = 0;
        self.listaSolucoes =[];
        self.sumBlocksValues = [];
        self.bestCandidate = 0;
        
    
    def inicializaPopulacao(self, blocks, target):
        for i in range(self.tamanhoPopulacao):
            self.populacao.append(Individuo(blocks, target));
        self.melhorSolucao = self.populacao[0];
      
    def ordenaPopulacao(self):
        self.populacao = sorted(self.populacao, key=lambda populacao: populacao.notaAvaliacao, reverse = True )          
        
    def melhorIndividuo(self, individuo):
        if individuo.notaAvaliacao > self.melhorSolucao.notaAvaliacao:
            self.melhorSolucao = individuo;
            
    #def bestIndividual(self):
    #    if len(self.selectedIndividuals) > 0:
    #        individuo = sorted(self.selectedIndividuals, key=lambda selectedIndividuals: selectedIndividuals.sumBlocks, reverse = False);
    #        return individuo[0];
    #    else:
    #        return 0;
    
    def somaAvaliacoes(self):
        soma = 0;
        for individuo in self.populacao:
            soma += individuo.notaAvaliacao;
            if individuo.selected:
                if self.bestCandidate == 0:
                    self.bestCandidate = individuo;
                    self.sumBlocksValues.append(self.bestCandidate.sumBlocks);
                elif individuo.sumBlocks < self.bestCandidate.sumBlocks:
                    self.bestCandidate = individuo;
                    self.sumBlocksValues.append(self.bestCandidate.sumBlocks);
        return soma;
    
    def selecionaPai(self, somaAvaliacao):
        pai = -1;
        valorSorteado = random()*somaAvaliacao;
        soma = 0;
        i = 0;
        while i < len(self.populacao) and soma < valorSorteado:
            soma += self.populacao[i].notaAvaliacao;
            pai += 1;
            i += 1; 
        return pai;
    
    def visualizaGeracao(self):
        melhor = self.populacao[0];
        print("Generation: %s, Availability %s, Nota %s, Cromossomo %s" % (self.populacao[0].geracao,
                                                                     melhor.resultModel,
                                                                     melhor.notaAvaliacao,
                                                                     melhor.cromossomo) ) 
        

    def resolver(self, taxaMutacao, numeroGeracoes, blocks, target):
        self.inicializaPopulacao(blocks, target);
        
        for individuo in self.populacao:
            individuo.avaliacao();
        
        self.ordenaPopulacao();
        self.melhorSolucao = self.populacao[0];
        self.listaSolucoes.append(self.melhorSolucao.notaAvaliacao);
        
        
        self.visualizaGeracao();
        
        for geracao in range(numeroGeracoes):
            somaAvaliacao = self.somaAvaliacoes();
            novaPopulacao = [];
            
            for individuosGerados in range(0, self.tamanhoPopulacao, 2):
                pai1 = self.selecionaPai(somaAvaliacao);
                pai2 = self.selecionaPai(somaAvaliacao);
                
             #   print(pai1, pai2)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2]);
                
                novaPopulacao.append(filhos[0].mutacao(taxaMutacao));
                novaPopulacao.append(filhos[1].mutacao(taxaMutacao));
            
            self.populacao = list(novaPopulacao);
            
            for individuo in self.populacao:
                individuo.avaliacao();
                
            self.ordenaPopulacao();
            
            self.visualizaGeracao();
            
            melhor = self.populacao[0];
            self.listaSolucoes.append(self.melhorSolucao.notaAvaliacao);
     
            self.melhorIndividuo(melhor);
        
        print("\n Melhor solucao -> G: %s, Availability %s, Nota %s,  Cromossomo %s, Soma %s " % (self.melhorSolucao.geracao, self.melhorSolucao.resultModel, self.melhorSolucao.notaAvaliacao, self.melhorSolucao.cromossomo, self.melhorSolucao.sumBlocks))

        return self.melhorSolucao.cromossomo;                                                                       
            
if __name__ == '__main__':
    
    target = float(input("Whats your target Availability? \n"));
    
    numberOfRBDBlocks = int(input("Number of RBD blocks ? \n"));
    
    blocks = [];
    
    for x in range(1, numberOfRBDBlocks+1):
         name = input("RBD Block %d name? \n" % x);
         option = int(input("RBD Block %s input? \n 1 - MTTF and MTTR \n 2 - Availability \n" % name));
         if option == 1:
            mttf = float(input("RBD Block %s MTTF ?\n" % name));
            mttr = float(input("RBD Block %s MTTR ?\n" % name));
            avail = mttf/(mttf+mttr);
            block = RbdBlock(avail, name);
            blocks.append(block);
         elif option == 2:
            avail = float(input("RBD Block %s Availability?\n" % name));
            block = RbdBlock(avail, name);
            blocks.append(block);
         else:
            print("Invalid option \n");
         
 #   target = 0.999999;
    
 #   blocks.append(RbdBlock(0.95, "a"));
 #   blocks.append(RbdBlock(0.95, "b"));
 #0   blocks.append(RbdBlock(0.8, "c"));    
    #blocks.append(RbdBlock(0.9, "d"));
    #blocks.append(RbdBlock(0.9, "a"));
    #blocks.append(RbdBlock(0.9, "b"));
    #blocks.append(RbdBlock(0.9, "a"));
    #blocks.append(RbdBlock(0.9, "b"));
    
    populationSize = 200;
    
    taxaMutacao = 0.25;
    
    numeroGeracoes = 5000;
        
    ag = AlgoritmoGenetico(populationSize);

    resultado = ag.resolver(taxaMutacao, numeroGeracoes, blocks, target);
    
    if ag.bestCandidate == 0:
        print("Não foram encontradas boas soluções");
    else:
        print("Foram encontradas %d boas soluções" % len(ag.sumBlocksValues))
        bestSolution = ag.bestCandidate;
        print("A melhor delas foi:");
        print("\n Geração: %s, Availability %s, Nota %s,  Cromossomo %s, Soma %s " % (bestSolution.geracao, bestSolution.resultModel, bestSolution.notaAvaliacao, bestSolution.cromossomo, bestSolution.sumBlocks))
        print("-------");
        
        
    f = plt.figure()
    plt.plot(ag.listaSolucoes);
    plt.title("Evaluation results of generations");
    plt.show();
    #f.savefig("PSize-50GN-100.pdf", bbox_inches='tight')

    fig = plt.figure()
    plt.plot(ag.sumBlocksValues, 'o', color='black');
    plt.title("Sum blocks");
    plt.show();    
        
    #for block in blocks:
    #    print(block.name, block.avail, block.parallelBlocks, block.blockAvailability);

  