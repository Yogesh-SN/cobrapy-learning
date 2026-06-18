from helpers import load_model, biomass_reaction, flux_sampling, flux_sampling_to_csv

def main():
   model_path = "/home/yogi/programming/cobrapy-learning/models/e_coli_core.xml"  
   model = load_model(model_path)

   print("Loaded in main.py")
   #print(model)

   print(biomass_reaction(model))

   flux_sampling_to_csv(model, 100, 'test_sampling')

if __name__ == "__main__":
   main()
