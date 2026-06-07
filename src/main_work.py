from helpers import load_model

def main():
   model_path = "/home/yogi/programming/cobra_learning/models/e_coli_core.xml"  
   model = load_model(model_path)


   print("Loaded in main.py")
   print(model.summary())


if __name__ == "__main__":
   main()
